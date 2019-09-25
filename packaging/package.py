#! /usr/bin/python3

import sys
import os
import json

from argparse import ArgumentParser
from subprocess import DEVNULL, check_output, check_call
from tempfile import TemporaryDirectory
from itertools import repeat, chain
from typing import List, Iterable

from time import sleep


def to_buildah_args(config) -> List[str]:
    """Convert in list of args that can be passed to 'buildah config'"""
    def arg_list(argname, xs):
        return list(chain(*zip(repeat(argname), xs)))

    def arg_if_set(argname, val):
        return [] if val is None else [argname, val]

    return (['--entrypoint',
             '[' + ','.join(['"{}"'.format(ep) for ep in config['entrypoint']]) + ']']
            + arg_list('--annotation', config['annotations'])
            + arg_list('--port', config['exposed_ports'])
            + arg_list('--volume', config['volumes'])
            + arg_list('--env', ('{}={}'.format(k, v) for k, v in config['env'].items()))
            + arg_if_set('--author', config['author'])
            + arg_if_set('--stop-signal', config['stop_signal'])
            + arg_if_set('--user', config['user']))

def main():
    parser = ArgumentParser()
    parser.add_argument('app_name')
    args = parser.parse_args()

    build_image(args.app_name)


def build_image( app_name, revision='1', tag='latest'):
    with TemporaryDirectory(dir='.', suffix='builddir') as builddir:
        return create_new_image('.', builddir, app_name, revision, tag)


def create_new_image(project_dir, builddir, app_name, revision, tag):
    full_app_name = app_name + '.bst'

    if not is_app_built(project_dir, full_app_name):
        raise RuntimeError((f'{app_name} has not been built yet. To build use '
                            f'\'bst build {full_app_name}\''))

    working_container_id = _call_buildah(['from',
                                          '--name=working-container-' + app_name,
                                          'scratch'])
    print('Staging container at \'{}\''.format(working_container_id))

    try:
        checkout_dir = checkout_bst_element(project_dir,
                                            builddir,
                                            full_app_name)

        print('Add sysroot to \'{}\''.format(working_container_id))

        _call_buildah(['add', working_container_id, checkout_dir, '/'])
        _fix_permissions(working_container_id, checkout_dir)

        print('Applying config to \'{}\''.format(working_container_id))
        cconfig = get_container_config(app_name)
        _call_buildah((['config']
                       + to_buildah_args(cconfig)
                       + default_buildah_config_args(project_dir,
                                                     full_app_name,
                                                     app_name, revision)
                       + [working_container_id]))

        container_name = cconfig['name']

        print('Committing to container \'{}\''.format(container_name))
        _call_buildah(['commit', working_container_id,
                       container_name + ':' + tag])
        print('Successfully Created OCI Container:' + container_name)
        print('> buildah images ' + container_name)
        print(_call_buildah(['images', container_name]))
    finally:
        print('Clearing up staging container \'{}\''.format(working_container_id))
        _call_buildah(['rm', working_container_id])

    return f'containers-storage:localhost/{container_name}:{tag}'


def checkout_bst_element(project_dir, builddir, element_name):
    checkout_dir = os.path.join(builddir, element_name + '-sysroot')
    _call_bst(project_dir, ['checkout', '--hardlinks',
                            element_name, checkout_dir])
    return checkout_dir


def get_container_config(app_name):
    data = ''
    path = 'packaging/' + app_name + '.json'
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def is_app_built(project_dir, app_name):
    state = _call_bst(project_dir, ['show',
                                    '--format=%{state}',
                                    '--deps=none',
                                    app_name])
    return state == 'cached'


def default_buildah_config_args(project_dir: str,
                                element: str,
                                container_name: str,
                                revision:str) -> List[str]:
    """
    Return a few default annotations and config for `buildah config`

    See https://github.com/opencontainers/image-spec/blob/master/annotations.md
    for more info.
    """
    return ['--annotation',
            'org.opencontainers.image.revision=' + revision,
            '--annotation',
            'org.opencontainers.image.title=' + container_name,
            '--annotation',
            'org.opencontainers.image.url=https://github.hpecorp.net/storex/build-meta',
            '--annotation',
            'com.hpe.build-meta.cache-key=' + get_buildstream_cache_key(project_dir,
                                                                        element),
            '--annotation', 'com.hpe.build-meta.element=' + element,
            '--created-by', 'Buildah (via build-meta)']


def get_git_commit(project_dir: str) -> str:
    return _call_git(project_dir, ['rev-parse', 'HEAD'])


def get_buildstream_cache_key(project_dir: str, element: str) -> str:
    return _call_bst(project_dir, ['show', element,
                                   '--deps', 'none', '-f', '%{full-key}'])


def _fix_permissions(working_container_id, checkout_dir):
    """
    Fix permission in the container for certain file paths

    This function needs some explaining - the buildstream sandbox filesystem
    is very restrictive - the only uid and gid is 0:0 and file permissions can
    only be 755 or 644 (non executable files). Which is great for build
    reproducibility, not so much for actual day-to-day use. So this function
    fixes up the filesystem permissions so the container is usable for non-root
    users.

    The following actions are taken:
    * Set the suid bit on /usr/bin/fusermount to allow non-root users to use
      fuse. (Only if /usr/bin/fusermount exists)
    * Allow any user to write to /tmp or /run
    * Recursively chown home directories to the appropriate gid and uid
      IMPORTANT we assume that: dirname == username
    * Chmod home dirs to 700
    """
    # TODO: Temporarily mount in chmod and chown binaries for containers
    #       where they're not available
    if not (os.path.exists(os.path.join(checkout_dir, 'usr/bin/chmod')) and
            os.path.exists(os.path.join(checkout_dir, 'usr/bin/chown'))):
        print('Warning: chmod or chown not present in the container',
              file=sys.stderr)
        return

    def run_in_container(cmds):
        _call_buildah(['run', working_container_id] + cmds)

    fusermount_path = 'usr/bin/fusermount'
    if os.path.exists(os.path.join(checkout_dir, fusermount_path)):
        run_in_container(['chmod', 'u+s', fusermount_path])

    for d in ('run', 'tmp'):
        dirname = os.path.join(checkout_dir, d)
        if os.path.exists(dirname):
            run_in_container(['chmod', '777', os.sep + d])

    passwd_data = _parse_passwd(checkout_dir)

    homedir = os.path.join(checkout_dir, "var", "home")
    if os.path.exists(homedir):
        for user in os.listdir(homedir):
            user_homedir = os.path.join(homedir, user)

            uid, gid = passwd_data[user]

            run_in_container(['chown', '-R', f'{uid}:{gid}',
                              os.path.join('/var/home/', user)])

            run_in_container(['chmod', '700',
                              os.path.join('/var/home/', user)])


def _parse_passwd(checkout_dir):
    passwd_filepath = os.path.join(checkout_dir, 'etc', 'passwd')
    if not os.path.exists(passwd_filepath):
        return {}

    passwd_data = {}
    with open(passwd_filepath, 'r') as passwd_file:
        for line in passwd_file.readlines():
            p = line.split(':')
            passwd_data[p[0]] = (int(p[2]), int(p[3]))

    return passwd_data


def _call_bst(project_dir: str, args: Iterable[str]) -> str:
    output = check_output(['bst', '--no-colors', '-C', project_dir] + list(args),
                          stderr=DEVNULL)
    return output.decode('utf-8').strip()


def _call_buildah(args: Iterable[str]) -> str:
    output = check_output(['buildah'] + list(args))
    return output.decode('utf-8').strip()


def _call_git(project_dir: str, args: Iterable[str]) -> str:
    output = check_output(['git', '-C', project_dir] + list(args))
    return output.decode('utf-8').strip()


if __name__ == '__main__':
    sys.exit(main())

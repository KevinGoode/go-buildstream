# Unpacks and installs golang executables in base image sandbox
kind: manual

config:
  install-commands:
  - mkdir -p %{install-root}%{libdir}
  - mkdir -p %{install-root}%{bindir}
  - mv go %{install-root}%{libdir}/
  - |
    for bin in %{install-root}%{goroot}bin/*; do
        bin2=$(basename $bin)
        ln -s %{goroot}bin/$bin2 %{install-root}%{bindir}/$bin2
    done

depends:
- filename: base.bst

sources:
- kind: tar
  url: https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz
  base-dir: ''
  ref: 94f874037b82ea5353f4061e543681a0e79657f787437974214629af8407d124

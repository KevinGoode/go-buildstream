
# Go Project Builder Using BuildStream

This is a technology demonstrator of [buildstream](https://docs.buildstream.build/) and [buildah](https://buildah.io/).  

The pre-requistes are  buildstream (version 1.2.7 +) and buildah (version 1.6 +)  
This build uses a flatpak sdk and extend this example:
[https://buildstream.gitlab.io/buildstream/examples/flatpak-autotools.html](https://buildstream.gitlab.io/buildstream/examples/flatpak-autotools.html)

NB The golang executable cannot be found when building unless the link to lib64 is added. This error message is confusing because go exectuable is in sandbox but linking fails because the golang tarball thinks dependent libs are in lib64)

# Configuration
NONE 

(Formerly had to execute getos.sh but no longer need to do this)

# Getting Started
**To build example project**: bst build hello-go-build.bst  
**To open the project build sandbox**:  bst --no-colors shell hello-go-build.bst  
(To execute the program in the sandbox /usr/bin/hello-go-build)  
**To build the project as an oci container**:  ./packaging/package.py hello-go-build  

# What Next?
 
 -  Running the container via docker:
> buildah push localhost/XX docker-daemon:localhost/XX:latest  
docker run localhost/XX  
(Note your user will need write access to /var/run/docker.sock)

- Running the container via podman
>podman run localhost/$CONTAINERNAME  
 - The script package.py can be used to build a container for any project that contains the following 2 files: /elements/project-name.bst, packaging/project-name.json.


# Versioning Info
Note previous version of this project had 2 base layers: alpine and gnome-sdk. This was a bit dumb. Golang dosn't sit very successfully on alpine due to missing shared libraries and this is why the gnome-sdk was put on top too. At time of writing the gnome-sdk URL was down so this project didn't build. Using the single flatpack image seems a simpler approach. NOTE the script in the utils directory to grab and modify the alpine image is kept for posterity because this could be useful going forward. It is currently not needed . 


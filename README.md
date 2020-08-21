
# Go Project Builder Using BuildStream

This is a technology demonstrator of [buildstream](https://docs.buildstream.build/) and [buildah](https://buildah.io/).  

The pre-requistes are  buildstream (version 1.2.7 +) and buildah (version 1.6 +)  

# Configuration
NONE 


# Getting Started
**To build example project**: 
```console
bst build hello-go-build.bst  
```
**To open the project build sandbox**:
```console
bst --no-colors shell hello-go-build.bst
```  
(To execute the program in the sandbox /usr/bin/hello-go-build)  
**To build the project as an oci container**:
```console
./packaging/package.py hello-go-build  
```
# What Next?
 
 -  Running the container via docker:
```console
buildah push localhost/XX docker-daemon:localhost/XX:latest  
docker run localhost/XX
```  
(Note your user will need write access to /var/run/docker.sock)

- Running the container via podman
```console
podman run localhost/$CONTAINERNAME
``` 
 - The script package.py can be used to build a container for any project that contains the following 2 files: /elements/project-name.bst, packaging/project-name.json.


# Versioning Info
Note first version of this project had 2 base layers: alpine and gnome-sdk. This was a bit dumb. Golang dosn't sit very successfully on alpine due to missing shared libraries and this is why the gnome-sdk was put on top too. At time of writing the gnome-sdk URL was down so this project didn't build. Using the single flatpack image seems a simpler approach. NOTE the script in the utils directory to grab and modify the alpine image is kept for posterity because this could be useful going forward. It is currently not needed . 

Note second version using flatpack was simpler but the image was still large. Hence going back to an alpine image with golang dependencies (libc, libpthread) installed
Image was built from alpine following these instructions https://github.com/KevinGoode/mini-li


# Tips
1. Clean build using
```console
sudo rm -rf ~/.cache/buildstream/
```

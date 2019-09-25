# Go Project Builder Using BuildStream

This is technology demonstrator of [buildstream](https://docs.buildstream.build/) and [buildah](https://buildah.io/).  

The pre-requistes are  buildstream (version 1.2.7 +) and buildah (version 1.6 +)  

# Configuration
Before buidling the example, need to get a small base os:  
cd utils  
./getos.sh  
Alternatively, comment out the ref and url lines in base.bst file and uncomment similar lines that point to  
the base os used in the buildstream examples   
# Getting Started
**To build example project**: bst build hello-go-build.bst  
**To open the project build sandbox**: bst shell hello-go-build.bst  
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


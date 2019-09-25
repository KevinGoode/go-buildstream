# (C) Copyright 2019 Hewlett Packard Enterprise Development LP
kind: import

public:
  bst:
    overlap-whitelist:
    - |
      **

    #integration-commands:
    #- ldconfig

sources:
- kind: tar
  base-dir: gnome-sdk/files
  url: alpine:gnome-sdk.tar.xz
  ref: 96d5062a19fa9ac3439f8a502664f8d46860bad7efd28e7909b03ddbcdbe66e6

kind: import
description: |

    Alpine Linux base runtime

sources:
- kind: tar

  # This is a post doctored, trimmed down system image
  # of the Alpine linux distribution.
  #
  #url: file:///home/goode/alpine-host-tools-3.6.1-x86_64.tar.gz
  #ref: a543dacbabeb1f3f29abc15c06fa64d45f2dce89a00709b6015c2832c5514a49
  url: alpine:integration-tests-base.v1.x86_64.tar.xz
  ref: 3eb559250ba82b64a68d86d0636a6b127aa5f6d25d3601a79f79214dc9703639

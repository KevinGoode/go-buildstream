kind: import
description: |

    Alpine Linux base runtime

sources:
- kind: tar

  # This is a post doctored, trimmed down system image
  # of the Alpine linux distribution. (Generated by script getbase.sh)
  #
  url: file:./utils/mini-li.tar.gz
  ref: 9004644dd096c9a9ca8f7ff5d67be84532eb809aa4b1fccece2feae52f059ade


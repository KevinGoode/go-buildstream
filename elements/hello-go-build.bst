kind: manual
description: |

  Building manually

# Depend on the base system
depends:
- base.bst
- filename: golang.bst
  type: build


# Stage the files/src directory for building
sources:
  - kind: local
    path: files

# Now configure the commands to run
config:

  build-commands:
    - go build -o hellogo ./hello-go-build

  install-commands:
    - mkdir -p %{install-root}%{bindir}
    - go install ./hello-go-build

environment:
  JOBS: -p %{max-jobs}
  V: 1

  # See https://github.com/golang/go/issues/27303
  CGO_ENABLED: '0'

  GOBIN: '%{install-root}%{bindir}'
  GOROOT: '%{libdir}/go/'

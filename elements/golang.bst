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
  url: https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz
  base-dir: ''
  ref: 66d83bfb5a9ede000e33c6579a91a29e6b101829ad41fffb5c5bb6c900e109d9

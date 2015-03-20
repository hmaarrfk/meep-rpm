#!/bin/bash

rpmdev-setuptree

cp mpb.spec ~/rpmbuild/SPECS/
#cp *.tar.gz ~/rpmbuild/SOURCES/
cp *.zip ~/rpmbuild/SOURCES/
cp *.patch ~/rpmbuild/SOURCES/


# build for both archetectures
#auto-br-rpmbuild -bb ~/rpmbuild/SPECS/mpb.spec
rpmbuild -bb ~/rpmbuild/SPECS/mpb.spec


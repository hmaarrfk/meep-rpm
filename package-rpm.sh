#!/bin/bash

rpmdev-setuptree

cp *.spec ~/rpmbuild/SPECS/
cp *.tar.gz ~/rpmbuild/SOURCES/
cp *.zip ~/rpmbuild/SOURCES/
cp *.patch ~/rpmbuild/SOURCES/


# build for both archetectures
#auto-br-rpmbuild -bb ~/rpmbuild/SPECS/meep.spec
rpmbuild -bs ~/rpmbuild/SPECS/meep.spec
rpmbuild -bs ~/rpmbuild/SPECS/mpb.spec
rpmbuild -bs ~/rpmbuild/SPECS/harminv.spec
#rpmbuild -bb ~/rpmbuild/SPECS/meep-mpi.spec


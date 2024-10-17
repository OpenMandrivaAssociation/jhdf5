%{?_javapackages_macros:%_javapackages_macros}
%define _disable_ld_no_undefined 1
Name:           jhdf5
Version:        2.10
Release:        1%{?dist}
Summary:        Java HDF5 Package


License:        BSD with advertising
URL:            https://www.hdfgroup.org/hdf-java-html/
Source0:        http://www.hdfgroup.org/ftp/HDF5/hdf-java/src/hdf-java-%{version}-source.tar.gz
Source1:        hdfview
Source2:        hdfview.xml
Source3:        hdfview.desktop

Patch1:         jhdf5-0001-add-a-generic-linux-host.patch
Patch2:         jhdf5-0002-add-H4_-prefix-to-constants.patch
Patch3:         jhdf5-0003-use-system-linker-for-shared-library.patch
Patch4:         jhdf5-0004-remove-writable-prefix-check.patch
Patch5:         jhdf5-0005-update-config.sub-and-config.guess.patch
Patch6:         jhdf5-0006-update-configure.patch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  hdf5-devel
BuildRequires:  netcdf-devel
BuildRequires:  jpeg-devel
BuildRequires:  slf4j

BuildRequires:  junit

Requires:       jpackage-utils
Requires:       java-headless
Requires:       slf4j
# hdf5 does not bump soname but check at runtime
Requires:       hdf5

%description
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This Java package wrap the native HDF5 library.

%package devel
Summary: JHDF5 development files

Requires: %{name} = %{version}-%{release}
Requires: hdf5-devel

%description devel
JHDF5 development headers and libraries.

%package -n jhdf
Summary:        Java HDF Package


BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  hdf-devel

Requires:       jpackage-utils
Requires:       java-headless
Requires:       slf4j

%description -n jhdf
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This Java package wrap the native HDF4 library.

%package -n jhdfobj
Summary:        Java HDF/HDF5 Object Package


BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  hdf5-devel
BuildRequires:  hdf-devel

Requires:       jpackage-utils
Requires:       java-headless
Requires:       slf4j
Requires:       hdf-util
# hdf5 does not bump soname but check at runtime
Requires:       hdf5
Requires:       jhdf = %{version}-%{release}
Requires:       jhdf5 = %{version}-%{release}

BuildArch:      noarch

%description -n jhdfobj
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This Java package implements HDF4/HDF5 data objects in an 
object-oriented form. It provides a common Java API for accessing HDF files.


%package -n hdfview
Summary:        Java HDF Object viewer


BuildRequires:  jpackage-utils
BuildRequires:  java-devel

# for convert
BuildRequires:  imagemagick
# for desktop-file-install
BuildRequires:  desktop-file-utils

Requires:       jpackage-utils
Requires:       java
Requires:       slf4j
Requires:       jhdfobj = %{version}-%{release}

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

BuildArch:      noarch

%description -n hdfview
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This package provides a HDF4/HDF5 viewer.


%prep
%setup -q -n hdf-java-%{version}-source
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# remove shipped jars
rm $(find -name \*.jar)

# build jar repo
build-jar-repository -p lib/ junit slf4j-
ln -s slf4j-api.jar lib/slf4j-api-1.7.5.jar
ln -s slf4j-nop.jar lib/slf4j-nop-1.7.5.jar


# fix spurious-executable-perm
chmod -x $(find docs -type f)
chmod -x $(find native -type f)
chmod -x COPYING

# fix wrong-file-end-of-line-encoding 
sed -i 's/\r//' docs/hdfview/UsersGuide/RELEASE.txt

%build
%configure --with-jdk=%{java_home}/include,%{java_home}/lib \
        --with-hdf5=%{_includedir},%{_libdir} \
        --with-hdf4=%{_includedir},%{_libdir} \
        --without-h4toh5 \
        --without-libsz \
        --with-libz=%{_includedir},%{_libdir} \
        --with-libjpeg=%{_includedir},%{_libdir}

# Make JNI (libjhdf.so libjhdf5.so) and
# make only required jars (not netcdf nor fits related packages)
pushd .
cd ncsa; \
make
popd

make natives jhdf-packages jhdf5-packages \
     jhdfobj-packages jhdfview-packages

%check
make tests

%install

# jhdf5 jars
install -dm 755 %{buildroot}%{_jnidir}
install -pm 0644 lib/jhdf5.jar %{buildroot}%{_jnidir}/jhdf5.jar

# jhdf5 lib
install -dm 755 %{buildroot}%{_libdir}/jhdf5
install -m 744 lib/linux/libjhdf5.so %{buildroot}%{_libdir}/jhdf5

# jhdf jars
install -dm 755 %{buildroot}%{_jnidir}
install -pm 0644 lib/jhdf.jar %{buildroot}%{_jnidir}/jhdf.jar

# jhdf lib
install -dm 755 %{buildroot}%{_libdir}/jhdf
install -m 744 lib/linux/libjhdf.so %{buildroot}%{_libdir}/jhdf

# jhdfobj jars
install -dm 755 %{buildroot}%{_javadir}
install -pm 0644 lib/jhdfobj.jar %{buildroot}%{_javadir}/jhdfobj.jar
install -pm 0644 lib/jhdf4obj.jar %{buildroot}%{_javadir}/jhdf4obj.jar
install -pm 0644 lib/jhdf5obj.jar %{buildroot}%{_javadir}/jhdf5obj.jar

# hdfview
install -dm 755 %{buildroot}%{_javadir}
install -pm 0644 lib/jhdfview.jar %{buildroot}%{_javadir}/jhdfview.jar

install -dm 755 %{buildroot}%{_bindir}
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/hdfview

# Create and install hicolor icons.
for i in 16 22 32 48 ; do
  mkdir -p icons/${i}x${i}/apps

  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes

  convert -resize ${i}x${i} ncsa/hdf/view/icons/hdf_large.gif \
    icons/${i}x${i}/apps/hdfview.png

  install -pm 0644 icons/${i}x${i}/apps/hdfview.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/hdfview.png

  install -pm 0644 icons/${i}x${i}/apps/hdfview.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-x-hdf.png

done

# .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install                                    \
        --dir %{buildroot}%{_datadir}/applications      \
        %{SOURCE3}

# mime types
mkdir -p %{buildroot}%{_datadir}/mime/packages
install -p -D -m 644 %{SOURCE2} \
        %{buildroot}%{_datadir}/mime/packages/hdfview.xml

%clean
rm -rf %{buildroot}

%post -n hdfview
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n hdfview
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n hdfview
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_jnidir}/jhdf5.jar
%attr(755,root,root) %{_libdir}/jhdf5/libjhdf5.so
%doc COPYING Readme.txt

%files -n jhdf
%{_jnidir}/jhdf.jar
%attr(755,root,root) %{_libdir}/jhdf/libjhdf.so
%doc COPYING Readme.txt

%files -n jhdfobj
%{_javadir}/jhdfobj.jar
%{_javadir}/jhdf4obj.jar
%{_javadir}/jhdf5obj.jar
%doc COPYING Readme.txt

%files -n hdfview
%{_bindir}/hdfview
%{_datadir}/applications/hdfview.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/hdfview.xml
%{_javadir}/jhdfview.jar
%doc COPYING Readme.txt
%doc docs 

%changelog
* Fri Feb 28 2014 Clément David <c.david86@gmail.com> - 2.10-1
- Update version
- Change R:java to R:java-headless (Bug 1068283).

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 2.9-4
- Rebuild for hdf5 1.8.12

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 2.9-2
- Rebuild for hdf5 1.8.11

* Thu Jan 24 2013 Clément David <c.david86@gmail.com> - 2.9-1
- Update to 2.9
- Upgrade to the Java packaging draft (JNI jar/so location)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.8-10
- rebuild due to "jpeg8-ABI" feature drop

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.8-9
- revbump after jnidir change

* Mon Dec 03 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8-8
- Rebuild for hdf5 1.8.10
- Add BR libjpeg-devel

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8-6
- Rebuild with hdf5 1.8.9

* Mon Feb 13 2012 Clément David <davidcl@fedoraproject.org> - 2.8-5
- bump version to depends on latest hdf5

* Tue Jan 31 2012 Clément David <davidcl@fedoraproject.org> - 2.8-4
- fix hdfview CLASSPATH

* Mon Jan 30 2012 Clément David <davidcl@fedoraproject.org> - 2.8-3
- split jhdfobj as an object oriented API of jhdf and jhdf5.

* Fri Jan 27 2012 Clément David <davidcl@fedoraproject.org> - 2.8-2
- use %%{_hdf5_version} for hdfview
- use same jhdf and jhdf5 versions for hdfview

* Wed Jan 25 2012 Clément David <davidcl@fedoraproject.org> - 2.8-1
- update to version 2.8

* Wed Jan 25 2012 Clément David <davidcl@fedoraproject.org> - 2.7-9
- move jars to more standard locations

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Orion Poplawski <orion@cora.nwra.com> - 2.7-7
- use %%{_hdf5_version}

* Thu Nov 17 2011 Clément David <c.david86@gmail.com> - 2.7-6
- use %%{hdf5ver} to avoid runtime crash

* Thu Nov 03 2011 Clément David <c.david86@gmail.com> - 2.7-5
- rebuilt
* Thu Nov  3 2011 Clément David <c.david86@gmail.com> - 2.7-4
- remove rpm-build BuildRequire

* Tue Oct 25 2011 Clément David <c.david86@gmail.com> - 2.7-3
- Fix executable permissions
- pass rpmlint

* Tue Aug 16 2011 Clément David <c.david86@gmail.com> - 2.7-2
- Update mime types to x-hdf and x-hdf5

* Tue Aug 16 2011 Clément David <c.david86@gmail.com> - 2.7-1
- Initial packaging


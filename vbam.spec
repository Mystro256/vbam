Name:           vbam
#Pre-release version 1.8.0.1228 is a snapshot of svn 1229
Version:        1.8.0.1229
Release:        2%{?dist}
#Will not create a binary vbam package, only vbam-gtk and vbam-sdl subpackages
Summary:        High compatibility Gameboy Advance Emulator combining VBA developments

License:        GPLv2
Url:            http://www.vba-m.com
#Grab code using:
#svn co svn://svn.code.sf.net/p/vbam/code/trunk -r 1229 vbam-1.8.0.1229
#tar -Jcv --exclude-vcs -f vbam-1.8.0.1229.tar.xz vbam-1.8.0.1229
Source:         vbam-%{version}.tar.xz
#Kudos to Michael Schwendt and Hans de Goede (updates paths for compat-SFML16-devel):
Patch0:         %{name}-%{version}-includedir.patch
BuildRequires:  SDL-devel
BuildRequires:  zip
BuildRequires:  ImageMagick
BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  libXv-devel
BuildRequires:  nasm
BuildRequires:  libpng-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtkglext-devel
BuildRequires:  gtkglextmm-devel
BuildRequires:  gtkmm24-devel
BuildRequires:  cairo-devel
BuildRequires:  compat-SFML16-devel
BuildRequires:  openal-soft-devel

%package        gtk
Summary:        GTK GUI for VBA-M, a high compatibility Gameboy Advance Emulator
Requires:       %{name}-common
#According to upstream, WX interface is currently not supported and should not be used yet
#See revision 1061: http://vba-m.com/forum/Thread-visualboyadvance-m-svn-1085?pid=4823#pid4823
Obsoletes:      %{name}-wx < 1.8.0.1097-1
Obsoletes:      %{name}-gui-common < 1.8.0.1097-1

%package        sdl
Summary:        SDL version (no GUI) for VBA-M, a high compatibility Gameboy Advance Emulator
Requires:       %{name}-common

%package        common
Summary:        Common configuration for VBA-M, a high compatibility Gameboy Advance Emulator
BuildArch:      noarch

%description
#Using info from here: http://vba-m.com/about.html and debian files
VisualBoyAdvance-M is a Nintendo Game Boy Emulator with high compatibility with
commercial games. It emulates the Nintendo Game Boy Advance hand held console,
in addition to the original Game Boy hand held systems and its Super and Color
variants. VBA-M is a continued development of the now inactive VisualBoy
Advance project, with many improvements from various developments of VBA.

%description    gtk
This package provides the GTK GUI version of VisualBoyAdvance-M.
VisualBoyAdvance-M is a Nintendo Game Boy Emulator with high compatibility with
commercial games. It emulates the Nintendo Game Boy Advance hand held console,
in addition to the original Game Boy hand held systems and its Super and Color
variants. VBA-M is a continued development of the now inactive VisualBoy
Advance project, with many improvements from various developments of VBA.


%description    sdl
This package provides the non GUI SDL version of VisualBoyAdvance-M.
VisualBoyAdvance-M is a Nintendo Game Boy Emulator with high compatibility with
commercial games. It emulates the Nintendo Game Boy Advance hand held console,
in addition to the original Game Boy hand held systems and its Super and Color
variants. VBA-M is a continued development of the now inactive VisualBoy
Advance project, with many improvements from various developments of VBA.

%description    common
This package provides common configurations for both GUI and SDL versions.
VisualBoyAdvance-M is a Nintendo Game Boy Emulator with high compatibility with
commercial games. It emulates the Nintendo Game Boy Advance hand held console,
in addition to the original Game Boy hand held systems and its Super and Color
variants. VBA-M is a continued development of the now inactive VisualBoy
Advance project, with many improvements from various developments of VBA.

%prep
%setup -q
%patch0 -p1
sed -i '/CMAKE_C.*_FLAGS/d' CMakeLists.txt

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DVERSION=%{version} -DCMAKE_SKIP_RPATH=ON -DENABLE_LINK=ON
#V=1 Needed for rpmfusion build servers
make V=1

%install
make install DESTDIR=%{buildroot}
desktop-file-install \
  --remove-category Application \
  --remove-key=Encoding \
  --dir %{buildroot}%{_datadir}/applications \
  src/gtk/g%{name}.desktop
install -p -D -m 0644  debian/%{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1
install -p -D -m 0644  debian/g%{name}.1 %{buildroot}/%{_mandir}/man1/g%{name}.1
%find_lang g%{name}

%files gtk -f g%{name}.lang
%{_datadir}/%{name}
%{_mandir}/man1/g%{name}.1*
%{_bindir}/g%{name}
%{_datadir}/applications/g%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files sdl
%doc doc/ReadMe.SDL.txt
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}

%files common
#excluded doc/ReadMe.MFC.txt and doc/DevInfo.txt,
#as the former is not utf8 and is windows only
#and the latter is only important for building/development
%doc doc/ips.htm doc/gpl.txt doc/License.txt
%config(noreplace) /etc/%{name}.cfg

%post gtk
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtk
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog
* Thu Sep 11 2014 Sérgio Basto <sergio@serjux.com> - 1.8.0.1229-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Apr 5 2014 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1229-1
- Update to latest "release" version

* Mon Nov 18 2013 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1228-3
- Update patch for SFML, thanks to Hans de Goede

* Sun Nov 17 2013 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1228-2
- Added patch for SFML

* Sun Nov 17 2013 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1228-1
- Updated to new snapshot version

* Fri Mar 1 2013 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1159-1
- Updated to new upstream version
- Fixed some spec date typos

* Mon Dec 10 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1149-1
- Updated to new upstream version
- FFMpeg dep removed due to only needed by wx and now disabled by default

* Thu Jul 5 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1097-1
- Updated to new upstream version
- Disabling WX because its not supported
- Removed extra sources as they are now included
- Removed FFMPEG fix
- Moved ips.htm doc file into common to avoid duplicates
- Various cleanup

* Wed Mar 28 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-6
- Added man pages

* Tue Feb 14 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-5
- Added Zip as a dependancy

* Tue Feb 14 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-4
- Changed building commands to avoid failed builds

* Sun Jan 29 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-3
- Added missing Build Requirement: openal-soft-devel
- Removed redundant license files

* Thu Jan 26 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-2
- Added DCMAKE_SKIP_RPATH=ON to cmake (fixes rpath error)
- Added more relevant package summaries
- Fixed up the descriptions a bit
- Enabled Linking Support
- Various tweaks

* Thu Jan 26 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-1
- Updated to new upstream version
- Added new WX subpackage for new GUI
- Adding WX requires gui common subpackage to avoid conflicts
- Added DVERSION cmake tag for aesthetic reasons

* Sun Jan 22 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1001-4
- Added vbam-common package to avoid conflicts with common files
- Added ImageMagick build dep, as cmake checks for it
- Building now uses cmake macro
- Turned off building shared libs
- Removed unnecessary lines
- Fixed debuginfo-without-sources issue

* Sun Jan 22 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1001-3
- Fixed SPM summary
- Cleaned up SPEC for easier reading

* Sun Jan 8 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1001-2
- Fixed up spec file
- Split into two packages: sdl, gtk

* Sun Dec 18 2011 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1001-1
- Initial package SPEC created


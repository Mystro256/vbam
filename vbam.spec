Name:           vbam
#Pre-release version 1.8.0.1054 is a snapshot of svn 1054
Version:        1.8.0.1054
Release:        4%{?dist}
#Will not create a binary vbam package, only vbam-gtk and vbam-sdl subpackages
Summary:        High compatibility Gameboy Advance Emulator combining VBA developments

License:        GPLv2
Url:            http://www.vba-m.com
Source:         https://downloads.sourceforge.net/project/%{name}/VBA-M%20svn%20r1054/%{name}-%{version}-src.tar.gz

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
BuildRequires:  ffmpeg-devel
BuildRequires:  wxGTK-devel
BuildRequires:  SFML-devel
BuildRequires:  openal-soft-devel

%package        gtk
Summary:        GTK GUI for VBA-M, a high compatibility Gameboy Advance Emulator
Requires:       vbam-common
Requires:       vbam-gui-common

%package        wx
Summary:        WX GUI for VBA-M, a high compatibility Gameboy Advance Emulator
Requires:       vbam-common
Requires:       vbam-gui-common

%package        sdl
Summary:        SDL version (no GUI) for VBA-M, a high compatibility Gameboy Advance Emulator
Requires:       vbam-common

%package        common
Summary:        Common configuration for VBA-M, a high compatibility Gameboy Advance Emulator
BuildArch:      noarch

%package        gui-common
Summary:        Common icons files for VBA-M, a high compatibility Gameboy Advance Emulator
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

%description    wx
This package provides the experimental WX GUI version of VisualBoyAdvance-M.
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

%description    gui-common
This package provides common icon files for either GUI versions.
VisualBoyAdvance-M is a Nintendo Game Boy Emulator with high compatibility with
commercial games. It emulates the Nintendo Game Boy Advance hand held console,
in addition to the original Game Boy hand held systems and its Super and Color
variants. VBA-M is a continued development of the now inactive VisualBoy
Advance project, with many improvements from various developments of VBA.

%prep
%setup -q
sed -i '/CMAKE_C.*_FLAGS/d' CMakeLists.txt
#To avoid confusion of the two .desktops:
sed -i '/Name=VBA-M/cName=VBA-M (WX)' src/wx/wx%{name}.desktop

%build
#Required for ffmpeg header to build
export CPATH='/usr/include/ffmpeg'
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DVERSION=%{version} -DCMAKE_SKIP_RPATH=ON -DENABLE_LINK=ON
free -m
make V=1

%install
make install DESTDIR=%{buildroot}
desktop-file-install \
  --remove-category Application \
  --remove-key=Encoding \
  --dir %{buildroot}%{_datadir}/applications \
  src/gtk/g%{name}.desktop
desktop-file-install \
  --remove-category Application \
  --remove-key=Encoding \
  --dir %{buildroot}%{_datadir}/applications \
  src/wx/wx%{name}.desktop
install -p -D -m 0644  debian/%{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1
%find_lang g%{name}
%find_lang wx%{name}

%files gtk -f g%{name}.lang
#excluded doc/ReadMe.MFC.txt, as it's not utf8 and seems very windows oriented
%doc doc/ips.htm
%{_datadir}/%{name}
%{_bindir}/g%{name}
%{_datadir}/applications/g%{name}.desktop

%files wx -f wx%{name}.lang
#excluded doc/ReadMe.MFC.txt, as it's not utf8 and seems very windows oriented
%doc doc/ips.htm
%{_bindir}/wx%{name}
%{_datadir}/applications/wx%{name}.desktop

%files sdl
%doc doc/ips.htm doc/ReadMe.SDL.txt
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}

%files common
%doc doc/gpl.txt doc/License.txt
%config(noreplace) /etc/%{name}.cfg

%files gui-common
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%post gtk
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtk
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post wx
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun wx
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans wx
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog
* Tue Feb 14 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-4
- Changed building commands to avoid failed builds
- Added Zip as a dependancy

* Thu Jan 29 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-3
- Added missing Build Requirement: openal-soft-devel
- Removed redundant license files

* Thu Jan 27 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-2
- Added DCMAKE_SKIP_RPATH=ON to cmake (fixes rpath error)
- Added more relevant package summaries
- Fixed up the descriptions a bit
- Enabled Linking Support
- Various tweaks

* Thu Jan 26 2012 Jeremy Newton <alexjnewt@hotmail.com> - 1.8.0.1054-1
- Updated new upstream version
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


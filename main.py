"""
Generates .DEB, .RPM, .TAR.GZ source for flatpak, and .ZIP SmartInstaller packages
System dependencies : zip, dpkg, rpmbuild, gzip, tar, fakeroot
pip packages : Pillow
WARNING : Please run ONLY on Linux

Made by Raouf Ould Ali
"""

import config, paths

import os
from PIL import Image

os.system("clear")

os.makedirs(paths.TMP, mode=0o755, exist_ok=True)
os.system(f"rm -rf {paths.TMP}/*")


def generate_desktop():
    return f'''[Desktop Entry]
Type=Application
Name={config.NAME}
Comment={config.DESCRIPTION}
Icon=/usr/bin/{config.ID}/{config.ICON}
Exec=/usr/bin/{config.ID}/{config.MAIN_BIN}
Terminal=false
StartupNotify=false
Categories={config.CATEGORIES}
Keywords={config.KEYWORDS}'''

def generate_deb():
    print(f'''-------------------------------------------------------------------------
        Eclipium Packager - Building {config.PACKAGE_ID}-{config.VERSION}.deb
-------------------------------------------------------------------------''')
    # On crée les dossiers nécessaires à la config
    os.makedirs(f'{paths.TMP}/deb/{config.PACKAGE_ID}/DEBIAN', mode=0o755, exist_ok=True)
    # On crée le fichier control
    control = open(f'{paths.TMP}/deb/{config.PACKAGE_ID}/DEBIAN/control', 'w')
    control.write(f'''Package: {config.PACKAGE_ID}
Version: {config.VERSION}
Section: base
Priority: optional
Architecture: all
Maintainer: {config.LINUX_MAINTAINER}
Description: {config.DESCRIPTION}
Homepage: {config.WEBSITE}
''')
    control.close()

    # Si nécessaire, on ajoute le script post-installation
    if config.POSTINST_COMMANDS:
        postinst = open(f'{paths.TMP}/deb/{config.PACKAGE_ID}/DEBIAN/postinst', 'w')
        postinst.write('#!/bin/bash\n' + config.POSTINST_COMMANDS)
        postinst.close()
    # On génére le raccourci dans les menus (.desktop)
    os.makedirs(f'{paths.TMP}/deb/{config.PACKAGE_ID}/usr/share/applications', mode=0o755)
    desktop = open(f'{paths.TMP}/deb/{config.PACKAGE_ID}/usr/share/applications/{config.ID}.desktop', 'w')
    desktop.write(generate_desktop())
    desktop.close()
    # On copie les binaires de l'app
    os.makedirs(f'{paths.TMP}/deb/{config.PACKAGE_ID}/usr/bin/{config.ID}', mode=0o755, exist_ok=True)
    os.system(f'cp -R {paths.LINUX_BINARIES}/* {paths.TMP}/deb/{config.PACKAGE_ID}/usr/bin/{config.ID}/')
    # Et l'icone de l'app
    os.system(f'cp {config.ICON} {paths.TMP}/deb/{config.PACKAGE_ID}/usr/bin/{config.ID}/')
    # Build le .DEB
    os.system(f"fakeroot sh -c 'cd {paths.TMP}/deb/ && dpkg-deb --build {config.PACKAGE_ID}'")
    # Déplacer dans le dossier build
    os.makedirs(f'{paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}', mode=0o755, exist_ok=True)
    os.system(f"mv {paths.TMP}/deb/{config.PACKAGE_ID}.deb {paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}/{config.PACKAGE_ID}-{config.VERSION}.deb")
    print(".deb package build succeeded !")


def generate_rpm():
    print(f'''-------------------------------------------------------------------------
        Eclipium Packager - Building {config.PACKAGE_ID}-{config.VERSION}-1.x86_64.rpm
-------------------------------------------------------------------------''')
    # On crée les dossiers nécessaires à la config
    os.makedirs(f'{paths.TMP}/rpm/SPECS', mode=0o755, exist_ok=True)
    # On crée le fichier spec
    spec = open(f'{paths.TMP}/rpm/SPECS/{config.PACKAGE_ID}.spec', 'w')
    content = '''%define name         ''' + config.PACKAGE_ID + '''
%define version      ''' + config.VERSION + '''
%define release      1
%define buildroot %{topdir}/%{name}-%{version}-root
%global __provides_exclude_from /*
%global __requires_exclude_from /*
BuildRoot: %{buildroot}
Summary: ''' + config.DESCRIPTION + '''
Name:     %{name}
Version:  %{version}
Release:  %{release}
License: ''' + config.LICENSE + '''
Group: ''' + config.RPM_GROUP + '''
URL: ''' + config.WEBSITE + '''

%description 
''' + config.DESCRIPTION + '''

%files
/usr/bin/''' + config.ID + '''/*
/usr/share/applications/''' + config.ID + '''.desktop

'''

    # Si nécessaire, on ajoute le script post-installation
    if config.POSTINST_COMMANDS:
        content = content + '%post\n' + config.POSTINST_SCRIPT

    spec.write(content)
    spec.close()

    # On génére le raccourci dans les menus (.desktop)
    os.makedirs(f'{paths.TMP}/rpm/BUILDROOT/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64/usr/share/applications', mode=0o755, exist_ok=True)
    desktop = open(f'{paths.TMP}/rpm/BUILDROOT/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64/usr/share/applications/{config.ID}.desktop', 'w')
    desktop.write(generate_desktop())
    desktop.close()
    # On copie les binaires de l'app
    os.makedirs(f'{paths.TMP}/rpm/BUILDROOT/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64/usr/bin/{config.ID}', mode=0o755)
    os.system(f'cp -R {paths.LINUX_BINARIES}/* {paths.TMP}/rpm/BUILDROOT/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64/usr/bin/{config.ID}/')
    # Et l'icone de l'app
    os.system(f'cp {config.ICON} {paths.TMP}/rpm/BUILDROOT/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64/usr/bin/{config.ID}/')
    # Build le .RPM
    os.system(f"sh -c 'cd {paths.TMP}/rpm/ && rpmbuild -v -ba ./SPECS/{config.PACKAGE_ID}.spec --define \"_topdir {paths.TMP}/rpm/\"'")
    # Déplacer dans le dossier build
    os.makedirs(f'{paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}', mode=0o755, exist_ok=True)
    os.system(f"mv {paths.TMP}/rpm/RPMS/x86_64/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64.rpm {paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}/{config.PACKAGE_ID}-{config.VERSION}-1.x86_64.rpm")
    print(".rpm package build succeeded !")



def generate_flatpak_source():
    print(f'''-------------------------------------------------------------------------
        Eclipium Packager - Building {config.PACKAGE_ID}-source-{config.VERSION}.tar.gz
-------------------------------------------------------------------------''')
    # On crée les dossiers nécessaires à la config
    os.makedirs(f'{paths.TMP}/src/{config.PACKAGE_ID}', mode=0o755)
    # On copie les binaires de l'app
    os.system(f'cp -R {paths.LINUX_BINARIES}/* {paths.TMP}/src/{config.PACKAGE_ID}/')
    # Et l'icone de l'app
    os.system(f'cp {config.ICON} {paths.TMP}/src/{config.PACKAGE_ID}/')
    image = Image.open(config.ICON)
    new_image = image.resize((128, 128))
    new_image.save(f'{paths.TMP}/src/{config.PACKAGE_ID}/128.png')
    new_image = image.resize((64, 64))
    new_image.save(f'{paths.TMP}/src/{config.PACKAGE_ID}/64.png')
    # Créer le package
    os.system(f"sh -c 'cd {paths.TMP}/src/{config.PACKAGE_ID}/ && tar -czvf ../{config.PACKAGE_ID}-source-{config.VERSION}.tar.gz ./'")
    # Déplacer dans le dossier cible
    os.makedirs(f'{paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}', mode=0o755, exist_ok=True)
    os.system(f'mv {paths.TMP}/src/{config.PACKAGE_ID}-source-{config.VERSION}.tar.gz {paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}/')
    print("Flatpak source build succeeded !")

def generate_smartinstaller_source():
    print(f'''-------------------------------------------------------------------------
        Eclipium Packager - Building {config.PACKAGE_ID}-{config.VERSION}.zip
-------------------------------------------------------------------------''')
    # On crée les dossiers nécessaires à la config
    os.makedirs(f'{paths.TMP}/win/{config.PACKAGE_ID}/bin', mode=0o755)
    # On copie les binaires de l'app
    os.system(f'cp -R {paths.WINDOWS_BINARIES}/* {paths.TMP}/win/{config.PACKAGE_ID}/bin/')
    # On génére le json de config
    pkg = open(f'{paths.TMP}/win/{config.PACKAGE_ID}/package.json', 'w')
    pkg.write('{'+f'''
	"Name": "{config.NAME}",
	"MainExe": "{config.MAIN_EXE}",
	"VersionName": "{config.VERSION}",
	"VersionCode": {config.VERSION_CODE},
	"Date": "{config.VERSION_DATE}"
'''+'}')
    pkg.close()
    # Créer le package
    os.system(f"sh -c 'cd {paths.TMP}/win/{config.PACKAGE_ID}/ && zip -r ../{config.PACKAGE_ID}-{config.VERSION}.zip ./'")
    # Déplacer dans le dossier cible
    os.makedirs(f'{paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}', mode=0o755, exist_ok=True)
    os.system(f'mv {paths.TMP}/win/{config.PACKAGE_ID}-{config.VERSION}.zip {paths.BUILD}/{config.PACKAGE_ID}-{config.VERSION}/')
    print("SmartInstaller source build succeeded !")

generate_deb()
generate_rpm()
generate_flatpak_source()
generate_smartinstaller_source()

os.system(f'rm -rf {paths.TMP}')

print(f'''-------------------------------------------------------------------------
        Eclipium Packager - Process finished
-------------------------------------------------------------------------''')

from rpmbuild import generate_rpm
from debbuild import generate_deb
from flatpaksourcebuild import generate_flatpak_source
from smartinstallerbuild import generate_smartinstaller
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Packages to build.')
    parser.add_argument('-r', '--rpm', action='store_true', help='Generate a RPM package')
    parser.add_argument('-d', '--deb', action='store_true', help='Generate a DEB package')
    parser.add_argument('-s', '--s_installer', action='store_true', help='Generate a SmartInstaller archive')
    parser.add_argument('-f', '--flatpak_source', action='store_true', help='Generate a Flatpak source archive')
    args = parser.parse_args()
    
    if args.rpm == args.deb == args.s_installer == args.flatpak_source == False:
        parser.print_help()
    if args.rpm:
        generate_rpm()
    if args.deb:
        generate_deb()
    if args.s_installer:
        generate_smartinstaller()
    if args.flatpak_source:
        generate_flatpak_source()
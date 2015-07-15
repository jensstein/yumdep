#!/usr/bin/python2
# -*- coding: utf-8 -*-

# The yum module has only been written for python2
# TODO: Use python3-dnf for python3 support
# http://yum.baseurl.org/api/yum/
# http://akozumpl.github.io/dnf/api.html

import argparse
import rpmUtils
import sys
import yum

def add_sizes(yumbase, package_list):
    size_total = 0
    size_download = 0
    size_installed = 0
    for package in package_list:
        size_total += package.installedsize
        if not yumbase.rpmdb.installed(package.name):
            size_download += package.size
            size_installed += package.installedsize
    return {"size_total": size_total, "size_download": size_download,
        "size_installed": size_installed}

def format_size(size):
    if size < 1024:
        return str(size) + " b"
    elif size < (1024 ** 2):
        return str(round(size / 1024.0, 1)) + " k"
    elif size < (1024 ** 3):
        return str(round(size / (1024.0 ** 2), 1)) + " M"
    elif size < (1024 ** 4):
        return str(round(size / (1024.0 ** 3), 1)) + " G"
    else:
        return str(size)

def get_deps(yumbase, package, package_list=[]):
    deps = yumbase.findDeps(package)
    for dep in deps:
        for key, values in deps[dep].iteritems():
            # packages excluded in yum.conf will have values as an empty list
            if len(values) > 0:
                value = sorted(values)[-1] # take the newest version of the package
                if value not in package_list:
                    package_list.append(value)
                    get_deps(yumbase, [value], package_list)
    return package_list

def print_all_packages(package_list):
    for package in package_list:
        print package.name + " " + format_size(package.size)

def print_noninstalled_packages(yumbase, package_list):
    for package in package_list:
        if not yumbase.rpmdb.installed(package.name):
            print package.name + " " + format_size(package.size)

def setup_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', metavar='package',
        help='package to search for',
        type=str)
    parser.add_argument('-v', '--verbose', action="store_true",
        help='print list of non-installed denpendencies')
    # hyphens are converted to underscores in the namespace
    parser.add_argument('-a', '--all-dependencies', action="store_true",
        help='print list of all individual denpendencies')
    return parser.parse_args()

def main():
    size_total = 0
    size_download = 0
    size_installed = 0
    package_dict = {}
    args = setup_args()
    yumbase = yum.YumBase()
    yumbase.setCacheDir()
    try:
        pkg_parts = args.package.split(".")
        if pkg_parts[-1] in rpmUtils.arch.getArchList():
            pkgs = yumbase.pkgSack.returnNewestByNameArch((pkg_parts[0], pkg_parts[1]))
        else:
            pkgs = yumbase.pkgSack.returnNewestByName(args.package)
        deps = yumbase.findDeps(pkgs)
    except yum.Errors.PackageSackError, e:
        print e
        sys.exit(1)
    if yumbase.rpmdb.installed(args.package):
        print args.package + " is already installed."
    size_total += pkgs[0].installedsize
    size_download += pkgs[0].size
    size_installed += pkgs[0].installedsize
    package_list = sorted(get_deps(yumbase, pkgs))
    sizes = add_sizes(yumbase, package_list)
    size_total += sizes["size_total"]
    size_download += sizes["size_download"]
    size_installed += sizes["size_installed"]

    print pkgs[0].name + ": " + format_size(pkgs[0].size)
    print "---------------------"
    if args.verbose:
        print_noninstalled_packages(yumbase, package_list)
        print "---------------------"
    elif args.all_dependencies:
        print_all_packages(package_list)
        print "---------------------"

    print "Size to download: " + format_size(size_download)
    print "Installed size: " + format_size(size_installed)
    print "Total size (all dependencies): " + format_size(size_total)

if __name__ == "__main__":
    main()

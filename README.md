yumdep
======
yumdep is a program to list dependencies and their size requirements of packages on yum-based systems.
it provides a similar functionality to the commands `repoquery --requires --resolve $package` and `yum deplist $package`, but including information about size requirements and giving cleaner output.
yumdep is inspired by the wonderful pacdep program for arch linux: https://github.com/jjk-jacky/pacdep

installing
==========
yumdep can be installed with make:`make install`  
the install location can be modified directly in the makefile or via the PREFIX and SYSCONFDIR variables. make of course needs to run with the proper permissions for the chosen directories (/usr/local and /etc by default).  
uninstalling is just `make uninstall`

author
======
jens stein

license
=======
yumdep is released under the MIT license. see COPYING for more details. 

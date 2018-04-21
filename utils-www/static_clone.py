import subprocess
import os
from static_domains import onepagers

if(os.geteuid()==0):
    print(" ")
    print(" ")
    print("ERROR: This script should not be run as root.")
    print(" ")
    print(" ")
    exit(1)


if( os.path.isdir('/www') is False ):
    print(" ")
    print(" ")
    print("ERROR: The /www directory does not exist.")
    print(" ")
    print(" ")
    exit(1)



for name in onepagers:
    url = onepagers[name]

    basedir = os.path.join("/www",name)
    mkdircmd = ["mkdir","-p",basedir]
    clonecmd = ["git","-C",basedir,"clone","--separate-git-dir=git","-b","gh-pages",url,"htdocs"]

    if( os.path.isdir( os.path.join(basedir,"git") ) 
    and os.path.isdir( os.path.join(basedir,"htdocs")) ):
        print(" ")
        print(" ")
        print("ERROR: The directories /www/%s/git and /www/%s/htodcs"%(name,name))
        print(" already exist. Use the static_update.py script instead. ")
        print(" ")
        exit(1)

    print(" ")
    print("About to run the command:")
    print("    $ " + " ".join(clonecmd))
    print(" ")
    response = input('Okay to proceed? (y/n) ')
    if(response=='y' or response=='Y' or response=='yes'):
        subprocess.call(mkdircmd)
        subprocess.call(clonecmd)


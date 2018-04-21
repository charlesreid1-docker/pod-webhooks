import subprocess
import os
from static_domains import onepagers


if( os.path.isdir('/www') is False ):
    mkdircmd = ["mkdir","/www"]
    subprocess.call(mkdircmd)

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
    subprocess.call(mkdircmd)
    subprocess.call(clonecmd)


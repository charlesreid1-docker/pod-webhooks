#!/usr/bin/env python3
import subprocess
import os

# Run a series of git clone commands to set up
# the subdomain pages for pages, bots, and hooks

subs = ['bots','pages','hooks']
urls = ['https://git.charlesreid1.com/charlesreid1/%s'%(sub) for sub in subs]
#urls = ['https://github.com/charlesreid1-docker/%s.charlesreid1.com'%(sub) for sub in subs]
pths = [os.path.join('/www',sub) for sub in subs]

for sub, url, pth in zip(subs,urls,pths):

    # Create the base directory
    subprocess.call(['mkdir','-p',pth])

    # Construct clone command
    workdir = os.path.join(pth,"htdocs",sub)
    gitdir = os.path.join(pth,"git.%s"%(sub))
    clonecmd = ['git','clone','--separate-git-dir=%s'%(gitdir),'-b','gh-pages',url,workdir]

    print("About to clone the submodule %s using command:\n"%(sub))
    print("    $ " + " ".join(clonecmd))
    print("\n")

    try:
        p = subprocess.Popen(clonecmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print("Something went wrong. Output:")
        print(p.stdout.readline())
        print(p.stderr.readline())
    finally:
        print("Done. Next command...")


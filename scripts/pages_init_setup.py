#!/usr/bin/env python3
import subprocess
import os

# Run a series of git clone commands to set up
# all the pages that should already exist in
# /www/pages.charlesreid1.com
#
# gh-pages branches only

repo_names = '''bots/b-apollo
bots/b-captain-hook
bots/b-ginsberg
bots/b-milton
bots/boring-mind-machine
charelsreid1/bots.charlesreid1.com
docker/d-gitea
docker/d-mediawiki
docker/d-mysql
docker/d-nginx-charlesreid1
docker/d-nginx-subdomains
docker/d-phpmyadmin
docker/d-python-files
docker/d-python-helium
charlesreid1/dont-sudo-pip
bots/embarcadero-mind-machine
charlesreid1/git-commit-ectomy
charlesreid1/git-subway-maps
charlesreid1/github-heroku-attack-rabbits
charlesreid1/hooks.charlesreid1.com
charlesreid1/how-do-i-heroku
charlesreid1/how-do-i-pandoc
charlesreid1/how-do-i-pelican
charlesreid1/how-do-i-pyenv
charlesreid1/how-do-i-snakemake
bots/mississippi-mind-machine
charlesreid1/pages.charlesreid1.com
bots/papyrus-mind-machine
docker/pod-bots
docker/pod-charlesreid1
docker/pod-webhooks
bots/rainbow-mind-machine
bots/russian-rainbow-mind-machine
charlesreid1/scurvy-knave-theme
charlesreid1/search-demo-mkdocs-material
charlesreid1/translate-yer-docs
charlesreid1/uncle-archie
bots/waxing-gibbous-mind-machine
charlesreid1/wisko-manual'''.split('\n')

repo_urls = ['https://git.charlesreid1.com/%s.git'%(j) for j in repo_names]

root = '/www'
pages = 'pages.charlesreid1.com'
basedir = os.path.join(root,pages)

subprocess.call(['mkdir','-p',basedir])

for name,url in zip(repo_names,repo_urls):
    
    # ------------------
    # pages
    #
    # for a hypothetical repo "project":
    # 
    # .git dir:     /www/pages.charlesreid1.com/git.project
    # htdocs dir:     /www/pages.charlesreid1.com/htdocs/project
    
    workdir = os.path.join(basedir,"htdocs",name)
    gitdir = os.path.join(basedir,"git.%s"%(name))
    
    # clone
    mkdircmd = ["mkdir","-p",basedir]
    clonecmd = ["git","clone","--separate-git-dir=%s"%(gitdir),"-b","gh-pages",url,workdir]
    print("About to run the command:\n")
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



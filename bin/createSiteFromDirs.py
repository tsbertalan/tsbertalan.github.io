#!/usr/bin/env python
from os import listdir, mkdir
from os.path import basename, join, isdir, dirname
from shutil import copy
from subprocess import check_output, CalledProcessError
import markdown
import json

from standalonePage import article
import utils
import index


baseDir = '/home/tsbertalan/Documents/Projects'

def listdirs(folder):
    return [
        d for d in (join(folder, d1) for d1 in listdir(folder))
        if isdir(d)
    ]
    
projectDirs = listdirs(baseDir)
cards = []

for projectDir in projectDirs:
        
    # Try to find a www.json file.
    docFolder = utils.first([f for f in listdirs(projectDir) if 'doc' in basename(f).lower()])
    imgSrc = 'images/1px.png'
    if docFolder is not None:
        configFile = utils.first([f for f in listdir(docFolder) if f == 'www.json'])
        if configFile is None:
            continue  # Skip this project if there's no www.json file.
        config = json.load(open(join(docFolder, configFile), 'r'))
        if 'skip project' in config and config['skip project']:
            continue  # Skip this project if we're explicitly told to.
        print 'docFolder is', docFolder
        baseProjectName = config.get('project name', basename(projectDir))
        hero = config.get('hero image', 'images/1px.png')
        blurb = config.get('blurb', '')
        description = config.get('description', 'see README.md')
        if description == 'see README.md':
            
            for f in listdir(projectDir):
                path = join(projectDir, f)
                basePath = basename(path)
                if basePath == 'README.md':
                #if len(basePath) >= 2 and basePath[-2:].lower() = 'md':
                    # Assume we've found a top-level markdown file.
                    print 'Found %s in directory %s.' % (basePath, projectDir)  
                    description = open(path).read()
        
    else:
        continue  # Skip this project if there's not /*doc*/ subfolder.
    
    # Prepare a folder to put the output in.
    destination = join('.', baseProjectName, 'index.html')
    try:
        mkdir(dirname(destination))
    except OSError:
        pass

    # Copy hero image to output folder.        
    print 'hero is', hero
    imgSrc = join(dirname(destination), basename(hero))
    copy(join(projectDir, hero), imgSrc)
    
    # Try to construct a github link.
    repo = None
    try:
        remotes = [l for l in check_output(["git", "remote", "-v"], cwd=projectDir).split('\n') if 'github' in l and 'bertalan' in l]
        if len(remotes) > 0:
            repo = 'http://github.com/' + remotes[0].split()[1][15:][:-4]
    except CalledProcessError:
        pass
        
    # Generate HTML for the page contents.
    readmeHtml = markdown.markdown(description)
    
    # Generate and write the full project page. 
    breadcrumbs = [utils.Tag('a', href='../index.html', tagText='Home'), utils.Tag('span', tagText=baseProjectName, parseTagText=False)]
    pageHtml = article(
                       #utils.Tag('a', href='../index.html', tagText='Tom Bertalan'),
                       'Tom Bertalan',
                       readmeHtml, breadcrumbs=breadcrumbs, sourceLink=repo, heading=False)
    utils.writePage(pageHtml, destination)
        
    # Generate a card for this project to put on the home page.
    cards.append(index.portfolioCard(baseProjectName, blurb, imgSrc=imgSrc, linkDest=destination, imgAlt=blurb))
    
# Generate, write, and display the home page. 
homepageHtml = index.index(cards=cards)
utils.displayHtml(homepageHtml, fname='./index.html')

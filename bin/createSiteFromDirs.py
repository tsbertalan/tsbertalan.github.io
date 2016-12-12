#!/usr/bin/env python
from os import listdir, mkdir
from os.path import basename, join, isdir, dirname
from shutil import copy
from subprocess import check_output, CalledProcessError
import markdown

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
    baseProjectName = basename(projectDir)
    contents = listdir(projectDir)
    for path in contents:
        path = join(projectDir, path)
        basePath = basename(path)
        if basePath == 'README.md':
        #if len(basePath) >= 2 and basePath[-2:].lower() = 'md':
        
            # Try to check for a github repo.
            repo = None
            try:
                remotes = [l for l in check_output(["git", "remote", "-v"], cwd=projectDir).split('\n') if 'github' in l and 'bertalan' in l]
                if len(remotes) > 0:
                    repo = 'http://github.com/' + remotes[0].split()[1][15:][:-4]
            except CalledProcessError:
                pass
                
            # Prepare a folder to put the output in.
            destination = join('.', baseProjectName, 'index.html')
            try:
                mkdir(dirname(destination))
            except OSError:
                pass
            
            # Assume we've found a top-level markdown file.
            print 'Found %s in directory %s.' % (basePath, projectDir)  
            readmeHtml = markdown.markdown(open(path).read())
            blurb = 'This is the blurb.'
            
            # Try to find a hero image.
            docFolder = utils.first([f for f in listdirs(projectDir) if 'doc' in basename(f).lower()])
            imgSrc = 'images/1px.png'
            if docFolder is not None:
                print 'docFolder is', docFolder
                hero = utils.first([f for f in listdir(docFolder) if 'hero' in f])
                if hero is not None:
                    print 'hero is', hero
                    imgSrc = join(dirname(destination), hero)
                    copy(join(docFolder, hero), imgSrc)
            breadcrumbs = [utils.Tag('a', href='../index.html', tagText='Home'), utils.Tag('span', tagText=baseProjectName, parseTagText=False)]

            pageHtml = article(
                               #utils.Tag('a', href='../index.html', tagText='Tom Bertalan'),
                               'Tom Bertalan',
                               readmeHtml, breadcrumbs=breadcrumbs, sourceLink=repo, heading=False)
            
            # Write the project page.
            utils.writePage(pageHtml, destination)
                
            # Add the page to a list to make a home page.
            cards.append(index.portfolioCard(baseProjectName, blurb, imgSrc=imgSrc, linkDest=destination, imgAlt=blurb))
    
homepageHtml = index.index(cards=cards)
utils.displayHtml(homepageHtml, fname='./index.html')
                
    
#     # Look for a doc[s]/www subdir.
#     subdirs = listdirs(projectDir)
#     for subdir in subdirs:
#         if 'doc' in basename(subdir):
#             docpath = subdir
#             
#             
#             break
#     # If we got here, we've either found and processed a doc subdir, or failed and should move on.
#!/usr/bin/env python
from os import listdir, mkdir
from os.path import basename, join, isdir, dirname
import codecs
from shutil import copy
from subprocess import check_output, CalledProcessError
import markdown
import json

from standalonePage import article, parseOrLoadMarkdown
import utils
import mainPage
from utils import writePage


baseDir = '/home/tsbertalan/Documents/Projects'
wwwDir = '../'

def listdirs(folder):
    return [
        d for d in (join(folder, d1) for d1 in listdir(folder))
        if isdir(d)
    ]
    
projectDirs = listdirs(baseDir)
projectDirs.sort()
projectDirs = projectDirs[::-1]
cards = []
starredCards = []

for projectDir in projectDirs:
        
    # Try to find a www.json file.
    docFolder = utils.first([f for f in listdirs(projectDir) if 'doc' in basename(f).lower()])
    imgSrc = 'images/1px.png'
    if docFolder is not None:
        configFile = utils.first([f for f in listdir(docFolder) if f == 'www.json'])
        if configFile is None:
            continue  # Skip this project if there's no www.json file.
        print 'Loading', configFile, 'for project', basename(projectDir)
        config = json.load(open(join(docFolder, configFile), 'r'))
        if 'skip project' in config and config['skip project']:
            continue  # Skip this project if we're explicitly told to.
        baseProjectName = config.get('project name', basename(projectDir))
        hero = config.get('hero image', None)
        print 'Got hero image',  hero
        blurb = config.get('blurb', '')
        description = config.get('description', None)
        starred = config.get('starred', False)
        description = parseOrLoadMarkdown(description, projectDir)
        entries = config.get('entries', [])
        for entry in entries:
            entry['content'] = markdown.markdown(
                parseOrLoadMarkdown(entry['content'], projectDir)
                )
        

    else:
        continue  # Skip this project if there's not /*doc*/ subfolder.

    # Prepare a folder to put the output in.
    destinationFileLocation = join(wwwDir, baseProjectName, 'index.html')
    linkDestination = join(baseProjectName, 'index.html')
    print 'Link destination is', linkDestination
    try:
        mkdir(dirname(destinationFileLocation))
    except OSError:
        pass

    # Copy hero image to output folder.        
    print 'hero is', hero
    if hero is None:
        imgSrc = None
    else:
        imgSrc = join(baseProjectName, basename(hero))
        fr = join(projectDir, hero)
        imgCpLoc = join(dirname(destinationFileLocation), basename(hero))
        to = imgCpLoc
        print 'Copying from %s to %s.' % (fr, to)
        copy(fr, to)
        
    if description is not None:    
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
        
        # Generate and write the project page. 
        breadcrumbs = [utils.Tag('a', href='../index.html', tagText='Home'), utils.Tag('span', tagText=baseProjectName, parseTagText=False)]
        pageHtml = article(
                           utils.Tag('a', tagText='Tom Bertalan', href='../index.html',
                                     cls='mdl-typography--headline', style='text-decoration:none; color:#444;'),
                           readmeHtml,
                           heading=False,
                           breadcrumbs=breadcrumbs,
                           sourceLink=repo,
                           entries=entries,
                           )
        utils.writePage(pageHtml, destinationFileLocation)
    else:
        linkDestination = None
        
    card = mainPage.portfolioCard(baseProjectName, blurb, imgSrc=imgSrc, linkDest=linkDestination, imgAlt=blurb)
    
    # Generate a card for this project to put on the home page.
    if starred:
        starredCards.append((starred, card))
    else:
        cards.append(card)
        
starredCards = [card for (starred, card) in sorted(starredCards)]

starredCards.extend(cards)

cards = starredCards
    
# Generate, write, and display the home page. 
homepageHtml = mainPage.index(cards=cards)
homepageFileLocation = join(wwwDir, 'index.html')
utils.writePage(homepageHtml, homepageFileLocation, DEBUG=True)
if False:
    utils.displayHtml(homepageHtml, fname=homepageFileLocation)

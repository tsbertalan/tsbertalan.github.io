#!/usr/bin/env python
from os import listdir, mkdir
from os.path import basename, join, isdir, dirname
import codecs
from shutil import copy as shcopy
def copy(f, t):
    print('$ cp %s %s' % (f, t))
    shcopy(f, t)
from subprocess import check_output, CalledProcessError
import markdown
import json

from standalonePage import article, parseOrLoadMarkdown, markdown_to_html
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
        config = json.load(open(join(docFolder, configFile), 'r'))
        if 'skip project' in config and config['skip project']:
            continue  # Skip this project if we're explicitly told to.
        baseProjectName = config.get('project name', basename(projectDir))
        hero = config.get('hero image', None)
        print('Got hero image:', hero)
        blurb = config.get('blurb', '')
        description = config.get('description', None)
        starred = config.get('starred', False)
        description = parseOrLoadMarkdown(description, projectDir)
        entries = config.get('entries', [])
        for entry in entries:
            entry['content'] = parseOrLoadMarkdown(entry['content'], projectDir)

    else:
        continue  # Skip this project if there's not /*doc*/ subfolder.

    # Also skip if we explicitly note that we should.
    if 'exclude_from_website' in config and config['exclude_from_website']:
    	continue

    # Prepare a folder to put the output in.
    destinationFileLocation = join(wwwDir, baseProjectName, 'index.html')
    linkDestination = join(baseProjectName, 'index.html')
    try:
        mkdir(dirname(destinationFileLocation))
    except OSError:
        pass

    # Copy hero image to output folder.        
    if hero is None:
        imgSrc = None
    else:
        imgSrc = join(baseProjectName, basename(hero))
        fr = join(projectDir, hero)
        imgCpLoc = join(dirname(destinationFileLocation), basename(hero))
        to = imgCpLoc
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
        readmeHtml = markdown_to_html(description)

        # Assign urls to the entry pages.
        for k, entry in enumerate(entries):
            entry['url'] = (
                # 'entry_%d-' % k
                # +
                utils.sanitize(entry['title'].replace(' ', '_'), extra='_')
                +'.html'
            )
            entry['save_path'] = join(wwwDir, baseProjectName, entry['url'])
        
        # Generate and write the project page. 
        breadcrumbs = [
            utils.Tag('a', href='../index.html', tagText='Home'), 
            utils.Tag('span', tagText=baseProjectName, parseTagText=False)
        ]

        home_title_link = utils.Tag(
            'a', tagText='Tom Bertalan', href='../index.html',
            cls='mdl-typography--headline', style='text-decoration:none; color:#444;'
        )

        pageHtml, pageFiles = article(
            home_title_link,
            readmeHtml,
            breadcrumbs=breadcrumbs,
            sourceLink=repo,
            entries=entries,
        )
        utils.writePage(pageHtml, pageFiles, destinationFileLocation, projectDir, DEBUG=False)

        # Write the entries to their own pages.
        for k, entry in enumerate(entries):
            articleHtml, _unused = article(
                home_title_link,
                markdown_to_html(entry['content']),
                heading=entry['title'],
                breadcrumbs=[
                    utils.Tag('a', href='../index.html', tagText='Home'), 
                    utils.Tag('a', tagText=baseProjectName, parseTagText=False, href='index.html'),
                    utils.Tag('span', tagText=entry['title'], parseTagText=False),
                ]
            )
            utils.writePage(articleHtml, [], entry['save_path'], projectDir, DEBUG=False)

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
utils.writePage(homepageHtml, [], homepageFileLocation, None, DEBUG=False)
if False:
    utils.displayHtml(homepageHtml, fname=homepageFileLocation)

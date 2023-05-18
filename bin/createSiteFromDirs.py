#!/usr/bin/env python2
from __future__ import print_function
from os import listdir, mkdir, makedirs
from os.path import basename, join, isdir, dirname, exists, realpath
import codecs
from shutil import copy, SameFileError
from subprocess import check_output, CalledProcessError
import markdown
import json

import sys
HERE = realpath(dirname(__file__))
sys.path.append(join(HERE, '..', 'src'))

# Change working directory to just above the script's directory.
from os import chdir
chdir(join(HERE, '..'))


from standalonePage import article, parseOrLoadMarkdown, markdown_to_html
import utils
import mainPage
from utils import writePage
from warnings import warn


def mkdir_p(path):
    # https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    import errno, os
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >= 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # possibly handle other errno cases here, otherwise finally:
        else:
            raise


baseDir = '/home/tsbertalan/Documents/Projects'
archiveDir = '/home/tsbertalan/Documents/Archived Projects'
dirs = baseDir, archiveDir, '/home/tsbertalan/Documents/Delayed Projects'
wwwDir = join(HERE, '..')

def listdirs(folder):
    return [
        d for d in (join(folder, d1) for d1 in listdir(folder))
        if isdir(d)
    ]


projectDirs = []
for search_dir in dirs:    
    if exists(search_dir):
        projectDirs.extend(listdirs(search_dir))
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
        config['archived'] = baseDir not in projectDir  # For future use.
        if 'skip project' in config and config['skip project']:
            continue  # Skip this project if we're explicitly told to.
        else:
            print('Adding project to site:', projectDir)
        baseProjectName = config.get('project name', basename(projectDir))
        hero = config.get('hero image', None)
        blurb = config.get('blurb', '')
        description = config.get('description', None)
        starred = config.get('starred', False)
        description = parseOrLoadMarkdown(description, projectDir)
        entries = config.get('entries', [])
        extra_files = config.get('extra files', [])
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError('Each entry must be a dict with at least a "content" key.')
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
        makedirs(dirname(destinationFileLocation), exist_ok=True)
    except OSError as e:
        print(f'Failed to make directory {dirname(destinationFileLocation)}: {e}')

    # Copy hero image to output folder.        
    if hero is None:
        imgSrc = None
    else:
        imgSrc = join(baseProjectName, basename(hero))
        fr = join(projectDir, hero)
        imgCpLoc = join(dirname(destinationFileLocation), basename(hero))
        to = imgCpLoc
        try:
            copy(fr, to)
        except IOError:
            warn('Failed copy from %s to %s.' % (fr, to))
        
    if description is not None:    
        # Try to construct a github link.
        repo = None
        try:
            cmd_output = check_output(["git", "remote", "-v"], cwd=projectDir).decode('utf-8').split('\n')
            remotes = [l for l in cmd_output if 'github' in l and 'bertalan' in l]
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
        to_copy = list(extra_files)
        for k, entry in enumerate(entries):
            articleHtml, _unused = article(
                home_title_link,
                markdown_to_html(entry['content']),
                heading=entry['title'],
                breadcrumbs=[
                    utils.Tag('a', href='../index.html', tagText='Home'), 
                    utils.Tag('a', tagText=baseProjectName, parseTagText=False, href='index.html'),
                    utils.Tag('span', tagText=entry['title'], parseTagText=False),
                ],
                sourceLink=entry.get("sourceLink", None),
                sourceLinkText=entry.get("sourceLinkText", '')
            )
            utils.writePage(articleHtml, [], entry['save_path'], projectDir, DEBUG=False)

            to_copy.extend(entry.get('files', []))

        # Copy any specified files to a subdir relative to the project.
        for file_path in to_copy:
            if file_path.startswith('/'):
                # Don't allow absolute paths.
                warn('Skipping copy for absolute path: %s' % file_path)
            else:
                src = join(projectDir, file_path)
                if not exists(src):
                    warn("Couldn't find file to copy: %s" % file_path)
                else:
                    dest = join(wwwDir, baseProjectName, file_path)
                    dest_dir = dirname(dest)
                    try:
                        mkdir_p(dest_dir)
                    except OSError:
                        pass
                    try:
                        copy(src, dest)
                        print('Putting file in %s.' % dest)
                    except SameFileError as e:
                        print('Skipping same-file copy of %s to %s.' % (src, dest))
                    


    else:
        linkDestination = None

    card = mainPage.portfolioCard(baseProjectName, blurb, imgSrc=imgSrc, linkDest=linkDestination, imgAlt=blurb)
    
    # Generate a card for this project to put on the home page.
    if starred:
        starredCards.append((starred, card))
    else:
        cards.append(card)
        
starredCards = [card for (starred, card) in sorted(starredCards, key=lambda starnumber_card: starnumber_card[0])]

starredCards.extend(cards)

cards = starredCards
    
# Generate, write, and display the home page. 
homepageHtml = mainPage.index(cards=cards)
homepageFileLocation = join(wwwDir, 'index.html')
utils.writePage(homepageHtml, [], homepageFileLocation, None, DEBUG=False)
if False:
    utils.displayHtml(homepageHtml, fname=homepageFileLocation)

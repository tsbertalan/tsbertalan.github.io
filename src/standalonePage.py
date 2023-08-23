'''
Created on Dec 8, 2016

@author: tsbertalan
'''
from page import Html
from utils import Tag, child, Div, parseAnonymousHTML, tostring, add_mathjax
from lxml.etree import _Element

from os import listdir
from os.path import basename, join
import codecs


def articleStyle():
# /**
#  * Copyright 2015 Google Inc. All Rights Reserved.
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  *      http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  */
    return '''
.demo-ribbon {
  width: 100%;
  height: 40vh;
  //background-image: url("hero.png");
  background-color: #f5f5f5;
  flex-shrink: 0;
}

.demo-main {
  margin-top: -35vh;
  flex-shrink: 0;
}

.demo-header .mdl-layout__header-row {
  padding-left: 40px;
}

.demo-container {
  max-width: 1600px;
  width: calc(100% - 16px);
  margin: 0 auto;
}

.demo-content {
  border-radius: 2px;
  padding: 80px 56px;
  margin-bottom: 80px;
}

.demo-layout.is-small-screen .demo-content {
  padding: 40px 28px;
}

.demo-content h3 {
  margin-top: 48px;
}

.demo-footer {
  padding-left: 40px;
}

.demo-footer .mdl-mini-footer--link-list a {
  font-size: 13px;
}
#view-source {
    float: right;
}
''' 


def article(title, content, heading=None, breadcrumbs=None, sourceLink=None, entries=[], sourceLinkText='Project Files'):
    
    html = Html()
    head = child(html, 'head')
    head.append(Tag('style', tagText=articleStyle(), parseTagText=False))
    add_mathjax(head)
    head.append(Tag('script', type="text/javascript", async_=None, src="../mermaid.min.js"))
    head.append(Tag('link', rel='stylesheet', href='../colorful.css'))
    head.append(Tag('link', rel='stylesheet', href='../styles.css'))
    head.append(Tag('link', rel='stylesheet', href='../pygments.css'))
    head.append(Tag('link', rel='stylesheet', href='../colorful.css'))


    
    # Add script for expanding entries.
    head.append(Tag('script',
                    tagText='''
                    function show(toExpand)
                    {
                    if(
                       document.getElementById(toExpand).style.display == 'none'
                       ||
                       document.getElementById(toExpand).style.display == ''
                       )
                        document.getElementById(toExpand).style.display = 'block';
                    else
                        document.getElementById(toExpand).style.display = 'none';
                    }
                    ''',
                    parseTagText=False,
                    ))
    
    body = child(html, 'body')
    
    container = Div(cls='demo-layout mdl-layout mdl-layout--fixed-header mdl-js-layout mdl-color--grey-100')
    body.append(container)
    
    if title is not None:
        header = Tag('header', cls='demo-header mdl-layout__header mdl-layout__header--scroll mdl-color--grey-100 mdl-color-text--grey-800')
        container.append(header)
        headerRow = Div(cls='mdl-layout__header-row')
        header.append(headerRow)
        if isinstance(title, _Element):
            headerRow.append(Tag('span', cls='mdl-layout-title', toAppend=[title]))
        else:
            headerRow.append(Tag('span', cls='mdl-layout-title', tagText=title))
        headerRow.append(Div(cls='mdl-layout-spacer'))
    
    container.append(Div(cls='demo-ribbon'))
    
    mainDiv = Tag('main', cls='demo-main mdl-layout__content')
    container.append(mainDiv)
    
    grid = Div(cls='demo-container mdl-grid')
    mainDiv.append(grid)
    
    def newBox():
        grid.append(Div(cls='mdl-cell mdl-cell--2-col mdl-cell--hide-tablet mdl-cell--hide-phone'))    
        col = Div(cls='demo-content mdl-color--white mdl-shadow--4dp content mdl-color-text--grey-800 mdl-cell mdl-cell--8-col')
        grid.append(col)
        grid.append(Div(cls='mdl-cell mdl-cell--2-col mdl-cell--hide-tablet mdl-cell--hide-phone'))
        return col
    

    # Construct breadcrumbs. 
    mainBox = newBox()
    breadcrumbsDiv = Div(cls='demo-crumbs mdl-color-text--grey-500',
                   toAppend=breadcrumbs)
    mainBox.append(breadcrumbsDiv)
    if breadcrumbs is not None:
        for crumb in breadcrumbs:
            assert isinstance(crumb, _Element)
        if len(breadcrumbs) > 1:
            for crumb in breadcrumbs[:-1]:
                if crumb.tail is None:
                    crumb.tail = ''
                crumb.tail += ' > '
        breadcrumbsDiv.extend(breadcrumbs)
        
    if sourceLink is not None:
        sourceButton = Tag('a', href=sourceLink, id='view-source',
                           tagText=sourceLinkText,
            cls="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--accent mdl-color-text--accent-contrast")
        breadcrumbsDiv.append(sourceButton)
    
    def extendWithHTML(html, elementToExtend):    
        initialSpan = Tag('span')
        elementToExtend.append(initialSpan)
        head, contents, tail = parseAnonymousHTML(html)
        if head is not None:
            initialSpan.tail = head
        if tail is not None:
            contents[-1].tail += tail
        elementToExtend.extend(contents)
       
    # For main pages, we don't want the heading, since they're often README.md files,
    # which have their own title heading. For entries, though, it's desirable.
    if heading:
        extendWithHTML('<h1>%s</h1>' % heading, mainBox)

    # Add the content into the mainbox.
    extendWithHTML(content, mainBox)

    # If we have entries to show, list them here.
    if len(entries) > 0:
        entry_list = '<h2>Entries</h2>'
        # entry_list += '<ul>'
        for entry in entries:
            # entry_list += '<li>'
            entry_list += '<p>'
            entry_list += '<a href="%s" title="%s">%s</a>' % (
                entry['url'], entry['subtitle'], entry['title'],
            )
            st = entry.get('subtitle', None)
            if st:
                entry_list += ' <small><i>%s</i></small>' % st
            # entry_list += '</li>'
            entry_list += '</p>'
        # entry_list += '</ul>'
        extendWithHTML(entry_list, mainBox)

    # If there are any journal entries to append, add them now.
    filePaths = []
    expandStyles = []
    if len(entries) > 0:
        for entryNum, entry in enumerate(entries):
            entryFilePaths = entry.get('files', [])
            filePaths.extend(entryFilePaths)
            
    # Append all generated expand/contract styles to the document HEAD. 
    head.append(Tag('style',
                    tagText='\n'.join(expandStyles),
                    parseTagText=False,
                    ))         
    
    return html, filePaths

from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree


class NoItalUndersclineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        # Do nothing.
        return None, None, None


class NoItalUnderscExtension(Extension):
    def extendMarkdown(self, md):
        USC_PATTERN = r'_(.*?)'  # like abcd_
        # Replace the existing underscore patterns with our No-Op.
        md.inlinePatterns.register(NoItalUndersclineProcessor(USC_PATTERN, md), 'strong2', 175)
        md.inlinePatterns.register(NoItalUndersclineProcessor(USC_PATTERN, md), 'emphasis2', 175)


def markdown_to_html(md):
    import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    import pymdownx.emoji
    import pymdownx.tasklist

    # My own crude re-escaping of double backslashes, so my latex arrays look the same as they do in typora.
    if r'\\' in md:
        md = md.replace(r'\\', r'\\\\')
    return markdown.markdown(md, extensions=[
        #'codehilite',
        CodeHiliteExtension(use_pygments=True),
        # 'markdown_checklist.extension',
        # 'pymdownx.tasklist',
        pymdownx.tasklist.makeExtension(custom_checkbox=True),
        'md_mermaid',
        'fenced_code',
        NoItalUnderscExtension(),
        # 'mdx_math',
        # 'pymdownx.arithmatex',
        'pymdownx.keys',
        pymdownx.emoji.makeExtension(
            emoji_generator=pymdownx.emoji.to_alt,
            # emoji_index=pymdownx.emoji.emojione,  # Doesn't work with :man_shrugging:, THE MOST IMPORTANT EMOJI
            # emoji_index=pymdownx.emoji.twemoji,
            emoji_index=pymdownx.emoji.gemoji,
        ),
    ])


def parseOrLoadMarkdown(path, projectDir):
    
    description = str(path)
    
    if description == 'see README.md':
            
        for f in listdir(projectDir):
            description = join(projectDir, f)
            basePath = basename(description)
            if basePath == 'README.md':
                # Assume we've found a top-level markdown file.
                description = codecs.open(description, mode="r", encoding="utf-8").read()
                break
    elif (
          isinstance(description, str)
          or
          isinstance(description, unicode)
          ) and '.md' in description:
        description = codecs.open(join(projectDir, description), mode="r", encoding="utf-8").read()

    html = markdown_to_html(description)

    return html

    
if __name__ == '__main__':
    content = '''<p>
                Cillum dolor esse sit incididunt velit eiusmod magna ad nostrud officia aute dolor dolor. Magna esse ullamco pariatur adipisicing consectetur eu commodo officia. Ex cillum consequat mollit minim elit est deserunt occaecat nisi amet. Quis aliqua nostrud Lorem occaecat sunt. Eiusmod quis amet ullamco aliquip dolore ut incididunt duis adipisicing. Elit consequat nisi eiusmod aute ipsum sunt veniam do est. Occaecat mollit aliquip ut proident consectetur amet ex dolore consectetur aliqua elit.
              </p>
              <p>
                Commodo nisi non consectetur voluptate incididunt mollit duis dolore amet amet tempor exercitation. Qui amet aute ea aute id ad aliquip proident. Irure duis qui labore deserunt enim in quis nisi sint consequat aliqua. Ex proident labore et laborum tempor fugiat sint magna veniam minim. Nulla dolor labore adipisicing in enim mollit laboris fugiat eu. Aliquip minim cillum ullamco voluptate non dolore non ex duis fugiat duis ad. Deserunt cillum ad et nisi amet non voluptate culpa qui do. Labore ullamco et minim proident est laborum mollit ad labore deserunt ut irure dolore. Reprehenderit ad ad irure ut irure qui est eu velit eu excepteur adipisicing culpa. Laborum cupidatat ullamco eu duis anim reprehenderit proident aute ad consectetur eiusmod.
              </p>'''
    html = article('Gunnar', content, sourceLink='https://github.com/tsbertalan/gunnar')
    from utils import displayHtml
    displayHtml(html)

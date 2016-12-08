'''
Created on Dec 8, 2016

@author: tsbertalan
'''
from page import Html
from utils import Tag, child, Div, parseAnonymousHTML, tostring


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
  background-color: #3F51B5;
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
      position: fixed;
      display: block;
      right: 0;
      bottom: 0;
      margin-right: 40px;
      margin-bottom: 40px;
      z-index: 900;
    }
''' 


def article(title, content, breadcrumbs=None, sourceLink=None):
    if breadcrumbs is None:
        breadcrumbs = 'Main', title
    html = Html()
    head = child(html, 'head')
    head.append(Tag('style', tagText=articleStyle()))
    body = child(html, 'body')
    
    container = Div(cls='demo-layout mdl-layout mdl-layout--fixed-header mdl-js-layout mdl-color--grey-100')
    body.append(container)
    
    if sourceLink is not None:
        sourceButton = Tag('a', href=sourceLink, target="_blank", id="view-source",
                           tagText='View project files.',
                           cls="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--accent mdl-color-text--accent-contrast")
        body.append(sourceButton)
    
    header = Tag('header', cls='demo-header mdl-layout__header mdl-layout__header--scroll mdl-color--grey-100 mdl-color-text--grey-800')
    container.append(header)
    
    headerRow = Div(cls='mdl-layout__header-row')
    header.append(headerRow)
    
    headerRow.append(Tag('span', cls='mdl-layout-title', tagText=title))
    headerRow.append(Div(cls='mdl-layout-spacer'))
    
    container.append(Div(cls='demo-ribbon'))
    
    mainDiv = Tag('main', cls='demo-main mdl-layout__content')
    container.append(mainDiv)
    
    grid = Div(cls='demo-container mdl-grid')
    mainDiv.append(grid)
    
    grid.append(Div(cls='mdl-cell mdl-cell--2-col mdl-cell--hide-tablet mdl-cell--hide-phone'))
    
    col = Div(cls='demo-content mdl-color--white mdl-shadow--4dp content mdl-color-text--grey-800 mdl-cell mdl-cell--8-col')
    grid.append(col)
    
    col.append(Div(cls='demo-crumbs mdl-color-text--grey-500',
                   tagText=' > '.join(breadcrumbs)))
    maintitle = Tag('h3', tagText=title)
    col.append(maintitle)
    parsed = parseAnonymousHTML(content)
    maintitle.tail = parsed.text
    col.extend(parsed)
    
    footer = Tag('footer', cls='demo-footer mdl-mini-footer')
    mainDiv.append(footer)

    lsec = Div(cls='mdl-mini-footer--left-section')
    footer.append(lsec)
    
    ul = Tag('ul', cls='mdl-mini-footer--link-list') 
    lsec.append(ul)

    ul.append(Tag('li', toAppend=[Tag('a', href='#', tagText='Help')]))
    ul.append(Tag('li', toAppend=[Tag('a', href='#', tagText='Privacy and terms')]))
    ul.append(Tag('li', toAppend=[Tag('a', href='#', tagText='User Agreement')]))
    
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

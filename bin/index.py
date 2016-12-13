#!/usr/var/env python
'''
@author:     Tom Bertalan
@contact:    tom@tombertalan.com
'''
from page import Html
from utils import child, Tag, Div, parseAnonymousHTML
import datetime

def portfolioCard(title, supportingText, linkDest=None, imgSrc=None, imgAlt=''):
    print 'Generating card with linkDest=', linkDest
    out = Div(cls='mdl-cell mdl-card mdl-shadow--4dp portfolio-card mdl-cell--4-col')
    if imgSrc is not None:
        out.append(Div(cls='mdl-card__media', toAppend=[
            Tag('img', cls='article-image', src=imgSrc, border='0', alt=imgAlt, width='100%')
                                                        ]))
    out.append(Div(cls='mdl-card__title', toAppend=[
        Tag('h2', cls='mdl-card__title-text', tagText=title)
                                                    ]))
    out.append(Div(cls='mdl-card__supporting-text', tagText=supportingText))
    if linkDest is not None:
        out.append(Div(cls='mdl-card__actions mdl-card--border', toAppend=[
            Tag('a', cls='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect mdl-button--accent', href=linkDest, tagText='Read more') 
                                                                            ]))
#     out = parseAnonymousHTML(
#     ''' <div class="mdl-cell mdl-card mdl-shadow--4dp portfolio-card">
#             <div class="mdl-card__media">
#                 <img class="article-image" src="%s" border="0" alt="%s" width="100%%" />
#             </div>
#             <div class="mdl-card__title">
#                 <h2 class="mdl-card__title-text">%s</h2>
#             </div>
#             <div class="mdl-card__supporting-text">
#                 %s
#             </div>
#             <div class="mdl-card__actions mdl-card--border">
#                 <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect mdl-button--accent" href="%s">Read more</a>
#             </div>
#          </div>''' % (imgSrc, imgAlt, title, supportingText, linkDest),
#         )[1][0]
    return out


def index(cards=[], DEBUG=False):
    html = Html(lang='en')
    head = child(html, 'head')
    body = child(html, 'body')
    
    head.append(Tag('title', tagText='Tom Bertalan'))
    head.append(Tag('link', rel='stylesheet', href='styles.css'))

    layout = Div(cls='mdl-layout mdl-js-layout')
    body.append(layout)
    
    mainContent = Tag('main', cls='mdl-layout__content')
    layout.append(mainContent)
    
    if DEBUG:
        grid = Div(cls='mdl-grid portfolio-max-width', style='border:1px solid brown;')
        bioCell = Div(cls='mdl-cell mdl-cell--4-col', style='border:1px solid green;')
        cardsCell = Div(cls='mdl-cell mdl-cell--8-col mdl-grid', style='border:1px solid black;')
    else:
        grid = Div(cls='mdl-grid portfolio-max-width')
        bioCell = Div(cls='mdl-cell mdl-cell--4-col')
        cardsCell = Div(cls='mdl-cell mdl-cell--8-col mdl-grid')

    mainContent.append(grid)
    grid.append(bioCell)
    
    bioCell.append(Div(cls='portfolio-logo'))
    bioCell.append(Tag('center', toAppend=[Tag('h1', cls='mdl-typography--display-3', style='color: #333;', tagText='Tom Bertalan')]))
    
    grid.append(cardsCell)
    cardsCell.extend(cards)
    
    
    return html
   
    
if __name__ == '__main__':
    from utils import displayHtml
    displayHtml(index(cards=[portfolioCard('Gunnar', 'Gunnar is a robot.', imgSrc='images/rover.jpg')]), fname='./.test.html')

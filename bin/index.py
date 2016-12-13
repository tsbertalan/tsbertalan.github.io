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
            Div(cls='card-img-heightcrop', style="background-image: url('%s');" % imgSrc),
                                                        ]))
    out.append(Div(cls='mdl-card__title', toAppend=[
        Tag('h2', cls='mdl-card__title-text', tagText=title)
                                                    ]))
    out.append(Div(cls='mdl-card__supporting-text', style='padding-bottom: 70px;', tagText=supportingText))
    if linkDest is not None:
        out.append(Div(cls='mdl-card__actions mdl-card--border button-at-bottom', toAppend=[
            Tag('a', cls='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect mdl-button--accent', href=linkDest, tagText='Read more') 
                                                                            ]))
    return out


def index(cards=[]):
    html = Html(lang='en')
    head = child(html, 'head')
    body = child(html, 'body')
    
    head.append(Tag('title', tagText='Tom Bertalan'))
    head.append(Tag('link', rel='stylesheet', href='styles.css'))

    layout = Div(cls='mdl-layout mdl-js-layout')
    body.append(layout)
    
    mainContent = Tag('main', cls='mdl-layout__content')
    layout.append(mainContent)
    
    grid = Div(cls='mdl-grid portfolio-max-width')
    bioCell = Div(cls='mdl-cell mdl-cell--4-col')
    cardsCell = Div(cls='mdl-cell mdl-cell--8-col mdl-grid')
    

    mainContent.append(grid)
    grid.append(bioCell)
    
    bioCell.append(Div(cls='portfolio-logo'))
    bioCell.append(Tag('center', toAppend=[Tag('h1', cls='mdl-typography--display-3 h1-mainpage', tagText='Tom Bertalan')]))
    bioCell.append(Div(cls='mdl-cell mdl-cell--12-col', toAppend=[
                                                                  Tag('p', tagText='''
    I'm a fifth-year grad student soon to receive my PhD from Princeton University's
    department of Chemical and Biological Engineering, with a Graduate Certificate in Computational and Information Science.  
                                                                  '''),
                                                                  Tag('p', tagText='''
    My research interests are in data mining and dimensionality reduction for high-dimensional dynamical systems,
    with applications in computational neuroscience.
    I also work on robotic design and perception projects.
                                                                  '''),
    ]))
    
    grid.append(cardsCell)
    cardsCell.append(Div(cls='mdl-cell mdl-cell--12-col', toAppend=[Tag('h3', tagText='Projects')]))
    cardsCell.extend(cards)
    
    
    return html
   
    
if __name__ == '__main__':
    from utils import displayHtml
    displayHtml(index(cards=[portfolioCard('Gunnar', 'Gunnar is a robot.', imgSrc='images/rover.jpg')]), fname='./.test.html')

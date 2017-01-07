#!/usr/var/env python
'''
@author:     Tom Bertalan
@contact:    tom@tombertalan.com
'''
from page import Html
from utils import child, Tag, Div, parseAnonymousHTML, textArea, textField
import datetime

def idSanitize(s):
    out = ''
    allowed = 'abcdefghijklmnopqrstuvwxyz'
    allowed += allowed.upper()
    allowed += '-_1234567890'
    for c in s:
        if c in allowed:
            out += c
    return out


def portfolioCard(title, supportingText, linkDest=None, imgSrc=None, imgAlt=''):
    if linkDest is not None:
        out = Div(
            cls='mdl-cell mdl-card mdl-shadow--4dp portfolio-card mdl-cell--3-col anim-card mdl-cell--12-col-phone mdl-cell--3-col-tablet',
            onclick="location.href='%s'" % linkDest
            )
    else:
        out = Div(
            cls='mdl-cell mdl-card mdl-shadow--4dp portfolio-card mdl-cell--3-col anim-card mdl-cell--12-col-phone mdl-cell--3-col-tablet',
            )
    if imgSrc is not None:
        out.append(Div(cls='mdl-card__media', toAppend=[
            Div(cls='card-img-heightcrop', style="background-image: url('%s');" % imgSrc),
                                                        ]))
    out.append(Div(cls='mdl-card__title', toAppend=[
        Tag('h2', cls='mdl-card__title-text', tagText=title)
                                                    ]))
    out.append(Div(cls='mdl-card__supporting-text', tagText=supportingText))
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
    mainContent.append(grid)
    
    bioCell = Div(cls='mdl-cell mdl-cell--4-col mdl-cell--12-col-phone')
    grid.append(bioCell)
    
    bioCell.append(Tag('br'))  # tiny vertical filler
    bioCell.append(Div(cls='portfolio-logo'))
    bioCell.append(Tag('center', toAppend=[Tag('h1', cls='mdl-typography--display-3 h1-mainpage', tagText='Tom Bertalan')]))
    bioCellSubcell = Div(cls='mdl-cell mdl-cell--12-col')
    bioCell.append(bioCellSubcell)
    bioCellSubcell.append(Tag('p', tagText='''
    I am a fifth-year graduate student soon to receive my PhD from Princeton University's
    department of Chemical and Biological Engineering, with a Graduate Certificate in Computational and Information Science.  
                                                                  '''))
    bioCellSubcell.append(Tag('p', tagText='''
    My research interests are in data mining and dimensionality reduction for high-dimensional dynamical systems,
    with applications in computational neuroscience.
    I also work on robotic design and perception projects.
                                                                  '''))
    
    # A menu.
    bioCellSubcell.append(
        Tag('center', toAppend=[
        Tag('button', id='open-contact-form-modal-button', tagText='Contact',
            cls='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect',
            ),
        Tag('a', href='resume.pdf', toAppend=[
            Tag('button', id='resume-button', tagText='Download Resume',
                cls='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect',
                ),
                                              ]
            ),
        ])
                          )
    
    # Contact form modal.
    modal = Div(cls='modal', id='contact-form-modal')
    body.append(modal)
    
    modalContent = Div(cls='modal-content')
    modal.append(modalContent)
    
    modalContent.append(Tag('span', cls='close', toAppend=[
        Tag('button', cls="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab mdl-button--colored",
            toAppend=[
                Tag('i', cls='material-icons', tagText='close'),
                ]
            )
        ]))
    form = Tag('form', action="https://docs.google.com/a/tombertalan.com/forms/d/e/1FAIpQLSfnXirD8eFRUVXDcXNlYJTzRf4rjLtmG3b8qzwXjDGQU6UYOw/formResponse?embedded=true",
               target="_self", method="POST", id="mG61Hd", width='100%')
    modalContent.append(form)
    form.append(textField('entry.2009303593', 'Name...'))
    form.append(textField('entry.2049904920', 'Email...'))
    form.append(Tag('br'))
    form.append(textArea('entry.59900832', 'Message...', rows='8', style='width: 80%;'))
    form.append(Tag('br'))
    form.append(Tag('button', tagText='Send', type='submit',
                    cls='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect',
                    ))
    
    
    body.append(Tag('script', tagText='''// Get the modal
var modal = document.getElementById('contact-form-modal');

// Get the button that opens the modal
var btn = document.getElementById("open-contact-form-modal-button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}'''))
    
    cardsCell = Div(cls='mdl-cell mdl-cell--8-col mdl-grid mdl-cell--12-col-phone')
    grid.append(cardsCell)
#     cardsCell.append(Div(cls='mdl-cell mdl-cell--12-col', toAppend=[Tag('h3', tagText='Projects')]))
    cardsCell.extend(cards)
    
    
    return html
   
    

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
    out = Div(cls='mdl-cell mdl-card mdl-shadow--4dp portfolio-card')
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


def index(cards=[]):
    html = Html(lang='en')
    head = child(html, 'head')
    body = child(html, 'body')
    
    head.append(Tag('title', tagText='Tom Bertalan'))
    head.append(Tag('link', rel='stylesheet', href='styles.css'))

    layout = Div(cls='mdl-layout mdl-js-layout mdl-layout--fixed-header')
    body.append(layout)
    
    head, content, tail = parseAnonymousHTML('''<header class="mdl-layout__header mdl-layout__header--waterfall portfolio-header">
            <div class="mdl-layout__header-row portfolio-logo-row">
                <span class="mdl-layout__title">
                    <div class="portfolio-logo"></div>
                    <span class="mdl-layout__title">Tom Bertalan</span>
                </span>
            </div>
            <div class="mdl-layout__header-row portfolio-navigation-row mdl-layout--large-screen-only">
                <!--
                <nav class="mdl-navigation mdl-typography--body-1-force-preferred-font">
                    <a class="mdl-navigation__link is-active" href="index.html">Portfolio</a>
                    <a class="mdl-navigation__link" href="about.html">About</a>
                </nav>
                -->
            </div>
        </header>''')
    layout.extend(content)
    
    head, content, tail = parseAnonymousHTML('''<div class="mdl-layout__drawer mdl-layout--small-screen-only">
            <!--
            <nav class="mdl-navigation mdl-typography--body-1-force-preferred-font">
                <a class="mdl-navigation__link is-active" href="index.html">Portfolio</a>
                <a class="mdl-navigation__link" href="about.html">About</a>
            </nav>
            -->
        </div>''')
    layout.extend(content)
    
    mainContent = Tag('main', cls='mdl-layout__content')
    layout.append(mainContent)
    
    grid = Div(cls='mdl-grid portfolio-max-width')
    mainContent.append(grid)
    
    grid.extend(cards)
    
    footer = Tag('footer', cls='mdl-mini-footer')
    layout.append(footer)
    
    leftFooter = Div(cls='mdl-mini-footer__left-section')
    footer.append(leftFooter)
    rightFooter = Div(cls='mdl-mini-footer__right-section')
    footer.append(rightFooter)
    now = datetime.datetime.now()
    leftFooter.append(Div(cls='mdl-logo', tagText='Copyright Tom Bertalan %d.' % now.year))
    rightFooter.append(Tag('ul', cls='mdl-mini-footer__link-list',
#                            toAppend=[
#                                      Tag('li', toAppend=[Tag('a', href='#', tagText='Help')]),
#                                      Tag('li', toAppend=[Tag('a', href='#', tagText='Pricacy & Terms')]),
#                                      ]
                           ))
    
    
#     <footer class="mdl-mini-footer">
#                 <div class="mdl-mini-footer__left-section">
#                     <div class="mdl-logo">Simple portfolio website</div>
#                 </div>
#                 <div class="mdl-mini-footer__right-section">
#                     <ul class="mdl-mini-footer__link-list">
#                         <li><a href="#">Help</a></li>
#                         <li><a href="#">Privacy & Terms</a></li>
#                     </ul>
#                 </div>
#             </footer>
    return html
   
    
if __name__ == '__main__':
    from utils import displayHtml
    displayHtml(index(cards=[portfolioCard('Gunnar', 'Gunnar is a robot.', imgSrc='images/rover.jpg')]), fname='./.test.html')

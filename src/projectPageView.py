'''
Created on Dec 8, 2016

@author: tsbertalan
'''
import page
from utils import child, tostring, Tag
from standalonePage import article

def makePage(projectName, projectDescription):
    return article(projectName, projectDescription)
    html = page.Html()
    
    head = child(html, 'head')
    head.append(Tag('title', tagText=projectName))
    
    body = child(html, 'body')
    body.append(Tag('h1', tagText=projectName))
    body.append(Tag('p', tagText=projectDescription))
                
    return html
                
if __name__ == '__main__':
    html = makePage('Gunnar', 'Gunnar is a <i>cool</i> robot.')
    from utils import displayHtml
    displayHtml(html)
    
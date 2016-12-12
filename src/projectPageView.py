'''
Created on Dec 8, 2016

@author: tsbertalan
'''
from standalonePage import article


def makePage(projectName, projectDescription, **kwargs):
    return article(projectName, projectDescription, heading=False, **kwargs)

                
if __name__ == '__main__':
    html = makePage('Gunnar', 'Gunnar is a <i>cool</i> robot.')
    from utils import displayHtml
    displayHtml(html)
    
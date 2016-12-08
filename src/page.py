from utils import tostring, child, Tag
        
def Head():
    head = Tag('head')
    head.append(Tag('link', rel='stylesheet', href="https://fonts.googleapis.com/icon?family=Material+Icons"))
    head.append(Tag('link', rel='stylesheet', href='https://code.getmdl.io/1.2.1/material.blue-amber.min.css'))
    script = Tag('script', src="https://code.getmdl.io/1.2.1/material.min.js", defer='true')
    head.append(script)
    head.append(Tag('meta', name='viewport', content="width=device-width, initial-scale=1.0"))
    return head

def Html(head=None, body=None, **kwargs):
    html = Tag('html', **kwargs)
    if head is None:
        head = Head()
    if body is None:
        body = Tag('body')
    
    html.append(head)
    html.append(body)
    return html


if __name__ == '__main__':
    html = Html()
    from components import button, cardTask
    child(html, 'body').append(button('test button'))
    child(html, 'body').append(cardTask('test card', text='contents'))
    from utils import displayHtml
    displayHtml(html)

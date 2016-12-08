from utils import Tag, Div, tostring

    

viewport = Div(id="viewport")
layout = Div(cls="mdl-layout mdl-js-layout mdl-layout--fixed-header mdl-layout--fixed-tabs")
header = Tag('header', cls="mdl-layout__header")
headerRow = Div(cls="mdl-layout__header-row")
tabBar = Div(cls="mdl-layout__tab-bar mdl-js-ripple-effect")
drawer = Div(cls="mdl-layout__drawer")
mainLayout = Tag('main', cls="mdl-layout__content")
secCams = Tag('section', cls="mdl-layout__tab-panel is-active", id="fixed-tab-1")
grid = Div(cls='mdl-grid')
# These columns are as parts of 12. I.e., 4-col means even thirds (4/12 units).
gridThird = Div(cls='mdl-cell mdl-cell--4-col')
gridOneth = Div(cls='mdl-cell mdl-cell--12-col')
card = Div(cls='mdl-card mdl-shadow--4dp')


def cardTask(title, text=None, img=None, shadowLevel=2, indent=1, color=None, primary=False, accent=False, spanStyle=''):
    assert shadowLevel in [2, 3, 4, 6, 8, 16]
    out = []
    if img is not None:
        out.append('''<div class="mdl-card__media">
                        <img src="%s" width="173" height="157" border="0" alt="%s" style="padding:10px;">
                    </div>''' % img)
       
    cls = "mdl-card__title"
    if accent:
        cls +=' mdl-color-text--accent-contrast'
    elif primary:
        cls += ' mdl-color-text--primary-contrast'
    div = Div(cls=cls)
    div.text = title
    out.append(div)
    if text is not None:
        cls = "mdl-card__supporting-text"
        if accent:
            cls += ' mdl-color-text--accent-contrast'
        elif primary:
            cls += ' mdl-color-text--primary-contrast'
        div = Div(cls=cls)
        div.text = text
        out.append(div)
        
    if color is not None:
        colorstyle = 'background-color: %s;' % color
    else:
        colorstyle = ''
    cls = 'mdl-card mdl-shadow--%ddp' % (shadowLevel,)
    if accent:
        cls += ' mdl-color--accent'
    elif primary:
        cls += ' mdl-color--primary'
    style = 'width: 90%%;%s' % colorstyle
    div = Div(cls=cls, style=style)
    for o in out:
        div.append(o)
    span = Tag('span', style='padding: 20px; margin-left: %dpx; %s' % ((indent-1)*4, spanStyle) )
    span.append(div)
    return span


def button(text, raised=True, primary=True, accent=False, **kwargs):
    cls = "mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--accent"
    if raised:
        cls += ' mdl-button--raised'
    if primary:
        cls += ' mdl-button--primary'
    elif accent:
        cls += ' mdl-button--accent'
    tag = Tag('button', cls=cls, **kwargs)
    tag.text = text
    return tag


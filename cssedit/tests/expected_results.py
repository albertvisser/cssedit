"""data definitions to compare test results with
"""
data = {
    'load_function': {
        'compressed': b'* { display: inline; } div { margin: 0 0 0 0; padding: 0 0 0 0; } '
                      b' p { text-align: center; vertical-align: middle } img { border: 1p'
                      b'x solid } .red { color: red; font-weight: bold } #page-title { fon'
                      b't-size: 55 } p::first-child { text-decoration: underline; } li:nth'
                      b'-child(3) { background-color: green } a:hover { background-color: '
                      b'blue } p.oms:before { content: "Hello, it`s me" } div div { displa'
                      b'y: block; } ul>li>ul>li { list-style: square; } ul + p { font-styl'
                      b'e: italic } p ~ p { font-variant: small-caps; } a[title] { color: '
                      b'yellowish; } td[valign="top"] { font-weight: bold; } a[href*="ads"'
                      b'] { display: none; } a[href^="http"]{ background: url(path/to/exte'
                      b'rnal/icon.png) no-repeat; padding-left: 10px; } a[href$="jpg"] { t'
                      b'ext-decoration: line-through; }',
        'other': b'/* simple css in this case means one selector for one definition */  /*'
                 b' some simple elements */ * { display: inline; } div { margin: 0 0 0 0; '
                 b'padding: 0 0 0 0; } p { text-align: center; vertical-align: middle } im'
                 b'g { border: 1px solid }  /* classes, ids and pseudo-classes */ .red { c'
                 b'olor: red; font-weight: bold } #page-title { font-size: 55 } p::first-c'
                 b'hild { text-decoration: underline; } li:nth-child(3) { background-color'
                 b': green } a:hover { background-color: blue } p.oms:before { content: "H'
                 b'ello, it`s me" }  /* document hierarchies */ div div { display: block; '
                 b'} ul>li>ul>li { list-style: square; } ul + p { font-style: italic } p ~'
                 b' p { font-variant: small-caps; } a[title] { color: yellowish; } td[vali'
                 b'gn="top"] { font-weight: bold; } a[href*="ads"] { display: none; } a[hre'
                 b'f^="http"] { background: url(path/to/external/icon.png) no-repeat; paddi'
                 b'ng-left: 10px; } a[href$="jpg"] { text-decoration: line-through; }'},
    'parse_function': [('/**/', 'simple css in this case means one selector for one definition'),
                       ('/**/', 'some simple elements'),
                       ('*', {'display': 'inline'}),
                       ('div', {'padding': '0 0 0 0', 'margin': '0 0 0 0'}),
                       ('p', {'text-align': 'center', 'vertical-align': 'middle'}),
                       ('img', {'border': '1px solid'}),
                       ('/**/', 'classes, ids and pseudo-classes'),
                       ('.red', {'font-weight': 'bold', 'color': 'red'}),
                       ('#page-title', {'font-size': '55'}),
                       ('p::first-child', {'text-decoration': 'underline'}),
                       ('li:nth-child(3)', {'background-color': 'green'}),
                       ('a:hover', {'background-color': 'blue'}),
                       ('p.oms:before', {'content': '"Hello, it\'s me"'}),
                       ('/**/', 'document hierarchies'),
                       ('div div', {'display': 'block'}),
                       ('ul>li>ul>li', {'list-style': 'square'}),
                       ('ul + p', {'font-style': 'italic'}),
                       ('p ~ p', {'font-variant': 'small-caps'}),
                       ('a[title]', {'color': 'yellowish'}),
                       ('td[valign="top"]', {'font-weight': 'bold'}),
                       ('a[href*="ads"]', {'display': 'none'}),
                       ('a[href^="http"]', {'background': 'url(path/to/external/icon.png)'
                                                          ' no-repeat',
                                            'padding-left': '10px'}),
                       ('a[href$="jpg"]', {'text-decoration': 'line-through'})],
    'editor_file': {'compressed': [('*', {'display': 'inline'}),
                                   ('div', {'padding': '0 0 0 0', 'margin': '0 0 0 0'}),
                                   ('p', {'text-align': 'center', 'vertical-align': 'middle'}),
                                   ('img', {'border': '1px solid'}),
                                   ('.red', {'font-weight': 'bold', 'color': 'red'}),
                                   ('#page-title', {'font-size': '55'}),
                                   ('p::first-child', {'text-decoration': 'underline'}),
                                   ('li:nth-child(3)', {'background-color': 'green'}),
                                   ('a:hover', {'background-color': 'blue'}),
                                   ('p.oms:before', {'content': '"Hello, it\'s me"'}),
                                   ('div div', {'display': 'block'}),
                                   ('ul>li>ul>li', {'list-style': 'square'}),
                                   ('ul + p', {'font-style': 'italic'}),
                                   ('p ~ p', {'font-variant': 'small-caps'}),
                                   ('a[title]', {'color': 'yellowish'}),
                                   ('td[valign="top"]', {'font-weight': 'bold'}),
                                   ('a[href*="ads"]', {'display': 'none'}),
                                   ('a[href^="http"]', {'background': 'url(path/to/external/'
                                                                      'icon.png) no-repeat',
                                                        'padding-left': '10px'}),
                                   ('a[href$="jpg"]', {'text-decoration': 'line-through'})],
                    'other': []},  # will be same as 'parse_function' value above
    'editor_tag': [('div p>span["red"]~a:hover', {'border': '5px solid red',
                                                  'content': '"gargl"',
                                                  'text-decoration': 'none'})],
    'editor_text': {'one': [],  # will be the same as 'editor_tag' value above
                    'more': [],  # will be the value for "one" above appended with 'addition'
                    'formatted': [],  # will be the value for "more" prepended with 'extra'
                    'addition': [('p', {'font-family': 'Arial sans-serif'}),
                                 ('div', {'float': 'left', 'display': 'inline'})],
                    'extra': [('/**/', 'this is a stupid comment')]},
    'editor_text2tree': {'one': [b'div p>span["red"]~a:hover',
                                 '    border',
                                 '        5px solid red',
                                 '    content',
                                 '        "gargl"',
                                 '    text-decoration',
                                 '        none'],
                         'more': [],  # will be value for "one" appended with value for "addition"
                         'addition': [b'p',
                                       '    font-family',
                                       '        Arial sans-serif',
                                       'div',
                                       '    display',
                                       '        inline',
                                       '    float',
                                       '        left']}}
data['editor_file']['other'] = data['parse_function']
data['editor_text']['one'] = [data['editor_tag'][0]]
data['editor_text']['more'] = data['editor_text']['one'] + \
    data['editor_text']['addition']
data['editor_text']['formatted'] = data['editor_text']['extra'] + \
    data['editor_text']['more']
data['editor_text2tree']['more'] = data['editor_text2tree']['one'] + \
    data['editor_text2tree']['addition']

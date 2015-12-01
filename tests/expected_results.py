data = {
    'load_function': {
        'compressed': """* { display: inline; } div { margin: 0 0 0 0; padding: 0 0 0 0; } p { text-align: center; vertical-align: middle } img { border: 1px solid } .red { color: red; font-weight: bold } #page-title { font-size: 55 } p::first-child { text-decoration: underline; } li:nth-child(3) { background-color: green } a:hover { background-color: blue } p.oms:before { content: "Hello, it's me" } div div { display: block; } ul>li>ul>li { list-style: square; } ul + p { font-style: italic } p ~ p { font-variant: small-caps; } a[title] { color: yellowish; } td[valign="top"] { font-weight: bold; } a[href*="ads"] { display: none; } a[href^="http"]{ background: url(path/to/external/icon.png) no-repeat; padding-left: 10px; } a[href$="jpg"] { text-decoration: line-through; }""",
        'other': """/* simple css in this case means one selector for one definition */  /* some simple elements */ * { display: inline; } div { margin: 0 0 0 0; padding: 0 0 0 0; } p { text-align: center; vertical-align: middle } img { border: 1px solid }  /* classes, ids and pseudo-classes */ .red { color: red; font-weight: bold } #page-title { font-size: 55 } p::first-child { text-decoration: underline; } li:nth-child(3) { background-color: green } a:hover { background-color: blue } p.oms:before { content: "Hello, it's me" }  /* document hierarchies */ div div { display: block; } ul>li>ul>li { list-style: square; } ul + p { font-style: italic } p ~ p { font-variant: small-caps; } a[title] { color: yellowish; } td[valign="top"] { font-weight: bold; } a[href*="ads"] { display: none; } a[href^="http"] { background: url(path/to/external/icon.png) no-repeat; padding-left: 10px; } a[href$="jpg"] { text-decoration: line-through; }"""
},
    'parse_function': [
        ('/**/', 'simple css in this case means one selector for one definition'),
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
        ('a[href^="http"]', {'background': 'url(path/to/external/icon.png) no-repeat', 'padding-left': '10px'}),
        ('a[href$="jpg"]', {'text-decoration': 'line-through'})
        ],
    'editor_file': {
        'compressed': [
            ('*', {'display': 'inline'}),
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
            ('a[href^="http"]', {'background': 'url(path/to/external/icon.png) no-repeat', 'padding-left': '10px'}),
            ('a[href$="jpg"]', {'text-decoration': 'line-through'})
            ],
        'other': [], # should be same as 'parse_function' value above
        },
    'editor_tag': [
        ('div p>span["red"]~a:hover', {
            'border': '5px solid red',
            'content': '"gargl"',
            'text-decoration': 'none',
            })
        ],
    'editor_text': {
        'one': [], # should be the same as 'editor_tag' value above
        'more': [], # should be the same as previous value above appended with 'addition'
        'formatted': [], # should be the same as previous value above prepended with 'extra'
        'addition': [
            ('p', {'font-family': 'Arial sans-serif'}),
            ('div', {'float': 'left', 'display': 'inline'})
            ],
        'extra': [
            ('/**/', 'this is a stupid comment')
            ]
        },
    'editor_text2tree': {
        'one': [
            'div p>span["red"]~a:hover',
            '    border',
            '        5px solid red',
            '    content',
            '        "gargl"',
            '    text-decoration',
            '        none'
            ],
        'more': [],
        'addition': [
            'p',
            '    font-family',
            '        Arial sans-serif',
            'div',
            '    display',
            '        inline',
            '    float',
            '        left'
            ],
        },
    }
data['editor_file']['other'] = data['parse_function']
data['editor_text']['one'] = [data['editor_tag'][0]]
data['editor_text']['more'] = data['editor_text']['one'] + \
    data['editor_text']['addition']
data['editor_text']['formatted'] = data['editor_text']['extra'] + \
    data['editor_text']['more']
data['editor_text2tree']['more'] = data['editor_text2tree']['one'] + \
    data['editor_text2tree']['addition']

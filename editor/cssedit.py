import sys
import os
import shutil
## import pathlib - don't think this is suitable
import collections
import cssutils
import logging

format_types = ("long", "medium", "short", "compressed")
comment_tag = '/**/'
logline_elements = ["severity", "subject", "message", "line", "pos", "data"]
LogLine = collections.namedtuple('LogLine', logline_elements)
text_type, list_type, table_type = '1', 'n', 'n*2'

cssutils.css.CSSRule.STYLE_RULE # dit is een integer net als cssutils.css.CSSStyleRule.type
RTYPES = {
    cssutils.css.CSSRule.STYLE_RULE: [("selectors", list_type), ("styles", table_type)],
    cssutils.css.CSSRule.MEDIA_RULE: [("media", list_type), ("rules", list_type)],
    cssutils.css.CSSRule.COMMENT: [("text", text_type)],
    cssutils.css.CSSRule.UNKNOWN_RULE: [("data", text_type)]
    }

# TODO: @media queries op niet-standaard attributen (bv, -webkit-min-device-pixel-ratio:2
#   gaan mis, dwz de css tekst gaat verloren
# Ik krijg hier meldingen op in de log:
# ERROR	MediaQuery: Unexpected syntax, expected "and" but found "(". [1:703: (]
# ERROR	MediaQuery: Unexpected syntax, expected "and" but found ":". [1:734: :]
# ERROR	Unexpected token (NUMBER, 2, 1, 735)
# ERROR	MediaQuery: Unexpected syntax, expected "and" but found ")". [1:736: )]
# ERROR	MediaList: Invalid MediaQuery:  (-webkit-min-device-pixel-ratio:2)
# is dit een bug (alleen een conditie in een mediaquery moet ook toegestaan zijn)?
# als ik (resolution:2) specificeer pikt-ie het ook niet dus ik denk van wel
# "A <media-query> is composed of a media type and/or a number of media features"
# maar:
# "A shorthand syntax is offered for media queries that apply to all media types;
#   the keyword ‘all’ can be left out (along with the trailing ‘and’).
#   I.e. if the media type is not explicitly given it is ‘all’."

def load(filename):
    "Note: does not return a string but a CSSStyleSheet instance"
    # compensate for missing feature(s)
    got_media = -1
    with open(filename) as f:
        data = f.read()
        got_media = data.find('@media (')
    if got_media > -1:
        return cssutils.parseString(data.replace('@media (', '@media all and ('))
    return cssutils.parseFile(filename)

def get_for_single_tag(cssdata):
    "Note: does not return a string but a CSSStyleDeclaration instance"
    return cssutils.parseStyle(cssdata)

def return_for_single_tag(cssdata):
    "not sure what to do with this one yet"
    ## " dict naar tekst"
    ## properties = []
    ## for property, value in sorted(cssdata.items()):
        ## properties.append("{}: {};".format(property, value))
    ## return " ".join(properties)

def parse(text):
    "Note: does not return a string but a CSSStyleSheet instance or..."
    return cssutils.parseString(text)

## def format(inputlist, mode="compressed"):
def set_format(mode="compressed"):
    "set global properties for cssutils"
    # To set a preference use: cssutils.ser.prefs.PREFNAME = NEWVALUE
    # don't think I'll be needing the inputlist parameter
    # set some properties depending om mode, e.g.
    # indent = 4 * ‘ ‘
        # Indentation of e.g Properties inside a CSSStyleDeclaration
    # indentClosingBrace = True
        # Defines if closing brace of block is indented to match indentation of the block
        # (default) oder match indentation of selector.
    # keepComments = True
        # If False removes all CSSComments
    # lineSeparator = u’n’
        # How to end a line. This may be set to e.g. u’’ for serializing of CSSStyleDeclarations
        # usable in HTML style attribute.

def save(data, filename, backup=True):
    "expects data to be a CSSStyleSheet instance"
    if backup and os.path.exists(filename):
        shutil.copyfile(filename, filename + "~")
    with open(filename, 'w', encoding='utf-8') as f_out:
        try:
            print(data.cssText, file=f_out)
        except AttributeError:
            print(data, file=f_out)


def get_definition_from_file(file, line, pos):
    with open(file) as _in:
        count = line
        while count > 0:
            data = _in.readline()
            count -= 1
    end = data.find('}', pos) + 1
    start = data.rfind('}', 0, pos) + 1
    text = data[start:end]
    return text

def init_ruledata(ruletype):
    ruledata = {} # {'selectors': [], 'styles', {}}
    for x, y in RTYPES[ruletype]:
        ruledata[x] = {} if y == table_type else [] if y == list_type else ''
    return ruledata

def complete_ruledata(ruledata, rule):
    if rule.type == cssutils.css.CSSRule.STYLE_RULE:
        ruledata['selectors'] = [x.selectorText for x in rule.selectorList]
        ruledata['styles'] = {x.name: x.propertyValue.cssText
            for x in rule.style.getProperties()}
    elif rule.type == cssutils.css.CSSRule.MEDIA_RULE:
        ruledata['media'] = [x.mediaText for x in rule.media]
        ruledata['rules'] = [(x.typeString, complete_ruledata(init_ruledata(x.type),
            x)) for x in rule.cssRules]
    elif rule.type == cssutils.css.CSSRule.COMMENT:
        ruledata['text'] = rule.cssText[2:-2].strip()
    else:
        ruledata['data'] = rule.cssText.strip()
    return ruledata

def parse_log_line(line):
    """turn a log line into a LogLine instance

    Let op: ik heb ook nog regels als:
    ERROR	Unexpected token (NUMBER, 2, 1, 735)
    ERROR	MediaList: Invalid MediaQuery:  (-webkit-min-device-pixel-ratio:2)
    """
    data = []
    test = line.split("\t", 1)
    if len(test) == 1:
        return  # this line can not be parsed
    severity, rest = test
    test = rest.split(": ", 1)
    if len(test) == 1: # unexpected token
        message = rest
        _, rest = message.split(" (", 1)
        subject, data, line, pos = rest[:-1].split(',')
    else:
        subject, rest = test
        test = rest.split(" [", 1)
        if len(test) == 1:
            message, data = rest.split(": ")
            line = pos = "-1"
        else:
            message, rest = test
            line, pos, rest = rest.split(':', 2)
            data = rest[:-1].strip()
    return LogLine(severity, subject, message, int(line), int(pos), data)



class Editor:

    def __init__(self, **kwargs): # filename="", tag="", text=""):
        """get css from a source and turn it into a structure
        """
        self.filename = self.tag = ""
        text = None # must be allowed to be empty (to create new inline style)
        try:
            self.filename = kwargs.pop('filename')
        except KeyError: pass
        try:
            self.tag = kwargs.pop('tag')
        except KeyError: pass
        try:
            text = kwargs.pop('text')
        except KeyError: pass
        if self.filename:
            if self.tag or text:
                raise ValueError('Ambiguous arguments')
        else:
            if text is None:
                raise ValueError("Not enough arguments")
        if kwargs:
            raise ValueError('Too many arguments')

        self.data = []
        hlp = '' if not self.filename else '_' + os.path.basename(self.filename)
        logfile = '/tmp/cssedit{}.log'.format(hlp)
        hdlr = self.set_logger(logfile)
        if self.filename:
            self.data = load(self.filename)
        elif self.tag:
            style = get_for_single_tag(text)
            self.data = cssutils.css.CSSStyleSheet()
            rule = cssutils.css.CSSStyleRule(selectorText=self.tag, style=style)
            self.data.add(rule)
        else:
            self.data = parse(text)
            text = str(self.data.cssText)
            if not text:
                self.data = None
            else:
                print('full text input in cssedit:', self.data.cssText)
            ## if isinstance(data, cssutils.css.CSSStyleSheet):
                ## self.data = data
            ## elif isinstance(data, cssutils.css.CSSStyleDeclaration):
                ## self.data = None
            # TODO: raise error when this doesn't parse into a CSSStylesheet

        hdlr.close()
        self.log = ['unable to get log info']
        with open(logfile) as _log:
            self.log = [line.strip() for line in _log]

        if not self.data:
            raise ValueError("Incorrect css data")

    def set_logger(self, logfile):
        ## with open('/tmp/cssedit.log', 'w') as _log:
            ## cssutils.log.setLog(_log)
        log = logging.getLogger('CSSEDIT')
        hdlr = logging.FileHandler(logfile, mode='w')
        formatter = logging.Formatter('%(levelname)s\t%(message)s')
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
        log.setLevel(logging.INFO)
        cssutils.log.setLog(log)
        return hdlr

    def datatotext(self):
        """turn the cssutils structure into a more generic one
        """
        # redesign: see trac ticket
        self.textdata = []
        for ix, rule in enumerate(list(self.data)):
            ruledata = init_ruledata(rule.type) # collections.defaultdict(dict)
            ruledata['seqnum'] = ix
            ruledata = complete_ruledata(ruledata, rule)
            self.textdata.append((rule.typeString, ruledata))

    def texttodata(self):
        """turn the generic structure into a cssutils one
        """
        self.data = cssutils.css.CSSStyleSheet()
        for ruletype, ruledata in self.textdata:
            ## print(selector, propertydata)
            # ruletype is een typeString
            # ruledata is een dict met mogelijke keys selectors, styles, seqnum, text, ...
            if 'selectors' in ruledata:
                rule = cssutils.css.CSSStyleRule()
                sellist = cssutils.css.SelectorList()
                for selector in ruledata['selectors']:
                    sellist.append(selector)
                rule.selectorList = sellist
                style = cssutils.css.CSSStyleDeclaration()
                for property, value in ruledata['styles'].items():
                    style[property] = value
                rule.style = style
            elif 'media' in ruledata:
                rule = cssutils.css.CSSMediaRule()
                # TODO: finish this
            elif 'text' in ruledata:
                if ruletype == cssutils.css.CSSComment().typeString:
                    rule = cssutils.css.CSSComment(cssText='/* {} */'.format(
                        ruledata['text']))
                else:
                    ## rule = cssutils.css.CSSRule()
                    ## rule.cssText=ruledata['text']
                    # for want of something better
                    rule = cssutils.css.CSSComment(cssText=ruledata['text'])
            self.data.add(rule)

    def return_to_source(self, backup=True, savemode="compressed"):
        "ahem"
        if savemode not in (format_types):
            info = "`, `".join(format_types[:-1])
            info = "` or `".join((info, format_types[-1]))
            raise AttributeError("wrong format type for save, should be either of "
                "`{}`".format(info))
        ## ## data = compile(self.data)
        set_format(savemode)
        if self.filename:
            save(self.data, self.filename, backup)
        elif self.tag:
            self.data = return_for_single_tag(self.data)
        else:
            self.data = self.data.cssText


if __name__ == "__main__":
    ## testdata = "../tests/simplecss-long.css"
    testdata = "../tests/common_pt1.css"
    ## testdata = "../tests/common_pt4.css"
    ## testdata = "../../htmledit/ashe/test.css"
    testname = os.path.basename(testdata)
    test = Editor(filename=testdata)
    ## with open("/tmp/{}_na_open".format(testname), "w") as f:
        ## for item in list(test.data): print(item, file=f)
    olddata = test.data
    test.datatotext()
    with open("/tmp/{}_na_datatotext".format(testname), "w") as f:
        for item in test.textdata: print(item, file=f)
    ## test.texttodata()
    ## print('nieuw = oud:', test.data == olddata)
    ## with open("/tmp/{}_na_texttodata".format(testname), "w") as f:
        ## for item in list(test.data): print(item, file=f)

    ## text = get_definition_from_file("../tests/common.css", 1, 60)
    ## print(text)









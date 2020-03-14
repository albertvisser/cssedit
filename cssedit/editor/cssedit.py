"""csseditor backend
"""
import os
import shutil
## import pathlib - don't think this is suitable if cssutls only woks with Python 2
import collections
import logging
import cssutils

format_types = ("long", "medium", "short", "compressed")
comment_tag = '/**/'
logline_elements = ["severity", "subject", "message", "line", "pos", "data"]
LogLine = collections.namedtuple('LogLine', logline_elements)
text_type, list_type, table_type = '1', 'n', 'n*2'

RTYPES = {
    cssutils.css.CSSRule.STYLE_RULE: (
        'STYLE_RULE', [
            ("selectors",
             list_type,
             lambda rule: [x.selectorText for x in rule.selectorList]),
            ("styles",
             table_type,
             lambda rule: {x.name: x.propertyValue.cssText
                           for x in rule.style.getProperties()})]),
    cssutils.css.CSSRule.CHARSET_RULE: (
        'CHARSET_RULE', [
            ("name",
             text_type,
             lambda rule: rule.encoding)]),
    cssutils.css.CSSRule.IMPORT_RULE: (
        'IMPORT_RULE', [
            ("uri",
             text_type,
             lambda rule: rule.href),
            ("media",
             list_type,
             lambda rule: [x.value.mediaText for x in rule.media])]),  # media is optional
    cssutils.css.CSSRule.MEDIA_RULE: (
        'MEDIA_RULE', [
            ("media",
             list_type,
             lambda rule: [x.value.mediaText for x in rule.media]),
            ("rules",
             list_type,
             lambda rule: [(x.typeString, complete_ruledata(init_ruledata(x.type), x))
                           for x in rule.cssRules])]),  # media is optional
    cssutils.css.CSSRule.FONT_FACE_RULE: (
        'FONT_FACE_RULE', [
            ("styles",
             table_type,
             lambda rule: {x.name: x.propertyValue.cssText
                           for x in rule.style.getProperties()})]),
    cssutils.css.CSSRule.PAGE_RULE: (
        'PAGE_RULE', [
            ("selector",
             list_type,
             lambda rule: rule.selectorText),
            ("styles",
             table_type,
             lambda rule: {x.name: x.propertyValue.cssText
                           for x in rule.style.getProperties()})]),
    cssutils.css.CSSRule.NAMESPACE_RULE: (
        'NAMESPACE_RULE', [
            ("name",
             text_type,
             lambda rule: rule.prefix),
            ("uri",
             text_type,
             lambda rule: rule.namespaceURI)]),  # name (prefix) is optional
    cssutils.css.CSSRule.COMMENT: (
        'COMMENT', [
            ("text",
             text_type,
             lambda rule: rule.cssText[2:-2].strip())]),
    ## cssutils.css.CSSRule.MARGIN_RULE: ('MARGIN_RULE',
        ## []), # experimental rule not in the offical spec
    ## cssutils.css.CSSRule.VARIABLES_RULE: ('VARIABLES_RULE',
        ## []), # experimental rule not in the offical spec
    ## # volgens MozDEv zijn er nog een aantal ruletypes (experimental) :
    ## @supports
    ## - text subnode (feature test)
    ## - list subnode (rules)
    ## @document
    ## - text subnode (url/url-prefix/domain/regexp)
    ## - table subnode (styles)
    ## @keyframes
    ## @viewport
    ## - table subnode (styles)
    ## @counter-style
    ## - text subnode (name of counter-style)
    ## - table subnode (declarations/styles)
    ## @font-feature-values
    ## - subrules: @swash @annotation @ornaments @stylistic @styleset @character-variant
    cssutils.css.CSSRule.UNKNOWN_RULE: (
        'UNKNOWN_RULE', [
            ("data",
             text_type,
             lambda rule: rule.cssText.strip())])}

# @media queries op niet-standaard attributen (bv, -webkit-min-device-pixel-ratio:2
#   gaan mis, dwz de css tekst gaat verloren
# Ik heb hier een fix op gemaakt maar cssutils zou het eigenlijk aan moeten kunnen


def set_logger(logfile):
    """define logger for parsing errors
    """
    log = logging.getLogger('CSSEDIT')
    hdlr = logging.FileHandler(logfile, mode='w')
    formatter = logging.Formatter('%(levelname)s\t%(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.INFO)
    cssutils.log.setLog(log)
    return hdlr


def load(filename):
    """Load a file

    Note: does not return a string but a CSSStyleSheet instance
    """
    # compensate for missing feature(s)
    got_media = -1
    with open(filename) as f:
        data = f.read()
        got_media = data.find('@media (')
    if got_media > -1:
        return cssutils.parseString(data.replace('@media (', '@media all and ('))
    return cssutils.parseFile(filename)


def get_for_single_tag(cssdata):
    """Parse attribute value from a style tag

    Note: does not return a string but a CSSStyleDeclaration instance
    """
    return cssutils.parseStyle(cssdata)


def return_for_single_tag(cssdata):
    """Build attribute value for a style tag

    return rule text or empty string
    """
    if list(cssdata):
        return list(cssdata)[0].style.getCssText()
    else:
        return ""


def parse(text):
    """Parse part of the file data

    Note: does not return a string but a CSSStyleSheet instance or...
    """
    return cssutils.parseString(text)


def set_format(mode="compressed"):
    "set global properties for cssutils"
    # To set a preference use: cssutils.ser.prefs.PREFNAME = NEWVALUE
    # don't think I'll be needing the inputlist parameter
    # set some properties depending om mode, e.g.
    # indent = 4 * ‘ ‘
    #     Indentation of e.g Properties inside a CSSStyleDeclaration
    # indentClosingBrace = True
    #     Defines if closing brace of block is indented to match indentation of the block
    #     (default) oder match indentation of selector.
    # keepComments = True
    #     If False removes all CSSComments
    # lineSeparator = u’n’
    #     How to end a line. This may be set to e.g. u’’ for serializing of CSSStyleDeclarations
    #     usable in HTML style attribute.


def save(data, filename, backup=True):
    """save to file

    expects data to be a CSSStyleSheet instance
    """
    if backup and os.path.exists(filename):
        shutil.copyfile(filename, filename + "~")
    try_again = False
    with open(filename, 'wb') as f_out:
        try:
            f_out.write(data.cssText)
        except AttributeError:
            try_again = True
    if try_again:
        with open(filename, 'w', encoding='utf-8') as f_out:
            print(data, file=f_out)


def get_definition_from_file(file, line, pos):
    """snip inline css definition from an HTML file
    """
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
    """prepare rule part of internal data structure
    """
    ruledata = {}  # {'selectors': [], 'styles', {}}
    for x, y, _ in RTYPES[ruletype][1]:
        ruledata[x] = {} if y == table_type else [] if y == list_type else ''
    return ruledata


def complete_ruledata(ruledata, rule):
    """finish rule part of internal data structure
    """
    for x, y, z in RTYPES[rule.type][1]:
        ruledata[x] = z(rule)
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
    if len(test) == 1:  # unexpected token
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
    """Basic editor functionality
    """
    def __init__(self, **kwargs):  # filename="", tag="", text=""):
        """get css from a source and turn it into a structure
        """
        self.filename = self.tag = ""
        self.data = []
        newfile = False
        # text = None  # must be allowed to be empty (to create new inline style)
        try:
            if kwargs.pop('new'):
                newfile = True
        except KeyError:
            pass
        try:
            self.filename = kwargs.pop('filename')
        except KeyError:
            pass
        try:
            self.tag = kwargs.pop('tag')
        except KeyError:
            pass
        try:
            text = kwargs.pop('text')
        except KeyError:
            text = ''  # pass
        if newfile:
            return

        if self.filename:
            if any((self.tag, text)):
                raise ValueError('Ambiguous arguments')
        else:
            if text is None:
                raise ValueError("Not enough arguments")
        if kwargs:
            raise ValueError('Too many arguments')

        if newfile:
            return
        hlp = '' if not self.filename else '_' + os.path.basename(self.filename)
        logfile = '/tmp/cssedit{}.log'.format(hlp)
        hdlr = set_logger(logfile)
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
            # TODO: raise error when this doesn't parse into a CSSStylesheet

        hdlr.close()
        self.log = ['unable to get log info']
        with open(logfile) as _log:
            self.log = [line.strip() for line in _log]

        if not self.data:
            raise ValueError("Incorrect css data")

    def datatotext(self):
        """turn the cssutils structure into a more generic one
        """
        self.textdata = []
        for ix, rule in enumerate(list(self.data)):
            ruledata = init_ruledata(rule.type)  # collections.defaultdict(dict)
            ruledata['seqnum'] = ix
            ruledata = complete_ruledata(ruledata, rule)
            self.textdata.append((rule.typeString, ruledata))

    def texttodata(self):
        """turn the generic structure into a cssutils one
        """
        self.data = cssutils.css.CSSStyleSheet()
        for ruletype, ruledata in self.textdata:
            ## print(selector, propertydata)
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
                medialist = cssutils.css.MediaList()
                for medium in ruledata['media']:
                    medialist.append(medium)
                rule.mediaList = medialist
                rule.styles = cssutils.css.RuleList()
                for name, value in ruledata['rules']:
                    srule = cssutils.css.CSSStyleRule()
                    ssellist = cssutils.css.SelectorList()
                    for selector in value['selectors']:
                        ssellist.append(selector)
                    srule.selectorList = ssellist
                    sstyle = cssutils.css.CSSStyleDeclaration()
                    for sprop, sdata in value['styles'].items():
                        sstyle[sprop] = sdata
                    srule.style = sstyle
                rule.styles.append(srule)

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
        """turn internal structure back into style(sheet) source
        """
        if savemode not in format_types:
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
            self.data = self.data.cssText  # maybe need to stringify this?


if __name__ == "__main__":
    testdata = ["../tests/simplecss-long.css",
                "../tests/common_pt1.css",
                "../tests/common_pt4.css",
                "../tests/extra_ruletypes.css",
                "../../htmledit/ashe/test.css"]
    testdata = [testdata[3]]
    for item in testdata:
        testname = os.path.basename(item)
        test = Editor(filename=item)
        ## with open("/tmp/{}_na_open".format(testname), "w") as f:
            ## for item in list(test.data): print(item, file=f)
        olddata = test.data
        test.datatotext()
        with open("/tmp/{}_na_datatotext".format(testname), "w") as f:
            for item in test.textdata:
                print(item, file=f)
        ## test.texttodata()
        ## print('nieuw = oud:', test.data == olddata)
        ## with open("/tmp/{}_na_texttodata".format(testname), "w") as f:
            ## for item in list(test.data): print(item, file=f)

        ## text = get_definition_from_file("../tests/common.css", 1, 60)
        ## print(text)

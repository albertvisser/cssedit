import os
import shutil
## import pathlib - don't think this is suitable
import collections
import cssutils
import logging

format_types = ("long", "medium", "short", "compressed")
comment_tag = '/**/'

def load(filename):
    "Note: does not return a string but a CSSStyleSheet instance"
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
    "Note: does not return a string but a CSSStyleSheet instance"
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
    with open(filename, 'w') as f_out:
        print(data.cssText, file=f_out)

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

class Editor:

    def __init__(self, **kwargs): # filename="", tag="", text=""):
        """get css from a source and turn it into a structure
        """
        self.filename = self.tag = text = ''
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
            if not text:
                raise ValueError("Not enough arguments")
        if kwargs:
            raise ValueError('Too many arguments')

        self.data = []
        hdlr = self.set_logger()
        if self.filename:
            self.data = load(self.filename)
        elif self.tag:
            style = get_for_single_tag(text)
            self.data = cssutils.css.CSSStyleSheet()
            rule = cssutils.css.CSSStyleRule(selectorText=self.tag, style=style)
            self.data.add(rule)
        else:
            self.data = parse(text)

        hdlr.close()
        self.log = ['unable to get log info']
        with open('/tmp/cssedit.log') as _log:
            self.log = [line.strip() for line in _log]

        if not self.data:
            raise ValueError("Incorrect css data")

    def set_logger(self):
        ## with open('/tmp/cssedit.log', 'w') as _log:
            ## cssutils.log.setLog(_log)
        log = logging.getLogger('CSSEDIT')
        hdlr = logging.FileHandler('/tmp/cssedit.log', mode='w')
        formatter = logging.Formatter('%(levelname)s\t%(message)s')
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
        log.setLevel(logging.INFO)
        cssutils.log.setLog(log)
        return hdlr

    def datatotext(self):
        """turn the cssutils structure into a more generic one
        """
        self.treedata = []
        for ix, value in enumerate(list(self.data)):
            ## print(value.selectorText)
            ## print(value.selectorList)
            ## print(list(value.selectorList))
            try:
                selector_list = list(value.selectorList)
            except AttributeError as e:
                if isinstance(value, cssutils.css.CSSComment):
                    self.treedata.append((comment_tag, value.cssText[1:-1].strip()))
                elif isinstance(value, cssutils.css.cssmediarule.CSSMediaRule):
                    # TODO
                else:
                    # TODO: newlines weer gewoon doorgeven en in GUI in zo'n geval een multiline veld maken oid
                    self.treedata.append((type(value), value.cssText[1:-1].replace(
                        '\n', '').strip()))
            else:
                propdict = {}
                for prop in value.style.getProperties():
                    propdict[prop.name] = prop.propertyValue.cssText
                for selector in selector_list:
                    self.treedata.append((selector, propdict))

    def texttodata(self):
        """turn the generic structure into a cssutils one
        """
        data = cssutils.css.CSSStyleSheet()
        for selector, propertydata in self.treedata:
            if selector == comment_tag:
                rule = cssutils.css.CSSComment(
                    cssText='/* {} */'.format(propertydata))
            else:
                style = cssutils.css.CSSStyleDeclaration()
                for property, value in propertydata.items():
                    style[property] = value
                rule = cssutils.css.CSSStyleRule(selectorText=selector,
                    style=style)
            data.add(rule)
        self.data = data # compile(data)

    def return_to_source(self, backup=True, savemode="compressed"):
        "ahem"
        if savemode not in (format_types):
            info = "`, `".join(format_types[:-1])
            info = "` or `".join((info, format_types[-1]))
            raise AttributeError("wrong format type for save, should be either of "
                "`{}`".format(info))
        ## ## data = compile(self.data)
        set_format(mode)
        if self.filename:
            save(self.data, self.filename, backup)
        elif self.tag:
            self.cssdata = return_for_single_tag(self.data)
        else:
            self.data = self.data.cssText

# this doesn't do anything yet with
# - comments, either inline or in between selectors
# - selectors which are used multiple times (defining different properties in different places)
#   a dictionary would take only the last defined property?
#   No, but you lose where what is defined
#   this can be solved by being clever making combinations in the parse function
# - groups of selectors with a common definition
#   so a "selector" can also be a (comma-separated) "list of selectors"
#   and you'd need to assign all the properties in the definition to all the
#   selectors in the list
#   this should be solved in the compile function

# might be useful to try and use the "cssutils" package
# instead of trying to solve this myself


if __name__ == "__main__":
    ## test = Editor(filename="../tests/simplecss-long.css")
    test = Editor(filename="../tests/common_pt3.css")
    ## for x in test.log:
        ## print(x.strip())
    ## print(test.log[0].strip())
    test.datatotext()
    ## test.texttodata()
    ## text = get_definition_from_file("../tests/common.css", 1, 60)
    ## print(text)










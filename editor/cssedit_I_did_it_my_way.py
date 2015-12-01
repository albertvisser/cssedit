# primary function: take a piece of css code and show it in a treeview
# making no difference between a "formatted" and a "compressed" version

# so you should be able to either load a file or load a piece of text
# and return a changed result to wherever it came form

# if the incoming text comes from inlines in a html source it should either be the part
# contained in <style><style> tags  or the part contained in a style="..." property; in
# the latter case it should be accompanied with the html tag it's a property of.

# so first of all we need
# - a load function that reads a file and returns it as text
# - a parse function that takes a piece text and returns it as a tree
# - a "compile" function that takes a tree and turns it into text
# - a save function that save a piece of text to a file, in the requested format
import os
import shutil
import collections
format_types = ("long", "medium", "short", "compressed")
comment_tag = '/**/'

def fsplit(text, delimiter, multi=False):
    """split text, but keep split character attached to first part
    """
    if multi:
        data = text.split(delimiter)
    else:
        data = text.split(delimiter, 1)
    for idx, item in enumerate(data[:-1]):
        data[idx] += delimiter.strip()
    return data

def load(filename):
    # TODO: handle blank lines (wrt output = input)
    with open(filename) as f_in:
        result = " ".join([x.strip() for x in f_in.readlines()])
    return result

def get_for_single_tag(cssdata):
    " tekst naar dict"
    propdict = {}
    for item in cssdata.split(';'):
        if item.strip() == "": continue
        if ':' not in item: continue
        prop, value = item.split(':')
        propdict[prop.strip()] = value.strip()
    return propdict # of moet tag ook mee voor het onthouden?

def return_for_single_tag(cssdata):
    " dict naar tekst"
    properties = []
    for property, value in sorted(cssdata.items()):
        properties.append("{}: {};".format(property, value))
    return " ".join(properties)

def parse(text):
    # TODO: handle inline comments
    def nodes():
        return collections.defaultdict(dict)
    seq = 0
    lines = text.split('}')
    selectors = []
    for line in lines:
        # skip empty lines
        if '{' not in line: continue
        # collect comments separately - works only for in between selectors
        comments = fsplit(line, '*/', multi=True)
        for item in comments[:-1]:
            selectors.append((comment_tag, item.strip()[2:-2].strip()))
        line = comments[-1]
        node, data = line.split('{')
        seq += 1
        node = node.strip()
        properties = data.split(';')
        propdict = {}
        for item in properties:
            if item.strip() == "": continue
            if ':' not in item: continue
            prop, value = item.split(':')
            propdict[prop.strip()] = value.strip()
        selectors.append((node, propdict))
    return selectors

## def compile(inputlist):
    ## # compile should not return a string but a list, so format knows better about separate lines`
    ## # or maybe we shouldn't use this at all?
    ## result = []
    ## for node, data in inputlist:
        ## if node == comment_tag:
            ## result.append('/* {} */'.format(data))
            ## continue
        ## components = []
        ## for key in sorted(data.keys()):
            ## components.append("{}: {};".format(key, data[key]))
        ## data = ' '
        ## if components:
            ## data += ' '.join(components) + ' '
        ## result.append('{} {{{}}}'.format(node, data))
    ## return result

def format(inputlist, mode="compressed"):
    "returns a text unless the compression mode is wrong"
    if mode not in (format_types):
        return
    lines = []
    for selector, data in inputlist:
        # elke regel is een tuple
        if selector == comment_tag:
            # element 1 geeft commentaar aan, element 2 is de commentaartekst
            if mode != "compressed":
                lines.append('/* {} */'.format(data))
            continue
        # element 1 is een string en element 2 een dictionary
        properties = []
        for property, value in sorted(data.items()):
            properties.append("{}: {};".format(property, value))
        propertiesline = " ".join(properties)
        selector_start, selector_end = selector + " {", "}"
        selectorline = " ".join((selector_start, propertiesline, selector_end))
        if mode in ("compressed", "short"):
            lines.append(selectorline)
        else: # mode in ("medium", "long")
            lines.append(selector_start)
            if mode == "medium":
                lines.append("    {}".format(propertiesline))
            else:
                lines.extend(["    {}".format(x) for x in properties])
            lines.append(selector_end)
    if mode == "compressed":
        return " ".join(lines)
    else:
        return "\n".join(lines)

def save(data, filename, backup=True):
    if backup and os.path.exists(filename):
        shutil.copyfile(filename, filename + "~")
    with open(filename, 'w') as f_out:
        f_out.write(data)


class Editor:

    def __init__(self, **kwargs): # filename="", tag="", text=""):
        """get css from a source and turn it into a structure
        """
        self.filename = self.tag = text = ''
        self.data = []
        if 'filename' in kwargs:
            self.filename = kwargs['filename']
            if self.filename == '':
                raise ValueError("Invalid filename")
            text = load(self.filename)
        if 'tag' in kwargs:
            self.tag = kwargs['tag']
        if 'text' in kwargs:
            text = kwargs['text']
        if not text:
            raise ValueError("Not enough arguments")
        elif ':' not in text:
            raise ValueError("Incorrect css data")
        elif self.tag:
            ## self.data = get_for_single_tag(text)
            self.data = [(self.tag, get_for_single_tag(text))]
        else:
            self.data = parse(text)
        if not self.data:
            raise ValueError("Incorrect css data")
        # TODO: andere controles op deze data

    def datatotext(self):
        self.treedata = self.data

    def texttodata(self):
        self.data = self.treedata

    def return_to_source(self, backup=True, savemode="compressed"):
        if savemode not in (format_types):
            info = "`, `".join(format_types[:-1])
            info = "` or `".join((info, format_types[-1]))
            raise AttributeError("wrong format type for save, should be either of "
                "`{}`".format(info))
        ## data = compile(self.data)
        if self.filename:
            save(format(self.data, savemode), self.filename, backup)
        elif self.tag:
            self.cssdata = return_for_single_tag(self.data[0][1])
        else:
            self.data = format(self.data, savemode) # otherwise it's not accessible


class DemoEditor:
    """Simple demo class using Editor
    """

    def __init__():
        self.css = Editor(filename="../tests/simplecss-long.css")
        self.css.datatotext()
        self.texttotree()
        self.treetotext()
        self.css.texttodata()

    def texttotree(self):
        """turn the structure into a generic thing
        """
        self.visual_data = []
        for ix, value in enumerate(self.css.data):
            ## self.treedata.append(str(ix + 1))
            item, contents = value
            if item == comment_tag:
                self.visual_data.append(comment_tag)
                self.visual_data.append('    {}'.format(contents))
                continue
            for selector in item.split(','):
                self.visual_data.append("{}".format(selector.strip()))
                for property, value in sorted(contents.items()):
                    self.visual_data.append("    {}".format(property))
                    self.visual_data.append("        {}".format(value))

    def treetotext(self):
        """turn the visual thing into a structure
        """
        data = []
        propdict = {}
        in_comment = False
        for item in self.treedata:
            if not item.startswith('    '):
                if propdict:
                    data.append((selector, propdict))
                selector = item.strip()
                if selector == comment_tag:
                    in_comment = True
                propdict = {}
            elif not item.startswith('        '):
                property = item.strip()
                if in_comment:
                    data.append((selector, property))
                    in_comment = False
            elif not item.startswith('            '):
                value = item.strip()
                propdict[property] = value
        if propdict:
            data.append((selector, propdict))
        self.css.data = data

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











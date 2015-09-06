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
    with open(filename) as f_in:
        result = " ".join([x.strip() for x in f_in.readlines()])
    return result

def get_for_single_tag(tag, cssdata):
    return "{} {{ {} }}".format(tag, cssdata.strip())

def return_for_single_tag(cssdata):
    return [x.strip() for x in cssdata.strip('}').split(" { ")]

def parse(text):
    def nodes():
        return collections.defaultdict(dict)
    seq = 0
    lines = text.split('}')
    selectors = []
    for line in lines:
        # skip empty lines
        if '{' not in line: continue
        # collect comments separately
        comments = fsplit(line, '*/', multi=True)
        for item in comments[:-1]:
            selectors.append(('/**/', item.strip()[2:-2].strip()))
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

def compile(inputlist):
    result = ""
    for node, data in inputlist:
        if node == '/**/':
            result += '/* {} */'.format(data)
            continue
        components = []
        for key in sorted(data.keys()):
            components.append("{}: {};".format(key, data[key]))
        data = ' '
        if components:
            data += ' '.join(components) + ' '
        result += '{} {{{}}} '.format(node, data)
    return result.strip()

def format(data, format="compressed"):
    "returns a text unless the compression format is wrong"
    if format not in (format_types):
        return
    if format == "compressed":
        return data
    result = []
    lines = data.split('} ')
    for line in lines:
        line = line.strip()
        if line == "": continue
        line = line.strip('}').strip()
        if format == "short":
            result.append(line + " }")
        else:
            selector, seldata = line.split('{ ')
            ## if not seldata.endswith(';'):
                ## seldata = seldata + ';'
            result.append(selector + "{")
            if format == "long":
                properties = seldata.split(';')
                for prop in properties:
                    test = prop.strip()
                    if test:
                        result.append("    {};".format(test))
            else:
                result.append("    {}".format(seldata.strip()))
            result.append("}")
    return os.linesep.join(result)

def save(data, filename, backup=True):
    if backup and os.path.exists(filename):
        shutil.copyfile(filename, filename + "~")
    with open(filename, 'w') as f_out:
        f_out.write(data)


class Editor:

    def __init__(self, **kwargs): # filename="", tag="", text=""):
        """get css from a source and turn it into a structure
        """
        filename = tag = text = ''
        if 'filename' in kwargs: filename = kwargs['filename']
        if 'tag' in kwargs: tag = kwargs['tag']
        if 'text' in kwargs: text = kwargs['text']
        self.filename = self.tag = ""
        if filename:                        # css file
            text = load(filename)
            self.filename = filename
        elif tag and text:                  # tag and contents of style property
            ## if ':' not in text:
                ## raise ValueError("Incorrect css data")
            text = get_for_single_tag(tag, text)
            self.tag = tag
        ## elif text:                          # contents of style tag
            ## if ':' not in text:
                ## raise ValueError("Incorrect css data")
        ## else:
        elif not text:
            raise ValueError("Not enough arguments")
        self.data = parse(text)
        if not self.data:
            raise ValueError("Incorrect css data")
        # TODO: andere controles op deze data

    def texttotree(self):
        """turn the structure into a visual thing
        """
        self.treedata = []
        for ix, value in enumerate(self.data):
            ## self.treedata.append(str(ix + 1))
            item, contents = value
            for selector in item.split(','):
                self.treedata.append("{}".format(selector.strip()))
                for property, value in sorted(contents.items()):
                    self.treedata.append("    {}".format(property))
                    self.treedata.append("        {}".format(value))

    def treetotext(self):
        """turn the visual thing into a structure
        """
        data = []
        propdict = {}
        for item in self.treedata:
            if not item.startswith('    '):
                if propdict:
                    data.append((selector, propdict))
                selector = item.strip()
                propdict = {}
            elif not item.startswith('        '):
                property = item.strip()
            elif not item.startswith('            '):
                value = item.strip()
                propdict[property] = value
        if propdict:
            data.append((selector, propdict))
        self.data = data # compile(data)

    def return_to_source(self, backup=True, savemode="compressed"):
        if savemode not in (format_types):
            info = "`, `".join(format_types[:-1])
            info = "` or `".join((info, format_types[-1]))
            raise AttributeError("wrong format type for save, should be either of "
                "`{}`".format(info))
        data = compile(self.data)
        if self.filename:
            save(format(data, savemode), self.filename, backup)
        elif self.tag:
            self.cssdata = return_for_single_tag(data)
        else:
            self.data = format(data, savemode) # otherwise it's not accessible



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











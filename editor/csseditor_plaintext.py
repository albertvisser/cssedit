import sys
import os
from cssedit import Editor, comment_tag

def formatted(text, indent):
    text = str(text) # make sure it's a string
    start = indent * ' '
    return start + text

def read_rules(data, indent):
    "recursive structure to read rules"
    retval = []
    for rltype, rldata in data:
        retval.append(formatted(rltype, indent))
        for key, value in rldata.items():
            retval.append(formatted(key, indent + 4))
            if key in ('seqnum', 'text'):
                retval.append(formatted(value, indent + 8))
            elif key == 'rules':
                retval.extend(read_rules(value, indent + 8))
            else:
                for it in value:
                    retval.append(formatted(it, indent + 8))
                    try:
                        retval.append(formatted(value[it], indent + 12))
                    except TypeError as e:
                        pass
    return retval

class DemoEditor:
    """Simple demo class using Editor
    """

    def __init__(self, fname):
        self.outname = os.path.join('/tmp', os.path.basename(fname)) + '.out'
        self.css = Editor(filename=fname)
        self.css.datatotext()
        self.texttotree()
        with open(self.outname, 'w') as f:
            for line in self.visual_data: print(line, file=f)

    def save(self):
        self.treetotext()
        self.css.texttodata()

    def texttotree(self):
        """turn the structure into a generic thing
        """
        self.visual_data = read_rules(self.css.textdata, 0)

            ## if item == comment_tag:
                ## self.visual_data.append(item)
                ## self.visual_data.append('    {}'.format(contents))
                ## continue
            ## else:
                ## try:
                    ## selector = item.selectorText
                ## except AttributeError:
                    ## self.visual_data.append(str(selector))
                    ## self.visual_data.append('    {}'.format(contents))
                    ## continue
                ## self.visual_data.append("{}".format(selector))
                ## for property, value in sorted(contents.items()):
                    ## self.visual_data.append("    {}".format(property))
                    ## self.visual_data.append("        {}".format(value))

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


if __name__ == "__main__":
    test = DemoEditor(sys.argv[1])

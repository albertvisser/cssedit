"""Plain text frontend (terminal version)
"""
import sys
import os
from cssedit import Editor, comment_tag


def formatted(text, indent):
    "return text with leading spaces"
    ## text = str(text) # make sure it's a string
    ## start = indent * ' '
    ## return start + text
    return text.rjust(len(text) + indent)


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
                    except TypeError:
                        pass
    return retval


class DemoEditor:
    """Simple demo class using Editor
    """
    def __init__(self, fname):
        """load css from file
        """
        self.outname = os.path.join('/tmp', os.path.basename(fname)) + '.out'
        self.css = Editor(filename=fname)
        self.css.datatotext()
        self.texttotree()
        with open(self.outname, 'w') as f:
            for line in self.visual_data:
                print(line, file=f)

    def save(self):
        """save css back
        """
        self.treetotext()
        self.css.texttodata()

    def texttotree(self):
        """convert the internal structure into visual data
        """
        self.visual_data = read_rules(self.css.textdata, 0)

    def treetotext(self):
        """convert the visual data into an internal structure
        """
        data = []
        propdict = {}
        in_comment = False
        for item in self.visual_data:
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

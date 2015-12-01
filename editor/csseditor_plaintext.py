from cssedit import Editor, comment_tag

class DemoEditor:
    """Simple demo class using Editor
    """

    def __init__(self, fname):
        self.css = Editor(filename=fname)
        self.css.datatotext()
        self.texttotree()
        for line in self.visual_data:
            print(line)

    def save(self):
        self.treetotext()
        self.css.texttodata()

    def texttotree(self):
        """turn the structure into a generic thing
        """
        self.visual_data = []
        ## for ix, value in enumerate(self.css.data):
            ## item, contents = value
        for item, contents in self.css.treedata:
            if item == comment_tag:
                self.visual_data.append(item)
                self.visual_data.append('    {}'.format(contents))
                continue
            else:
                try:
                    selector = item.selectorText
                except AttributeError:
                    self.visual_data.append(str(selector))
                    self.visual_data.append('    {}'.format(contents))
                    continue
                self.visual_data.append("{}".format(selector))
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


if __name__ == "__main__":
    test = DemoEditor("../tests/simplecss-long.css")

class Breadcrumbs:
    patterns = None
    location = None
    tree = None

    def __init__(self, *, patterns, location=None):
        self.patterns = patterns
        self.location = location

        if self.location:
            self.update_tree(location)
        else:
            self.tree = self.patterns

    def update_tree(self, location):
        self.location = location
        try:
            self.tree = self.patterns[self.location]
            return self.tree
        except KeyError:
            self.tree = self.patterns
            return False

    def as_html(self):
        pass


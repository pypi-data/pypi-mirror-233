class Changelog:

    def __init__(self, data: dict):
        self.data: dict = data or {}

    def get_added(self):
        return self["added"]

    def get_removed(self):
        return self["removed"]

    def get_changed(self):
        return self["changed"]

    def get_fixed(self):
        return self["fixed"]

    def __getitem__(self, key):
        return self.data[key]

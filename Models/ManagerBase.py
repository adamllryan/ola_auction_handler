from collections.abc import Iterable


class ManagerBase:

    manager_name: str

    def __init__(self, name: str):

        self.manager_name = name
        print("Init Manager -> ({name})".format(name=self.manager_name))


    def dispose(self):
        print("Disposing Manager -> ({name})".format(name=self.manager_name))
        pass

    def get_auctions(self):
        print("Getting auctions with Manager -> ({name})".format(name=self.manager_name))
        pass

    def filter_auctions(self):
        print("Filtering auctions for Manager -> ({name})".format(name=self.manager_name))
        pass

    def get_items_raw(self, is_my_items: bool):
        print("Getting all items for ({name})".format(name=self.manager_name))
        pass

    def read_listings(self, f: Iterable[str]):
        print("Loading all items on file for ({name})".format(name=self.manager_name))

    def read_my_listings(self, f: Iterable[str]):
        print("Loading my items on file for ({name})".format(name=self.manager_name))

    def filter_items(self):
        print("Filtering items for ({name})".format(name=self.manager_name))
        pass

    def refresh(self):
        print("Refreshing items for ({name})".format(name=self.manager_name))
        pass

    def refresh_my(self):
        print("Refreshing select items for ({name})".format(name=self.manager_name))
        pass

    def add_listings(self, items: list[int]):
        print("Adding listings for ({name})".format(name=self.manager_name))
        pass

    def remove_listings(self, items: list[int]):
        print("Removing listings for ({name})".format(name=self.manager_name))
        pass

    def add_filters(self, items: list[str]):
        print("Adding filter items for ({name})".format(name=self.manager_name))
        pass

    def remove_filters(self, items: list[str]):
        print("Removing filter items for ({name})".format(name=self.manager_name))
        pass

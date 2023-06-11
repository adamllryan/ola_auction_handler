

class UIBase:

    view_name: str

    def __init__(self, name: str):

        self.view_name = name

        print("Init UI -> ({name})".format(name=self.view_name))
        pass

    def dispose(self):
        print("Disposing UI -> ({name})".format(name=self.view_name))
        pass

    def add_item(self, data:str):
        print("Adding Listing to ({name})".format(name=self.view_name))
        pass

    def remove_item(self, data:str):
        print("Removing Listing from ({name})".format(name=self.view_name))
        pass

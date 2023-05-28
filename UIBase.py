class UIBase:
    def __init__(self):
        if self.ui_name is None:
            self.ui_name = "UIBase"
        print("Init UI -> ({name})".format(name=self.ui_name))
        pass

    def dispose(self):
        print("Disposing UI -> ({name})".format(name=self.ui_name))
        pass

    def add_item(self, data:str):
        print("Adding Listing to ({name})".format(name=self.ui_name))
        pass

    def remove_item(self, data:str):
        print("Removing Listing from ({name})".format(name=self.ui_name))
        pass

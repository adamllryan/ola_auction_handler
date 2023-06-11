import os

from Controllers.ControllerBase import ControllerBase
from enum import Enum

from Models.ManagerBase import ManagerBase
from Views.UIBase import UIBase


class Commands(Enum):
    REFRESH = 1
    ADD_ITEM = 2
    REMOVE_ITEM = 3
    ADD_FILTER = 4
    REMOVE_FILTER = 5
    LOAD_FILE = 6


class Controller0(ControllerBase):

    filter_terms: list[str]

    def __init__(self, model: ManagerBase, view: UIBase):

        super().__init__('Controller0', model, view)



    def input(self, command: Commands, data):

        print()
        super().input(command, data)

        if command is Commands.REFRESH:

            if data == 'All Items':

                print('Refreshing all items...')
                self.model.refresh()

            elif data == 'Your Items':

                print('Refreshing your items...')
                self.model.refresh_my()

        elif command is Commands.ADD_ITEM:

            print('Adding listings')
            self.model.add_listings(data)

        elif command is Commands.REMOVE_ITEM:

            print('Removing listings')
            self.model.remove_listings(data)

        elif command is Commands.ADD_FILTER:

            print('Adding filters')
            self.model.add_filters(data)

        elif command is Commands.REMOVE_FILTER:

            print('Removing filters')
            self.model.remove_filters(data)

        elif command is Commands.LOAD_FILE:

            print('Loading from file')
            if data == 'All Items':

                print('Loading all items...')
                self.model.read_listings()

            elif data == 'Your Items':

                print('Loading your items...')
                self.model.read_my_listings()

        else:

            print("Unhandled Command\n\n")
        print('\n\n')

    def run(self):
        self.input(Commands.REFRESH, 'All Items')
        data = ['kid', 'men', 'women', 'shelf', 'artwork', 'scratch', 'cat', 'shoe', 'shelv', 'gaming chair', 'desk',
                'table', 'costume', 'baby']
        self.input(Commands.ADD_FILTER, data)

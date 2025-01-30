import numpy as np
import random

from utilities import *
from ui import UI

class Location:
    def __init__(self, name: str, prep='in'):
        self.name = name
        self.neighbors = set()
        self.items = set()
        self.message = 'You are ' + prep + ' ' + self.name
    
    # Adds neighbors to self.neighbors, doesn't add self as neighbor to neighbors
    def add_neighbors(self, neighbors):
        for n in neighbors:
            self.neighbors.add(neighbors[n])
    
    # Adds item to location.
    # This means item will show up and be interactable when interacting with location
    def add_item(self, item):
        self.items.add(item)
    
    # Removes item from location
    def remove_item(self, item):
        self.items.remove(item)
    
    # Called when player enters location.
    # Lists neighbors and items so player can interact with them.
    def interact(self):
        UI.set_loc(self.message)
        actions = [] # List of locations and items that player can interact with
        options = '' # String to present available actions to player
        i=0 # Option index as presented to player, one more than actual list index
        for loc in self.neighbors:
            i+=1
            actions.append(loc)
            options += '\n(' + str(i) + ') Enter ' + loc.name
        for item in self.items:
            i+=1
            actions.append(item)
            options += '\n(' + str(i) + ') ' + item.command + item.name
        
        

        UI.get_user_input(
            'Options:' + options.replace('\n', '\n  '), # Indent options
            choose_action,
            actions    
        )
                
    # Adds all locations as neighbors to each other
    @staticmethod
    def connect(*locs):
        for loc0 in locs:
            for loc1 in locs:
                if loc0 != loc1:
                    loc0.add_neighbors({'loc':loc1})

class Item:
    loc = ''

    def __init__(self, name, loc, command = 'Check out ', interact = None, message = '', attr = {}):
        self.name = name
        self.move(loc)
        self.command = command
        if interact:
            self.interact = interact
        self.message = message or 'This is ' + self.name
        # Add custom attributes to item 
        for k in attr.keys():
            setattr(self, k, attr[k])
    
    def interact(self):
        UI.get_user_input(
            self.message,
            lambda user_input, loc : loc.interact(),
            self.loc
        )
    
    def move(self, destination):
        if self.loc:
            self.loc.remove_item(self)
        destination.add_item(self)
        self.loc = destination
    
    def move_random(self):
        locs = list(self.loc.neighbors)
        if len(locs):
            self.move(random.choice(locs))

class Animal(Item):
    def __init__(self, name, loc, command='Check out ', interact=None, message='', attr={}, player_love = {'main': 0}):
        super().__init__(name, loc, command, interact, message, attr)
        self.player_love = player_love
    
    def get_total_player_love(self):
        love = 0
        for k in self.player_love.keys():
            love += self.player_love[k]
        return love
    
    def interact(self):
        UI.get_user_input(
            self.message,
            lambda user_input, loc : loc.interact(),
            self.loc
        )
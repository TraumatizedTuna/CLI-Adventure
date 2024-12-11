import numpy as np
import random

from ui import UI

class Location:
    def __init__(self, name, prep='in'):
        self.name = name
        self.neighbors = set()
        self.items = set()
        self.message = 'You are ' + prep + ' ' + self.name
    
    def add_neighbors(self, neighbors):
        for n in neighbors:
            self.neighbors.add(neighbors[n])
    
    def add_item(self, item):
        self.items.add(item)
    
    def remove_item(self, item):
        self.items.remove(item)
    
    def interact(self):
        UI.set_loc(self.message)
        actions = []
        options = ''
        i=0
        for loc in self.neighbors:
            i+=1
            actions.append(loc)
            options += '\n(' + str(i) + ') Enter ' + loc.name
        for item in self.items:
            i+=1
            actions.append(item)
            options += '\n(' + str(i) + ') ' + item.command + item.name
        
        def next(user_input: str, actions: list):
            action = None
            while True:
                try:
                    action = actions[int(user_input)-1]
                    break
                except:
                    user_input = input('Try again stupid\n')
            action.interact()

        UI.get_user_input(
            'Options:' + options.replace('\n', '\n  '),
            next,
            actions    
        )
                
    
    @staticmethod
    def connect(*locs):
        for loc0 in locs:
            for loc1 in locs:
                if loc0 != loc1:
                    loc0.add_neighbors({'loc':loc1})

class Item:
    loc = ''

    def __init__(self, name, loc, command = 'Check out ', interact = None, message = ''):
        self.name = name
        self.move(loc)
        self.command = command
        if interact:
            self.interact = interact
        self.message = message or 'This is ' + self.name
    
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
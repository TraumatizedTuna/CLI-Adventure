from utilities import *
from classes import *
from ui import *
from datetime import datetime
import random


def play():
    locs = {
        'living_room': Location('living room'),
        'bedroom': Location('bedroom'),
        'bathroom': Location('bathroom'),
        'kitchen': Location('kitchen'),
        'heaven': Location('heaven'),
        'hell': Location('hell')
    }

    hyperspace = Location('hyperspace')
    hyperspace.add_neighbors(locs)

    Location.connect(locs['bedroom'], locs['living_room'])
    Location.connect(locs['living_room'], locs['bathroom'])
    Location.connect(locs['living_room'], locs['kitchen'])

    def int_watch():
        UI.get_user_input(
            "It's " + datetime.now().strftime('%X'),
            lambda user_input, loc : loc.interact(),
            items['watch'].loc
        )
    
    def int_teleporter():
        def next0(user_input, loc):
            if user_input == password:
                def next1(user_input, loc):
                    if parse_user_bool(user_input):
                        if random.random() < .2:
                            if random.random() < .5: locs['heaven'].interact()
                            else: locs['hell'].interact()
                        else: hyperspace.interact()
                    else: loc.interact()
                
                UI.get_user_input(
                    'Proceed into hyperspace? (Probability of fatal error: 2E-1)',
                    next1,
                    loc
                )
            else:
                UI.get_user_input('Antimatter security system triggered.', lambda _ : locs['hell'].interact())
        UI.get_user_input(
            'Please enter password',
            next0,
            items['teleporter'].loc
        )

    def int_cat():
        def next(user_input, cat):
            loc = cat.loc
            cat.move_random()
            loc.interact()
        UI.get_user_input('Cat successfully petted.', next, items['cat'])

    def int_bob():
        def next0(user_input, bob):
            def talk_to_bob(name, bob, talk_to_bob):
                name = clean_str(name)
                if name:
                    #You have to be more creative than that
                    if name == 'bob':
                        UI.get_user_input('Bob: "Yeah, right. What\'s your name?"', talk_to_bob, bob, talk_to_bob)
                    
                    #Bob knows the password to the teleporter
                    elif ('password' in name or 'code' in name) and 'teleport' in name:
                        UI.get_user_input(
                            'Bob: "' + password + '"',
                            lambda user_input, loc : loc.interact(),
                            bob.loc
                        )
                    
                    #If your name is a palindrome Bob will be satisfied and leave you alone
                    elif name == name [::-1]:
                        def next1(user_input, bob):
                            loc = bob.loc
                            bob.move_random()
                            loc.interact()
                        UI.get_user_input('Bob: "Oh, cool, that\'s a palindrome, bye."', next1, bob)

                    #If it isn't you'll have to try harder
                    else:
                        def next1(user_input, bob):
                            #One in five risk that Bob dies
                            if random.random() < .2:
                                loc = bob.loc
                                bob.move(locs['hell'])
                                #Add a dead Bob
                                Item('corpse', loc, message='This used to be a happy linguist until he was brutally murdered')
                                UI.get_user_input(
                                    'Bob was killed by the non-palindromity of your name.',
                                    lambda user_input, loc : loc.interact(),
                                    loc
                                    )
                                loc.interact()
                            else:
                                UI.get_user_input('Bob: "What\'s your name?', talk_to_bob, bob, talk_to_bob)

                        UI.get_user_input('Bob: "That\'s not a palindrome though."', next1, bob)

                    
            UI.get_user_input('Bob: "What\'s your name?"', talk_to_bob, bob, talk_to_bob)
        UI.get_user_input('Bob: "Hey, my name is Bob, did you know that\'s a palindrome?"', next0, items['bob'])

    def int_god():
        def next0(user_input, god):
            def next1(user_input, god):
                if parse_user_bool(user_input):
                    god.interact()
                else:
                    god.loc.interact()

            UI.get_user_input('Keep talking to God?', next1, god)

        UI.get_user_input('', next0, items['god'])

    def int_chair():
        def next0(user_input, chair):
            def next1(user_input, chair):
                if parse_user_bool(user_input):
                    chair.interact()
                else:
                    chair.loc.interact()

            UI.get_user_input('Keep sitting on chair?', next1, chair)

        UI.get_user_input('You sit on chair.', next0, items['chair'])
    
    items = {
        'watch':        Item('watch',       locs['bedroom'],        'Watch ',   int_watch                   ),
        'teleporter':   Item('teleporter',  locs['bathroom'],       'Use ',     int_teleporter              ),
        'cat':          Item('cat',         locs['living_room'],    'Pet ',     int_cat                     ),
        'bob':          Item('Bob',         locs['living_room'],    'Talk to ', int_bob                     ),
        'god':          Item('God',         locs['heaven'],         'Talk to ', int_god                     ),
        'chair':        Item('chair',       locs['kitchen'],        'Sit on ',  int_chair                   ),
        'satan':        Item('Satan',       locs['hell'],           'Poke ',    message='Satan: "Ouch!"'    ),
        'alice':        Item('Alice',       locs['bathroom']),
        'cloud':        Item('cloud',       locs['heaven']),
        'demon':        Item('demon',       locs['hell'])
    }

    password = random.choice([
        'Ah, Satan sees Natasha',
        'Do geese see God?',
        'Go hang a salami, I\'m a lasagna hog',
        'May a moody baby doom a yam?',
        'Mr. Owl ate my metal worm',
        'Nurse, I spy gypsies, run!',
        'Oozy rat in a sanitary zoo',
        'Won\'t lovers revolt now?'
    ])

    locs['bedroom'].interact()

play()
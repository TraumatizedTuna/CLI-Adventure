from utilities import *
from classes import *
from ui import *
from datetime import datetime
import random


def play():

    locs = {
        'back_yard': Location('back yard'),
        'living_room': Location('living room'),
        'bedroom': Location('bedroom'),
        'bathroom': Location('bathroom'),
        'kitchen': Location('kitchen'),
        'heaven': Location('heaven'),
        'hell': Location('hell')
    }

    hyperspace = Location('hyperspace')
    hyperspace.add_neighbors(locs)

    Location.connect(locs['back_yard'], locs['living_room'])
    Location.connect(locs['bedroom'], locs['living_room'])
    Location.connect(locs['living_room'], locs['bathroom'])
    Location.connect(locs['living_room'], locs['kitchen'])


    # Interaction methodss for special items.
    # These will be passed into the Item constructor to override the defalt interactions method.
    def int_watch():
        UI.get_user_input(
            "It's " + datetime.now().strftime('%X'),
            lambda user_input, loc : loc.interact(),
            items['watch'].loc
        )
    
    def int_teleporter():
        def next0(user_input, loc):
            if user_input == password:
                err_prob = .2 if items['bike helmet'] in player_items else .8
                def next1(user_input, loc):
                    if parse_user_bool(user_input):
                        if random.random() < err_prob:
                            if random.random() < .5: locs['heaven'].interact()
                            else: locs['hell'].interact()
                        else: hyperspace.interact()
                    else: loc.interact()
                
                UI.get_user_input(
                    f'Proceed into hyperspace? (Probability of fatal error: {err_prob*10}E-1)',
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

    def talk_bob():
        def next0(user_input, bob: Animal):
            def check_password(user_input, bob: Animal):
                if ('password' in user_input or 'code' in user_input) and 'port' in user_input:
                    love = bob.get_total_player_love()
                    if love > 10:
                        msg = password
                    elif love > -10:
                        msg = 'I\'m sorry, that\'s a secret.'
                    else:
                        msg = 'I\'m not telling you the password because you suck!'
                    loc = bob.loc
                    bob.move_random()
                    UI.get_user_input(
                        'Bob: "' + msg + '"',
                        lambda user_input, loc : loc.interact(),
                        loc
                    )
                    return True
                return False

            if not check_password(clean_str(user_input), bob):
                if parse_user_bool(user_input, True, 'Bob: "Huh?"'):
                    bob.player_love['main'] += .1
                else:
                    bob.player_love['main'] -= .1
                def talk_to_bob(name, bob, talk_to_bob):
                    name = clean_str(name)
                    if name:
                        #You have to be more creative than that
                        if name == 'bob':
                            bob.player_love['main'] -= 1
                            UI.get_user_input('Bob: "Yeah, right. What\'s your name?"', talk_to_bob, bob, talk_to_bob)
                        
                        #Bob knows the password to the teleporter
                        elif check_password(name, bob):
                            pass
                        
                        #If your name is a palindrome Bob will be satisfied and leave you alone
                        elif name == name [::-1]:
                            #Bob will like you more now that he knows your name is a palindrome. Palindrome love can't exceed 1.
                            bob.player_love['pal'] = min(bob.player_love['pal'] + 10, 12)

                            def next1(user_input, bob):
                                loc = bob.loc
                                bob.move_random()
                                loc.interact()
                            UI.get_user_input('Bob: "Oh, cool, that\'s a palindrome, bye."', next1, bob)

                        #If it isn't you'll have to try harder
                        else:
                            #Bob will like you less
                            bob.player_love['pal'] -= 20
                            bob.player_love['main'] -= 3

                            def next1(user_input, bob):
                                #One in five risk that Bob dies
                                if random.random() < .2:
                                    bob.player_love['main'] -= 10
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
                    else:
                        bob.player_love['main'] -= 1
                        UI.get_user_input('Bob: "Come on, just tell me your name!"', talk_to_bob, bob, talk_to_bob)

                UI.get_user_input('Bob: "What\'s your name?"', talk_to_bob, bob, talk_to_bob)
        UI.get_user_input('Bob: "Hey, my name is Bob, did you know that\'s a palindrome?"', next0, items['bob'])

    def gift_react_bob(bob, i: Item):

        if all(map(lambda x : x in bob.items, [items['pot'], items['stop_sign']])) and i in [items['pot'], items['stop_sign']]:
            msg = 'Bob: "Yay! Such a beautiful new specimen for my collection of stop pots! I am eternally grateful!"'
            bob.player_love['main'] += 20
        else:
            msg = 'Bob: "What am I supposed to do with ' + i.name + '?"'

        UI.get_user_input(
            msg,
            lambda user_input, loc : loc.interact(),
            bob.loc
        )

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

    def int_satan():
        satan = items['satan']
        if satan.patience > 0:
            satan.patience -= 1
            UI.get_user_input(
                'Satan: "Ouch!"',
                lambda user_input, loc : loc.interact(),
                satan.loc
            )
        else:
            satan.patience = random.random()*4+4
            not_hell = locs.copy()
            not_hell.pop('hell')
            not_hell = list(not_hell.values())
            not_hell.append(hyperspace)
            loc = random.choice(not_hell)
            UI.get_user_input(
                'Satan: "Alright, that\'s enough! I\'m sending you to ' + loc.name + ', pathetic mortal!"',
                lambda user_input, loc : loc.interact(),
                loc
            )

    items = {
        'watch':        Item('watch',       locs['bedroom'],        'Watch ',   int_watch       ),
        'teleporter':   Item('teleporter',  locs['bathroom'],       'Use ',     int_teleporter  ),
        'cat':          Item('cat',         locs['living_room'],    'Pet ',     int_cat         ),
        'bob':          Animal('Bob',       locs['living_room'],    '',         player_love = {'main': 0, 'pal': 0}, talk=talk_bob, gift_react=gift_react_bob),
        'god':          Item('God',         locs['heaven'],         'Talk to ', int_god         ),
        'chair':        Item('chair',       locs['kitchen'],        'Sit on ',  int_chair       ),
        'bike helmet':  Item('bike helmet', locs['kitchen'],        'Put on ',  pickupable=True, pick_up_msg='You wear helmet.'),
        'stop_sign':    Item('stop sign',   locs['back_yard'],      'Steal ',   pickupable=True),
        'pot':          Item('flower pot',  locs['kitchen'],                    pickupable=True),
        'satan':        Item('Satan',       locs['hell'],           'Poke ',    int_satan,  attr={'patience': random.random()*4+4}),
        'alice':        Item('Alice',       locs['back_yard']),
        'cloud':        Item('cloud',       locs['heaven']),
        'demon':        Item('demon',       locs['hell'])
    }

    # Set the password to teleporter to a random palindrome.
    # This way, the player can't reuse the password from a previous session.
    password = random.choice([
        'Ah, Satan sees Natasha',
        'Do geese see God?',
        'Go hang a salami, I\'m a lasagna hog',
        'May a moody baby doom a yam?',
        'Mr. Owl ate my metal worm',
        'Oozy rat in a sanitary zoo',
        'Won\'t lovers revolt now?'
    ])

    # Start the game in bedroom
    locs['bedroom'].interact()

play()
from math import comb
from printers import *
from rumi_api import *
import os
from itertools import cycle
import colorama

# get data how many players will be playing


def player_count_loop():
    while True:
        player_count_input = input('How many players? 1-6 values only\n')
        player_count = 0
        try:
            player_count = int(player_count_input)
        except Exception:
            pass

        if(player_count < 1 or player_count > 6):
            print('incorrect. 1-6 please.')
        else:
            return player_count


def get_player_list(player_count):
    player_list = []
    for player_num in range(0, player_count):
        name = input(f'Player {player_num+1}, enter your name.\n')
        player = Player(name)
        player.take_starters(deck)
        player_list.append(player)
    return player_list

# infinite cycle of players' turns
# def players_iterate_loop(deck, player_list):
#     player_cycle = cycle(player_list)

#     for current_player in player_cycle:
#         _prepare_next_player_terminal(current_player)
#         player_command_loop(deck, current_player)
        

def players_iterate_loop_2(deck, player_list):
    idx = 0
    while True:
        if idx >= len(player_list):
            idx = 0

        current_player = player_list[idx]
        
        _prepare_next_player_terminal(current_player)
        print(f'DEBUG--> idx beginning: {idx}')
        current_player.turn_over = False
        print(f'DEBUG--> curr_pl turn_over: {current_player.name}:{current_player.turn_over}')
        
        while not current_player.turn_over:
            player_command_loop(deck, current_player)

        idx += 1 

def _prepare_next_player_terminal(current_player: Player):
        # clear terminal output
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{current_player.name}, it\'s your turn!\n')

        #for colorful output
        colorama.init()
        global table
        print_pretty_table(table)
        print_pretty_own(current_player.tiles)


def player_command_loop(deck, player):
    global table
    # print_commands()
    flag = True
    while flag:
        player_input = input(
            "What will you do? (write command + [Enter] to confirm).\n").split(':')

        #Command is followed by ':' symbol. Input_vars can be a list, as each subcommand is also followed by ':'.
        cmd = player_input.pop(0).capitalize()
        input_vars = []
        for inp in player_input:
            input_vars.append(inp.strip())

        if cmd == 'Q':
            #finish command loop. Outer loop changes player to the next one
            player.turn_over = True
            flag = False
        if cmd == 'T':
            #take random and finish command loop √
            player.take_random(deck)
            player.turn_over = True
            flag = False
        if cmd == 'E' and len(input_vars) ==  1:
            #Enter the game with combos that have 30+ in value, finish command loop √
            enter_table(input_vars[0], player)
            player.turn_over = True
            flag = False
        if cmd == 'C' and len(input_vars) == 1:
            #create a new combination, without ending your turn TODO print ADDED TO THE TABLE
            create_combination(input_vars[0], player)
        # TODO NEXT add/remove tile to existing (A: | R:)
        if cmd == 'T' and len(input_vars) == 2:
            pass


def enter_table(user_input, player: Player):
    global table
    combination_id_list = user_input.split('|')
    print(f'DEBUG--> combination_id_list:{combination_id_list}')
    combination_list = []

    for combo_str in combination_id_list:
        combination_list.append(_parse_combo_string(combo_str, player))

    for combo in combination_list:
        print(f'DEBUG--> combo:{combo}')
    player.enter_game(combination_list)

    if player.is_out:
        for combo in combination_list:
            table.append(combo)


def create_combination(user_input, player: Player):
    global table
    if player.is_out:
        table.append(_parse_combo_string(user_input, player))


def _parse_combo_string(combo_string: str, player: Player) -> Combination:
    tile_list = []
    tile_id_list = combo_string.split(' ')
    print(f'DEBUG--> tile_id_list: {tile_id_list}')

    for tile_id in tile_id_list:
        tile_list.append(player.take_from_own_list(tile_id))
    return _create_combo(player,tile_list)


def _create_combo(player: Player, tile_list: List[Tile]):
    try:
        combo = Combination(tile_list)
        return combo
    except ValueError as ve:
        for tile in tile_list:
            player.return_to_own_list(tile)
        print(str(ve))

flag = True
# game loop
while(flag):
    # global deck state is not messing up for now I think
    global table

    deck = init_deck()
    table = []

    # gather game start information
    player_count = player_count_loop()
    player_list = get_player_list(player_count)

    # starting point
    # print_game_status(deck, player_list, table)
    players_iterate_loop_2(deck, player_list)

    # kill game loop for now
    flag = False

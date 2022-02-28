from math import comb
from printers import *
from rumi_api import *
import os
import sys
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


def players_iterate_loop(deck, player_list):
    idx = 0
    while True:

        if idx >= len(player_list):
            idx = 0

        current_player = player_list[idx]
        _prepare_next_player_terminal(current_player)
        current_player.turn_over = False
        while not current_player.turn_over:
            player_command_loop(deck, current_player)

        idx += 1


def _clean_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def _print_default_view(current_player:Player):
    global table
    print_pretty_comb_list(table)
    print_pretty_own(current_player.tiles)


def _prepare_next_player_terminal(current_player: Player):
    _clean_terminal()
    print(f'{current_player.name}, it\'s your turn!\n')
    # for colorful output
    colorama.init()
    _print_default_view(current_player)


def player_command_loop(deck, player):
    global table
    turn_not_over = True
    while turn_not_over:
        cmd, input_vars = _get_cmd_input()
        # parse game commands, return bool about if the cmd_loop shoud be killed
        turn_not_over = _handle_game_commands(
            cmd, player, turn_not_over, input_vars)
        # if no game ending command was given, check util commands
        if turn_not_over:
            turn_not_over = _handle_misc_commands(cmd, player, turn_not_over)


def _get_cmd_input():
    inp = input(
        "What will you do? (write command + [Enter] to confirm). 'H' for help.\n").split(':')

    # Command is followed by ':' symbol. Input_vars can be a list, as each subcommand is also followed by ':'.
    cmd = inp.pop(0).upper()
    input_vars = []
    for inp in inp:
        input_vars.append(inp.strip())
    return cmd, input_vars


def enter_table(user_input, player: Player):
    global table
    combination_id_list = user_input.split('|')
    combination_list = []

    for combo_str in combination_id_list:
        combo_str = combo_str.strip()
        combination_list.append(_parse_combo_string(combo_str.strip(), player))

    for combo in combination_list:
        player.enter_game(combination_list)

    if player.is_out:
        for combo in combination_list:
            table.append(combo)


def create_combination(user_input, player: Player):
    global table
    if player.is_out:
        table.append(_parse_combo_string(user_input, player))
        _clean_terminal()
        _print_default_view(player)
        print('Added!')


def _parse_combo_string(combo_string: str, player: Player) -> Combination:
    tile_list = []
    tile_id_list = combo_string.split(' ')

    for tile_id in tile_id_list:
        tile_list.append(player.take_from_own_list(tile_id))
    return _create_combo(player, tile_list)


def _create_combo(player: Player, tile_list: List[Tile]):
    try:
        combo = Combination(tile_list)
        return combo
    except ValueError as ve:
        for tile in tile_list:
            player.return_to_own_list(tile)
        print(str(ve))


def _handle_game_commands(cmd, player, turn_not_over, input_vars):
    if cmd == 'T':
        # take random and finish command loop √
        player.take_random(deck)
        player.turn_over = True
        turn_not_over = False
    if cmd == 'E' and len(input_vars) == 1:
        # Enter the game with combos that have 30+ in value, finish command loop √
        enter_table(input_vars[0], player)
        player.turn_over = True
        turn_not_over = False
    if cmd == 'C' and len(input_vars) == 1:
        # create a new combination, without ending your turn
        create_combination(input_vars[0], player)
    # TODO NEXT add/remove tile to existing (A: | R:)
    if cmd == 'T' and len(input_vars) == 2:
        pass

    return turn_not_over


def _handle_misc_commands(cmd, player, turn_not_over):
    if cmd == 'Q':
        # finish command loop. Outer loop changes player to the next one
        player.turn_over = True
        turn_not_over = False
    if cmd == 'H':
        print_commands()
    if cmd == 'QUIT':
        sys.exit('Quitted..')
    if cmd == 'CLEAR':
        _clean_terminal()
        _print_default_view(player)

    return turn_not_over


is_game_played = True
# game loop (todo add kill to the loop when game won)
while(is_game_played):
    # global deck state is not messing up for now I think
    global table

    deck = init_deck()
    table = []

    # gather game start information
    player_count = player_count_loop()
    player_list = get_player_list(player_count)

    # starting point
    players_iterate_loop(deck, player_list)

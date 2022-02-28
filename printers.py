from typing import List
from rumi_api import *
import colorama


# simple data without pretty formatting
def print_game_status(deck, player_list, table):
    print('DECK\n')
    print(len(deck))

    for player in player_list:
        print('\n')
        print(player)

    print('TABLE')
    print(table)

# format terminal output for more clear visibility
def print_pretty_comb_list(table: List[Combination]):
    print('Currently on the table:')
    for combination in table:
        print(f'ID: {combination.comb_id}')
        _print_pretty_list(combination.tile_list, with_id=False)
        print()
    print('_________________')

# format own tiles for a player to choose from
def print_pretty_own(tile_list):
    print('Your deck:')
    if len(tile_list) > 15:
        _print_pretty_list(tile_list[:15])
        _print_pretty_list(tile_list[15:])
    else:
        _print_pretty_list(tile_list)


def _print_pretty_list(tile_list, with_id=True):
    bld_str = 'Val:'
    id_bld_str = 'ID: '
    for tile in tile_list:
        tile_str, id_str = _build_pretty_with_id(tile)
        id_bld_str += id_str
        bld_str += tile_str
    print(bld_str, colorama.Style.RESET_ALL)

    if with_id:
        print(id_bld_str, colorama.Style.RESET_ALL)


def _build_pretty_with_id(tile: Tile):
    full_str = colorama.Style.RESET_ALL + " | "
    id_str = " | "
    tile_str = ''
    tile_id_str = ''
    tile_str = _build_color_str(tile)
    tile_str, tile_id_str = pad_nums(tile, tile_str)

    full_str = full_str + tile_str + colorama.Style.RESET_ALL + " | "
    id_str = id_str + tile_id_str + colorama.Style.RESET_ALL + " | "
    return full_str, id_str


def _build_color_str(tile):
    if tile.color == Color.RED:
        tile_str = colorama.Fore.RED
    if tile.color == Color.BLACK:
        tile_str = colorama.Back.WHITE + colorama.Fore.BLACK
    if tile.color == Color.BLUE:
        tile_str = colorama.Fore.BLUE
    if tile.color == Color.YELLOW:
        tile_str = colorama.Fore.YELLOW
    return tile_str


# if len(id) != len(val), append with space
# | 4 |  --> |  4  |, | 1 | ---> |  1  |
# | 12 | --> | 12  |, | 103 | -> | 103 |
def pad_nums(tile: Tile, tile_str: str):
    id_str = ''
    val_len = len(str(tile.number))
    id_len = len(str(tile.tile_id))

    # id 12 val 12
    if id_len == val_len:
        tile_str += str(tile.number)
        id_str += str(tile.tile_id)
    # id: 123 val: 1
    elif id_len - val_len == 2:
        tile_str += f" {tile.number} "
        id_str += str(tile.tile_id)
    # id 123 val 12 or id 12 val 1
    elif id_len - val_len == 1:
        tile_str += f" {tile.number} "
        id_str += f"{tile.tile_id} "
    # id 1 val 12, no other options (id 0:105, val 1:13)
    else:
        tile_str += str(tile.number)
        id_str += f"{tile.tile_id} "

    return tile_str, id_str


def print_commands():
    print('\nCommands:')
    print('[Q:] Done with moves. Next player                           [T:] Take from the deck. Next player ')
    print('[S: ID ID] Split combination AFTER tile ID                  [T: ID R ID] Remove tile from combination')
    print('[C: ID ID..] Create combination from tiles in given order')
    print('[E: ID ID.. | ID ID ..] Enter with combinations from tiles in given order')
    print('[T: ID A ID h/t] Add tile to combination (head/tail)')
    print()

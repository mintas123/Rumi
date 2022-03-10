from typing import List
import colorama

from rumi_api import Color, Combination, Tile

"""
Collection of helper methods that format data
 for better visibility in the terminal
"""

# simple data without pretty formatting


def print_game_status(deck, player_list, table):
    print('DECK\n')
    print(len(deck))

    for player in player_list:
        print('\n')
        print(player)

    print('TABLE')
    print(table)


def print_pretty_comb_list(table: List[Combination], is_compact= False):
    '''
    Print to the CLI all provided combinations, each in its own row with ID
    '''

    if is_compact:
        for combination in table:
            print_pretty_list(combination.tile_list, with_id_row= False, comb_id= combination.comb_id)
            print()
    else:
        print('Currently on the table:')
        for combination in table:
            print(f'ID: {combination.comb_id}')
            print_pretty_list(combination.tile_list, with_id_row= False)
            print()
        print('_________________')


def print_pretty_own(tile_list: List[Tile], is_compact = False):
    '''
    Print to the CLI all provided tiles, split into two rows if over 15 elements
    '''

    if not is_compact: print('Your deck:')

    if len(tile_list) > 15:
        print_pretty_list(tile_list[:15])
        print_pretty_list(tile_list[15:])
    else:
        print_pretty_list(tile_list)


def print_pretty_list(tile_list: List[Tile], with_id_row=True, comb_id=None):
    '''
    Print to the CLI full row of tiles with applied formatting

    Input: 
    tile_list - List[Tile], obejcts to be properly displayed
    with_id - boolean, should the row with ID numbers be displayed
    comb_id - int, the combination ID to be displayed (optional)
    '''

    bld_str = ''
    if comb_id is not None:
        bld_str += f'C_ID: {comb_id} --> '

    bld_str += 'Val:'
    id_bld_str = 'ID: '
    for tile in tile_list:
        tile_str, id_str = _build_pretty_with_id(tile)
        id_bld_str += id_str
        bld_str += tile_str
    print(bld_str, colorama.Style.RESET_ALL)

    if with_id_row:
        print(id_bld_str, colorama.Style.RESET_ALL)


def _build_pretty_with_id(tile: Tile):
    """
    Return Tile information with the visual help,
    to be better displayed in the CLI. 

    Input:
    tile - Tile object

    Output:
    full_str - properly formatted string with information about tile color and number
    id_str - properly formatted string with tile ID number

    Example:
    Tile(id=34,num=12)
    full_str: |12| (with colorama.Style applied)
    id_str:  |34| 
    """

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
    """
    Return string with initialized styled formatting of the CLI
    that fits the tile color
    """

    if tile.color == Color.RED:
        tile_str = colorama.Fore.RED
    if tile.color == Color.BLACK:
        tile_str = colorama.Back.WHITE + colorama.Fore.BLACK
    if tile.color == Color.BLUE:
        tile_str = colorama.Fore.BLUE
    if tile.color == Color.YELLOW:
        tile_str = colorama.Fore.YELLOW
    return tile_str


def pad_nums(tile: Tile, tile_str: str):
    """
    Method that appends given string with properly formatted data from tile.
    Because of displaying both number and id, padding is applied to make
    the displayed in the CLI

    Input:
    tile - object with data to be properly displayed 
    tile_str - string to append the data with

    Output:
    tile_str - string with number
    id_str - string with id

    Example:
         Tile(id=12,num=4)  ;  Tile(id=103,num=1)
    NUM: | 4 |  --> |  4  | ; | 1 | ---> |  1  |
    ID:  | 12 | --> | 12  | ; | 103 | -> | 103 |
    """

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
    print('[Q:] Done with moves. Next player')
    print('[G:] Grab from the deck. Next player')
    print('[quit] Turn off the game.')
    print('[clear] Clear the user input')
    print('[sort] Sort your hand')
    print('[toggle] Toggle compact view')
    # print('[S: ID ID] Split combination AFTER tile ID') todo 
    print('[C: ID ID..] Create combination from tiles in given order')
    print('[E: ID ID.. | ID ID ..] Enter with combinations from tiles in given order')
    print('[T: ID_C | A ID_T h/t] Add tile to combination (head/tail)')
    # print('[T: ID_C | R ID_T] Take tile from combination (head/tail)') todo
    print()

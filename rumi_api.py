from copy import deepcopy
from enum import Enum
from ordered_enum import OrderedEnum
import random


class Color(OrderedEnum):
    RED = 1
    BLUE = 2
    BLACK = 3
    YELLOW = 4


class Tile():
    """
    Base of the Rummikub game. 
    Tile has number in color, which allow forming combinations and winning the game.
    Input:
    number - number of the tile. In range 1-13
    color - color of the tile, one of Enum Color values
    is_fake - boolean, default False. If True, its a temporary facade for a Joker tile

    Adidional parameters:
    id - identifier of the tile, used for table and combination manipulations
    """
    _static_id_counter = 0

    def __init__(self, number: int, color: Color, is_fake=False):
        if(number > 13) or (number < 1):
            raise ValueError("Only 1-13 numbers ")

        self.number = number
        self.color = color

        # Jokers have Tile atribute, no need to add ID's to temp tiles
        if not is_fake:
            self.tile_id = Tile._static_id_counter
            Tile._static_id_counter += 1

    def __str__(self):
        return f'Tile#{self.tile_id}({self.color}___Value:{self.number})'

    def __repr__(self):
        return str(self)


class Joker():
    _static_id_counter = 105  # 104 regular tiles

    def __init__(self, tile: Tile = None):
        if Joker._static_id_counter > 106:
            raise ValueError('Only two Jokers')
        self.tile_id = Joker._static_id_counter
        # TODO handle Jokers
        self.fake_tile = tile
        self.number = 'X'  # just for display
        if self.tile_id == 105:
            self.color = Color.BLACK
        else:
            self.color = Color.RED
        Joker._static_id_counter += 1

    def __str__(self):
        return f'JOKER#{self.tile_id}(As:{self.fake_tile})'


class Mode(Enum):
    COLORS = 1
    NUMBERS = 2


class Combination():
    _static_id_counter = 0

    def __init__(self, tile_list: list[Tile]):
        self.tile_list = tile_list
        self.comb_id = Combination._static_id_counter
        self.mode = get_combo_mode(tile_list)
        Combination._static_id_counter += 1

    def add_tile(self, tile: Tile, is_head=False):
        temp_tile_list = self.tile_list
        if is_head:
            temp_tile_list.insert(0, tile)
        else:
            temp_tile_list.append(tile)

        # verify if the combination is correct
        _ = get_combo_mode(temp_tile_list)
        self.tile_list = temp_tile_list

    # chaos mode to be able to skip validation in order to do a mess on the table

    def remove_tile(self, tile: Tile, is_chaos_mode=False):
        self.tile_list.remove(tile)

        # Until switched off, verify if whats left if correct.
        if not is_chaos_mode:
            _ = get_combo_mode(self.tile_list)

    def get_score(self, is_start=False):
        score = 0
        for tile in self.tile_list:
            if tile.number != 'X':
                score += tile.number
            elif(is_start):
                print('Cannot use Joker for entering.')
                return 0
        return score


class Player():
    def __init__(self, name):
        self.name = name
        # TODO change to dictionary!!!
        self.tiles = []
        self.is_out = False
        self.turn_over = False
        self.moved_this_turn = False

    def __str__(self):
        return f'Player(\nName:{self.name}\nTiles:(\n' + "\n".join([str(x) for x in self.tiles]) + '\n)'

    def take_starters(self, deck):
        '''
        At the beggining of the game, each player takes 14 tiles from the deck.
        '''

        if len(self.tiles) > 0:
            raise ValueError('Cant take initial pieces when pieces in hand')
        for _ in range(0, 14):
            self.take_random(deck)

    # take from the bag random piece when you have nothing to add
    def take_random(self, deck):
        '''
        Each round player can surrender and take a piece, if he has no possible actions.
        '''
        if len(deck) > 0:
            self.tiles.append(deck.pop(random.randint(0, len(deck)-1)))
        else:
            print('No more tiles left in the deck')

    def create_combination(self, user_input: str, table):
        '''
        Parse and add given combination to the table, by taking the tiles from player.tile_list.
        Return boolean is performed.
        '''

        if self.is_out:
            try:
                table.append(parse_combo_string(user_input, self))
                self.moved_this_turn = True
                return True
            except ValueError:
                return False

        else:
            return False

    def modify_combination(self, user_input: str, table: list[Combination]):
        '''
        Parse the input to add or remove a tile from the combination with given ID
        Return boolean is performed
        '''

        if not self.is_out:
            return False

        input_list = user_input.split('|')
        comb_id = int(input_list[0].strip())
        comb = get_combination_from_list(table, comb_id)
        tile_input = input_list[1].strip()
        # example: "T: 3 | A 76 t" <- add tile_id=76 to combiantion_id=3 at tail
        tile_cmds = tile_input.split(' ')
        tile, self.tiles = pop_tile_from_list(self.tiles, tile_cmds[1])

        if tile_cmds[0] == 'A' and len(tile_cmds) == 3:
            return self._add_tile_to_comb(tile_cmds, tile, comb)

        if tile_cmds[0] == 'R':
            return self._remove_tile_from_comb(tile, comb, table)

        return False

    def _add_tile_to_comb(self, tile_cmds: list[str], tile: Tile, comb: Combination):
        is_head = tile_cmds[2].upper == 'H'
        try:
            comb.add_tile(tile, is_head)
            return True
        except ValueError:
            # rollback
            comb.remove_tile(tile)
            return False

    def _remove_tile_from_comb(self, tile: Tile, comb: Combination, table: list[Combination]):
        # creating a copy of an object to not care about restoring the state after modification
        comb_snapshot = deepcopy(comb)
        try:
            comb.remove_tile(tile)
            self.tiles.append(tile)
            return True
        except ValueError:
            table.remove(comb)
            table.append(comb_snapshot)

    def split_combination(self, combination, is_chaos_mode=False):
        pass

    # when you want to destroy the whole table but have to end up with correct table setup
    # some flag that disables validation, after toggle off validate all combos on the table
    def toggle_chaos_mode(self, *dgsgds):
        pass

    # reaarange tiles by color and number. Jokers at the end.
    def sort_tiles(self):
        found = [x for x in self.tiles if x.number == 'X']
        print(found)
        for joker in found:
            self.tiles.remove(joker)
        self.tiles = sorted(self.tiles, key=lambda x: (x.color, x.number))
        self.tiles.extend(found)

    def enter_game(self, combination_list: list[Combination]):
        if (self.is_out):
            print('Already in the game - no need to enter.')
            return

        score = 0
        for combination in combination_list:
            score += combination.get_score(is_start=True)

        if score < 30:
            print(
                f'Sorry, not enough points:{score}/30. Take one and try again next turn.')
        else:
            self.is_out = True
            print(f'Nice one! {score} on the table.')


def get_combo_mode(tile_list: list[Tile]):
    try:
        _verify_number_sequence(tile_list)
        return Mode.NUMBERS
    except ValueError:
        try:
            _verify_number_set(tile_list)
            return Mode.COLORS
        except ValueError:
            raise ValueError('Given list is neither a set or a sequence')


def _verify_length(tile_list: list[Tile]):
    if len(tile_list) < 3:
        raise ValueError('Combination too short')


def _verify_number_set(tile_list: list[Tile]):
    # if I dont create copy here Python fucks with my (Combination) self.tile_list and modifies it
    local_tile_list = deepcopy(tile_list)
    _verify_length(local_tile_list)
    first = local_tile_list.pop(0)
    col_set = set()
    col_set.add(first.color)
    val = first.number
    # number set has to contain distinct colors and same number
    for tile in local_tile_list:
        if(tile.color in col_set or tile.number is not val):
            raise ValueError("Incorrect set")
        col_set.add(tile.color)


def _verify_number_sequence(tile_list: list[Tile]):
    # if I dont create copy here Python fucks with my (Combination) self.tile_list and modifies it
    local_tile_list = deepcopy(tile_list)
    _verify_length(local_tile_list)
    first = local_tile_list.pop(0)
    col = first.color
    val = first.number
    sequence = val

    # number set has to contain same colors and sequential numbers
    for tile in local_tile_list:
        if(tile.number > first.number):
            sequence += 1
        elif(tile.number < first.number):
            sequence -= 1
        else:
            raise ValueError("Incorrect sequence")

        if(col is not tile.color or sequence is not tile.number):
            raise ValueError("Incorrect sequence")


def init_deck():
    deck = []
    for color in Color:
        for x in range(1, 14):
            deck.append(Tile(x, color))
            deck.append(Tile(x, color))

    deck.append(Joker())
    deck.append(Joker())
    return deck


def parse_combo_string(combo_string: str, player: Player) -> Combination:
    tile_list = []
    tile_id_list = combo_string.split(' ')

    for tile_id in tile_id_list:
        tile, player.tiles = pop_tile_from_list(player.tiles, tile_id)
        tile_list.append(tile)
    return create_combo(player, tile_list)


def create_combo(player: Player, tile_list: list[Tile]):
    try:
        combo = Combination(tile_list)
        return combo
    except ValueError:
        # if invalid combinaiton, restore the state before creating combination, throw it further.
        for tile in tile_list:
            add_to_list(player.tiles, tile)
        raise ValueError('Invalid combination')


def pop_tile_from_list(tile_list: list[Tile], tile_id):
    found = next(x for x in tile_list if x.tile_id == int(tile_id))
    tile_list = [x for x in tile_list if x.tile_id != int(tile_id)]
    return found, tile_list


# rollback in case of incorrect combination
def add_to_list(tile_list, tile: Tile):
    tile_list.append(tile)


def get_combination_from_list(combination_list: list[Combination], comb_id) -> Combination:
    return next(x for x in combination_list if x.comb_id == int(comb_id))

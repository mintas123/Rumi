from enum import Enum
import random
from traceback import print_tb


class Color(Enum):
    RED = 1
    BLUE = 2
    BLACK = 3
    YELLOW = 4


class Tile():
    _static_id_counter = 0

    def __init__(self, number, color, is_fake=False):
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


class Joker():
    _static_id_counter = 105  # 104 regular tiles

    def __init__(self, tile: Tile = None):
        if Joker._static_id_counter > 106:
            raise ValueError('Only two Jokers')
        self.tile_id = Joker._static_id_counter
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

    def __init__(self, tile_list):
        if(len(tile_list) < 3):
            raise ValueError("Must contain at least 3 tiles")

        self.tile_list = tile_list
        self.comb_id = Combination._static_id_counter
        self.mode = get_combo_mode(tile_list)
        Combination._static_id_counter += 1

    def add_tile(self, tile: Tile, is_chaos_mode=False):
        pass

    def remove_tile(self, tile: Tile, is_chaos_mode=False):
        pass

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
        #TODO change to dictionary!!!
        self.tiles = []
        self.is_out = False
        self.turn_over = False

    def __str__(self):
        return f'Player(\nName:{self.name}\nTiles:(\n' + "\n".join([str(x) for x in self.tiles]) + '\n)'

    # take first 14 tiles
    def take_starters(self, deck):
        if len(self.tiles) > 0:
            raise ValueError('Cant take initial pieces when pieces in hand')
        for _ in range(0, 14):
            self.take_random(deck)

    # take from the bag random piece when you have nothing to add
    def take_random(self, deck):
        if len(deck) > 0:
            self.tiles.append(deck.pop(random.randint(0, len(deck)-1)))

    def take_from_own_list(self, tile_id) -> Tile:
        found = next(x for x in self.tiles if x.tile_id == int(tile_id))
        self.tiles = [x for x in self.tiles if x.tile_id != int(tile_id)]
        return found

    # rollback in case of incorrect combination
    def return_to_own_list(self, tile: Tile):
        self.tiles.append(tile)


    def place_new_combination(self, tiles):
        pass

    def add_to_combination(self, tiles, combination):
        pass

    def split_combination(self, combination, is_chaos_mode=False):
        pass

    # when you want to destroy the whole table but have to end up with correct table setup
    # some flag that disables validation, after toggle off validate all combos on the table
    def toggle_chaos_mode(self, *dgsgds):
        pass

    #reaarange tiles
    def shake(self):
        pass

    def mark_turn_over(self):
        pass

    def enter_game(self, combination_list):
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


def get_combo_mode(tile_list):
    #if I dont create copy here Python fucks with my (Combination) self.tile_list and modifies it
    local_tile_list = []
    local_tile_list.extend(tile_list)
    try:
        _verify_number_sequence(local_tile_list)
        return Mode.NUMBERS
    except ValueError:
        try:
            _verify_number_set(local_tile_list)
            return Mode.COLORS
        except ValueError:
            raise ValueError('Given list is neither a set or a sequence')


def _verify_number_set(tile_list):
    first = tile_list.pop(0)

    col = first.color
    val = first.number
    # number set has to contain distinct colors and same number
    for tile in tile_list:
        if(col == tile.color or val is not tile.number):
            raise ValueError("Incorrect set")


def _verify_number_sequence(tile_list):
    # tile_list.sort(key=lambda x: x.number, reverse=True)
    first = tile_list.pop(0)
    col = first.color
    val = first.number
    sequence = val

    # number set has to contain same colors and sequential numbers
    for tile in tile_list:
        if(tile.number > first.number):
            sequence += 1
        else:
            sequence -= 1

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

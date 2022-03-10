import unittest

from rumi_api import Color, Mode, Tile, get_combo_mode

class TestValidity(unittest.TestCase):

    #sequence
    def test_seq_correct(self):
        tile_list = [Tile(7,Color.RED),Tile(8,Color.RED),Tile(9,Color.RED)]
        self.assertEqual(get_combo_mode(tile_list), Mode.NUMBERS)

    def test_seq_incorrect_color(self):
        tile_list = [Tile(7,Color.RED),Tile(8,Color.RED),Tile(9,Color.BLACK)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)

    def test_seq_incorrect_number(self):
        tile_list = [Tile(7,Color.RED),Tile(8,Color.RED),Tile(10,Color.RED)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)

    def test_seq_random(self):
        tile_list = [Tile(3,Color.RED),Tile(8,Color.BLACK),Tile(11,Color.YELLOW)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)
    
    #set
    def test_set_correct(self):
        tile_list = [Tile(7,Color.RED),Tile(7,Color.BLACK),Tile(7,Color.BLUE)]
        self.assertEqual(get_combo_mode(tile_list), Mode.COLORS)

    def test_set_incorrect_color(self):
        tile_list = [Tile(7,Color.RED),Tile(7,Color.RED),Tile(7,Color.YELLOW)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)

    def test_set_incorrect_color(self):
        tile_list = [Tile(7,Color.RED),Tile(7,Color.BLACK),Tile(7,Color.YELLOW),Tile(7,Color.YELLOW)]
        with self.assertRaises(ValueError):
           get_combo_mode(tile_list)

    def test_set_incorrect_number(self):
        tile_list = [Tile(7,Color.RED),Tile(7,Color.RED),Tile(9,Color.YELLOW)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)

    def test_set_random(self):
        tile_list = [Tile(7,Color.RED),Tile(4,Color.RED),Tile(7,Color.BLACK)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)

    #length
    def test_too_short(self):
        tile_list = [Tile(7,Color.RED),Tile(4,Color.RED)]
        with self.assertRaises(ValueError):
            get_combo_mode(tile_list)


if __name__ == '__main__':
    unittest.main()
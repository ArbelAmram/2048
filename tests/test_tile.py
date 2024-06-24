import unittest
# import pygame
from core.tile import Tile

class TestTile(unittest.TestCase):
    
    def setUp(self):
        self.tile = Tile(2, 0, 0, 100, 100)

    def test_initial_position(self):
        """Test if the tile is initialized at the correct position."""
        self.assertEqual(self.tile.row, 0, "Initial row should be 0.")
        self.assertEqual(self.tile.col, 0, "Initial column should be 0.")
        self.assertEqual(self.tile.x, 0, "Initial x position should be 0.")
        self.assertEqual(self.tile.y, 0, "Initial y position should be 0.")
        
    def test_get_color(self):
        """Test if the tile gets the correct color."""
        self.assertEqual(self.tile.get_color(), (237, 229, 218), "Color for tile value 2 should be (237, 229, 218).")

    def test_move(self):
        """Test if the tile moves correctly."""
        self.tile.move((100, 100))
        self.assertEqual(self.tile.x, 100, "Tile x position should be 100 after moving right by 100.")
        self.assertEqual(self.tile.y, 100, "Tile y position should be 100 after moving down by 100.")
        
    def test_set_pos(self):
        """Test if the tile sets its position correctly."""
        self.tile.move((100, 100))
        self.tile.update_position()
        self.assertEqual(self.tile.row, 1, "Tile row should be 1 after moving down by 100.")
        self.assertEqual(self.tile.col, 1, "Tile column should be 1 after moving right by 100.")

if __name__ == '__main__':
    unittest.main()

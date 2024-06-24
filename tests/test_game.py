import unittest
import pygame
from core.game import Game

class TestGame(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        self.window = pygame.Surface((800, 800))
        self.game = Game(self.window)

    def test_initial_tiles(self):
        """Test if the initial number of tiles is correct."""
        self.assertEqual(len(self.game.tiles_dict), 2, "There should be exactly 2 initial tiles.")

    def test_random_pos(self):
        """Test if the random position is within bounds and not already taken."""
        row, col = self.game.get_random_position()
        self.assertTrue(0 <= row < 4, "Row should be within valid range.")
        self.assertTrue(0 <= col < 4, "Column should be within valid range.")
        self.assertNotIn(f"{row}{col}", self.game.tiles_dict, "Random position should not be already occupied.")

    def test_can_move(self):
        """Test if the game can detect available moves."""
        self.assertTrue(self.game.can_make_move(), "There should be possible moves at the start of the game.")
        
    def test_game_status(self):
        """Test the game status logic."""
        self.assertEqual(self.game.evaluate_game_status(), "continue", "Game should continue at the start.")
        
if __name__ == '__main__':
    unittest.main()

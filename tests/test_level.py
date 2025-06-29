import unittest
import pygame
from Levels.L1 import Level

class TestLevel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        
    def tearDown(self):
        pygame.quit()

    def test_level_initialization(self):
        level = Level(number=1, difficulty="easy", bg_color=(135, 206, 235))
        self.assertEqual(level.number, 1)
        self.assertEqual(level.difficulty, "easy")
        self.assertEqual(level.bg_color, (135, 206, 235))
        self.assertIsInstance(level.fondo_piso, pygame.Surface)
        self.assertIsInstance(level.trees, list)
        self.assertIsInstance(level.houses, list)

    def test_level_assets_loaded(self):
        level = Level(number=1, difficulty="normal", bg_color=(100, 100, 100))
        self.assertTrue(len(level.trees) > 0)
        self.assertTrue(len(level.houses) > 0)
        self.assertNotEqual(level.fondo_piso.get_size(), (0, 0))

    def test_level_different_difficulties(self):
        level_easy = Level(number=1, difficulty="easy", bg_color=(135, 206, 235))
        level_hard = Level(number=1, difficulty="hard", bg_color=(135, 206, 235))
        self.assertNotEqual(level_easy.difficulty, level_hard.difficulty)

    def test_level_background_color(self):
        custom_color = (50, 100, 150)
        level = Level(number=1, difficulty="normal", bg_color=custom_color)
        self.assertEqual(level.bg_color, custom_color)

if __name__ == '__main__':
    unittest.main()

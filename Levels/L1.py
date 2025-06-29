"""
Level class representing a game level with background elements and rendering methods.

Manages level-specific assets like floor, grass, trees, houses, and clouds. Provides methods
to draw these elements with parallax scrolling effects. Supports level customization through
initialization parameters like level number, difficulty, and background color.

Attributes:
    number (int): The level number.
    difficulty (str): The difficulty setting for the level.
    bg_color (tuple): Background color for the level.
    fondo_piso (pygame.Surface): Floor texture.
    trees (list): Randomly scaled and flipped tree images.
    houses (list): Randomly scaled and flipped house images.
"""
import pygame
import random

class Level:
    def __init__(self, number, difficulty, bg_color):
        """
        Initialize the Level with specific parameters and load level assets.

        Args:
            number (int): The number of the current level.
            difficulty (str): The difficulty setting for the level.
            bg_color (tuple): Background color for the level rendering.
        """
        self.number = number
        self.difficulty = difficulty
        self.bg_color = bg_color
        self.level_length = 2000  # Longitud total del nivel
        
        # Límites del nivel
        self.left_limit = 0
        self.right_limit = self.level_length
        
        # Asegurar que los límites estén dentro de los límites del nivel
        self.left_limit = max(0, self.left_limit)
        self.right_limit = min(self.level_length, self.right_limit)
        
        # Load level textures
        self.fondo_piso = pygame.image.load("img/Levels/L1/F-1.png")
        self.g = pygame.image.load("img/Levels/L1/G-1.png")
        self.g = pygame.transform.scale(self.g, (364, 103))
        self.a = pygame.image.load("img/Levels/L1/A-1.png")

        # Create trees with random heights and random flipping
        self.trees = [pygame.transform.scale(self.a, (180, random.randint(300, 500))) for _ in range((2000 // 200) + 1)]
        self.trees = [pygame.transform.flip(x, True, False) if random.choice([True, False]) else x for x in self.trees]

        # Load and prepare houses
        self.houses = [pygame.image.load(f"img/Levels/L1/H-{i}.png") for i in range(1, 5)]
        self.c = [pygame.transform.scale(x, (56, 68)) for x in self.houses]
        self.c = [pygame.transform.flip(x, True, False) if random.choice([True, False]) else x for x in self.c]

        # Load background behind houses
        self.back_house = pygame.image.load("img/Levels/L1/B-1.png")
        self.back_house = pygame.transform.scale(self.back_house, (109, 116))
        self.back_house_flipped = pygame.transform.flip(self.back_house, True, False)

        # Load cloud images
        self.cloud_images = [pygame.image.load(f"img/Levels/L1/C-{i}.png") for i in range(1, 7)]
        self.clouds_large = [pygame.transform.scale(c, (150, 100)) for c in self.cloud_images]
        self.clouds_small = [pygame.transform.scale(c, (75, 50)) for c in self.cloud_images]

    def draw_floor(self, surface, offset):
        """
        Draw the floor texture across the surface with horizontal scrolling.

        Args:
            surface (pygame.Surface): The surface to draw the floor on.
            offset (int): Horizontal scrolling offset.
        """
        y = surface.get_height() - self.fondo_piso.get_height()
        for i in range((2000 // self.fondo_piso.get_width()) + 1):
            surface.blit(self.fondo_piso, (i * self.fondo_piso.get_width() - offset, y))

    def draw_grass(self, surface, offset):
        """
        Draw grass texture with parallax scrolling and alternating flipping.

        Args:
            surface (pygame.Surface): The surface to draw the grass on.
            offset (int): Horizontal scrolling offset.
        """
        y = surface.get_height() - self.fondo_piso.get_height() - self.g.get_height()
        parallax_offset = offset * 0.7
        for i in range((2000 // self.g.get_width()) + 1):
            r = self.g if i % 2 == 0 else pygame.transform.flip(self.g, True, False)
            surface.blit(r, (i * self.g.get_width() - parallax_offset, y))

    def draw_trees(self, surface, offset):
        """
        Draw trees with parallax scrolling effect.

        Args:
            surface (pygame.Surface): The surface to draw the trees on.
            offset (int): Horizontal scrolling offset.
        """
        for i, tree in enumerate(self.trees):
            y = surface.get_height() - self.fondo_piso.get_height() - tree.get_height()
            surface.blit(tree, (i * 200 - offset * 0.4, y))

    def draw_houses(self, surface, offset):
        """
        Draw houses and their backgrounds with parallax scrolling.

        Args:
            surface (pygame.Surface): The surface to draw the houses on.
            offset (int): Horizontal scrolling offset.
        """
        y = surface.get_height() - self.fondo_piso.get_height() - self.g.get_height() - self.c[0].get_height() + 40
        houses_offset = offset * 0.4
        backgrounds_offset = offset * 0.2
        for i in range((2000 // 120) + 1):
            x_bg = i * 120 - backgrounds_offset
            yf = y - 60
            bg = self.back_house if i % 2 == 0 else self.back_house_flipped
            surface.blit(bg, (x_bg, yf))
            x_house = i * 120 - houses_offset
            house = self.c[i % len(self.c)]
            surface.blit(house, (x_house, y))
            surface.blit(house, (x_house + 5, y - 5))

    def draw_clouds(self, surface, clouds_large_pos, clouds_small_pos):
        """
        Draw and animate clouds with horizontal movement.

        Args:
            surface (pygame.Surface): The surface to draw the clouds on.
            clouds_large_pos (list): Positions of large clouds.
            clouds_small_pos (list): Positions of small clouds.
        """
        for i, pos in enumerate(clouds_large_pos):
            surface.blit(self.clouds_large[i], pos)
            pos[0] -= 1
            if pos[0] < -150:
                pos[0] = surface.get_width()
                pos[1] = random.randint(50, 150)

        for i, pos in enumerate(clouds_small_pos):
            surface.blit(self.clouds_small[i], pos)
            pos[0] -= 2
            if pos[0] < -75:
                pos[0] = surface.get_width()
                pos[1] = random.randint(200, 300)

    def draw_level(self, surface, offset, clouds_large_pos, clouds_small_pos):
        """
        Render the entire level with all background elements in correct order.

        Args:
            surface (pygame.Surface): The surface to draw the level on.
            offset (int): Horizontal scrolling offset.
            clouds_large_pos (list): Positions of large clouds.
            clouds_small_pos (list): Positions of small clouds.
        """
        # Draw elements in the correct order
        self.draw_floor(surface, offset)          # Floor
        self.draw_clouds(surface, clouds_large_pos, clouds_small_pos)  # Clouds
        self.draw_grass(surface, offset)          # Grass (G-1 behind)
        self.draw_houses(surface, offset)         # Background behind houses (B-1 behind)
        self.draw_trees(surface, offset)          # Trees (A-1 in front)
"""
Level class representing a game level with background elements and rendering methods.

Manages level-specific assets like floor, grass, trees, houses, and clouds. Provides methods
to draw these elements with parallax scrolling effects. Supports level customization through
initialization parameters like level number, difficulty, and background color.

Attributes:
    number (int): The level number.
    difficulty (str): The difficulty setting for the level.
    bg_color (tuple): Background color for the level.
    fondo_piso (pygame.Surface): Floor texture.
    trees (list): Randomly scaled and flipped tree images.
    houses (list): Randomly scaled and flipped house images.
"""
import pygame
import random

class Level:
    def __init__(self, number, difficulty, bg_color):
        self.number = number
        self.difficulty = difficulty
        self.bg_color = bg_color

        # Cargar texturas del nivel
        self.fondo_piso = pygame.image.load("img/Levels/L1/F-1.png")
        self.g = pygame.image.load("img/Levels/L1/G-1.png")
        self.g = pygame.transform.scale(self.g, (364, 103))
        self.a = pygame.image.load("img/Levels/L1/A-1.png")

        # Crear árboles con alturas aleatorias
        self.trees = [pygame.transform.scale(self.a, (180, random.randint(300, 500))) for _ in range((2000 // 200) + 1)]
        self.trees = [pygame.transform.flip(x, True, False) if random.choice([True, False]) else x for x in self.trees]

        # Casas
        self.houses = [pygame.image.load(f"img/Levels/L1/H-{i}.png") for i in range(1, 5)]
        self.c = [pygame.transform.scale(x, (56, 68)) for x in self.houses]
        self.c = [pygame.transform.flip(x, True, False) if random.choice([True, False]) else x for x in self.c]

        # Fondo detrás de casas
        self.back_house = pygame.image.load("img/Levels/L1/B-1.png")
        self.back_house = pygame.transform.scale(self.back_house, (109, 116))
        self.back_house_flipped = pygame.transform.flip(self.back_house, True, False)

        # Nubes
        self.cloud_images = [pygame.image.load(f"img/Levels/L1/C-{i}.png") for i in range(1, 7)]
        self.clouds_large = [pygame.transform.scale(c, (150, 100)) for c in self.cloud_images]
        self.clouds_small = [pygame.transform.scale(c, (75, 50)) for c in self.cloud_images]

    def draw_floor(self, surface, offset):
        y = surface.get_height() - self.fondo_piso.get_height()
        for i in range((2000 // self.fondo_piso.get_width()) + 1):
            surface.blit(self.fondo_piso, (i * self.fondo_piso.get_width() - offset, y))

    def draw_grass(self, surface, offset):
        y = surface.get_height() - self.fondo_piso.get_height() - self.g.get_height()
        parallax_offset = offset * 0.7
        for i in range((2000 // self.g.get_width()) + 1):
            r = self.g if i % 2 == 0 else pygame.transform.flip(self.g, True, False)
            surface.blit(r, (i * self.g.get_width() - parallax_offset, y))

    def draw_trees(self, surface, offset):
        for i, tree in enumerate(self.trees):
            y = surface.get_height() - self.fondo_piso.get_height() - tree.get_height()
            surface.blit(tree, (i * 200 - offset * 0.4, y))

    def draw_houses(self, surface, offset):
        y = surface.get_height() - self.fondo_piso.get_height() - self.g.get_height() - self.c[0].get_height() + 40
        houses_offset = offset * 0.4
        backgrounds_offset = offset * 0.2
        for i in range((2000 // 120) + 1):
            x_bg = i * 120 - backgrounds_offset
            yf = y - 60
            bg = self.back_house if i % 2 == 0 else self.back_house_flipped
            surface.blit(bg, (x_bg, yf))
            x_house = i * 120 - houses_offset
            house = self.c[i % len(self.c)]
            surface.blit(house, (x_house, y))
            surface.blit(house, (x_house + 5, y - 5))

    def draw_clouds(self, surface, clouds_large_pos, clouds_small_pos):
        for i, pos in enumerate(clouds_large_pos):
            surface.blit(self.clouds_large[i], pos)
            pos[0] -= 1
            if pos[0] < -150:
                pos[0] = surface.get_width()
                pos[1] = random.randint(50, 150)

        for i, pos in enumerate(clouds_small_pos):
            surface.blit(self.clouds_small[i], pos)
            pos[0] -= 2
            if pos[0] < -75:
                pos[0] = surface.get_width()
                pos[1] = random.randint(200, 300)

    def draw_level(self, surface, offset, clouds_large_pos, clouds_small_pos):
        # Dibuja los elementos en el orden correcto
        self.draw_floor(surface, offset)          # Piso
        self.draw_clouds(surface, clouds_large_pos, clouds_small_pos)  # Nubes
        self.draw_grass(surface, offset)          # Hierba (G-1 detrás)
        self.draw_houses(surface, offset)         # Fondo detrás de casas (B-1 detrás)
        self.draw_trees(surface, offset)          # Árboles (A-1 al frente)
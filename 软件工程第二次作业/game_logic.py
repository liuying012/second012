# game_logic.py
from constants import NUM_TILES_X, NUM_TILES_Y

import random

def generate_tiles():
    # 随机生成图案
    return [[random.choice(['A', 'B', 'C', 'D']) for _ in range(NUM_TILES_X)] for _ in range(NUM_TILES_Y)]

def find_matches(tiles):
    matches = []
    # 检测横向匹配
    for y in range(NUM_TILES_Y):
        for x in range(NUM_TILES_X - 2):
            if tiles[y][x] == tiles[y][x + 1] == tiles[y][x + 2]:
                matches.append((x, y))
                matches.append((x + 1, y))
                matches.append((x + 2, y))
    # 检测纵向匹配
    for x in range(NUM_TILES_X):
        for y in range(NUM_TILES_Y - 2):
            if tiles[y][x] == tiles[y + 1][x] == tiles[y + 2][x]:
                matches.append((x, y))
                matches.append((x, y + 1))
                matches.append((x, y + 2))
    return matches

def remove_matches(tiles, matches):
    for (x, y) in matches:
        tiles[y][x] = None
    return tiles

def refill_tiles(tiles):
    for y in range(NUM_TILES_Y):
        for x in range(NUM_TILES_X):
            if tiles[y][x] is None:
                tiles[y][x] = random.choice(['A', 'B', 'C', 'D'])
    return tiles

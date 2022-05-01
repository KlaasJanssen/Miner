WIDTH = 1280
HEIGHT = 720
TILE_SIZE = 64

MAP_BLOCK_WIDTH = 40
MAP_BLOCK_HEIGHT = 100

LEFT_LIMIT = 0
RIGHT_LIMIT = TILE_SIZE*MAP_BLOCK_WIDTH
UP_LIMIT = -4*TILE_SIZE
DOWN_LIMIT = TILE_SIZE*MAP_BLOCK_HEIGHT

MINE_BACKGROUND_COLOR = "#55341b"

# Player data

# Inventory
PLAYER_INV_SLOTS = 4

INV_TILE_SIZE = TILE_SIZE * 1.5

# UI

# Tile data
tile_data = {
"grass":{"drop":"dirt", "drop_amount":1},
"dirt":{"drop":"dirt", "drop_amount":1},
"coal":{"drop":"coal", "drop_amount":1},
"iron":{"drop":"iron", "drop_amount":1}
}

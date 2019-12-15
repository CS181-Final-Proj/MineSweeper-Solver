import random
from mineblock import *

def get_random_block():
    random_x = random.randint(0,29)
    random_y = random.randint(0,15)
    return random_x, random_y
import random
import pygame
import time
import sys
from game import *
from mineblock import *


BLOCK = MineBlock()


def solver():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('MineSweeper')

    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)  # font of score
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40)

    # load pics, and normalize
    img0 = pygame.image.load('resources/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('resources/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('resources/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('resources/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('resources/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('resources/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('resources/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('resources/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('resources/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('resources/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('resources/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_ask = pygame.image.load('resources/ask.bmp').convert()
    img_ask = pygame.transform.smoothscale(img_ask, (SIZE, SIZE))
    img_mine = pygame.image.load('resources/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('resources/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('resources/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.image.load('resources/face_fail.bmp').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_face_normal = pygame.image.load('resources/face_normal.bmp').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('resources/face_success.bmp').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2

    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }

    bgcolor = (225, 225, 225)   # background color

    
    game_status = GameStatus.started
    # start_time = None   # start time
    start_time = time.time()   # start time
    elapsed_time = 0    # elapse time



    while True:
        # fill the background color
        screen.fill(bgcolor)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


        if game_status == GameStatus.over:
            # game_status = GameStatus.started
            # block = MineBlock()
            # start_time = time.time()
            # elapsed_time = 0
            # continue
            print("+---------------+")
            print("  you lose !!!!")
            print("+---------------+")
            #time.sleep(1000)
            sys.exit()
        

        if sys.argv[2] == "--random":
            next_x, next_y = get_random_block()
        elif sys.argv[2] == "--RL":
            next_x, next_y = RL_Agent()
        elif sys.argv[2] == "--LG":
            next_x, next_y = LG_Agent()
        elif sys.argv[2] == "--BN":
            next_x, next_y = BN_Agent()
        elif sys.argv[2] == "--DQN":
            next_x, next_y = BN_Agent()
        else:
            continue



        if game_status == GameStatus.started:
            mine = BLOCK.getmine(next_x, next_y)
            if mine.status == BlockStatus.normal:
                if not BLOCK.open_mine(next_x, next_y):
                    game_status = GameStatus.over


        flag_count = 0
        opened_count = 0

        for row in BLOCK.block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == BlockStatus.opened:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == BlockStatus.double:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                elif mine.status == BlockStatus.bomb:
                    screen.blit(img_blood, pos)
                elif mine.status == BlockStatus.flag:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif mine.status == BlockStatus.ask:
                    screen.blit(img_ask, pos)
                elif mine.status == BlockStatus.hint:
                    screen.blit(img0, pos)
                elif game_status == GameStatus.over and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.value == 0 and mine.status == BlockStatus.flag:
                    screen.blit(img_error, pos)
                elif mine.status == BlockStatus.normal:
                    screen.blit(img_blank, pos)


        print_text(screen, font1, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (MINE_COUNT - flag_count), red)
        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)

        if flag_count + opened_count == BLOCK_WIDTH * BLOCK_HEIGHT:
            game_status = GameStatus.win

        if game_status == GameStatus.over:
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        elif game_status == GameStatus.win:
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))

        pygame.display.update()
        time.sleep(1)



###################################### don't modify code above ######################################
################################## implement different agent below ##################################


# use BLOCK.get_block_state(x, y) to get the state of the block at location (x,y)
# P.S. 0 <= x <= 29, 0 <= y <= 15



# use BLOCK.get_game_state() to get the state of all blocks
# the function will return a 2D list
# None in the list means the block is not yet opened






def get_random_block():
    #print(BLOCK.get_block_state(0, 0))
    random_x = random.randint(0,29)
    random_y = random.randint(0,15)
    return random_x, random_y


def RL_Agent():

    ####### need to implement ######


    print("not implement yet")
    sys.exit()
    return next_x, next_y

def LG_Agent():

    ####### need to implement ######


    print("not implement yet")
    sys.exit()
    return next_x, next_y



def BN_Agent():

    ####### need to implement ######


    print("not implement yet")
    sys.exit()
    return next_x, next_y


def DQN_Agent():

    ####### need to implement ######


    print("not implement yet")
    sys.exit()
    return next_x, next_y



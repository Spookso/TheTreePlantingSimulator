import pygame
import random
import json

pygame.init()
win = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Tree Planting Simulator")
clock = pygame.time.Clock()

pygame.mixer.music.set_volume(.05)
music = random.randint(1, 3)
if music == 1:
    pygame.mixer.music.load('Track_1.mp3')
elif music == 2:
    pygame.mixer.music.load('Track_2.mp3')
else:
    pygame.mixer.music.load('Track_3.mp3')

font = pygame.font.SysFont('cambria', 60, False)
font2 = pygame.font.SysFont('cambria', 40, False)
font3 = pygame.font.SysFont('cambria', 30, False)
font4 = pygame.font.SysFont('cambria', 35, False)


class Ground(object):
    def __init__(self, x, y, height, width, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


class Tree(object):
    def __init__(self, x, y, size, colour, colour_value, timer, timer_displace, leaf_colour, type, leaf_displace=None):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.colour_value = colour_value
        self.timer = timer
        self.timer_displace = timer_displace
        self.is_grounded = False
        self.leaf_colour = leaf_colour
        self.type = type
        self.leaf_displace = leaf_displace
        self.touching = False


class Button(object):
    def __init__(self, x, y, width, height, colour, icon_value, text='', small_text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.icon_value = icon_value
        self.text = text
        self.small_text = small_text

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def highlight_check(self, mouse_pos):
        if self.is_over(mouse_pos):
            self.colour = (200, 200, 200)
        else:
            self.colour = (255, 255, 255)

    def draw(self, win, outline_colour=None):
        if outline_colour:
            pygame.draw.rect(win, outline_colour, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.icon_value == 1:
            pygame.draw.circle(win, (78, 46, 40), (self.x + self.width // 2, self.y + self.height // 2), 15)
        if self.icon_value == 2:
            pygame.draw.circle(win, (170, 150, 100), (self.x + self.width // 2, self.y + self.height // 2), 15)
        if self.icon_value == 3:
            pygame.draw.circle(win, (58, 26, 20), (self.x + self.width // 2, self.y + self.height // 2), 15)

        if self.text != '':
            if not self.small_text:
                font = pygame.font.SysFont('cambria', 50)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
            else:
                font = pygame.font.SysFont('cambria', 30)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


def tree_colour_select(tree, stage):
    if stage == 1:
        if tree.colour_value == 1:
            tree.colour = (0, 85, 10)
        if tree.colour_value == 2:
            tree.colour = (0, 100, 20)
        if tree.colour_value == 3:
            tree.colour = (10, 120, 30)
        if tree.colour_value == 4:
            tree.colour = (20, 140, 40)
        if tree.colour_value == 5:
            tree.colour = (30, 160, 65)
    if stage == 2:
        if tree.colour_value == 1:
            tree.colour = (0, 70, 5)
        if tree.colour_value == 2:
            tree.colour = (0, 85, 10)
        if tree.colour_value == 3:
            tree.colour = (0, 100, 20)
        if tree.colour_value == 4:
            tree.colour = (10, 120, 30)
        if tree.colour_value == 5:
            tree.colour = (20, 140, 40)
    if stage == 3:
        if tree.colour_value == 1:
            tree.colour = (0, 50, 0)
        if tree.colour_value == 2:
            tree.colour = (0, 60, 0)
        if tree.colour_value == 3:
            tree.colour = (0, 70, 5)
        if tree.colour_value == 4:
            tree.colour = (0, 85, 10)
        if tree.colour_value == 5:
            tree.colour = (0, 100, 20)


def leaf_colour_select(tree, stage):
    if stage == 2:
        if tree.colour_value == 1:
            tree.leaf_colour = (0, 85, 10)
        if tree.colour_value == 2:
            tree.leaf_colour = (0, 100, 20)
        if tree.colour_value == 3:
            tree.leaf_colour = (10, 120, 30)
        if tree.colour_value == 4:
            tree.leaf_colour = (20, 140, 40)
        if tree.colour_value == 5:
            tree.leaf_colour = (30, 160, 65)
    if stage == 3:
        if tree.type == 1:
            if tree.colour_value == 1:
                tree.leaf_colour = (0, 70, 5)
            if tree.colour_value == 2:
                tree.leaf_colour = (0, 85, 10)
            if tree.colour_value == 3:
                tree.leaf_colour = (0, 100, 20)
            if tree.colour_value == 4:
                tree.leaf_colour = (10, 120, 30)
            if tree.colour_value == 5:
                tree.leaf_colour = (20, 140, 40)
        elif tree.type == 2:
            if tree.colour_value == 1:
                tree.leaf_colour = (15, 80, 10)
            if tree.colour_value == 2:
                tree.leaf_colour = (30, 100, 20)
            if tree.colour_value == 3:
                tree.leaf_colour = (50, 120, 40)
            if tree.colour_value == 4:
                tree.leaf_colour = (70, 140, 60)
            if tree.colour_value == 5:
                tree.leaf_colour = (90, 160, 80)


def tree_timer_check():
    for seed in seeds:
        seed.timer += 1
        if seed.is_grounded:
            if seed.timer >= 250 + seed.timer_displace:
                tree_colour_select(seed, 1)
                sprouts.append(Tree(seed.x, seed.y, seed.size, seed.colour, seed.colour_value, 0, seed.timer_displace, seed.leaf_colour, seed.type, seed.leaf_displace))
                seeds.pop(seeds.index(seed))
    for sprout in sprouts:
        sprout.timer += 1
        if sprout.timer >= 500 + sprout.timer_displace * 2:
            tree_colour_select(sprout, 2)
            leaf_colour_select(sprout, 2)
            saplings.append(Tree(sprout.x, sprout.y, sprout.size, sprout.colour, sprout.colour_value, 0, sprout.timer_displace, sprout.leaf_colour, sprout.type, sprout.leaf_displace))
            sprouts.pop(sprouts.index(sprout))
    for sapling in saplings:
        sapling.timer += 1
        if sapling.timer >= 750 + sapling.timer_displace * 3:
            tree_colour_select(sapling, 3)
            leaf_colour_select(sapling, 3)
            trees.append(Tree(sapling.x, sapling.y, sapling.size, sapling.colour, sapling.colour_value, 0, sapling.timer_displace, sapling.leaf_colour, sapling.type, sapling.leaf_displace))
            saplings.pop(saplings.index(sapling))


def seed_fall_check():
    for seed in seeds:
        if seed.y < base.y:
            seed.y += 5
        if seed.y > base.y:
            seed.y = base.y
        else:
            seed.is_grounded = True


def tree_draw():
    for seed in seeds:
        if seed.type == 1:
            pygame.draw.circle(win, (78, 46, 40), (seed.x, seed.y), seed.size)
        elif seed.type == 2:
            pygame.draw.circle(win, (170, 150, 100), (seed.x, seed.y), seed.size)
        elif seed.type == 3:
            pygame.draw.circle(win, (58, 26, 20), (seed.x, seed.y), seed.size)
    for sprout in sprouts:
        pygame.draw.rect(win, sprout.colour, (sprout.x, sprout.y - sprout.size * 4, sprout.size * 2, sprout.size * 4))
    for sapling in saplings:
        pygame.draw.rect(win, sapling.colour, (sapling.x, sapling.y - sapling.size * 12, sapling.size * 3, sapling.size * 15))
        if sapling.type == 1:
            pygame.draw.circle(win, sapling.leaf_colour, (sapling.x + round(sapling.size * 1.5), sapling.y - sapling.size * 15), sapling.size * 5)
        elif sapling.type == 2:
            pygame.draw.rect(win, sapling.leaf_colour, (sapling.x + round(sapling.size * 1.5) - sapling.size * 6, sapling.y - sapling.size * 15, sapling.size * 12, sapling.size * 8))
        elif sapling.type == 3:
            pygame.draw.polygon(win, sapling.leaf_colour, [(round(sapling.x + sapling.size * 1.5), sapling.y - sapling.size * 16), (sapling.x - sapling.size * 3, round(sapling.y - sapling.size * 5)), (sapling.x + sapling.size * 6, round(sapling.y - sapling.size * 5))], 0)
    for tree in trees:
        pygame.draw.rect(win, tree.colour, (tree.x, tree.y - tree.size * 30, tree.size * 6, tree.size * 30))
        if tree.type == 1:
            pygame.draw.circle(win, tree.leaf_colour, (tree.x + round(tree.size * 3), tree.y - tree.size * 38), tree.size * 7)
            pygame.draw.circle(win, tree.leaf_colour, (tree.x - tree.size * 2, tree.y - tree.size * 30), tree.size * 7)
            pygame.draw.circle(win, tree.leaf_colour, (tree.x + tree.size * 8, tree.y - tree.size * 30), tree.size * 7)
        elif tree.type == 2:
            pygame.draw.rect(win, tree.leaf_colour, (tree.x + round(tree.size * 3) - tree.size * 10, tree.y - tree.size * 30 - tree.leaf_displace, tree.size * 20, tree.size * 14))
        elif tree.type == 3:
            pygame.draw.polygon(win, tree.leaf_colour, [(round(tree.x + tree.size * 3), tree.y - tree.size * 42), (tree.x - tree.size * 8, round(tree.y - tree.size * 8)), (tree.x + tree.size * 14, round(tree.y - tree.size * 8))], 0)


def is_touching(pos, tree_status, tree):
    if tree_status == 1:
        if pos[0] > tree.x and pos[0] < tree.x + tree.size * 3:
            if pos[1] > tree.y - tree.size * 15 and pos[1] < tree.y:
                tree.touching = True

            else:
                tree.touching = False
        else:
            tree.touching = False
    if tree_status == 2:
        if pos[0] > tree.x and pos[0] < tree.x + tree.size * 6:
            if pos[1] > tree.y - tree.size * 30 and pos[1] < tree.y:
                tree.touching = True

            else:
                tree.touching = False
        else:
            tree.touching = False


def redraw_game_window():
    if game_start:
        wood1_val = font3.render('Brown Wood: ' + str(wood1), 1, (0, 0, 0))
        wood2_val = font3.render('Creme Wood: ' + str(wood2), 1, (0, 0, 0))
        wood3_val = font3.render('Dark Wood: ' + str(wood3), 1, (0, 0, 0))
        win.fill((135, 206, 235))
        tree_draw()
        base.draw(win)
        but1.draw(win, (0, 0, 0))
        but2.draw(win, (0, 0, 0))
        but3.draw(win, (0, 0, 0))
        but4.draw(win, (0, 0, 0))
        shop_open_but.draw(win, (0, 0, 0))
        seed1_amount_text = font4.render(str(seed1_amount), 1, (0, 0, 0))
        seed2_amount_text = font4.render(str(seed2_amount), 1, (0, 0, 0))
        seed3_amount_text = font4.render(str(seed3_amount), 1, (0, 0, 0))

        if seed1_amount < 10:
            win.blit(seed1_amount_text, (5 + but1.width // 2 - 10, 65))
        else:
            win.blit(seed1_amount_text, (5 + but1.width // 2 - 16, 65))
        if seed2_amount < 10:
            win.blit(seed2_amount_text, (85 + but1.width // 2 - 12, 65))
        else:
            win.blit(seed2_amount_text, (85 + but1.width // 2 - 18, 65))
        if seed3_amount < 10:
            win.blit(seed3_amount_text, (165 + but1.width // 2 - 18, 65))
        else:
            win.blit(seed3_amount_text, (165 + but1.width // 2 - 24, 65))

        win.blit(wood1_val, (300, 15))
        win.blit(wood2_val, (500, 15))
        win.blit(wood3_val, (700, 15))
    else:
        if shop:
            wood1_val = font4.render('Brown Wood: ' + str(wood1), 1, (0, 0, 0))
            wood2_val = font4.render('Creme Wood: ' + str(wood2), 1, (0, 0, 0))
            wood3_val = font4.render('Dark Wood: ' + str(wood3), 1, (0, 0, 0))
            money_val = font4.render('Money: ' + str(money), 1, (0, 0, 0))
            win.fill((222, 184, 135))
            shop_close_but.draw(win, (0, 0, 0))
            win.blit(wood1_val, (10, 15))
            win.blit(wood2_val, (250, 15))
            win.blit(wood3_val, (500, 15))
            win.blit(money_val, (750, 15))
            if shop1_open:
                shop2_open_but.draw(win, (0, 0, 0))
                shop3_open_but.draw(win, (0, 0, 0))
            if shop2_open:
                exchange1_1.draw(win, (0, 0, 0))
                exchange1_2.draw(win, (0, 0, 0))
                exchange1_3.draw(win, (0, 0, 0))
                exchange2_1.draw(win, (0, 0, 0))
                exchange2_2.draw(win, (0, 0, 0))
                exchange2_3.draw(win, (0, 0, 0))
                exchange3_1.draw(win, (0, 0, 0))
                exchange3_2.draw(win, (0, 0, 0))
                exchange3_3.draw(win, (0, 0, 0))
            if shop3_open:
                buy_seed1_1.draw(win, (0, 0, 0))
                buy_seed1_2.draw(win, (0, 0, 0))
                buy_seed1_3.draw(win, (0, 0, 0))
                buy_seed2_1.draw(win, (0, 0, 0))
                buy_seed2_2.draw(win, (0, 0, 0))
                buy_seed2_3.draw(win, (0, 0, 0))
                buy_seed3_1.draw(win, (0, 0, 0))
                buy_seed3_2.draw(win, (0, 0, 0))
                buy_seed3_3.draw(win, (0, 0, 0))
        else:
            win.fill((135, 206, 235))
            base.draw(win)
            title = font.render('Tree Simulator', 1, (0, 50, 0))
            win.blit(title, (350, 150))
            start_but.draw(win, (0, 0, 0))
    pygame.display.update()


def check_json_file():
    global seed1_amount
    global seed2_amount
    global seed3_amount
    global wood1
    global wood2
    global wood3
    global money

    with open('score_record.json') as json_file:
        data = json.load(json_file)

        seed1_amount = int(data['seed1_amount'])
        seed2_amount = int(data['seed2_amount'])
        seed3_amount = int(data['seed3_amount'])
        wood1 = int(data['wood1'])
        wood2 = int(data['wood2'])
        wood3 = int(data['wood3'])
        money = int(data['money'])

        json_file.close()


def update_json_file():
    global seed1_amount
    global seed2_amount
    global seed3_amount
    global wood1
    global wood2
    global wood3
    global money

    open('score_record.json', 'w')
    data = {'seed1_amount': seed1_amount, 'seed2_amount': seed2_amount, 'seed3_amount': seed3_amount, 'wood1': wood1,
            'wood2': wood2, 'wood3': wood3, 'money': money}

    with open('score_record.json', 'w') as json_file:
        json.dump(data, json_file)
        json_file.close()


base = Ground(0, 430, 70, 1000, (86, 176, 0))
but1 = Button(5, 5, 50, 50, (255, 255, 255), 1)
but2 = Button(80, 5, 50, 50, (255, 255, 255), 2)
but3 = Button(155, 5, 50, 50, (255, 255, 255), 3)
but4 = Button(230, 5, 50, 50, (255, 255, 255), -1)
start_but = Button(370, 300, 250, 100, (255, 255, 255), 0, 'Start')
shop_open_but = Button(895, 5, 100, 50, (255, 255, 255), 0, 'Shop')
shop_close_but = Button(5, 445, 100, 50, (255, 255, 255), 0, 'Back')
shop2_open_but = Button(100, 200, 300, 100, (255, 255, 255), 0, 'Exchange Wood')
shop3_open_but = Button(600, 200, 300, 100, (255, 255, 255), 0, 'Buy Seeds')
buy_seed1_1 = Button(25, 110, 300, 80, (255, 255, 255), 0, 'Buy 1 Brown Seed ($4)', True)
buy_seed1_2 = Button(350, 110, 300, 80, (255, 255, 255), 0, 'Buy 5 Brown Seeds ($20)', True)
buy_seed1_3 = Button(675, 110, 300, 80, (255, 255, 255), 0, 'Buy 20 Brown Seeds ($80)', True)
buy_seed2_1 = Button(25, 220, 300, 80, (255, 255, 255), 0, 'Buy 1 Creme Seed ($60)', True)
buy_seed2_2 = Button(350, 220, 300, 80, (255, 255, 255), 0, 'Buy 5 Creme Seeds ($300)', True)
buy_seed2_3 = Button(675, 220, 300, 80, (255, 255, 255), 0, 'Buy 20 Creme Seeds ($1200)', True)
buy_seed3_1 = Button(25, 330, 300, 80, (255, 255, 255), 0, 'Buy 1 Dark Seed ($1000)', True)
buy_seed3_2 = Button(350, 330, 300, 80, (255, 255, 255), 0, 'Buy 5 Dark Seeds ($5000)', True)
buy_seed3_3 = Button(675, 330, 300, 80, (255, 255, 255), 0, 'Buy 20 Dark Seeds ($20000)', True)
exchange1_1 = Button(buy_seed1_1.x + buy_seed1_1.width // 2 - 145, 110, 300, 80, (0, 0, 0), 0, 'Exchange 5 Brown Wood', True)
exchange1_2 = Button(buy_seed1_2.x + buy_seed1_2.width // 2 - 145, 110, 300, 80, (0, 0, 0), 0, 'Exchange 50 Brown Wood', True)
exchange1_3 = Button(buy_seed1_3.x + buy_seed1_3.width // 2 - 145, 110, 300, 80, (0, 0, 0), 0, 'Exchange 500 Brown Wood', True)
exchange2_1 = Button(buy_seed1_1.x + buy_seed1_1.width // 2 - 145, 220, 300, 80, (0, 0, 0), 0, 'Exchange 5 Creme Wood', True)
exchange2_2 = Button(buy_seed1_2.x + buy_seed1_2.width // 2 - 145, 220, 300, 80, (0, 0, 0), 0, 'Exchange 50 Creme Wood', True)
exchange2_3 = Button(buy_seed1_3.x + buy_seed1_3.width // 2 - 145, 220, 300, 80, (0, 0, 0), 0, 'Exchange 500 Creme Wood', True)
exchange3_1 = Button(buy_seed1_1.x + buy_seed1_1.width // 2 - 145, 330, 300, 80, (0, 0, 0), 0, 'Exchange 5 Dark Wood', True)
exchange3_2 = Button(buy_seed1_2.x + buy_seed1_2.width // 2 - 145, 330, 300, 80, (0, 0, 0), 0, 'Exchange 50 Dark Wood', True)
exchange3_3 = Button(buy_seed1_3.x + buy_seed1_3.width // 2 - 145, 330, 300, 80, (0, 0, 0), 0, 'Exchange 500 Dark Wood', True)
seeds = []
sprouts = []
saplings = []
trees = []

run = True
seed_type = 1
type_timer = 0
game_start = False
shop = False
shop1_open = False
shop2_open = False
shop3_open = False
shop_cooldown = 0
sound = 0

while run:
    clock.tick(30)
    type_timer -= 1
    pos = pygame.mouse.get_pos()
    shop_cooldown -= 1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            update_json_file()
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_but.is_over(pos):
                if not game_start:
                    if not shop:
                        game_start = True
                        seed_type = 7
                        check_json_file()
                        pygame.mixer.music.play(-1)
            if but1.is_over(pos):
                seed_type = 1
            if but2.is_over(pos):
                seed_type = 2
            if but3.is_over(pos):
                seed_type = 3
            if but4.is_over(pos):
                seed_type = 0
            if shop_open_but.is_over(pos):
                if not shop:
                    game_start = False
                    shop = True
                    shop1_open = True
            if shop1_open:
                if shop_close_but.is_over(pos):
                    seed_type = 7
                    game_start = True
                    shop = False
                    shop1_open = False
                if shop2_open_but.is_over(pos):
                    shop_cooldown = 25
                    shop1_open = False
                    shop2_open = True
                if shop3_open_but.is_over(pos):
                    shop_cooldown = 25
                    shop1_open = False
                    shop3_open = True
            if shop_cooldown <= 0:
                if shop2_open:
                    if shop_close_but.is_over(pos):
                        shop1_open = True
                        shop2_open = False
                    if exchange1_1.is_over(pos):
                        if wood1 >= 5:
                            wood1 -= 5
                            money += 1
                    if exchange1_2.is_over(pos):
                        if wood1 >= 50:
                            wood1 -= 50
                            money += 10
                    if exchange1_3.is_over(pos):
                        if wood1 >= 500:
                            wood1 -= 500
                            money += 100
                    if exchange2_1.is_over(pos):
                        if wood2 >= 5:
                            wood2 -= 5
                            money += 20
                    if exchange2_2.is_over(pos):
                        if wood2 >= 50:
                            wood2 -= 50
                            money += 200
                    if exchange2_3.is_over(pos):
                        if wood2 >= 500:
                            wood2 -= 500
                            money += 2000
                    if exchange3_1.is_over(pos):
                        if wood3 >= 5:
                            wood3 -= 5
                            money += 400
                    if exchange3_2.is_over(pos):
                        if wood3 >= 50:
                            wood3 -= 50
                            money += 4000
                    if exchange3_3.is_over(pos):
                        if wood3 >= 500:
                            wood3 -= 500
                            money += 40000
                if shop3_open:
                    if shop_close_but.is_over(pos):
                        shop1_open = True
                        shop3_open = False
                    if buy_seed1_1.is_over(pos):
                        if money >= 4:
                            seed1_amount += 1
                            money -= 4
                    if buy_seed1_2.is_over(pos):
                        if money >= 20:
                            seed1_amount += 5
                            money -= 20
                    if buy_seed1_3.is_over(pos):
                        if money >= 80:
                            seed1_amount += 20
                            money -= 80
                    if buy_seed2_1.is_over(pos):
                        if money >= 60:
                            seed2_amount += 1
                            money -= 60
                    if buy_seed2_2.is_over(pos):
                        if money >= 300:
                            seed2_amount += 5
                            money -= 300
                    if buy_seed2_3.is_over(pos):
                        if money >= 1200:
                            seed2_amount += 20
                            money -= 1200
                    if buy_seed3_1.is_over(pos):
                        if money >= 1000:
                            seed3_amount += 1
                            money -= 1000
                    if buy_seed3_2.is_over(pos):
                        if money >= 5000:
                            seed3_amount += 5
                            money -= 5000
                    if buy_seed3_3.is_over(pos):
                        if money >= 20000:
                            seed3_amount += 20
                            money -= 20000

            if game_start:
                if not but1.is_over(pos) and not but2.is_over(pos):
                    if not but3.is_over(pos):
                        if not but4.is_over(pos):
                            if seed_type == 0:
                                for sapling in saplings:
                                    is_touching(pos, 1, sapling)
                                    if sapling.touching:
                                        if sapling.type == 1:
                                            wood1 += sapling.size * 3
                                        if sapling.type == 2:
                                            wood1 += sapling.size * 3
                                        if sapling.type == 3:
                                            wood1 += sapling.type * 3
                                        saplings.pop(saplings.index(sapling))
                                        sapling.touching = False
                                for tree in trees:
                                    is_touching(pos, 2, tree)
                                    if tree.touching:
                                        if tree.type == 1:
                                            wood1 += tree.size * 5
                                        if tree.type == 2:
                                            wood2 += tree.size * 5
                                        if tree.type == 3:
                                            wood3 += tree.size * 5
                                        trees.pop(trees.index(tree))
                                        tree.touching = False
                            elif seed_type == 1:
                                if seed1_amount > 0:
                                    seeds.append(Tree(pos[0], pos[1], random.randint(4, 6), 0, random.randint(1, 5), 0, random.randint(20, 120), 0, 1))
                                    seed1_amount -= 1
                            elif seed_type == 2:
                                if seed2_amount > 0:
                                    seeds.append(Tree(pos[0], pos[1], random.randint(4, 6), 0, random.randint(1, 5), 0, random.randint(20, 120), 0, 2, random.randint(0, 30)))
                                    seed2_amount -= 1
                            elif seed_type == 3:
                                if seed3_amount > 0:
                                    seeds.append(Tree(pos[0], pos[1], random.randint(4, 6), 0, random.randint(1, 5), 0, random.randint(20, 120), 0, 3))
                                    seed3_amount -= 1

        if event.type == pygame.MOUSEMOTION:
            but1.highlight_check(pos)
            but2.highlight_check(pos)
            but3.highlight_check(pos)
            but4.highlight_check(pos)
            start_but.highlight_check(pos)
            shop_open_but.highlight_check(pos)
            shop_close_but.highlight_check(pos)
            shop2_open_but.highlight_check(pos)
            shop3_open_but.highlight_check(pos)
            exchange1_1.highlight_check(pos)
            exchange1_2.highlight_check(pos)
            exchange1_3.highlight_check(pos)
            exchange2_1.highlight_check(pos)
            exchange2_2.highlight_check(pos)
            exchange2_3.highlight_check(pos)
            exchange3_1.highlight_check(pos)
            exchange3_2.highlight_check(pos)
            exchange3_3.highlight_check(pos)
            buy_seed1_1.highlight_check(pos)
            buy_seed1_2.highlight_check(pos)
            buy_seed1_3.highlight_check(pos)
            buy_seed2_1.highlight_check(pos)
            buy_seed2_2.highlight_check(pos)
            buy_seed2_3.highlight_check(pos)
            buy_seed3_1.highlight_check(pos)
            buy_seed3_2.highlight_check(pos)
            buy_seed3_3.highlight_check(pos)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        for seed in seeds:
            seeds.pop(seeds.index(seed))
        for sprout in sprouts:
            sprouts.pop(sprouts.index(sprout))
        for sapling in saplings:
            saplings.pop(saplings.index(sapling))
        for tree in trees:
            trees.pop(trees.index(tree))
        win.fill((135, 206, 235))

    if keys[pygame.K_m]:
        if sound % 2 == 0:
            pygame.mixer.quit()
        else:
            pygame.mixer.init()
            if music == 1:
                pygame.mixer.music.load('Track_1.mp3')
            elif music == 2:
                pygame.mixer.music.load('Track_2.mp3')
            else:
                pygame.mixer.music.load('Track_3.mp3')
            pygame.mixer.music.set_volume(.05)
            pygame.mixer.music.play(-1)
        sound += 1

    if keys[pygame.K_h]:
        if keys[pygame.K_a]:
            if keys[pygame.K_c]:
                if keys[pygame.K_k]:
                    seed1_amount = 999
                    seed2_amount = 999
                    seed3_amount = 999
                    wood1 = 999
                    wood2 = 999
                    wood3 = 999
                    money = 999999

    if keys[pygame.K_x]:
        seed1_amount = 0
        seed2_amount = 0
        seed3_amount = 0
        wood1 = 0
        wood2 = 0
        wood3 = 0
        money = 0

    seed_fall_check()
    tree_timer_check()
    redraw_game_window()

pygame.quit()



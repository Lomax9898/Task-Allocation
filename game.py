import math
import pygame as pg
import random
import sys
import time
from copy import deepcopy

clock = pg.time.Clock()


class Task:
    task_tomake = 0
    x = random.randint(20, 72) * 15
    y = random.randint(1, 50) * 15
    x_pos = random.randint(20, 72) * 15
    y_pos = random.randint(1, 50) * 15

    def __init__(self, parent_screen):
        self.red = pg.image.load("red.jpg").convert()
        self.green = pg.image.load("green.jpg").convert()
        self.pink = pg.image.load("pink.jpg").convert()
        self.parent_screen = parent_screen

    def draw(self):
        self.parent_screen.blit(self.green, (Task.x, Task.y))


class Bots:
    x_pos = random.randint(20, 72) * 15
    y_pos = random.randint(1, 50) * 15

    def __init__(self):
        pass


class Game:

    def __init__(self):
        pg.init()
        self.score_list = []
        self.busy_bot_list = []
        self.target_list = []
        self.task_completed = 0
        self.end_time = 0
        self.start_time = 0
        self.run_time = 0
        self.screen = pg.display.set_mode((1390, 790))
        self.active_game = False
        self.user_bots = ""
        self.user_tasks = ""
        self.user_waves = ""
        self.user_uncertainty = ""
        self.user_strat = ""
        self.input_bots = pg.Rect(490, 100, 50, 32)
        self.input_tasks = pg.Rect(705, 150, 50, 32)
        self.input_waves = pg.Rect(720, 200, 50, 32)
        self.input_uncertainty = pg.Rect(555, 250, 50, 32)
        self.input_strat = pg.Rect(460, 300, 50, 32)
        self.base_font = pg.font.SysFont('arial', 30)
        self.active_bots = False
        self.active_tasks = False
        self.active_waves = False
        self.active_uncertainty = False
        self.active_strat = False
        self.bot = pg.image.load("smile.jpg").convert()
        self.pink = pg.image.load("pink.jpg").convert()
        self.red = pg.image.load("red.jpg").convert()
        self.Task = Task(self.screen)
        self.randomize = True
        self.result = 0
        self.missteps = 0
        self.eternal_bot_list = []
        self.eternal_task_list = []
        self.misguided_list = []
        self.distance_list = []
        self.result_list = []
        self.task_list = []
        self.bot_list = []

    def setup(self):
        self.busy_bot_list.clear()
        self.target_list.clear()
        self.score_list.clear()
        self.bot_list.clear()
        self.task_list.clear()
        while len(self.busy_bot_list) != int(self.user_bots):
            self.busy_bot_list.append(0)
        while len(self.target_list) != int(self.user_bots):
            self.target_list.append((0, 0))
        while len(self.score_list) != int(self.user_bots):
            self.score_list.append(0)

    def play(self):
        if self.active_game:
            if self.randomize:
                self.eternal_lists()
            self.setup()
            self.bot_list = deepcopy(self.eternal_bot_list)
            self.task_list = deepcopy(self.eternal_task_list)
            self.start_time = time.time()
            self.task_completed = 0
            print(self.user_strat)
            while self.task_completed != int(self.user_tasks) * int(self.user_waves):
                if int(self.user_strat) == 1:
                    self.Commited_Coordinated()
                elif int(self.user_strat) == 2:
                    self.Opportunistic()
                elif int(self.user_strat) == 3:
                    self.loners()
                elif int(self.user_strat) == 4:
                    self.commited_loners()
                elif int(self.user_strat) == 5:
                    self.distancefinder()
                    self.fitnesschecker(self.distance_list)
                    self.chase(self.bot, self.bot_list[self.result][0], self.bot_list[self.result][1], Task.x, Task.y)
                    self.task_completed += 1
            self.end_time = time.time()
            self.run_time = self.end_time - self.start_time
            self.screen.fill(pg.Color("grey"))
            pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
            self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
            self.draw_bots(self.bot_list)
            self.display_score()
            pg.display.flip()
            self.randomize = False
            time.sleep(2)

            self.show_ending()

    def commited_loners(self):
        for idx, bot in enumerate(self.bot_list):
            self.result = 0
            self.distance_list.clear()
            try:
                for task in self.task_list:
                    bot_distance = distance(self.bot_list[idx][0], self.bot_list[idx][1], task[0], task[1])
                    self.distance_list.append(bot_distance)
                self.result = self.distance_list.index(min(self.distance_list))
                holder = self.task_list[self.result]
                self.target_list[idx] = holder
                self.result = self.distance_list.index(min(self.distance_list))
                self.move_bot(idx, self.bot_list[idx][0], self.bot_list[idx][1],
                              self.target_list[idx][0], self.target_list[idx][1])
            except ValueError:
                pass
        self.screen.fill(pg.Color("grey"))
        pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
        self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
        self.draw_bots(self.bot_list)
        self.draw_misguided()
        self.unprepared_tasks(self.task_list)
        pg.display.flip()
        clock.tick(30)

    def loners(self):
        for idx, bot in enumerate(self.bot_list):
            self.result = 0
            self.distance_list.clear()
            for task in self.task_list:
                bot_distance = distance(bot[0], bot[1], task[0], task[1])
                self.distance_list.append(bot_distance)
            try:
                self.result = self.distance_list.index(min(self.distance_list))
                self.move_bot(idx, self.bot_list[idx][0], self.bot_list[idx][1],
                              self.task_list[self.result][0], self.task_list[self.result][1])
            except ValueError:
                pass
        self.screen.fill(pg.Color("grey"))
        pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
        self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
        self.draw_bots(self.bot_list)
        self.draw_misguided()
        self.unprepared_tasks(self.task_list)
        pg.display.flip()
        clock.tick(30)

    def Opportunistic(self):
        self.result = 0
        self.distance_list.clear()
        check = all(x == 1 for x in self.busy_bot_list)
        if check:
            counter_loop = 0
            for _ in self.bot_list:
                self.move_bot(counter_loop, self.bot_list[counter_loop][0], self.bot_list[counter_loop][1],
                              self.target_list[counter_loop][0], self.target_list[counter_loop][1])
                counter_loop += 1
                check = all(x == 1 for x in self.busy_bot_list)
                if not check:
                    break
            pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
            self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
            self.draw_bots(self.bot_list)
            self.draw_misguided()
            self.unprepared_tasks(self.task_list)
            pg.display.flip()
            clock.tick(60)
        target_in_list = False
        for task in self.task_list:
            self.distance_list.clear()
            for target in self.target_list:
                if target[0] == task[0]:
                    if target[1] == task[1]:
                        target_in_list = True
            if target_in_list:
                counter_loop = 0
                for _ in self.bot_list:
                    if self.target_list[counter_loop][0] == 0:
                        pass
                    else:
                        self.move_bot(counter_loop, self.bot_list[counter_loop][0], self.bot_list[counter_loop][1],
                                      self.target_list[counter_loop][0], self.target_list[counter_loop][1])
                    counter_loop += 1
                self.screen.fill(pg.Color("grey"))
                pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
                self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
                self.draw_bots(self.bot_list)
                self.draw_misguided()
                self.unprepared_tasks(self.task_list)
                pg.display.flip()
                clock.tick(60)
            else:
                for bot in self.bot_list:
                    bot_distance = distance(bot[0], bot[1], task[0], task[1])
                    self.distance_list.append(bot_distance)
                self.result = self.distance_list.index(min(self.distance_list))
                if self.busy_bot_list[self.result] == 1:
                    target_distance = distance(self.bot_list[self.result][0], self.bot_list[self.result][1],
                                               self.target_list[self.result][0], self.target_list[self.result][1])
                    self.score_list[self.result] = int(target_distance)
                    if self.score_list[self.result] > int(self.distance_list[self.result]):
                        print("bot changed task for new one")
                        self.target_list[self.result] = task[0], task[1]
                        self.busy_bot_list[self.result] = 1
                        counter_loop = 0
                        for _ in self.bot_list:
                            if self.target_list[counter_loop][0] == 0:
                                pass
                            else:
                                self.move_bot(counter_loop, self.bot_list[counter_loop][0],
                                              self.bot_list[counter_loop][1],
                                              self.target_list[counter_loop][0], self.target_list[counter_loop][1])
                            counter_loop += 1
                    pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
                    self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
                    self.draw_bots(self.bot_list)
                    self.draw_misguided()
                    self.unprepared_tasks(self.task_list)
                    pg.display.flip()
                    clock.tick(60)
                elif self.busy_bot_list[self.result] == 0:
                    self.target_list[self.result] = task[0], task[1]
                    self.busy_bot_list[self.result] = 1
                    counter_loop = 0
                    for _ in self.bot_list:
                        if self.target_list[counter_loop][0] == 0:
                            pass
                        else:
                            self.move_bot(counter_loop, self.bot_list[counter_loop][0], self.bot_list[counter_loop][1],
                                          self.target_list[counter_loop][0], self.target_list[counter_loop][1])
                        counter_loop += 1
                    self.screen.fill(pg.Color("grey"))
                    pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
                    self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
                    self.draw_bots(self.bot_list)
                    self.draw_misguided()
                    self.unprepared_tasks(self.task_list)
                    pg.display.flip()
                    clock.tick(60)

    def Commited_Coordinated(self):
        target_in_list = False
        for task in self.task_list:
            self.distance_list.clear()
            for target in self.target_list:
                if target[0] == task[0]:
                    if target[1] == task[1]:
                        target_in_list = True
            if target_in_list:
                counter_loop = 0
                for _ in self.bot_list:
                    if self.target_list[counter_loop][0] == 0:
                        pass
                    else:
                        self.move_bot(counter_loop, self.bot_list[counter_loop][0], self.bot_list[counter_loop][1],
                                      self.target_list[counter_loop][0], self.target_list[counter_loop][1])
                    counter_loop += 1
                self.screen.fill(pg.Color("grey"))
                pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
                self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
                self.draw_bots(self.bot_list)
                self.draw_misguided()
                self.unprepared_tasks(self.task_list)
                pg.display.flip()
                clock.tick(60)
            else:
                for bot in self.bot_list:
                    bot_distance = distance(bot[0], bot[1], task[0], task[1])
                    self.distance_list.append(bot_distance)
                counter_two = 0
                for x in self.busy_bot_list:
                    if x == 1:
                        self.distance_list[counter_two] = 9999
                        counter_two += 1
                    else:
                        counter_two += 1
                check = all(x == 1 for x in self.busy_bot_list)
                if check:
                    break
                self.result = self.distance_list.index(min(self.distance_list))
                self.target_list[self.result] = task[0], task[1]
                self.busy_bot_list[self.result] = 1
        self.screen.fill(pg.Color("grey"))
        pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
        self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
        self.draw_bots(self.bot_list)
        self.draw_misguided()
        self.unprepared_tasks(self.task_list)
        pg.display.flip()
        clock.tick(60)

    def show_start(self):
        color = pg.Color('grey37')
        color_active = pg.Color('grey100')
        color1 = pg.Color('grey37')
        color_active1 = pg.Color('grey100')
        color2 = pg.Color('grey37')
        color_active2 = pg.Color('grey100')
        color3 = pg.Color('grey37')
        color_active3 = pg.Color('grey100')
        color4 = pg.Color('grey37')
        color_active4 = pg.Color('grey100')
        bigsmile = pg.image.load("big smile.jpg").convert()
        self.screen.fill(pg.Color("grey"))
        if self.active_bots:
            color = color_active
        if self.active_tasks:
            color1 = color_active1
        if self.active_waves:
            color2 = color_active2
        if self.active_uncertainty:
            color3 = color_active3
        if self.active_strat:
            color4 = color_active4
        pg.draw.rect(self.screen, color, self.input_bots)
        pg.draw.rect(self.screen, color1, self.input_tasks)
        pg.draw.rect(self.screen, color2, self.input_waves)
        pg.draw.rect(self.screen, color3, self.input_uncertainty)
        pg.draw.rect(self.screen, color4, self.input_strat)
        text_surface = self.base_font.render(self.user_bots, True, (pg.Color("black")))
        text_surface2 = self.base_font.render(self.user_tasks, True, (pg.Color("black")))
        text_surface3 = self.base_font.render(self.user_waves, True, (pg.Color("black")))
        text_surface4 = self.base_font.render(self.user_uncertainty, True, (pg.Color("black")))
        text_surface5 = self.base_font.render(self.user_strat, True, (pg.Color("black")))
        self.screen.blit(text_surface, self.input_bots)
        self.screen.blit(text_surface2, self.input_tasks)
        self.screen.blit(text_surface3, self.input_waves)
        self.screen.blit(text_surface4, self.input_uncertainty)
        self.screen.blit(text_surface5, self.input_strat)
        font = pg.font.SysFont('arial', 30)
        line1 = font.render(f"How many Bots (e.g., 10, 20 ,30)?: ", True, (pg.Color("black")))
        self.screen.blit(line1, (100, 100))
        line2 = font.render(f"How many Tasks on screen at once (e.g., 10, 20 ,30)?: ", True, (pg.Color("black")))
        self.screen.blit(line2, (100, 150))
        line3 = font.render(f"How many waves of Tasks will appear (e.g., 1, 2, 3, 4)?: ", True, (pg.Color("black")))
        self.screen.blit(line3, (100, 200))
        line34 = font.render(f"What is the uncertainty (e.g., 5, 10, 15)?: ", True, (pg.Color("black")))
        self.screen.blit(line34, (100, 250))
        line4 = font.render(f"Which Task Allocation Strategy?: ", True, (pg.Color("black")))
        self.screen.blit(line4, (100, 300))
        line5 = font.render(f"1 for Committed and Mutual Exclusive ", True, (pg.Color("black")))
        self.screen.blit(line5, (100, 350))
        line6 = font.render(f"2 for Opportunistic and Mutual Exclusive ", True, (pg.Color("black")))
        self.screen.blit(line6, (100, 400))
        line7 = font.render(f"3 for Opportunistic and Individual ", True, (pg.Color("black")))
        self.screen.blit(line7, (100, 450))
        line8 = font.render(f"4 for Committed and Individual ", True, (pg.Color("black")))
        self.screen.blit(line8, (100, 500))
        line8 = font.render(f"5 for Simple Allocation", True, (pg.Color("dark grey")))
        self.screen.blit(line8, (100, 550))
        self.screen.blit(bigsmile, (850, 100))
        pg.display.flip()
        clock.tick(60)

    def show_ending(self):
        self.screen.fill(pg.Color("grey"))
        font = pg.font.SysFont('arial', 30)
        line1 = font.render(f"Tasks Completed: {self.task_completed}", True, (pg.Color("black")))
        self.screen.blit(line1, (450, 300))
        line3 = font.render(
            f"Time taken to reach {self.task_completed} tasks with {len(self.bot_list)} bots: {round(self.run_time, 2)}"
            f" seconds", True, (pg.Color("black")))
        self.screen.blit(line3, (450, 350))
        line2 = font.render("To restart the program, press Enter.", True, (pg.Color("black")))
        self.screen.blit(line2, (450, 400))

        pg.display.flip()

    def move_bot(self, var, x1, y1, x2, y2):
        if random.randint(0, 100) < int(self.user_uncertainty):
            if random.randint(0, 1) == 1:
                x1 -= random.randint(1, 2) * 15
            if random.randint(0, 1) == 1:
                x1 += random.randint(1, 2) * 15
            if random.randint(0, 1) == 1:
                y1 -= random.randint(1, 2) * 15
            if random.randint(0, 1) == 1:
                y1 += random.randint(1, 2) * 15
            self.bot_list[var][0] = x1
            self.bot_list[var][1] = y1
            self.misguided_list.append((x1, y1))
            self.missteps += 1
        else:
            if x2 < x1:
                x1 -= 15
            elif x2 > x1:
                x1 += 15
            if y2 < y1:
                y1 -= 15
            elif y2 > y1:
                y1 += 15
            self.bot_list[var][0] = x1
            self.bot_list[var][1] = y1
            if x1 == x2 and y1 == y2:
                self.busy_bot_list[var] = 0
                try:
                    for idx, task in enumerate(self.task_list):
                        if self.task_list[idx][0] == x2 and self.task_list[idx][1] == y2:
                            self.task_list.pop(idx)
                            self.task_completed += 1
                            self.target_list[var] = 0, 0
                except IndexError:
                    pass

    def fitnesschecker(self, distance_list):
        for _ in distance_list:
            fitness = _ * random.randint(2, 4)
            self.result_list.append(fitness)
        self.result = self.result_list.index(min(self.result_list))

    def chase(self, var, x1, y1, x2, y2):

        while x1 != x2 or y1 != y2:
            if x2 < x1:
                x1 -= 15
            elif x2 > x1:
                x1 += 15
            if y2 < y1:
                y1 -= 15
            elif y2 > y1:
                y1 += 15
            self.bot_list[self.result][0] = x1
            self.bot_list[self.result][1] = y1
            self.screen.fill(pg.Color("grey"))
            pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
            self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
            self.draw_bots(self.bot_list)
            self.unprepared_tasks(self.task_list)
            self.Task.draw()
            self.draw_tasks()
            self.screen.blit(var, (x1, y1))
            pg.display.flip()
            clock.tick(60)
        try:
            self.task_list.pop(0)
            Task.x = self.task_list[0][0]
            Task.y = self.task_list[0][1]
        except IndexError:
            pass
        self.distance_list.clear()
        self.result_list.clear()

    def eternal_lists(self):
        self.eternal_bot_list.clear()
        self.eternal_task_list.clear()
        while len(self.eternal_bot_list) != int(self.user_bots):
            Bots.x_pos = random.randint(20, 72) * 15
            Bots.y_pos = random.randint(1, 50) * 15
            self.eternal_bot_list.append([Bots.x_pos, Bots.y_pos])

        task_created = (int(self.user_tasks) * int(self.user_waves))
        while task_created != 0:
            task_created -= 1
            Task.x_pos = random.randint(20, 72) * 15
            Task.y_pos = random.randint(1, 50) * 15
            self.eternal_task_list.append([Task.x_pos, Task.y_pos])

    def unprepared_tasks(self, task_list):
        index = 0
        unfocused_task = pg.image.load("blue.jpg").convert()
        for _ in task_list:
            self.screen.blit(unfocused_task, (self.task_list[index][0], self.task_list[index][1]))
            index += 1

    def draw_tasks(self):
        try:
            self.screen.blit(self.pink, (self.task_list[1][0], self.task_list[1][1]))
            self.screen.blit(self.red, (self.task_list[2][0], self.task_list[2][1]))
        except IndexError:
            pass

    def draw_bots(self, bot_list):
        index = 0
        self.display_score()
        for _ in bot_list:
            new_bot = pg.image.load("smile.jpg").convert()
            self.screen.blit(new_bot, (self.bot_list[index][0], self.bot_list[index][1]))
            index += 1

    def draw_misguided(self):
        index = 0
        self.display_score()
        for _ in self.misguided_list:
            misguided_bot = pg.image.load("gasp.jpg").convert()
            self.screen.blit(misguided_bot, (self.misguided_list[index][0], self.misguided_list[index][1]))
            index += 1
        self.misguided_list.clear()

    def display_score(self):
        font = pg.font.SysFont('arial', 30)
        score = font.render(f"Tasks Completed:{self.task_completed} / {(int(self.user_tasks) * int(self.user_waves))}",
                            True,
                            (pg.Color("black")))
        self.screen.blit(score, (15, 15))

    def distancefinder(self):
        for bot in self.bot_list:
            bot_distance = distance(bot[0], bot[1], Task.x, Task.y)
            self.distance_list.append(bot_distance)

    def reset(self):
        self.result = 0
        self.user_bots = ""
        self.user_tasks = ""
        self.user_waves = ""
        self.user_uncertainty = ""
        self.user_strat = ""
        self.distance_list.clear()
        self.result_list.clear()
        self.randomize = True

    def run(self):
        running = True
        while running:
            for event in pg.event.get():

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_bots.collidepoint(event.pos):
                        self.active_bots = True
                    else:
                        self.active_bots = False

                if event.type == pg.KEYDOWN:
                    if self.active_bots:
                        if event.key == pg.K_BACKSPACE:
                            self.user_bots = self.user_bots[:-1]
                        else:
                            self.user_bots += event.unicode

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_tasks.collidepoint(event.pos):
                        self.active_tasks = True
                    else:
                        self.active_tasks = False

                if event.type == pg.KEYDOWN:
                    if self.active_tasks:
                        if event.key == pg.K_BACKSPACE:
                            self.user_tasks = self.user_tasks[:-1]
                        else:
                            self.user_tasks += event.unicode

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_waves.collidepoint(event.pos):
                        self.active_waves = True
                    else:
                        self.active_waves = False

                if event.type == pg.KEYDOWN:
                    if self.active_waves:
                        if event.key == pg.K_BACKSPACE:
                            self.user_waves = self.user_waves[:-1]
                        else:
                            self.user_waves += event.unicode

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_uncertainty.collidepoint(event.pos):
                        self.active_uncertainty = True
                    else:
                        self.active_uncertainty = False

                if event.type == pg.KEYDOWN:
                    if self.active_uncertainty:
                        if event.key == pg.K_BACKSPACE:
                            self.user_uncertainty = self.user_uncertainty[:-1]
                        else:
                            self.user_uncertainty += event.unicode

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_strat.collidepoint(event.pos):
                        self.active_strat = True
                    else:
                        self.active_strat = False

                if event.type == pg.KEYDOWN:
                    if self.active_strat:
                        if event.key == pg.K_BACKSPACE:
                            self.user_strat = self.user_strat[:-1]
                        else:
                            self.user_strat += event.unicode

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.active_game = True
                        self.play()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.active_game = False
                        self.reset()
                        self.show_start()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.randomize = True

                elif event.type == pg.QUIT:
                    sys.exit()

            if not self.active_game:
                self.show_start()


def distance(x, y, x2, y2):
    return math.sqrt((x - x2) ** 2) + (math.sqrt((y - y2) ** 2))


if __name__ == '__main__':
    game = Game()
    game.run()

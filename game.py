import sys, pygame as pg
import random
import time
import math

clock = pg.time.Clock()


class Task:
    task_completed = 0
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
        self.end_time = 0
        self.start_time = 0
        self.run_time = 0
        self.screen = pg.display.set_mode((1390, 790))
        self.screen.fill(pg.Color("grey"))
        pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
        self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
        pg.display.flip()
        self.bot = pg.image.load("smile.jpg").convert()
        self.pink = pg.image.load("pink.jpg").convert()
        self.red = pg.image.load("red.jpg").convert()
        self.Task = Task(self.screen)
        Task.task_tomake = 29
        self.result = 0
        self.busy_bot_list = []
        while len(self.busy_bot_list) != 10:
            self.busy_bot_list.append(0)
        self.target_list = []
        while len(self.target_list) != 10:
            self.target_list.append((0, 0))
        self.bot_list = []
        self.distance_list = []
        self.result_list = []
        self.task_pos = [Task.x, Task.y]
        self.Task.draw()
        self.task_list = [self.task_pos]
        self.task_creator(self.task_list)
        self.bot_control(self.bot_list)
        self.draw_bots(self.bot_list)
        self.play()

    def play(self):
        self.Task.draw()
        # self.start_time = time.time()
        while Task.task_completed != 30:
            self.Commited_Coordinated()
            # self.distancefinder(self.bot_list)
            # self.fitnesschecker(self.distance_list)
            # self.chase(self.bot, self.bot_list[self.result][0], self.bot_list[self.result][1], Task.x, Task.y)
            # Task.task_completed += 1
        # self.end_time = time.time()
        # self.run_time = self.end_time - self.start_time
        # self.screen.fill(pg.Color("grey"))
        # pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
        # self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
        # self.draw_bots(self.bot_list)
        # self.display_score()
        # pg.display.flip()
        # time.sleep(2)
        # self.show_ending()

    def Commited_Coordinated(self):
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
            self.screen.fill(pg.Color("grey"))
            pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(300, 15, 1080, 750), 10)
            self.screen.fill((0, 70, 0,), (305, 20, 1070, 740))
            self.draw_bots(self.bot_list)
            self.unprepared_tasks(self.task_list)
            pg.display.flip()
            clock.tick(50)
        else:
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
                    self.unprepared_tasks(self.task_list)
                    pg.display.flip()
                    clock.tick(50)
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
        self.unprepared_tasks(self.task_list)
        pg.display.flip()
        clock.tick(50)

    def show_ending(self):
        self.screen.fill(pg.Color("grey"))
        font = pg.font.SysFont('arial', 30)
        line1 = font.render(f"Tasks Completed: {Task.task_completed}", True, (pg.Color("black")))
        self.screen.blit(line1, (450, 300))
        line3 = font.render(
            f"Time taken to reach {Task.task_completed} tasks with {len(self.bot_list)} bots: {round(self.run_time, 2)}"
            f" seconds", True, (pg.Color("black")))
        self.screen.blit(line3, (450, 350))
        line2 = font.render("To restart the program, press Enter.", True, (pg.Color("black")))
        self.screen.blit(line2, (450, 400))
        pg.display.flip()

    def move_bot(self, var, x1, y1, x2, y2):
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
                        Task.task_completed += 1
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
            clock.tick(20)
        try:
            self.task_list.pop(0)
            Task.x = self.task_list[0][0]
            Task.y = self.task_list[0][1]
        except IndexError:
            pass
        self.distance_list.clear()
        self.result_list.clear()

    def task_creator(self, task_list):
        task_created = Task.task_tomake
        while task_created != 0:
            task_created -= 1
            Task.x_pos = random.randint(20, 72) * 15
            Task.y_pos = random.randint(1, 50) * 15
            task_list.append([Task.x_pos, Task.y_pos])

    def bot_control(self, bot_list):
        while len(bot_list) != 10:
            Bots.x_pos = random.randint(20, 72) * 15
            Bots.y_pos = random.randint(1, 50) * 15
            bot_list.append([Bots.x_pos, Bots.y_pos])

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

    def display_score(self):
        font = pg.font.SysFont('arial', 30)
        score = font.render(f"Tasks Completed:{Task.task_completed} / {Task.task_tomake + 1}", True,
                            (pg.Color("black")))
        self.screen.blit(score, (15, 15))

    def distancefinder(self, list):
        for bot in self.bot_list:
            bot_distance = distance(bot[0], bot[1], Task.x, Task.y)
            self.distance_list.append(bot_distance)

    def reset(self):
        Task.task_completed = 0
        self.result = 0
        self.bot_list = []
        self.distance_list = []
        self.result_list = []
        self.task_pos = [Task.x, Task.y]
        self.task_list = [self.task_pos]
        self.Task.draw()
        self.task_creator(self.task_list)
        self.bot_control(self.bot_list)
        self.draw_bots(self.bot_list)
        self.play()

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.reset()
                elif event.type == pg.QUIT:
                    sys.exit()


def checkIfDuplicates_1(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True


def distance(x, y, x2, y2):
    return math.sqrt((x - x2) ** 2) + (math.sqrt((y - y2) ** 2))


if __name__ == '__main__':
    game = Game()
    game.run()

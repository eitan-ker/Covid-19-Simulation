import numpy as np
import pygame
from random import randrange
import copy
import matplotlib.pyplot as plt
import time

WIDTH, HEIGHT = 1400, 850
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
font1 = pygame.font.Font(None, 32)
font2 = pygame.font.Font(None, 22)

pygame.display.set_caption("COVID 19 Simulation")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 2
num_of_cells = 200

update_object_list = []


class Game:

    def __init__(self, n, n0, n1, n2, p, pv, t):
        # PARAMS:
        self.simulation = ""
        self.N = n
        self.N0 = n0
        self.N1 = n1
        self.N2 = n2
        self.P = p
        self.Pv = pv
        self.T = t

    def window_display_and_init(self):
        grid = self.make_sections()
        pygame.display.update()

        return grid

    def make_sections(self):
        self.simulation = Grid(self.N, self.N0, self.N1, self.N2)  # constructor
        # update_object_list.append(grid)
        # params_grid = pygame.Rect(0, 0, 400, 200)
        #
        # pygame.draw.rect(WIN, SECTION_COLOR, params_grid, 2)

    def update(self):
        grid = self.simulation.grid
        # grid2 = self.simulation.grid

        z = 2

        # healthy/recovered gets sick
        # grid2 = copy.copy(grid)
        for i in range(num_of_cells):
            for j in range(num_of_cells):
                if grid[i][j].state == 1:
                    # check if neighbours
                    for x in grid[i][j].neighbours:
                        if grid[x[0]][x[1]].state == 0:
                            chance = (randrange(99) + 1) / 100
                            if chance <= self.P:
                                grid[x[0]][x[1]].change_status(1)
                                self.simulation.add_sick_cell()
                        elif grid[x[0]][x[1]].state == 2:
                            chance = (randrange(99) + 1) / 100
                            if chance <= self.Pv:
                                grid[x[0]][x[1]].change_status(1)
                                self.simulation.add_sick_cell()

        z = 2

        # generations of sick people
        for i in range(num_of_cells):
            for j in range(num_of_cells):
                grid[i][j].generation_counter()
                if grid[i][j].state == 1 and grid[i][j].num_of_generations >= self.T:
                    grid[i][j].change_status(2)
                if grid[i][j].state == 2 and grid[i][j].num_of_generations >= self.T:
                    grid[i][j].change_status(0)

        z = 2

        grid3 = copy.deepcopy(grid)
        # # deal with population of cells
        for i in range(num_of_cells):
            for j in range(num_of_cells):
                random_move = randrange(9)
                cell_to_move = grid3[i][j].neighbours[random_move]

                #     # check if cell to move is empty
                #     # if cell is empty - populate
                if ((grid[cell_to_move[0]][cell_to_move[1]].state == 3) and
                        (grid3[cell_to_move[0]][cell_to_move[1]].state == 3)):
                    state_to_change = grid[i][j].state
                    # move cell, and change status of previous cell to empty
                    grid[cell_to_move[0]][cell_to_move[1]].change_state(state_to_change)
                    grid[i][j].change_status(3)


        z = 2

        for i in range(num_of_cells):
            for j in range(num_of_cells):
                WIN.fill(grid[i][j].colour, grid[i][j].reck)
                pygame.draw.rect(WIN, BLACK, grid[i][j].reck, 1)


class Grid:
    size = 800

    # def __init__(self, grid):
    #     self.grid = grid

    def __init__(self, N, N0, N1, N2):
        self.grid = []
        simulation_block = pygame.Rect(595, 5, self.size, self.size)
        cell_x = simulation_block.x
        cell_y = simulation_block.y
        pygame.draw.rect(WIN, (100, 100, 100), simulation_block, 5)

        shuffled_state_list = self.make_shuffled_list(N, N0, N1, N2)
        counter = 0

        for x in range(num_of_cells):
            self.grid.append([])
            for y in range(num_of_cells):
                # random_state = randrange(4)
                # cell = Cell(random_state, x, y, cell_x, cell_y)
                cell = Cell(shuffled_state_list[counter], x, y, cell_x, cell_y)
                self.grid[x].append(cell)
                WIN.fill(cell.colour, cell.reck)
                pygame.draw.rect(WIN, BLACK, cell.reck, 1)
                counter += 1
        self.empty_cells = []
        self.sick_cells = 0
        for i in range(num_of_cells):
            for j in range(num_of_cells):
                if self.grid[i][j].state == 1:
                    self.sick_cells += 1
        z = 2

    def add_sick_cell(self):
        self.sick_cells += 1

    def make_shuffled_list(self, N, N0, N1, N2):
        arr = []
        for i in range(N0):
            arr.append(0)
        for i in range(N1):
            arr.append(1)
        for i in range(N2):
            arr.append(2)
        total = (num_of_cells * num_of_cells)
        for i in range(total - N):
            arr.append(3)
        np.random.shuffle(arr)
        return arr

    def find_empty_cells(self):
        empty_cells = []
        for i in range(num_of_cells):
            for j in range(num_of_cells):
                # save all empty cells 2 gens forward
                if len(self.grid[i][j].list_of_potential_population) == 0 and self.grid[i][j].state == 3:
                    self.empty_cells.append((i, j))


class Cell:
    size = 4

    # object state
    # color (0=healty, 1=sick, 2=recovery, 3=unpopulated)
    def __init__(self, state, x, y, cell_x, cell_y):
        self.state = state
        self.num_of_generations = 0
        self.colour = self.get_state_color(state)
        self.x_index = x
        self.y_index = y
        self.neighbours = self.find_neighbours()
        # self.neighbours = []
        # change neighbour to cell object
        self.reck = pygame.Rect(cell_x + x * self.size, cell_y + y * self.size, self.size, self.size)
        # self.find_neighbours()

    def find_neighbours(self):
        neighbours = []
        for i in range(3):
            for j in range(3):
                neighbour_x = (self.x_index + (i - 1)) % num_of_cells
                neighbour_y = (self.y_index + (j - 1)) % num_of_cells
                neighbours.append((neighbour_x, neighbour_y))
        return neighbours

    def change_state(self, state):

        if self.state != state:
            self.state = state
            self.colour = self.get_state_color(state)

    def change_status(self, state):

        self.state = state
        self.colour = self.get_state_color(state)
        self.num_of_generations = 0

    def generation_counter(self):
        self.num_of_generations = self.num_of_generations + 1

    def add_potintial_cell(self, x, y):
        self.list_of_potential_population.append((x, y))

    def delete_potintial_cells(self):
        self.list_of_potential_population.clear()

    def get_state_color(self, state):
        if state == 0:
            return (0, 255, 0)
        elif state == 1:
            return (255, 0, 0)
        elif state == 2:
            return (0, 0, 255)
        else:
            return (0, 0, 0)


def check_data(grid):
    num_of_healty = 0
    num_of_sick = 0
    num_of_recovered = 0
    for i in range(num_of_cells):
        for j in range(num_of_cells):
            state = grid[i][j].state
            if state == 0:
                num_of_healty += 1
            elif state == 1:
                num_of_sick += 1
            elif state == 2:
                num_of_recovered += 1
    return num_of_healty, num_of_sick, num_of_recovered


def check_percentage(num_of_people, array):
    sum = 0
    size = len(array)
    for i in range(size):
        sum += array[i]
    avarage = sum / num_of_people
    return avarage


def find_distribution(grid):
    healthy, sick, recovering = 0, 0, 0
    for i in range(num_of_cells):
        for j in range(num_of_cells):
            if grid[i][j].state == 0:
                healthy += 1
            elif grid[i][j].state == 1:
                sick += 1
            elif grid[i][j].state == 2:
                recovering += 1
    return healthy, sick, recovering


# main func to iterate over the changes in the board.
def main():
    #
    # open menu get params
    #
    num_people = 0
    num_healthy = 0
    num_sick = 0
    num_recovering = 0
    chance_healthy = 0
    chance_recovering = 0
    t = 0

    instructions_text = "Click the Rectangle and please type the following:"
    instructions2_text = "# People, # Healthy, # Sick, # Recovering, % Infection Healthy, % Infection Recovering and " \
                         "Number of Sick Iterations. example: 1000,500,200,300,0.5,0.5,5"
    user_input = ''
    submit_text = "Start"
    num_of_healthy = ''
    num_of_sick = ''
    num_of_recovering = ''
    error = ''

    instructions_rect = pygame.Rect(20, 20, 50, 32)
    instructions2_rect = pygame.Rect(20, 70, 50, 32)
    user_input_rect = pygame.Rect(20, 120, 450, 50)
    submit_rect = pygame.Rect(100, 200, 140, 32)

    error_rect = pygame.Rect(200, 350, 450, 50)

    num_of_healthy_rect = pygame.Rect(20, 300, 100, 32)
    num_of_sick_rect = pygame.Rect(20, 350, 100, 32)
    num_of_recovering_rect = pygame.Rect(20, 400, 100, 32)

    color_active = pygame.Color('lightskyblue')
    color_passive = pygame.Color('gray')
    color = color_passive
    active = False
    submit_color = (255, 255, 255)

    flag = 0
    init_flag = 0
    runnning = 0
    ok = False

    game = ''

    # start game

    clock = pygame.time.Clock()
    run = True
    # init board and return objects
    # game.window_display_and_init()
    # self.simulation.find_empty_cells()

    # run game as long as run = true.
    iteration = 0
    while run:
        clock.tick(FPS)
        # loop over all events to check changes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # enter here only if simulation is not running yet
            if runnning == 0:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if user_input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    # check data and continue
                    if submit_rect.collidepoint(event.pos):
                        text = user_input
                        input = text.split(',')
                        try:
                            if len(input) < 7:
                                # error rect
                                # delete user_input
                                # mot allow to enter next lines
                                error = 'Error: Not Enough Arguments, Try again'
                                pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                error_text_surface = font1.render(error, True, (255, 255, 255))
                                WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                user_input = ''
                                pygame.display.update()
                                time.sleep(5)
                            else:
                                try:
                                    num_people = int(input[0])
                                    num_healthy = int(input[1])
                                    num_sick = int(input[2])
                                    num_recovering = int(input[3])
                                except:
                                    error = 'Error: N, N0, N1, N2 Must BE INTEGERS.'
                                    pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                    error_text_surface = font1.render(error, True, (255, 255, 255))
                                    WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                    # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                    user_input = ''
                                    pygame.display.update()
                                    time.sleep(5)
                                    raise
                                if num_people > 35000:
                                    error = 'Error: N Must BE N < 35000, Try again'
                                    pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                    error_text_surface = font1.render(error, True, (255, 255, 255))
                                    WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                    # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                    user_input = ''
                                    pygame.display.update()
                                    time.sleep(5)
                                elif num_people != (num_healthy + num_sick + num_recovering):
                                    error = 'Error: N Must BE N=N0+N1+N2, Try again'
                                    pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                    error_text_surface = font1.render(error, True, (255, 255, 255))
                                    WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                    # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                    user_input = ''
                                    pygame.display.update()
                                    time.sleep(5)
                                else:
                                    try:
                                        chance_healthy = float(input[4])
                                        chance_recovering = float(input[5])
                                        t = int(input[6])
                                    except:
                                        error = 'Error: P and Pv Must be float, T INTEGER.'
                                        pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                        error_text_surface = font1.render(error, True, (255, 255, 255))
                                        WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                        # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                        user_input = ''
                                        pygame.display.update()
                                        time.sleep(5)
                                        raise
                                    if chance_healthy > 1 or chance_healthy < 0:
                                        error = 'Error: P must be 0<P<1, Try again'
                                        pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                        error_text_surface = font1.render(error, True, (255, 255, 255))
                                        WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                        # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                        user_input = ''
                                        pygame.display.update()
                                        time.sleep(5)
                                    elif chance_recovering > 1 or chance_recovering < 0:
                                        error = 'Error: Pv must be 0<Pv<1, Try again'
                                        pygame.draw.rect(WIN, (255, 0, 0), error_rect, 2)
                                        error_text_surface = font1.render(error, True, (255, 255, 255))
                                        WIN.blit(error_text_surface, (error_rect.x + 5, error_rect.y + 10))
                                        # error_rect.w = max(100, error_text_surface.get_width() + 10)
                                        user_input = ''
                                        pygame.display.update()
                                        time.sleep(5)
                                    else:
                                        ok = True
                        except:
                            ok = False

                        if ok:
                            submit_color = (100, 100, 100)

                            num_people = int(input[0])
                            num_healthy = int(input[1])
                            num_sick = int(input[2])
                            num_recovering = int(input[3])
                            chance_healthy = float(input[4])
                            chance_recovering = float(input[5])
                            t = int(input[6])

                            flag = 1
                            init_flag = 1

                if event.type == pygame.KEYDOWN:
                    if active == True:
                        if event.key == pygame.K_BACKSPACE:
                            user_input = user_input[:-1]
                        else:
                            user_input += event.unicode

        WIN.fill((0, 0, 0))
        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(WIN, (0, 0, 0), instructions_rect, 2)
        pygame.draw.rect(WIN, (0, 0, 0), instructions2_rect, 2)
        pygame.draw.rect(WIN, color, user_input_rect, 2)
        pygame.draw.rect(WIN, submit_color, submit_rect)

        instructions_text_surface = font1.render(instructions_text, True, (255, 255, 255))
        WIN.blit(instructions_text_surface, (instructions_rect.x + 5, instructions_rect.y + 5))

        instructions_text_surface2 = font2.render(instructions2_text, True, (255, 255, 255))
        WIN.blit(instructions_text_surface2, (instructions2_rect.x + 5, instructions2_rect.y + 5))

        text_surface = font1.render(user_input, True, (255, 255, 255))
        WIN.blit(text_surface, (user_input_rect.x + 5, user_input_rect.y + 5))

        text_surface2 = font1.render(submit_text, True, (0, 0, 0))
        WIN.blit(text_surface2, (submit_rect.x + 5, submit_rect.y + 5))




        # pygame.display.flip()

        if flag == 1:
            if init_flag == 1:
                runnning = 1
                game = Game(num_people, num_healthy, num_sick, num_recovering, chance_healthy, chance_recovering, t)
                game.window_display_and_init()
                init_flag = 0

            generations = 'Generation: '
            iteration += 1


            generations = generations + str(iteration)
            generations_surface = font1.render(generations, True, (255, 255, 255))
            generation_rect = generations_surface.get_rect()
            generation_rect.center = (100, 500)
            WIN.blit(generations_surface, (generation_rect.x + 5, generation_rect.y + 5))


            game.update()

            healthy, sick, recovering = find_distribution(game.simulation.grid)
            healthy = str(healthy)
            sick = str(sick)
            recovering = str(recovering)

            pygame.draw.rect(WIN, (0, 255, 0), num_of_healthy_rect, 2)
            healthy_text_surface = font1.render(healthy, True, (255, 255, 255))
            WIN.blit(healthy_text_surface, (num_of_healthy_rect.x + 5, num_of_healthy_rect.y + 5))

            pygame.draw.rect(WIN, (255, 0, 0), num_of_sick_rect, 2)
            sick_text_surface = font1.render(sick, True, (255, 255, 255))
            WIN.blit(sick_text_surface, (num_of_sick_rect.x + 5, num_of_sick_rect.y + 5))

            pygame.draw.rect(WIN, (0, 0, 255), num_of_recovering_rect, 2)
            recovering_text_surface = font1.render(recovering, True, (255, 255, 255))
            WIN.blit(recovering_text_surface, (num_of_recovering_rect.x + 5, num_of_recovering_rect.y + 5))

            z = 2

        pygame.display.update()

    pygame.quit()


def check_generations_of_sick():
    p_array = []
    sick_array = []

    for p in range(10):
        print(p)
        num_of_people = 12000
        to_p = (p + 1) * 0.1
        p_array.append(to_p)
        game = Game(num_of_people, 0.9375, 0.05, 0.0125, to_p, to_p * 0.1, 5)
        clock = pygame.time.Clock()
        run = True
        # init board and return objects
        game.window_display_and_init()
        counter = 0
        iteration = 0
        # run game as long as run = true.
        while run:
            clock.tick(FPS)
            # loop over all events to check changes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                counter += 1

            game.update()
            iteration += 1

            total_people_were_sick = []
            if iteration == 12:
                sick_people = game.simulation.sick_cells
                # for i in range(num_of_cells):
                #     for j in range(num_of_cells):
                #         if game.simulation.grid[i][j].was_sick == 1:
                #             sick_people += 1
                total_people_were_sick.append(sick_people)
                # print(sick_people)
                run = False

        T_sick = check_percentage(num_of_people, total_people_were_sick)
        sick_array.append(T_sick)

    plt.plot(p_array, sick_array, color='red', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='gray', markersize=12)
    plt.xlabel("Change Of Infections\nPv =  10% P")
    plt.ylabel("Percentage")
    plt.title("Infection Rate")
    plt.show()

    pygame.quit()


def check_density():
    num_of_people_array = []
    populated_per = []
    healthy_per = []
    sick_per = []
    recovered_per = []

    for iter in range(20):
        print(iter)
        # start game
        num_of_people = (iter + 1) * 1600
        populated_per.append(num_of_people / (num_of_cells * num_of_cells))
        game = Game(num_of_people, 0.9375, 0.05, 0.0125, 0.15, 0.015, 5)
        num_of_people_array.append(num_of_people)

        clock = pygame.time.Clock()
        run = True

        # init board and return objects
        game.window_display_and_init()
        # self.simulation.find_empty_cells()

        counter = 0
        iteration = 0

        num_of_healty = 0
        num_of_sick = 0
        num_of_recovered = 0
        num_of_healty_array = []
        num_of_sick_array = []
        num_of_recovered_array = []

        # run game as long as run = true.
        while run:
            clock.tick(FPS)
            # loop over all events to check changes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                counter += 1

            game.update()

            num_of_healty, num_of_sick, num_of_recovered = check_data(game.simulation.grid)
            # num_of_healty_array.append(num_of_healty)
            # num_of_sick_array.append(num_of_sick)
            # num_of_recovered_array.append(num_of_recovered)

            iteration += 1

            if iteration == 11:
                num_of_healty_array.append(num_of_healty)
                num_of_sick_array.append(num_of_sick)
                num_of_recovered_array.append(num_of_recovered)
                run = False

        healty = check_percentage(num_of_people, num_of_healty_array)
        sick = check_percentage(num_of_people, num_of_sick_array)
        recovered = check_percentage(num_of_people, num_of_recovered_array)

        healthy_per.append(healty)
        sick_per.append(sick)
        recovered_per.append(recovered)

    plt.plot(num_of_people_array, healthy_per, color='green', linestyle='dashed',
             linewidth=3,
             marker='o', markerfacecolor='gray', markersize=12)
    plt.plot(num_of_people_array, sick_per, color='red', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='gray', markersize=12)
    plt.plot(num_of_people_array, recovered_per, color='blue', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='gray', markersize=12)
    plt.plot(num_of_people_array, populated_per, color='black', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='gray', markersize=12)

    plt.xlabel("Number of people")
    plt.ylabel("Percentage")

    plt.title("Density graph")

    plt.show()

    z = 2
    pygame.quit()


def test():
    # check_density()
    check_generations_of_sick()


if __name__ == '__main__':
    main()
    # test()

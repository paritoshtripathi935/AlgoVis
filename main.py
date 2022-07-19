import pygame
import random
pygame.init()
import math


# class for global variables
# global variables are variables that are accessible from all functions
# class drawInformation


class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)
    GREY = (128, 128, 128)
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont("comicsansms", 20)
    LARGE_FONT = pygame.font.SysFont("comicsansms", 35)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):  # constructor
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))  # create window
        pygame.display.set_caption("AlgoVisualizer") # set window title

        self.set_list(lst) # list of nodes
    

    def set_list(self, lst): # set list of nodes
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.pixel_width = round((self.width - self.SIDE_PAD) / len(lst)) # width of drwaing area
        self.pixel_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR) # fill background with white color (default) or with color specified in constructor
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))
    
    controls = draw_info.FONT.render( # draw text on screen (text, color, position) (x, y, text)
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 35)) # draw text on screen (text, color, position) (x, y, text)
    
    
    sorting = draw_info.FONT.render( # draw text on screen (text, color, position) (x, y, text)
        "I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 55)) # draw text on screen (text, color, position) (x, y, text)
    
    draw_list(draw_info)
    pygame.display.update()
    

def draw_list(draw_info, color_postions={}, clear_bg=False):

    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD) 
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.pixel_width  # x coordinate of node i in pixels (left to right) (center of node) 
        y = draw_info.height - (val - draw_info.min_val) * draw_info.pixel_height # y coordinate of node i in pixels (top to bottom) (center of node)
        
        color = draw_info.GRADIENTS[i % 3]

        if i in color_postions:
            color = color_postions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.pixel_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()


def generate_random_list(n, min_val, max_val):  # generate random list of n elements
    lst = []
    for i in range(n):
        lst.append(random.randint(min_val, max_val))
    return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        j = i
        while j > 0 and (lst[j] < lst[j - 1] and ascending) or (lst[j] > lst[j - 1] and not ascending):
            lst[j], lst[j - 1] = lst[j - 1], lst[j]
            draw_list(draw_info, {j: draw_info.GREEN, j - 1: draw_info.RED}, True)
            yield True
            j -= 1

    return lst


def main():   # main event loop
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_random_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sorting_algo_generator)  # get next element from generator
            except StopIteration:
                sorting = False  # stop sorting
        else:
            draw(draw_info, sorting_algo_name, ascending)  # draw list

        for event in pygame.event.get():  # pygame event get 
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_random_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
                
    pygame.quit()


if __name__ == "__main__":  # main function call (only if file is run directly) (not if file is imported)
    main()
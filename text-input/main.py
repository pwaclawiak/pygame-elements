import random
import pygame


pygame.init()

##############==============-------------- SET UP GLOBAL VARIABLES AND CONSTANTS --------------==============##############
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

exit_game = False
current_events = []

title_font = pygame.font.Font(size = 150)
label_font = pygame.font.Font(size = 70)
input_font = pygame.font.Font(size = 40)

##############==============-------------- SET UP VIEW VARIABLES --------------==============##############
cursor_tick_event = pygame.event.Event(12345, {"name": "CURSOR_TICK"})  # Integer value not used by other events
cursor_tick_event_set = False
show_cursor = True

final_input_1_value = ""
final_input_2_value = ""

tmp_input_1_value = ""
tmp_input_2_value = ""

input_1_done = False
input_2_done = False

input_1_label = label_font.render("Label 1", True, 'white')
input_2_label = label_font.render("Label 2", True, 'white')

label_1_width = input_1_label.get_width()
label_2_width = input_2_label.get_width()

cursor_gap_above_line = 1  # value in pixels
cursor_width = 2  # pixels as well
cursor_height = input_font.get_height() - cursor_gap_above_line

##############==============-------------- VIEW FUNCTION --------------==============##############
def text_input_view(screen):
    global show_cursor, cursor_tick_event_set
    global input_1_done, input_2_done
    global tmp_input_1_value, tmp_input_2_value
    global final_input_1_value, final_input_2_value
    
    if not cursor_tick_event_set:
        pygame.time.set_timer(cursor_tick_event, 700)
        cursor_tick_event_set = True

    input_1_div_pos = (SCREEN_WIDTH / 3 - label_1_width, 100)
    input_2_div_pos = (SCREEN_WIDTH / 3 * 2, 100)

    screen.blit(input_1_label, input_1_div_pos)
    screen.blit(input_2_label, input_2_div_pos)
    
    input_1_line = pygame.draw.line(screen, "white", (input_1_div_pos[0]-30, input_1_div_pos[1]+100), (input_1_div_pos[0]+label_1_width+30, input_1_div_pos[1]+100))
    input_2_line = pygame.draw.line(screen, "white", (input_2_div_pos[0]-30, input_2_div_pos[1]+100), (input_2_div_pos[0]+label_2_width+30, input_2_div_pos[1]+100))
    
    input_1_render = input_font.render(tmp_input_1_value, True, "white")
    input_2_render = input_font.render(tmp_input_2_value, True, "white")
    
    cursor_y = input_1_line.top - input_font.get_height() - cursor_gap_above_line
    
    screen.blit(input_1_render, (input_1_line.left, cursor_y))
    screen.blit(input_2_render, (input_2_line.left, cursor_y))

    if not input_1_done:
        cursor = pygame.Rect(input_1_line.left + input_1_render.get_width(), cursor_y, cursor_width, cursor_height)
    elif not input_2_done:
        cursor = pygame.Rect(input_2_line.left + input_2_render.get_width(), cursor_y, cursor_width, cursor_height)
    else:
        cursor = None

    for event in current_events:
        if event.type == cursor_tick_event.type:
            show_cursor = not show_cursor
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_TAB):
                if not input_1_done:
                    input_1_done = True
                elif not input_2_done:
                    input_2_done = True
                else:
                    if event.key == pygame.K_RETURN:
                        pass  # consume the value / change game view / etc.
            if event.key == pygame.K_BACKSPACE:
                if not input_1_done:
                    tmp_input_1_value = tmp_input_1_value[:-1]
                elif not input_2_done:
                    tmp_input_2_value = tmp_input_2_value[:-1]
            else:
                if not input_1_done:
                    tmp_input_1_value += event.unicode
                elif not input_2_done:
                    tmp_input_2_value += event.unicode

    if cursor and show_cursor:
        pygame.draw.rect(screen, "white", cursor)
        
    if input_1_done and input_2_done:
        pygame.time.set_timer(cursor_tick_event, 0)  # Turn off the timer; stop adding events
        cursor_tick_event_set = False

    return


##################################################################################################################
#################================---------------- MAIN GAME LOOP ----------------================#################
##################################################################################################################



fps_clock = pygame.time.Clock()
while not exit_game:
    fps_clock.tick(60)
    screen.fill('black')

    current_events = list(pygame.event.get())  # store events in a global variable to consume in different places
    for event in current_events:
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pass  # open menu / close game / whatever

    text_input_view(screen)

    pygame.display.update()

import sudoku
import pygame
import time
import colorsys
pygame.init()
pygame.display.set_caption('sudoku')

COLORS = {
    'black': (0,0,0),
    'white': (255,255,255),
    'lighter_grey': (212,212,212),
    'light_grey': (192,192,192),
    'mid_grey': (153,153,153),
    'grey': (138,138,138),
    'dark_grey':(85,85,85),
    'red': (255,0,0),
    'orange': (255,130,0),
    'yellow': (255,230,0),
    'green': (0,255,0),
    'blue': (0,0,255),
    'pink': (255,0,230),
    'purple': (140, 0, 255),
    
}

class GridGUI():
    def __init__(self, screen_length, const_border=5):
        self.g = sudoku.Grid()
        self.screen_length = screen_length

        timer = TimerBar(screen_length)

        self.screen = timer.play_area
        self.full_screen = timer.full_screen
        self.timer = timer
        
        self.row_length = len(self.g.grid)
        self.const_border = const_border
        self.total_border = const_border + self.get_border_padding()
        self.box_size = self.get_box_size() 
        self.font_multiplier = self.get_px_to_pt_multiplier()
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(self.box_size*self.font_multiplier))
        
        self.hover_color = COLORS['lighter_grey']
        self.selected_color = COLORS['grey']

        self.hover = None
        self.selected = None
        self.blink_on = False
        self.blink_restore_color = None

        self.game_won = False
        self.draw_grid()
        pygame.display.update() 

    def get_px_to_pt_multiplier(self, ch='O'):
        # x -> font pt, y -> font px
        y1 = 10
        f1 = pygame.font.Font(pygame.font.get_default_font(), y1)
        x1 = f1.size(ch)[0]
        y2 = 100
        f2 = pygame.font.Font(pygame.font.get_default_font(), y2)
        x2 = f2.size(ch)[0]
        return (x1/y1 + x2/y2)/2
                
    def get_border_padding(self):
        W = self.screen_length
        C = self.const_border
        A = self.row_length
        D = W - 2*C
        T = D // A
        x = (W - 2*C - A*T)/2
        return x
    
    def get_box_size(self):
        W = self.screen_length
        B = self.total_border
        A = self.row_length
        return (W - 2*B)/A

    def draw_grid(self):   
        self.screen.fill(COLORS['grey'])
        for i, row in enumerate(self.g.grid):
            for j, v in enumerate(row):
                    self.draw_tile(i,j)

    def draw_selected_tile(self):
        i, j = self.selected
        t1 = self.draw_tile(i,j, color=self.hover_color)
        t2 = self.draw_tile(i,j, color=self.selected_color, width=5)
        tile_list = [t1, t2]
        return tile_list

    def draw_tile(self, i, j, color=COLORS['light_grey'], width=0):
        xpos, ypos = self.get_pos_from_inds(i,j)
        box = pygame.Rect(xpos, ypos, self.box_size, self.box_size)
        pygame.draw.rect(self.screen, color, box, width)
        if self.g.viewable_grid[i][j].isdigit():
            num_color = COLORS['black'] if (i, j) in self.g.hints else COLORS['dark_grey']
            cell_number = self.font.render(self.g.viewable_grid[i][j], True, num_color)
            aligner = cell_number.get_rect(center=(box.centerx, box.centery))
            self.screen.blit(cell_number, aligner)

        cell = pygame.draw.rect(self.screen, COLORS['black'], box, 1)
        cell_translated = pygame.Rect(self.translate_coords_from_grid(*cell.topleft), cell.size)
        return cell_translated

    def color_hover(self, i, j):
        tile_list = []
        if self.hover is not None and not self.g.is_hint(*self.hover) and self.hover != self.selected:
            tile_list.append(self.draw_tile(*self.hover))
            self.hover = None
        if self.g.is_in_bounds(i,j) and not self.g.is_hint(i,j) and (i,j) != self.selected:
            tile_list.append(self.draw_tile(i, j, self.hover_color))
            self.hover = (i, j)
        if tile_list:
            pygame.display.update(tile_list)
    
    def change_selected(self, i, j):
        # restore if double click
        if self.selected == (i,j):
            t = self.draw_tile(*self.selected)
            self.selected = None
            pygame.display.update(t)
            self.blink_restore_color = None
            return
        
        tile_list = []
        # restore previous
        if self.selected is not None:
            t = self.draw_tile(*self.selected)
            tile_list.append(t)
            self.selected = None
            self.blink_restore_color = None
        # draw selected tile
        if self.g.is_in_bounds(i,j) and not self.g.is_hint(i,j): 
            self.selected = (i,j)
            tiles = self.draw_selected_tile()
            tile_list.extend(tiles)
        if tile_list:
            pygame.display.update(tile_list)
    
    def handle_arrow_key(self, key_n):
        # 0 = RIGHT
        # 1 = LEFT
        # 2 = DOWN
        # 3 = UP

        i, j = self.selected
        # (i,j) offset
        offset_mat = [  [0, 1],
                        [0, -1],
                        [1,  0],
                        [-1, 0]
                     ]
        
        r_increase, c_increase = offset_mat[key_n]

        i, j = (i+r_increase)%self.g.dim, (j+c_increase)%self.g.dim
        while self.g.is_hint(i,j):
            i, j = (i+r_increase)%self.g.dim, (j+c_increase)%self.g.dim
        self.change_selected(i, j)

    def translate_coords_from_grid(self, x, y):
        return (x, y+self.timer.h)

    def translate_coords_to_grid(self, x, y):
        return (x, y-self.timer.h)

    def get_pos_from_inds(self, i, j): 
        x, y = [ind*self.box_size + self.total_border for ind in (j, i)]
        return (x,y)

    def get_box_inds_from_pos(self, x, y):
        x, y = self.translate_coords_to_grid(x,y)
        B = self.total_border
        
        row = ((y-B)//self.box_size)
        col = ((x-B)//self.box_size)
        return (int(row), int(col)) # for indexing, needs to be int

    def is_in_playable_area(self, x, y):
        i, j = self.get_box_inds_from_pos(x,y)
        return self.g.is_in_bounds(i,j)

    def blur_screen(self, full=False):
        screen = self.screen if not full else self.full_screen
        old_dims = screen.get_size()
        new_dims = list(d*0.1 for d in old_dims)
        
        new_screen = pygame.transform.smoothscale(screen, new_dims)
        new_screen = pygame.transform.smoothscale(new_screen, old_dims)
        screen.blit(new_screen, (0,0))
    
    def pause_menu(self):
        # blur screen
        self.blur_screen(full=True)

        # setup boxes
        screen_box = pygame.Rect(0,0, self.screen_length, self.screen_length)
        exit_main_menu_box = pygame.Rect(0, 0, self.screen_length*0.25, self.screen_length*0.2)
        resume_game_box = pygame.Rect(exit_main_menu_box)
        exit_main_menu_box.midleft = screen_box.midleft
        resume_game_box.midright = screen_box.midright
        exit_main_menu_box.x += exit_main_menu_box.w/1.5
        resume_game_box.x -= resume_game_box.w/1.5

        # setup text
        font_pt = self.get_px_to_pt_multiplier()*resume_game_box.w/4
        font = pygame.font.Font(pygame.font.get_default_font(), int(font_pt))
        resume_text = font.render('Resume', True, COLORS['white'])
        resume_text2 = font.render('game', True, COLORS['white'])
        exit_text = font.render('Exit', True, COLORS['white'])
        exit_text2 = font.render('to menu', True, COLORS['white'])
        bt_height = resume_game_box.centery-resume_game_box.h/7.5
        resume_aligner = resume_text.get_rect(center=(resume_game_box.centerx, bt_height))
        exit_aligner = exit_text.get_rect(center=(exit_main_menu_box.centerx, bt_height))
        resume_aligner2 = resume_text2.get_rect(center=(resume_game_box.centerx, bt_height+resume_aligner.h))
        exit_aligner2 = exit_text2.get_rect(center=(exit_main_menu_box.centerx, bt_height+exit_aligner.h))  
        
        # setup big text
        paused_str = 'PAUSED'
        big_font_pt = font_pt*3.5
        big_font = pygame.font.Font(pygame.font.get_default_font(), int(big_font_pt))
        paused_text = big_font.render(paused_str, True, COLORS['blue'])
        bigt_height = bt_height*(.50)
        bigt_centerx = (exit_main_menu_box.x+resume_game_box.right)/2
        paused_aligner = paused_text.get_rect(center=(bigt_centerx, bigt_height))
        big_text, big_text_aligner = paused_text, paused_aligner
        
        # setup outline for big text
        big_outline_font_pt = big_font_pt+1
        big_outline_font = pygame.font.Font(pygame.font.get_default_font(), int(big_outline_font_pt))
        paused_outline = big_outline_font.render(paused_str, True, COLORS['black'])
        paused_outline_aligner = paused_outline.get_rect(center=(bigt_centerx, bigt_height))
        
        big_outline, big_outline_aligner = paused_outline, paused_outline_aligner

        # draw
        box_border_length = int(resume_game_box.w/15)
        pygame.draw.rect(self.screen, COLORS['red'], exit_main_menu_box, box_border_length)
        pygame.draw.rect(self.screen, COLORS['green'], resume_game_box, box_border_length)
        self.screen.blit(resume_text, resume_aligner)
        self.screen.blit(exit_text, exit_aligner)
        self.screen.blit(resume_text2, resume_aligner2)
        self.screen.blit(exit_text2, exit_aligner2)
        self.screen.blit(big_outline, big_outline_aligner)
        self.screen.blit(big_text, big_text_aligner)

        pygame.display.update()

        resume_game = False
        while not resume_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    raise StopIteration

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    resume_game = True

                if event.type == pygame.MOUSEBUTTONUP and resume_game_box.collidepoint(event.pos):  
                    resume_game = True

                if event.type == pygame.MOUSEBUTTONUP and exit_main_menu_box.collidepoint(event.pos):
                    return False

        self.draw_grid()
        self.draw_selected_tile()
        pygame.display.update()
        return resume_game

    def end_menu(self, win=True):
        # blur
        self.blur_screen()

        # setup boxes
        screen_box = pygame.Rect(0,0, self.screen_length, self.screen_length)
        exit_main_menu_box = pygame.Rect(0, 0, self.screen_length*0.25, self.screen_length*0.2)
        continue_game_box = pygame.Rect(exit_main_menu_box)
        exit_main_menu_box.midleft = screen_box.midleft
        continue_game_box.midright = screen_box.midright
        exit_main_menu_box.x += exit_main_menu_box.w/1.5
        continue_game_box.x -= continue_game_box.w/1.5

        # setup text
        font_pt = self.get_px_to_pt_multiplier()*continue_game_box.w/4
        font_pt2 = font_pt/2
        font = pygame.font.Font(pygame.font.get_default_font(), int(font_pt))
        font_smaller = pygame.font.Font(pygame.font.get_default_font(), int(font_pt2))
        continue_text = font.render('Play', True, COLORS['white'])
        continue_text2 = font.render('again', True, COLORS['white'])
        continue_text3 = font_smaller.render('(same settings)', True, COLORS['white'])
        exit_text = font.render('Exit', True, COLORS['white'])
        exit_text2 = font.render('to menu', True, COLORS['white'])
        bt_height = continue_game_box.centery-continue_game_box.h/7.5
        continue_aligner = continue_text.get_rect(center=(continue_game_box.centerx, bt_height))
        continue_aligner2 = continue_text2.get_rect(center=(continue_game_box.centerx, bt_height+continue_aligner.h))   
        continue_aligner3 = continue_text3.get_rect(center=(continue_game_box.centerx, bt_height+continue_aligner2.h*1.25))
        continue_aligner3.y += continue_aligner3.h

        exit_aligner = exit_text.get_rect(center=(exit_main_menu_box.centerx, bt_height))
        exit_aligner2 = exit_text2.get_rect(center=(exit_main_menu_box.centerx, bt_height+exit_aligner.h))  

        # setup big text
        win_str, lose_str = 'YOU WIN!', 'YOU LOSE'
        big_font_pt = font_pt*3.5
        big_font = pygame.font.Font(pygame.font.get_default_font(), int(big_font_pt))
        win_text = big_font.render(win_str, True, COLORS['green'])
        lose_text = big_font.render(lose_str, True, COLORS['red'])
        bigt_height = bt_height*(.50)
        bigt_centerx = (exit_main_menu_box.x+continue_game_box.right)/2
        win_aligner = win_text.get_rect(center=(bigt_centerx, bigt_height))
        lose_aligner = lose_text.get_rect(center=(bigt_centerx, bigt_height))
        (big_text, big_text_aligner) = (win_text, win_aligner) if win else (lose_text, lose_aligner)
        
        # setup outline for big text
        big_outline_font_pt = big_font_pt+1
        big_outline_font = pygame.font.Font(pygame.font.get_default_font(), int(big_outline_font_pt))
        win_outline = big_outline_font.render(win_str, True, COLORS['black'])
        lose_outline = big_outline_font.render(lose_str, True, COLORS['black']) 
        win_outline_aligner = win_outline.get_rect(center=(bigt_centerx, bigt_height))
        lose_outline_aligner = lose_outline.get_rect(center=(bigt_centerx, bigt_height))    
        (big_outline, big_outline_aligner) = (win_outline, win_outline_aligner) if win else (lose_outline, lose_outline_aligner)
        
        # draw
        box_border_length = int(continue_game_box.w/15)
        pygame.draw.rect(self.screen, COLORS['red'], exit_main_menu_box, box_border_length)
        pygame.draw.rect(self.screen, COLORS['green'], continue_game_box, box_border_length)
        self.screen.blit(continue_text, continue_aligner)
        self.screen.blit(continue_text2, continue_aligner2) 
        self.screen.blit(continue_text3, continue_aligner3)
        self.screen.blit(exit_text, exit_aligner)
        self.screen.blit(exit_text2, exit_aligner2) 
        self.screen.blit(big_outline, big_outline_aligner)
        self.screen.blit(big_text, big_text_aligner)

        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    raise StopIteration
                
                if event.type == pygame.MOUSEBUTTONDOWN and continue_game_box.collidepoint(event.pos):  
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN and exit_main_menu_box.collidepoint(event.pos):
                    return False

    def blink_cursor(self):
        # setup values
        cursor_dims = self.box_size*.1, self.box_size*.8
        cursor_pos = self.get_pos_from_inds(*self.selected)
        
        # modify position
        cursor_offset = self.box_size*.1
        cursor_pos_updated = [p + cursor_offset for p in cursor_pos]
        
        # create rect
        cursor = pygame.Rect(cursor_pos_updated, cursor_dims)
        
        # get color
        if self.blink_restore_color is None:
            self.blink_restore_color = self.screen.get_at([int(p) for p in cursor_pos_updated])[:3]
        color = COLORS['black'] if self.blink_on else self.blink_restore_color
        
        # set blinking interval
        blinks_per_sec = 2
        timing_divisor = 1000//blinks_per_sec
        self.blink_on = (self.timer.clock[0]//timing_divisor) % 2 == 0

        # draw
        pygame.draw.rect(self.screen, color, cursor)

        # translate coords & update display
        cursor.x, cursor.y = self.translate_coords_from_grid(cursor.x, cursor.y)
        pygame.display.update(cursor)
    
    def place_number(self, i, j, n):
        self.g.guess_number(i,j, str(n))
        t = self.draw_selected_tile()
        pygame.display.update(t)

    def remove_number(self, i, j):
        self.g.remove_guess(i,j)
        t = self.draw_tile(i,j) if (i,j) != self.selected else self.draw_selected_tile()
        pygame.display.update(t)

    def play_game(self):
        first_click = False
        print(self.g.grid)
        while True: 
            self.timer.update_clock_dynamic()
            if self.selected is not None:
                self.blink_cursor()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise StopIteration
               
                if self.selected is not None and event.type == pygame.KEYDOWN and event.key in range(pygame.K_1, pygame.K_9+1):
                    n = (event.key - pygame.K_1)+1
                    self.place_number(*self.selected, n)
                    if self.g.is_solved():
                        self.end_menu()
                
                if self.selected is not None and event.type == pygame.KEYDOWN and event.key in range(pygame.K_RIGHT, pygame.K_UP+1):
                    n = event.key - pygame.K_RIGHT
                    self.handle_arrow_key(n)
                
                if self.selected is not None and event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.remove_number(*self.selected)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_in_playable_area(*event.pos):
                    i, j = self.get_box_inds_from_pos(*event.pos)
                    if self.g.is_guess(i,j):
                        self.remove_number(i,j)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    resume_game = self.pause_menu()
                    if not resume_game:
                        return False
                    if not first_click:
                        self.timer.update_clock(0)
                
                if event.type == pygame.MOUSEMOTION:
                    i, j = self.get_box_inds_from_pos(*event.pos)
                    self.color_hover(i,j)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_in_playable_area(*event.pos):
                    if not first_click:
                        self.timer.start_clock()
                        first_click = True

                    i, j = self.get_box_inds_from_pos(*event.pos)
                    self.change_selected(i,j)
                    
class TimerBar:
    def __init__(self, play_area_length):
        bar_height = play_area_length//20 # 5%
        full_screen = pygame.display.set_mode((play_area_length, play_area_length+bar_height))

        screen_rect = pygame.Rect(0,0, play_area_length, bar_height)
        play_area_rect = pygame.Rect(0,0, play_area_length, play_area_length)
        play_area_rect.y += screen_rect.h

        self.w, self.h = screen_rect.size
        self.screen = full_screen.subsurface(screen_rect)   
        self.play_area = full_screen.subsurface(play_area_rect)
        self.full_screen = full_screen

        self.screen.fill(COLORS['blue'])

        self.clock = self.get_clock()
        self.update_clock(0)

    def get_px_to_pt_multiplier(self, ch='O'):
        # x -> font pt, y -> font px
        y1 = 10
        f1 = pygame.font.Font(pygame.font.get_default_font(), y1)
        x1 = f1.size(ch)[0]
        y2 = 100
        f2 = pygame.font.Font(pygame.font.get_default_font(), y2)
        x2 = f2.size(ch)[0]
        return (y1/x1 + y2/x2)/2

    def get_clock(self):
        clock_aligner = pygame.Rect(0,0, self.w/6, self.h/1.25)
        clock_aligner.center = self.screen.get_rect().midright
        clock_aligner.x -= self.screen.get_rect().w*0.1

        clock_time = 0

        m = self.get_px_to_pt_multiplier('00:00.00')
        pt = int(m*self.h*4)
        clock_font = pygame.font.Font(pygame.font.get_default_font(), pt)
        
        last_clock_update = None
        
        return [clock_time, clock_aligner, clock_font, last_clock_update]

    def start_clock(self):
        self.clock[3] = time.perf_counter() # start clock

    def update_clock(self, elapsed_time): # elapsed time in ms
        self.clock[0] += elapsed_time

        clock_time, clock_rect, clock_font, _ = self.clock
        
        hundreth_secs = int(clock_time//10)%100
        secs = int(clock_time//1000)%60
        mins = int(clock_time//1000//60)

        clock_str = f"{mins}:{str(secs/10)[::2]}.{str(hundreth_secs/10)[::2]}"
        
        clock_text = clock_font.render(clock_str, True, COLORS['white'])
        #clock_aligner = clock_text.get_rect(center=clock_rect.center)
        
        self.screen.fill(COLORS['blue'])
        
        self.screen.blit(clock_text, self.clock[1])
        #self.screen.blit(clock_text, clock_aligner)
        pygame.display.update(self.screen.get_rect())

    def update_clock_dynamic(self):
        last_clock_update = self.clock[3]
        if last_clock_update is None:
            return
        cur_time = time.perf_counter()
        time_diff_ms = (cur_time-last_clock_update)*1000
        self.clock[3] = cur_time
        self.update_clock(time_diff_ms)

if __name__ == '__main__':
    board = GridGUI(800)
    try:
        board.play_game()
    except (StopIteration, KeyboardInterrupt) as game_exit: # Game quit
        pass
    pygame.quit()

"""
if event.type == pygame.MOUSEMOTION:
            print(event.pos)
            r, g = [p // 2 for p in event.pos]
            b = (r + g) % 256
            color = (r, g, b)
            screen.fill(color)
            pygame.display.update()

"""

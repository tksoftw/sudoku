import sudoku
import pygame
import time
import colorsys
pygame.init()
pygame.display.set_caption('sudoku')

COLORS = {
    'black': (0,0,0),
    'white': (255,255,255),
    'light_grey': (192,192,192),
    'mid_grey': (153,153,153),
    'grey': (138,138,138),
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

        self.hover = None
        self.selected = None

        self.game_won = False
        self.draw_grid()

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

        pygame.display.update() 

    def draw_tile(self, i, j, color=COLORS['light_grey']):
        xpos, ypos = [ind*self.box_size + self.total_border for ind in (j, i)]
        box = pygame.Rect(xpos, ypos, self.box_size, self.box_size)
        pygame.draw.rect(self.screen, color, box)
        if self.g.viewable_grid[i][j].isdigit():
            num_color = COLORS['black'] if (i, j) in self.g.hints else COLORS['mid_grey']
            cell_number = self.font.render(self.g.viewable_grid[i][j], True, num_color)
            aligner = cell_number.get_rect(center=(box.centerx, box.centery))
            self.screen.blit(cell_number, aligner)

        cell = pygame.draw.rect(self.screen, COLORS['black'], box, 1)
        return cell

    def color_hover(self, i, j):
        if A:=(self.hover is not None and self.g.viewable_grid[self.hover[0]][self.hover[1]] == '-'):
            self.draw_tile(*self.hover)
            self.hover = None
        if B:=(self.g.is_in_bounds(i,j) and self.g.viewable_grid[i][j] == '-'):
            self.draw_tile(i, j, COLORS['mid_grey'])
            self.hover = (i, j)
        if A or B:
            pygame.display.update()
    
    def change_selected(self, i, j):
        if B:=(self.selected is not None):
            self.draw_tile(*self.selected)
            self.selected = None
        if A:=(self.g.is_in_bounds(i,j) and not self.g.is_hint(i,j)):
            self.draw_tile(i, j, COLORS['grey'])
            self.selected = (i,j)
        if A or B:
            pygame.display.update()

    def translate_coords_to_grid(self, x, y):
        return (x, y-self.timer.h)

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

    
    def play_game(self):
        first_click = False
        while True:
            self.timer.update_clock_dynamic()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise StopIteration

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
        clock_aligner.center = self.screen.get_rect().center

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

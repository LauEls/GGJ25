import pygame

def write_text(screen, text, color="white", font="comic sans", size=20, x: int = 0, y: int = 0):
  
        # creating font object score_font
        score_font = pygame.font.Font("assets/geo_regular.ttf", size)
        # SysFont(font, size)
        
        # create the display surface object 
        # score_surface
        score_surface = score_font.render(text, True, color)
        
        # create a rectangular object for the text
        # surface object
        score_rect = score_surface.get_rect()
        score_rect.x = x-score_rect.width/2
        score_rect.y = y-score_rect.height/2-score_rect.height/12
        
        # displaying text
        screen.blit(score_surface, score_rect)
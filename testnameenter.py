# import sys module
import pygame
import sys
  
  
pygame.init()
  
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600, 500])
base_font = pygame.font.Font(None, 32)
user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)
  
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
  
active = False
done_naming = False
  
while True:
    for event in pygame.event.get():
  
      # if quit or user presses RETURN, exit
        if event.type == pygame.QUIT or done_naming == True:
            print(user_text)
            pygame.quit()
            sys.exit()
  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
  
        if event.type == pygame.KEYDOWN:
  
            # check if backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to end
                user_text = user_text[:-1]
            
            elif event.key == pygame.K_RETURN:
                # done collecting name, store it
                nickname = user_text
                done_naming = True
  
            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode
      
    # it will set background color of screen
    screen.fill((255, 255, 255))
  
    if active:
        color = color_active
    else:
        color = color_passive
          
    # draw rectangle and argument
    pygame.draw.rect(screen, color, input_rect)
  
    text_surface = base_font.render(user_text, True, (255, 255, 255))
      
    # render (position is from arguments)
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
      
    # set width of textfield 
    input_rect.w = max(100, text_surface.get_width()+10)
      
    # display.flip() will update only part of screen , not full area
    pygame.display.flip()
      
    # clock.tick(60) --> for every second at most 60 frames should be passed.
    clock.tick(60)
import pygame, sys
import button, client


def showmenu():
        menuscreen = pygame.display.set_mode((500,500))
        menuscreen.fill((255,0,0))
        
        #load button images
        enterserver_img = pygame.image.load("images/button_options.png").convert_alpha()
        quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
        back_img = pygame.image.load('images/button_back.png').convert_alpha()

        #create button instances
        enterserver_button = button.Button(180, 250, enterserver_img, 1)
        quit_button = button.Button(336, 375, quit_img, 1)
        back_button = button.Button(332, 450, back_img, 1)
        
        menu_state = "main"
        
        while True:
            #check menu state
            if menu_state == "main":
                #enterserver button
                if enterserver_button.draw(menuscreen):
                    menu_state = "main"
                    #screen to collect server info input
                #quit button
                if quit_button.draw(menuscreen):
                    pygame.quit()
                    sys.exit()
                    
            elif menu_state == "start":
                if back_button.draw(menuscreen):
                    break

            else:
                #if we get here, then we go to the game! exit menu loop
                break
            
            
def main():
    pygame.init()
    showmenu()
    #client.runclient()
    
if __name__ == '__main__':
    main()
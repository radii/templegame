#!/usr/bin/env python

import optparse
import pygame
import time

allkeys = []
surf = None

def update_img(img_id):
    filename = "img/" + img_id
    img=pygame.image.load(filename)
    img=pygame.transform.scale(img, (800,600))
##    surf.blit(img,(0,0))
##    pygame.display.flip() # update the display

    for alpha in range(0,255,5):
        img.set_alpha(alpha)
        surf.blit(img,(0,0))
        pygame.display.flip() # update the display
        pygame.display.update()
mainloop = True

def keydown(s):
    '''called by mainloop when a key is pressed.  Takes a string representing
    the key that was pressed.'''
    global allkeys
    global mainloop
    print "keydown got %r" % s
    if s == '\r':
        tag = ''.join(allkeys)
        print(tag)
        update_img(tag)
        allkeys = []
    elif s == 'q' or s == 'Q':
        mainloop = False
    else:
        allkeys.append(s.encode('UTF8'))

def run_game(opts):
    global surf
    global mainloop
    pygame.init()

    if opts.full:
        surf = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    else:
        surf = pygame.display.set_mode((800, 600))
    surf.fill((255,255,255))

    update_img("default")
    while mainloop:
        for event in pygame.event.get():
            print "got event %r" % ((event,event.type, pygame.QUIT),)
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                keydown(event.unicode)
        pygame.display.update()

    pygame.quit()


def main():
    parser = optparse.OptionParser()
    parser.add_option('-f', '--full', action='store_true')

    (opts, args) = parser.parse_args()

    run_game(opts)


if __name__ == '__main__':
    main()

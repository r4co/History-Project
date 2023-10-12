import pygame
import random


def get_mouse():
    return pygame.mouse.get_pos()


class Person:
    def __init__(self, surface, face, posx, posy):
        self.surface = surface
        self.surf_rect = self.surface.get_rect()
        self.face = face
        self.mode = True
        self.speed = 1
        self.posx = posx
        self.posy = posy
        self.rect = pygame.Rect((self.posx, self.posy), self.face.get_rect().size)

    def move_person(self, people):

        mouse_pos = get_mouse()

        posx_copy = self.posx
        posy_copy = self.posy

        disx = self.posx - mouse_pos[0]
        disy = self.posy - mouse_pos[1]

        if self.mode:
            self.speed = 1

        elif not self.mode:
            self.speed = -1

        self.posx = self.direction(disx, self.posx)
        self.posy = self.direction(disy, self.posy)

        self.rect = pygame.Rect((self.posx, self.posy), self.face.get_rect().size)

        if self.check_collison(people):
            self.posx = posx_copy
            self.posy = posy_copy

    def direction(self, dis, pos):
        if dis < 0:
            pos += self.speed
        elif dis > 0:
            pos -= self.speed
        return pos

    def check_collison(self, people):
        for person in people:
            if self.rect != person and self.rect.colliderect(person.rect):
                return True
            elif self.rect not in self.surf_rect:
                return True

        else:
            return False

    def render_person(self):
        self.rect = pygame.Rect((self.posx, self.posy), self.face.get_rect().size)
        self.surface.blit(self.face, self.rect)


def set_text(surface, font, mode, color):
    text = font.render(mode, True, color)
    surface.blit(text, (surface.get_rect().centerx - text.get_rect().centerx, 30))


def main():
    WIDTH = 500
    HEIGHT = 500

    WHITE = (255, 255, 255)
    rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    pygame.init()
    font = pygame.font.SysFont("arial.ttf", 60)

    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Inclusion and Exclusion")

    smile_path = "smile.png"
    smile_image = pygame.image.load(smile_path)

    anger_path = "anger.png"
    anger_image = pygame.image.load(anger_path)

    mode_text = "Inclusion"
    people_amount = 10

    people = [Person(display_surface, smile_image, i * 50, i % 2 * 400) for i in range(people_amount)]

    clock = pygame.time.Clock()

    run = True
    while run:
        display_surface.fill(WHITE)

        for person in people:
            person.move_person(people)
            person.render_person()

        set_text(display_surface, font, mode_text, rand_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_SPACE:
                    for person in people:
                        if person.face == smile_image:
                            person.face = anger_image
                            person.mode = False
                            mode_text = "Exclusion"
                        else:
                            person.face = smile_image
                            person.mode = True
                            mode_text = "Inclusion"

        pygame.display.update()
        clock.tick(20)

    pygame.quit()


main()

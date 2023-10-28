import pygame
import threading
import socket
import time

class Chat:

    def __init__(self, game, x, y, width, height):
        self.game = game

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.chat = "Connecting with game chat server... "
        self.server = None
        self.update_chat_thread = threading.Thread(target=self.update_chat, daemon=True)
        self.update_chat_thread.start()

        self.show = False
                      
        self.font = pygame.font.SysFont("Arial",int(self.width/100) * 3, bold=True)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.entry_rect = pygame.Rect(self.rect.left, self.rect.bottom + 10, self.width - self.width/4, self.font.get_height() + 10)
        self.input = ''

    def blit_text(self, surface, text, pos, font, color=pygame.Color('green')):
        line = [word for word in text.split(' ')]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = (self.rect.w, self.rect.h)
        x, y = pos
        remove_words = 0
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if word.startswith('\n'):
                x = pos[0]
                y += word_height
                word = word.replace('\n','')
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if y + word_height >= self.rect.bottom:
                    x += word_width + space
                    remove_words += 1
                    continue
            elif x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
                if y + word_height >= self.rect.bottom:
                    x += word_width + space
                    remove_words += 1
                    continue
            surface.blit(word_surface, (x, y))
            x += word_width + space

        self.chat = self.chat.split(' ', remove_words)[remove_words]

    def update_chat(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server.connect((self.game.server[0], self.game.server[1]-1))
                self.chat += f'\nConnected! '
                while True:
                    try:
                        message = self.server.recv(2048)
                        self.chat += f'\n{message.decode()} '
                    except:
                        continue
            except Exception as ex:
                self.chat += '\nConnecting.. '
                time.sleep(1)
                continue

    def update(self):
        pass

    def send_chat(self):
        try:
            self.server.send(str(f"<{self.game.user['username']}>{self.input} ").encode())
            self.chat += str('\n'+ f"<{self.game.user['username']}>{self.input} ")
            self.input = ''
        except:
            pass

    def render(self):
        if self.show:
            pygame.draw.rect(self.game.screen, 'gray', self.rect, width=5, border_radius=10)
            self.blit_text(self.game.screen, self.chat, (self.rect.left + 20, self.rect.y + 10), self.font)

            pygame.draw.rect(self.game.screen, 'gray', self.entry_rect, border_radius=10)
            input_text = self.font.render(f"{self.input}", True, "red")
            self.game.screen.blit(input_text, (self.entry_rect.left + self.font.get_height(), self.entry_rect.y + 5)) 



            
        
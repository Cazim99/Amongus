""" 
THIS MODULE IS CREATE BY CAZIM HAMIDOVIC (ZC-Team)
CONTACT INFO: cazimhamidovic@outlook.com
"""
import pygame
import os

class ImageLoader:  
    @staticmethod
    def load_images(path):
        images = {}
        for file_name in os.listdir(path):
            if file_name.endswith(".png"):
                image = pygame.image.load(path + os.sep + file_name).convert_alpha()
                images[file_name] = image
        return images
#!/usr/bin/python3.7
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
import pygame
from random import randint
import random
import UltraSnake.MAIN.Screens.GameScreen as game
from ENGINE import shape
from ENGINE import fx
from ENGINE import utils

class Food:
    def __init__(self, X=0, Y=0):
        self.Rectangle = pygame.Rect(X, Y, 32, 32)
        self.Iteration = 0
        self.RandColor = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.AnimationController = utils.AnimationController(multiplierSpeed=0.1)
        self.Deleted = False
        self.DeleteToggle = False
        self.DeleteEnd = False
        self.DeleteValue = randint(1, 5)

    def Render(self, DISPLAY):
        FoodSurface = pygame.Surface((32, 32), pygame.SRCALPHA)
        FoodSurface.set_alpha(self.AnimationController.Value)

        shape.Shape_Circle(FoodSurface, 32 / 2, 32 / 2, 6, (self.RandColor[0] + (self.AnimationController.Value - 255), self.RandColor[1] + (self.AnimationController.Value - 255), self.RandColor[2] + (self.AnimationController.Value - 255)))

        DISPLAY.blit(fx.Surface_Blur(FoodSurface, 4), (game.CameraX + self.Rectangle[0], game.CameraY + self.Rectangle[1]))

    def Update(self):
        self.AnimationController.Update()

        if self.Deleted:
            self.DeleteToggle = True

        if self.DeleteToggle:
            self.DeleteToggle = False

            self.AnimationController.CurrentMode = False
            self.AnimationController.Enabled = True
            self.AnimationController.ValueMultiplier = 1.0

        if self.AnimationController.Value <= 0:
            self.DeleteEnd = True


class Player:
    def __init__(self, nickname):
        self.PlayerPos = (0, 0)
        self.Rectangle = pygame.Rect(0, 0, 32, 32)
        self.MovPos = 0  # 0 = X+, 1 = X-, 2 = Y+, 3 = Y-, -1 = Stopped
        self.SnakeSize = 0
        self.snake_list = []
        self.Speed = 4
        self.PlayerColor = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.Nickname = nickname
        self.Score = 0
        self.IsClient = False
        self.IsDead = False
        self.VarListClearWhenDeadTrigger = False
        self.VarList = list()
        self.IsOnScreen = False

    def Draw(self, DISPLAY):
        # -- draw the snake -- #
        if not self.IsDead:
            for i, x in enumerate(self.snake_list):
                shape.Shape_Circle(DISPLAY, game.CameraX + x[0] + 26 / 2, game.CameraY + x[1] + 26 / 2, 26 / 2, ((self.PlayerColor[0]) + i, (self.PlayerColor[1]) + i, (self.PlayerColor[2]) + i))

        # -- Draw the Head -- #
        if self.IsDead:
            shape.Shape_Circle(DISPLAY, game.CameraX + self.Rectangle[0] + 26 / 2, game.CameraY + self.Rectangle[1] + 26 / 2, 26 / 2, (200, 55, 75))
        else:
            shape.Shape_Circle(DISPLAY, game.CameraX + self.Rectangle[0] + 26 / 2, game.CameraY + self.Rectangle[1] + 26 / 2, 26 / 2, self.PlayerColor)

        # -- Draw the Nickname -- #
        TextX = game.CameraX + self.Rectangle[0] - game.Game.ConteudoPadrao.GetFont_width("/PressStart2P.ttf", 12, self.Nickname) / 2
        TextY = game.CameraY + self.Rectangle[1]
        Text = self.Nickname

        if self.IsDead:
            Text += "\nDead"
        Opacity = 155

        if self.Nickname == game.CurrentNickname:
            Opacity = 255

        game.Game.ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 12, Text, (255, 255, 255), TextX, TextY, backgroundColor=(0, 0, 0), Opacity=Opacity)

    def Update(self):
        self.Rectangle = pygame.Rect(self.PlayerPos[0], self.PlayerPos[1], 26, 26)

        # Move the Player
        if not self.IsDead:
            if self.MovPos == 0:
                self.PlayerPos = (self.PlayerPos[0] + self.Speed, self.PlayerPos[1])

            elif self.MovPos == 1:
                self.PlayerPos = (self.PlayerPos[0] - self.Speed, self.PlayerPos[1])

            elif self.MovPos == 2:
                self.PlayerPos = (self.PlayerPos[0], self.PlayerPos[1] + self.Speed)

            elif self.MovPos == 3:
                self.PlayerPos = (self.PlayerPos[0], self.PlayerPos[1] - self.Speed)

        # -- Check if player is not outside the map -- #
        if self.PlayerPos[0] <= 0:
            self.PlayerPos = (0, self.PlayerPos[1])

        if self.PlayerPos[0] + self.Rectangle[2] >= game.ArenaSize[0]:
            self.PlayerPos = (game.ArenaSize[0] - self.Rectangle[2], self.PlayerPos[1])

        if self.PlayerPos[1] <= 0:
            self.PlayerPos = (self.PlayerPos[0], 0)

        if self.PlayerPos[1] + self.Rectangle[3] >= game.ArenaSize[1]:
            self.PlayerPos = (self.PlayerPos[0], game.ArenaSize[1] - self.Rectangle[3])

        # Limit Snake Size
        if self.SnakeSize > 700:
            self.SnakeSize = 700

        # Update the Snake Logic
        if len(self.snake_list) > self.SnakeSize:
            del self.snake_list[0]
        else:
            self.snake_list.append((self.PlayerPos[0], self.PlayerPos[1]))

        # Detect if Player Colides with withself
        if len(self.snake_list) > 16:
            for i, snl in enumerate(self.snake_list[:-16]):
                CollideRect = pygame.Rect(snl[0], snl[1], 32, 32)

                if self.Rectangle.colliderect(CollideRect):
                    self.IsDead = True

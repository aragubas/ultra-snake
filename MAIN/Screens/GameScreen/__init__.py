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
from UltraSnake.MAIN import Objects
import UltraSnake.MAIN as Game
from ENGINE import shape
from ENGINE import fx
from random import randint

# Objetos
ColecaoJogador = list()
ColecaoComida = list()
Jogador = None

CurrentNickname = "ceira"
CurrentIndex = 0

#Camera
CameraX = 0
CameraY = 0

#Game Logic
ArenaSize = (5000, 5000)
FoodSpawnRate = 64

def Initialize():
    Reset()

def GameDraw(DISPLAY):
    global Jogador
    global ColecaoComida
    global GameOver
    global ArenaSize

    RenderMap(DISPLAY)

    for jogador in ColecaoJogador:
        jogador.Draw(DISPLAY)

    for food in ColecaoComida:
        food.Render(DISPLAY)

    HUD_Surface = pygame.Surface((300, 75))
    HUD_Surface.blit(pygame.transform.chop(DISPLAY, (5, 600 - HUD_Surface.get_height() - 5, HUD_Surface.get_width(), HUD_Surface.get_height())), (5, 600 - HUD_Surface.get_height() - 5))

    RenderHUD(HUD_Surface)

    DISPLAY.blit(HUD_Surface, (5, 600 - HUD_Surface.get_height() - 5))

def RenderMap(DISPLAY):
    # Draw the Borders
    shape.Shape_Rectangle(DISPLAY, (abs(CameraX), abs(CameraY), abs(CameraY)), (CameraX - 4, CameraY - 4, ArenaSize[0] + 8, ArenaSize[1] + 8), 5, 10)

    for x in range(int(ArenaSize[0] / 60)):
        for y in range(int(ArenaSize[1] / 60)):
            Game.ConteudoPadrao.ImageRender(DISPLAY, "/Background.png", CameraX + x * 64, CameraY + y * 64)

def RenderHUD(DISPLAY):
    if not Jogador is None:
        Text = "Size: {0}\n" \
               "Score: {1}".format(Jogador.SnakeSize, Jogador.Score)
        Game.ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 12, Text, (200, 200, 215), 5, 5)

def Reset():
    global ColecaoComida
    global ColecaoJogador
    global Jogador

    del Jogador
    Jogador = None

    ColecaoComida.clear()
    ColecaoJogador.clear()

    ColecaoJogador.append(Objects.Player(CurrentNickname))
    ColecaoJogador.append(Objects.Player("Bot uau"))


def Update():
    global Jogador
    global ColecaoComida
    global GameOverWait
    global GameOver
    global ColecaoJogador
    global CameraX
    global CameraY
    global CurrentIndex

    # -- Acha o jogador na lista de Jogadores -- #
    if Jogador is None:
        for i, jogador in enumerate(ColecaoJogador):
            if jogador.Nickname == CurrentNickname:
                Jogador = jogador
                CurrentIndex = i

    # -- Spawn comida se não tiver mais -- #
    if len(ColecaoComida) < FoodSpawnRate:
        ColecaoComida.append(Objects.Food(randint(32, ArenaSize[0] - 32), randint(32, ArenaSize[1] - 32)))

    if not Jogador is None:
        ColecaoJogador[CurrentIndex] = Jogador

        for i, jogador in enumerate(ColecaoJogador):
            if i == CurrentIndex:
                CameraX = (800 / 2) - Jogador.PlayerPos[0]
                CameraY = (600 / 2) - Jogador.PlayerPos[1]

            jogador.Update()

            for i, food in enumerate(ColecaoComida):
                food.Iteration = i
                food.Update()
                if jogador.Rectangle.colliderect(food.Rectangle):
                    # -- Delete the Food -- #
                    if not food.Deleted:
                        food.Deleted = True
                        # -- Increase snake size when food is deleted -- #
                        jogador.SnakeSize += food.DeleteValue
                        jogador.Score += 1

                    # -- Remove the Food -- #
                    if food.DeleteEnd:
                        ColecaoComida.pop(i)

            # -- Update bot AI -- #
            if jogador.PlayerPos[0] >= ArenaSize[0] - jogador.Rectangle[2]:
                if jogador.SnakeSize > 15:
                    jogador.MovPos = 3

                jogador.MovPos = 1


def EventUpdate(event):
    global Jogador

    if event.type == pygame.KEYUP and event.key == pygame.K_d:
        Jogador.MovPos = 0

    if event.type == pygame.KEYUP and event.key == pygame.K_a:
        Jogador.MovPos = 1

    if event.type == pygame.KEYUP and event.key == pygame.K_s:
        Jogador.MovPos = 2

    if event.type == pygame.KEYUP and event.key == pygame.K_w:
        Jogador.MovPos = 3

    if event.type == pygame.KEYUP and event.key == pygame.K_g:
        Jogador.SnakeSize += 10

    if event.type == pygame.KEYUP and event.key == pygame.K_f:
        Jogador.SnakeSize -= 10

        if Jogador.SnakeSize <= 0:
            Jogador.SnakeSize = 1

    if event.type == pygame.KEYUP and event.key == pygame.K_k:
        Jogador.Speed -= 1

        if Jogador.Speed < 4:
            Jogador.Speed = 4

    if event.type == pygame.KEYUP and event.key == pygame.K_j:
        Jogador.Speed += 1

    if event.type == pygame.MOUSEBUTTONUP:
        ColecaoComida.append(Objects.Food(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    if event.type == pygame.KEYUP and event.key == pygame.K_r:
        Reset()

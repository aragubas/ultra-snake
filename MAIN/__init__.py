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
from ENGINE import cntMng
from ENGINE import shape
from ENGINE import MAIN
import pygame
from random import randint
from UltraSnake.MAIN.Screens import GameScreen

ConteudoPadrao = cntMng.ContentManager()

def Initialize(DISPLAY):
    ConteudoPadrao.SetFontPath("Conteudo/Fonts")
    ConteudoPadrao.LoadSpritesInFolder("Conteudo/Sprite")
    ConteudoPadrao.LoadSoundsInFolder("Conteudo/Sound")

    MAIN.ReceiveCommand(0, 60)
    MAIN.ReceiveCommand(5, "Ultra Snake 1.0")

    GameScreen.Initialize()

def Update():
    GameScreen.Update()

def GameDraw(DISPLAY):
    global Jogador
    global FoodCollection
    global GameOver

    DISPLAY.fill((0, 0, 0))

    GameScreen.GameDraw(DISPLAY)

    DebugText = "FPS: {0}/{1}\n" \
                "CameraX: {2}\n" \
                "CameraY: {3}\n".format(str(MAIN.clock.get_fps()), str(MAIN.clock.get_time()), str(GameScreen.CameraX), str(GameScreen.CameraY))

    ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 12, DebugText, (255, 0, 255), 5 ,5)

def EventUpdate(event):
    GameScreen.EventUpdate(event)

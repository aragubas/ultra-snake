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
from ENGINE import utils

# Objetos
ColecaoJogador = list()
ColecaoComida = list()
Jogador = None

# Camera and Spectator Mode
FocusCameraPlayerObj = None
SpectatorModeDelay = 0
SpectatorModeEnabled = False
SpectatorModePlayerToFocusObject = None
SpectatorModePlayerToFocusToggle = True
SpectatorModeIndex = 0

CurrentNickname = "ceira"
CurrentIndex = 0

#Camera
CameraX = 0
CameraY = 0

#Game Logic
ArenaSize = (5000, 5000)
FoodSpawnRate = 128

MessagesList = list()
MessagesList.append("Game Started")
MessagesScroll = 0

def Initialize():
    Reset()

def GameDraw(DISPLAY):
    global Jogador
    global ColecaoComida
    global GameOver
    global ArenaSize

    RenderMap(DISPLAY)

    for jogador in ColecaoJogador:
        if Game.ConteudoPadrao.IsOnScreen(DISPLAY, CameraX + jogador.PlayerPos[0], CameraY + jogador.PlayerPos[1], jogador.Rectangle[2], jogador.Rectangle[3]):
            jogador.IsOnScreen = True
            jogador.Draw(DISPLAY)
        else:
            jogador.IsOnScreen = False

    for food in ColecaoComida:
        if Game.ConteudoPadrao.IsOnScreen(DISPLAY, CameraX + food.Rectangle[0], CameraY + food.Rectangle[1], food.Rectangle[2], food.Rectangle[3]):
            food.Render(DISPLAY)

    # -- Render Player Statistics -- #
    HUD_Surface = pygame.Surface((475, 100))
    RenderHUD(HUD_Surface, DISPLAY)
    DISPLAY.blit(HUD_Surface, (5, 600 - HUD_Surface.get_height() - 5))

    # -- Render Scoreboard -- #
    HUD_Surface = pygame.Surface((200, 230))
    RenderScoreboard(HUD_Surface, DISPLAY)
    DISPLAY.blit(HUD_Surface, (800 - HUD_Surface.get_width() + 5, 5))


def RenderMap(DISPLAY):
    # Draw the Borders
    shape.Shape_Rectangle(DISPLAY, (abs(CameraX), abs(CameraY), abs(CameraY)), (CameraX - 4, CameraY - 4, ArenaSize[0] + 8, ArenaSize[1] + 8), 5, 10)

    for x in range(int(ArenaSize[0] / 60)):
        for y in range(int(ArenaSize[1] / 60)):
            Game.ConteudoPadrao.ImageRender(DISPLAY, "/Background.png", CameraX + x * 64, CameraY + y * 64)

def RenderScoreboard(DISPLAY, SourceDisplay):
    global ColecaoJogador
    ScreenCopy = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCALPHA)
    ScreenCopy.blit(SourceDisplay, (0, 0), (5, 600 - DISPLAY.get_height() - 5, DISPLAY.get_width(), DISPLAY.get_height()))
    DarkRect = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCALPHA)
    DarkRect.fill((0, 0, 0, 200))
    ScreenCopy.blit(DarkRect, (0, 0))
    DISPLAY.blit(fx.Surface_Blur(ScreenCopy, 15), (0, 0))

    Text = " -- The Best of {0}'s -- \n".format(len(ColecaoJogador))

    for jogador in ColecaoJogador:
        Text += "{0} : {1}\n".format(jogador.Nickname, utils.FormatNumber(jogador.Score).replace(".00", ""))

    Game.ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 8, Text, (230, 230, 230), 3, 3)

    DISPLAY.set_alpha(100)

def RenderHUD(DISPLAY, SourceDisplay):
    global MessagesScroll

    ScreenCopy = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCALPHA)
    ScreenCopy.blit(SourceDisplay, (0, 0), (5, 600 - DISPLAY.get_height() - 5, DISPLAY.get_width(), DISPLAY.get_height()))
    DarkRect = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCALPHA)
    DarkRect.fill((0, 0, 0, 200))
    ScreenCopy.blit(DarkRect, (0, 0))
    DISPLAY.blit(fx.Surface_Blur(ScreenCopy, 15), (0, 0))


    Text = "null"
    if not Jogador is None:
        if not Jogador.IsDead:
            Text = "Size: {0}\n" \
                   "Score: {1}".format(Jogador.SnakeSize, Jogador.Score)

    if SpectatorModeEnabled:
        if not SpectatorModePlayerToFocusObject is None:
            Text = "Spectator Mode\nSpecting: {0}".format(SpectatorModePlayerToFocusObject.Nickname)

        else:
            Text = "Spectator Mode\nSpecting: Unknow"

    Game.ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 12, Text, (200, 200, 215), 3, 3)

    # -- Render the Messages -- #
    for i, message in enumerate(MessagesList):
        Text = message
        TextHeight = Game.ConteudoPadrao.GetFont_height("/PressStart2P.ttf", 10, Text)
        TextWidth = Game.ConteudoPadrao.GetFont_width("/PressStart2P.ttf", 10, Text)
        TextY = MessagesScroll + i * TextHeight + 2
        Color = (155, 155, 155)

        if Text.startswith("$"):
            Color = (255, 155, 175)

        if Text.startswith("$#"):
            Color = (155, 200, 109)

        Text = Text.replace("$#", "").replace("$", "")

        if TextY > DISPLAY.get_height():
            MessagesScroll -= TextHeight * 1.2

        Game.ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 10, Text, Color, DISPLAY.get_width() - TextWidth - 5, TextY)

def AddMessage(text):
    global MessagesScroll
    global MessagesList

    # -- Check if is time to clear the list -- #
    if len(MessagesList) >= 128:
        MessagesList.clear()

    # -- Calculate the Scroll Margin -- #
    Text = text
    TextHeight = Game.ConteudoPadrao.GetFont_height("/PressStart2P.ttf", 10, Text)
    TextY = MessagesScroll + len(MessagesList) * TextHeight + 10

    if TextY > 100:
        MessagesScroll -= TextY

    MessagesList.append(text)
    Game.ConteudoPadrao.PlaySound("/Chat_Message.wav")

def DeletePlayer():
    global Jogador
    global ColecaoJogador
    global CurrentIndex

    if not Jogador is None:
        del Jogador
        del ColecaoJogador[CurrentIndex]

        Jogador = None

def Reset():
    global ColecaoComida
    global ColecaoJogador
    global Jogador
    global MessagesList
    global MessagesScroll
    global SpectatorModeDelay
    global FocusCameraPlayerObj
    global SpectatorModeEnabled
    global SpectatorModePlayerToFocusObject
    global SpectatorModePlayerToFocusToggle
    del Jogador
    global ArenaSize

    Jogador = None

    # -- Remove Any Residual Data -- #
    ColecaoComida.clear()
    ColecaoJogador.clear()
    MessagesList.clear()
    MessagesScroll = 0

    ColecaoJogador.append(Objects.Player(CurrentNickname))
    FocusCameraPlayerObj = ColecaoJogador[0]

    for _ in range(32):
        ColecaoComida.append(Objects.Food(randint(0, ArenaSize[0]), randint(0, ArenaSize[1])))

    for i in range(0, 24):
        utils.GarbageCollector_Collect()
        ColecaoJogador.append(Objects.Player("Bot #{0}".format(i)))

    FocusCameraPlayerObj = None
    SpectatorModeDelay = 0
    SpectatorModeEnabled = False
    SpectatorModePlayerToFocusObject = None
    SpectatorModePlayerToFocusToggle = True
    utils.GarbageCollector_Collect()

def SpectateRandomPlayer(random_player=True, index=0):
    global SpectatorModePlayerToFocusObject
    global SpectatorModePlayerToFocusToggle

    # Set Random Focus
    if random_player:
        Index = randint(0, len(ColecaoJogador) - 1)
    else:
        Index = index
    SpectatorModePlayerToFocusObject = ColecaoJogador[Index]
    SpectatorModePlayerToFocusToggle = True

    AddMessage("$#Spectating:" + ColecaoJogador[Index].Nickname)

def Update():
    global Jogador
    global ColecaoComida
    global GameOverWait
    global GameOver
    global ColecaoJogador
    global CameraX
    global CameraY
    global CurrentIndex
    global FocusCameraPlayerObj
    global SpectatorModeDelay
    global SpectatorModeEnabled
    global SpectatorModePlayerToFocusToggle
    global SpectatorModePlayerToFocusObject
    global FocusCameraPlayerObj
    global SpectatorModeEnabled

    # -- Detect if Player is Dead then Delete it instance and Spectate a Random Player -- #
    if not Jogador is None:
        if Jogador.IsDead:
            SpectatorModeEnabled = True
            SpectatorModeDelay += 1

            if SpectatorModeDelay >= 50:
                DeletePlayer()
                SpectateRandomPlayer()

    if SpectatorModeEnabled:
        if SpectatorModePlayerToFocusToggle:
            SpectatorModePlayerToFocusToggle = False

            FocusCameraPlayerObj = SpectatorModePlayerToFocusObject

    # -- Acha o jogador na lista de Jogadores -- #
    if Jogador is None and not SpectatorModeEnabled:
        for i, jogador in enumerate(ColecaoJogador):
            if not Jogador is None:
                break

            if jogador.Nickname == CurrentNickname:
                Jogador = jogador
                CurrentIndex = i
                FocusCameraPlayerObj = Jogador

                AddMessage("$#Player found in Server")
            else:
                AddMessage("$Player not found in Server")
                SpectatorModeEnabled = True
                SpectateRandomPlayer()

    # -- Aways Update Player Index -- #
    if not Jogador is None:
        CurrentIndex = ColecaoJogador.index(Jogador)

        # -- Move the Player -- #
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            Jogador.MovPos = 0

        if pressed[pygame.K_a]:
            Jogador.MovPos = 1

        if pressed[pygame.K_s]:
            Jogador.MovPos = 2

        if pressed[pygame.K_w]:
            Jogador.MovPos = 3

    # -- Spawna comida se não tiver mais -- #
    if len(ColecaoComida) < FoodSpawnRate:
        ColecaoComida.append(Objects.Food(randint(32, ArenaSize[0] - 32), randint(32, ArenaSize[1] - 32)))

    # -- Atualiza o Jogador e o Bot -- #
    if not Jogador is None:
        # -- Atualiza o objeto do jogador na lista -- #
        ColecaoJogador[CurrentIndex] = Jogador

    for i, jogador in enumerate(ColecaoJogador):
        # -- if Instance is Client, Center the camera to it -- #
        if jogador == FocusCameraPlayerObj:
            CameraX = (800 / 2) - jogador.PlayerPos[0]
            CameraY = (600 / 2) - jogador.PlayerPos[1]

        # -- Update Player Object -- #
        jogador.Update()

        # -- Eat the Food -- #
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
                    if jogador.IsOnScreen:
                        Game.ConteudoPadrao.PlaySound("/Food_Eat.wav")

                # -- Remove the Food -- #
                if food.DeleteEnd:
                    ColecaoComida.pop(i)

        # -- Kill player when coliding with each other -- #
        for player in ColecaoJogador:
            if not player == jogador: # -- Workaround to fix: Player killing when coliding with itself
                if jogador.Rectangle.colliderect(player.Rectangle) and jogador.Score > 1 and not player.IsDead:
                    player.IsDead = True
                    jogador.IsDead = False
                    jogador.Score += player.Score

        # -- Delete Player when Dead -- #
        if jogador.IsDead:
            if not jogador.VarListClearWhenDeadTrigger:
                jogador.VarListClearWhenDeadTrigger = True
                jogador.VarList.clear()
                AddMessage("${0} is dead".format(jogador.Nickname))

                Game.ConteudoPadrao.PlaySound("/Player_Dead.wav")

            if not jogador.Nickname == CurrentNickname:
                ColecaoJogador[ColecaoJogador.index(jogador)] = Objects.Player(utils.Random_String(12))
                break

        if not jogador.Nickname == CurrentNickname and not jogador.IsDead:
            try:
                jogador.Stop = True
                DestX = jogador.VarList[0].Rectangle[0]
                DestY = jogador.VarList[0].Rectangle[1]
                jogador.MovePlayer()


                if DestX - jogador.Speed < jogador.PlayerPos[0]:
                    jogador.PlayerPos = (jogador.PlayerPos[0] - jogador.Speed, jogador.PlayerPos[1])
                    jogador.MovPos = 1


                if DestX - jogador.Speed > jogador.PlayerPos[0]:
                    jogador.PlayerPos = (jogador.PlayerPos[0] + jogador.Speed, jogador.PlayerPos[1])
                    jogador.MovPos = 0

                if DestY - jogador.Speed < jogador.PlayerPos[1]:
                    jogador.PlayerPos = (jogador.PlayerPos[0], jogador.PlayerPos[1] - jogador.Speed)
                    jogador.MovPos = 3

                if DestY - jogador.Speed > jogador.PlayerPos[1]:
                    jogador.PlayerPos = (jogador.PlayerPos[0], jogador.PlayerPos[1] + jogador.Speed)
                    jogador.MovPos = 2

                # -- Check if food exists -- #
                Found = False
                for food in ColecaoComida:
                    if food == jogador.VarList[0]:
                        Found = True

                if not Found:
                    Index = randint(0, len(ColecaoComida) - 1)
                    RandomFood = ColecaoComida[Index]
                    print("Novo endereço de Cumida:\n" + str(Index))

                    jogador.VarList.clear()
                    jogador.VarList.append(RandomFood)
                    jogador.VarList.append(False)

            except IndexError:
                Index = randint(0, len(ColecaoComida) - 1)
                RandomFood = ColecaoComida[Index]
                print(Index)

                jogador.VarList.append(RandomFood)
                jogador.VarList.append(False)


def EventUpdate(event):
    global Jogador
    global MessagesList
    global SpectatorModePlayerToFocusObject
    global SpectatorModePlayerToFocusToggle
    global SpectatorModeIndex
    global MessagesScroll

    if not Jogador is None:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                Jogador.SnakeSize += 10

            if event.key == pygame.K_f:
                Jogador.SnakeSize -= 10

                if Jogador.SnakeSize <= 0:
                    Jogador.SnakeSize = 1

            if event.key == pygame.K_k:
                Jogador.Speed -= 1

                if Jogador.Speed < 4:
                    Jogador.Speed = 4

            if event.key == pygame.K_j:
                Jogador.Speed += 1

    if event.type == pygame.KEYUP and SpectatorModeEnabled:
        if event.key == pygame.K_c:
            SpectateRandomPlayer()
            Game.ConteudoPadrao.PlaySound("/HUD_Click.wav")

        if event.key == pygame.K_n:
            SpectatorModeIndex += 1

            if SpectatorModeIndex > len(ColecaoJogador) - 1:
                SpectatorModeIndex = 0

            SpectateRandomPlayer(False, SpectatorModeIndex)
            Game.ConteudoPadrao.PlaySound("/HUD_Click.wav")

        if event.key == pygame.K_b:
            SpectatorModeIndex -= 1

            if SpectatorModeIndex <= 0:
                SpectatorModeIndex = len(ColecaoJogador) - 1

            SpectateRandomPlayer(False, SpectatorModeIndex)
            Game.ConteudoPadrao.PlaySound("/HUD_Click.wav")

    if event.type == pygame.MOUSEBUTTONUP:
        ColecaoComida.append(Objects.Food(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    # -- Scroll the Chat -- #
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            MessagesScroll -= 5
            Game.ConteudoPadrao.PlaySound("/HUD_Click.wav", 0.2)

        elif event.button == 5:
            MessagesScroll += 5
            Game.ConteudoPadrao.PlaySound("/HUD_Click.wav", 0.2)

    if event.type == pygame.KEYUP and event.key == pygame.K_r:
        Reset()
        Game.ConteudoPadrao.PlaySound("/HUD_Click.wav")






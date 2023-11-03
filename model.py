from random import randrange, choice
from pynput import keyboard

from data import data

# TODO <remove>
from icecream import ic
# TODO </remove>
        
class Game():
    def __init__(self, mapSize: int = 4) -> None:
        self.mapSize = mapSize
        self.map = [[None for _ in range(mapSize)] for _ in range(mapSize)]
        self.score = 0
        self.spawnTile()
    
    def spawnTile(self) -> None:
        empty_space = [(i%self.mapSize, int(i//self.mapSize)) for i in range(self.mapSize**2) if self.map[i%self.mapSize][int(i//self.mapSize)] == None]
        x, y = choice(empty_space)
        self.map[x][y] = 2 if randrange(100)<90 else 4
        
    def move(self, player_choise):
        key = keyboard.Key
        is_change = False
        match player_choise:
            case key.left:
                for x in range(self.mapSize):
                    for y in range(self.mapSize):
                        tile_value = self.map[x][y]
                        if tile_value != None:
                            new_x = x 
                            while new_x > 0 and (self.map[new_x-1][y] == None or self.map[new_x-1][y] == tile_value):
                                new_x -= 1
                            if new_x != x:
                                is_change = True
                                self.map[x][y] = None
                                if self.map[new_x][y] == tile_value:
                                    self.map[new_x][y] = tile_value*2
                                    self.score += tile_value*2
                                else:
                                    self.map[new_x][y] = tile_value
                                
            case key.right:
                 for x in range(self.mapSize-1, -1, -1):
                    for y in range(self.mapSize-1, -1, -1):
                        tile_value = self.map[x][y]
                        if tile_value != None:
                            new_x = x 
                            while new_x < self.mapSize-1 and (self.map[new_x+1][y] == None or self.map[new_x+1][y] == tile_value):
                                new_x += 1
                            if new_x != x:
                                is_change = True
                                self.map[x][y] = None
                                if self.map[new_x][y] == tile_value:
                                    self.map[new_x][y] = tile_value*2
                                    self.score += tile_value*2
                                else:
                                    self.map[new_x][y] = tile_value
                                    
            case key.up:
                for x in range(self.mapSize):
                    for y in range(self.mapSize):
                        tile_value = self.map[x][y]
                        if tile_value != None:
                            new_y = y 
                            while new_y > 0 and (self.map[x][new_y-1] == None or self.map[x][new_y-1] == tile_value):
                                new_y -= 1
                            if new_y != y:
                                is_change = True
                                self.map[x][y] = None
                                if self.map[x][new_y] == tile_value:
                                    self.map[x][new_y] = tile_value*2
                                    self.score += tile_value*2
                                else:
                                    self.map[x][new_y] = tile_value
                                    
            case key.down:
                for x in range(self.mapSize-1, -1, -1):
                    for y in range(self.mapSize-1, -1, -1):
                        tile_value = self.map[x][y]
                        if tile_value != None:
                            new_y = y 
                            while new_y < self.mapSize-1 and (self.map[x][new_y+1] == None or self.map[x][new_y+1] == tile_value):
                                new_y += 1
                            if new_y != y:
                                is_change = True
                                self.map[x][y] = None
                                if self.map[x][new_y] == tile_value:
                                    self.map[x][new_y] = tile_value*2
                                    self.score += tile_value*2
                                else:
                                    self.map[x][new_y] = tile_value
                                    
            case key.esc:
                ic('game over')
                
        if is_change:
            self.spawnTile()
            self.displayMap()
            self.checkGameEnd()
            
    def checkGameEnd(self) -> None:
        is_move_possible = False
        for x in range(self.mapSize):
            for y in range(self.mapSize):
                if self.map[x][y] == None:
                    is_move_possible = True
                    break
                else:
                    if x < self.mapSize-1 and self.map[x][y] == self.map[x+1][y]:
                        is_move_possible = True
                        break
                    elif y < self.mapSize-1 and self.map[x][y] == self.map[x][y+1]:
                        is_move_possible = True
                        break
            if is_move_possible:
                break
        if not is_move_possible:
            keyboard.Controller().tap(keyboard.Key.esc)
     
    def displayMap(self, is_console_need_refresh: bool = True) -> None:
        data['map'] = self.map
        if is_console_need_refresh:
            LINE_UP  = '\033[1A'
            for _ in range(self.mapSize*2-1):
                print(LINE_UP, end='')
            print('\r', end='')

        res = f"score: {data['score']}\n"
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                if self.map[j][i] == None:
                    res += "   0 "
                else:
                    res += f"{self.map[j][i]:>4} "
            res += "\n\n"
        print(res[:-2], end='')
        
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self, newValue):
        data['score'] = newValue
        self.__score = newValue
    
def model():
    game = Game()
    game.displayMap(False)
    with keyboard.Events() as events:
        is_running = True
        while is_running:
            event = events.get()
            if type(event) == keyboard.Events.Press:
                game.move(event.key)
            if event.key == keyboard.Key.esc:
                is_running = False
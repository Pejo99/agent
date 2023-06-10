import random
import pandas as pd
from config import *

class Agent:
    
    def __init__(self, color, index):
        self.color = color
        self.index = index
        self.visible_worlds = []
        self.positions = []
        self.can_shoots = []
        self.holding_flags = []
        self.actions = []
        self.directions = []
    
    def __update__(self, visible_world, position, can_shoot, holding_flag):
        if can_shoot and random.random() > 0.5:
            action = "shoot"
        else:
            action = "move"
            
        if self.color == "blue":
            preferred_direction = "right"
            if holding_flag:
                preferred_direction = "left"
        elif self.color == "red":
            preferred_direction = "left"
            if holding_flag:
                preferred_direction = "right"
        
        r = random.random() * 1.5
        if r < 0.25:
            direction = "left"
        elif r < 0.5:
            direction = "right"
        elif r < 0.75:
            direction = "up"
        elif r < 1.0:
            direction = "down"
        else:
            direction = preferred_direction
        
        self.visible_worlds.append(visible_world)
        self.positions.append(position)
        self.can_shoots.append(can_shoot)
        self.holding_flags.append(holding_flag)
        self.actions.append(action)
        self.directions.append(direction)
        
        return action, direction
    
    def __terminate__(self, reason):
        if reason == "died":
            print(self.color, self.index, "died")

        # Create a DataFrame from the collected data
        data = {
            'visible_world': self.visible_worlds,
            'position': self.positions,
            'can_shoot': self.can_shoots,
            'holding_flag': self.holding_flags,
            'action': self.actions,
            'direction': self.directions
        }
        df = pd.DataFrame(data)

        # Save the data to a CSV file
        df.to_csv("data.csv", index=False)

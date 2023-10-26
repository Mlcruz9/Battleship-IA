import numpy as np

# After training, you can use the Q-table to make moves and play the game
# The Q-table contains the learned Q-values for each state-action pair
# You can use a policy (e.g., epsilon-greedy) to choose actions based on the Q-table
# The policy will balance exploration and exploitation



class Ship:
    '''
        Class for a ship in the game, allows to create a 
        ship with a random position and orientation
            '''
    
    def __init__(self, size):
        self.row = np.random.randint(10) #Random row
        self.col = np.random.randint(10) #Random column
        self.size = size #Size of the ship
        self.orientation = np.random.choice(['h', 'v']) #Random orientation
        self.indexes = self.compute_indexes() #Compute the indexes of the ship

    def compute_indexes(self):
        start_index = [self.row, self.col] #Initial index of the ship
        while True:
            if self.orientation == 'h' and (self.col + self.size <= 9): #If the orientation is horizontal and the ship fits in the board
                return [(self.row, self.col + i) for i in range(self.size)] #Return the indexes of the ship, grows in the column
                break
            
            elif self.orientation == 'v' and (self.row + self.size <= 9): #If the orientation is vertical and the ship fits in the board
                return [(self.row + i, self.col) for i in range(self.size)] #Return the indexes of the ship, grows in the row
                break

            else:
                self.row = np.random.randint(10) #If the ship doesn't fit, create a new random position and orientation
                self.col = np.random.randint(10) 
                self.orientation = np.random.choice(['h', 'v'])
            

class Player:
    '''
    Class Player, allows to create a player with 10 ships
    '''
    def __init__(self):
        self.ships = [] #List of ships
        #self.search = ["U" for i in range(100)] # U: Unknown, M: Miss, H: Hit -- Unused
        self.place_ships(sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]) #Sizes of the ships

    def place_ships(self, sizes): #Place the ships on the board
        for size in sizes:
            uncolocated = True #While the ship is not placed
            while uncolocated:
                ship = Ship(size) #Ship for each size

                if len(self.ships) == 0: #If there are no ships, append the ship
                    self.ships.append(ship.indexes)
                    uncolocated = False
                    break
                
                else: #If there are ships, check if the new ship overlaps with the existing ones
                    for (i, j) in ship.indexes: #For each index of the ship
                        is_overlap = any((i, j) in existing_ship for existing_ship in self.ships) #Check if the index is in the existing ships
                        if is_overlap:
                                break
                            
                        in_sorroundings = any((i + 1, j) in existing_ship or (i - 1, j) in existing_ship or \
                                            (i, j + 1) in existing_ship or (i, j - 1) in existing_ship for \
                                                existing_ship in self.ships) #Check if the index is in the surroundings of the existing ships
                        if in_sorroundings:
                            break

                        in_diagonals = any((i + 1, j + 1) in existing_ship or (i - 1, j - 1) in existing_ship or \
                                                (i + 1, j - 1) in existing_ship or (i - 1, j + 1) in existing_ship for \
                                                    existing_ship in self.ships) #Check if the index is in the diagonals of the existing ships
                        
                        if in_diagonals:
                            break

                    else: #If the ship doesn't overlap with the existing ones, not in sorroundings, not in diagonals, append the ship
                        self.ships.append(ship.indexes)
                        uncolocated = False

class Game:

    '''
    Class Game, allows to create a game with 2 players
    '''

    def __init__(self):
        self.player_1 = Player() #Player 1 with 10 ships
        self.player_2 = Player() #Player 2 with 10 ships
        self.player_1_turn = True #Player 1 starts
        self.over = False #Game is not over
        self.player_1_removed_positions = [] #List of removed positions of player 1
        self.player_2_removed_positions = [] #List of removed positions of player 2
        self.player_1_shots = [] #List of shots of player 1
        self.player_2_shots = [] #List of shots of player 2

    def make_move(self, row, col): #Make a move on the battleship board
        player = self.player_1 if self.player_1_turn else self.player_2 #Player 1 if it's player 1 turn, player 2 otherwise
        opponent = self.player_2 if self.player_1_turn else self.player_1 #Player 2 if it's player 1 turn, player 1 otherwise
        removed_positions = self.player_1_removed_positions if self.player_1_turn else self.player_2_removed_positions #Removed positions of player 1 if it's player 1 turn, removed positions of player 2 otherwise	
        players_shots = self.player_1_shots if self.player_1_turn else self.player_2_shots #Shots of player 1 if it's player 1 turn, shots of player 2 otherwise

        while not self.over: #While the game is not over
            
            if (row, col) not in removed_positions and (row, col) not in players_shots: #If the position is not in the removed positions and not in the shots

                for ship in opponent.ships: #For each ship of the opponent
                    if (row, col) in ship: #If the position is in the ship
                        removed_positions.append((row, col))  # Append to removed_positions for hits
                        ship.remove((row, col)) #Remove the position from the ship
                        if len(ship) == 0: #If the ship is sunk
                            opponent.ships.remove(ship) #Remove the ship from the opponent
                            if len(opponent.ships) == 0: #If there are no ships left
                                self.over = True
                                return "W"  # All ships are sunk, game over (win) --- Note this and S, H are not used, are for future implementations
                            return "S"  # Ship is sunk but there are remaining ships
                        return "H"  # Ship is hit but not sunk

                # If it's not a hit, handle miss or invalid shot
                if ((row, col) not in players_shots) and ((row, col) not in removed_positions): #If the position is not in the shots and not in the removed positions
                    players_shots.append((row, col)) #Append the position to the shots
                    self.player_1_turn = not self.player_1_turn #Change the turn
                    return "M"  # Miss

                return "M"  # If it's already shot or removed position, it's a miss
            
            else: #If the position is in the removed positions or in the shots
                row = np.random.randint(10)
                col = np.random.randint(10)
        

    #Make a move on the battleship board with a QAgent instead of doing it randomly
    # def make_move_qagent(self, row, col):
    #     player = self.player_1 if self.player_1_turn else self.player_2
    #     opponent = self.player_2 if self.player_1_turn else self.player_1
    #     removed_positions = self.player_1_removed_positions if self.player_1_turn else self.player_2_removed_positions
    #     players_shots = self.player_1_shots if self.player_1_turn else self.player_2_shots

    #     while not self.over:

    #         for ship in opponent.ships:
    #             if (row, col) in ship:
    #                 removed_positions.append((row, col))  # Always append to removed_positions for hits
    #                 ship.remove((row, col))
    #                 if len(ship) == 0:
    #                     opponent.ships.remove(ship)
    #                     if len(opponent.ships) == 0:
    #                         self.over = True
    #                         return "W"
    #                     return "S"
    #                 return "H"


# #Create a qagent class for movements on the battleship board
# class QAgent:
#     board = 10
#     Num_Actions = 100
#     num_states = 2

#     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
#         self.q_table = np.zeros((self.board, self.board, self.num_states, self.Num_Actions))
#         self.alpha = alpha
#         self.gamma = gamma
#         self.epsilon = epsilon

#     def get_action(self, state):
#         if np.random.uniform() < self.epsilon:
#             action = np.random.randint(self.Num_Actions)
#         else:
#             action = np.argmax(self.q_table[state])
#         return action
    
#     def update(self, state, action, reward, next_state):
#         self.q_table[state][action] = (1 - self.alpha) * self.q_table[state][action] + \
#             self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]))
    
#     def train(self, num_episodes=1000):
#         for i in range(num_episodes):
#             game = Game()
#             while not game.over:
#                 state = np.random.randint(2)
#                 action = self.get_action(state)
#                 reward = game.make_move(action // 10, action % 10)
#                 next_state = 1 if game.player_1_turn else 0
#                 self.update(state, action, reward, next_state)
    
#     def play(self):
#         game = Game()
#         while not game.over:
#             state = 1 if game.player_1_turn else 0
#             action = self.get_action(state)
#             reward = game.make_move(action // 10, action % 10)
#             next_state = 1 if game.player_1_turn else 0
#             self.update(state, action, reward, next_state)
#         return game.player_1_turn
    
#     def save(self, file_name):
#         np.save(file_name, self.q_table)
    
#     def load(self, file_name):
#         self.q_table = np.load(file_name)
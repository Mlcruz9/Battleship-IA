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
        self.board = np.full((10, 10), "U") #Board of the player

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
    
    def update_board(self, row, col, value):
        self.board[row, col] = value

class MonteCarloPlayer(Player):

    '''This is a class for a Monte Carlo player, it inherits from the class Player'''

    def __init__(self):
        super().__init__() #Inherits from the class Player
        self.ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.simulated_board = self.board.copy() #Copy of the board
    
    def analyze_hits(self):
        # Analiza el tablero para ajustar los tamaños de los barcos restantes
        visited = set()
        for i in range(10):
            for j in range(10):
                if self.simulated_board[i, j] == "H" and (i, j) not in visited:
                    ship_cells = self.find_contiguous_hits(i, j, visited)
                    ship_size = len(ship_cells)
                    if ship_size in self.ship_sizes:
                        self.ship_sizes.remove(ship_size)
                    for cell in ship_cells:
                        visited.add(cell)
        
        return visited
    
    def find_contiguous_hits(self, i, j, visited):
        if i < 0 or i >= 10 or j < 0 or j >= 10 or self.simulated_board[i, j] != "H" or (i, j) in visited:
            return []
        visited.add((i, j))
        ship_cells = [(i, j)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for di, dj in directions:
            ship_cells.extend(self.find_contiguous_hits(i + di, j + dj, visited))
        return ship_cells
    
    def place_simulated_ships(self):
        self.analyze_hits()  # Ajusta los tamaños de los barcos restantes basado en los "H"
        for size in self.ship_sizes:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                ship = Ship(size)
                if self.can_place_ship(ship.indexes, size):
                    self.ships.append(ship.indexes)
                    for (i, j) in ship.indexes:
                        self.simulated_board[i, j] = 'S'
                    placed = True
                attempts += 1

    def can_place_ship(self, ship_indexes, size):
        for (i, j) in ship_indexes:
            if self.simulated_board[i, j] in ['M', 'S']:
                return False
            if not (0 <= i < 10 and 0 <= j < 10) or self.is_near_other_ship(i, j):
                return False
        return True

    def is_near_other_ship(self, i, j):
        checks = [(i-1, j-1), (i-1, j), (i-1, j+1),
                (i, j-1),(i, j+1),
                (i+1, j-1), (i+1, j), (i+1, j+1)]
        for x, y in checks:
            if 0 <= x < 10 and 0 <= y < 10 and (self.simulated_board[x, y] == 'S' or self.simulated_board[x, y] == 'H'):
                return True
        return False
    
    def reset_ship_sizes(self):
        # Reset ship sizes to full set. Adjust this if the board state is mid-game.
        self.ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    
    def simulate_shot(self):
        """Simula un disparo a una posición aleatoria del tablero y devuelve el resultado junto con las coordenadas."""
        i, j = np.random.randint(0, 10), np.random.randint(0, 10)
        hit = 1 if self.simulated_board[i, j] == 'S' else 0
        return hit, (i, j)


    def simulate_shooting(self, num_shots):
        """Realiza una serie de disparos y cuenta los aciertos por coordenadas."""
        hits_by_coords = {}  # Diccionario para contar aciertos por coordenadas
        for _ in range(num_shots):
            hit, coords = self.simulate_shot()
            if hit:
                if coords not in hits_by_coords:
                    hits_by_coords[coords] = 0
                hits_by_coords[coords] += 1
        return hits_by_coords

    
    def reset_board(self):
        self.simulated_board = self.board.copy()

    def multiple_board_simulations(self, num_simulations, num_shots_per_simulation):
        """Realiza múltiples simulaciones y determina la mejor coordenada para disparar basado en los aciertos."""
        coords_hits = {}
        for _ in range(num_simulations):
            self.reset_board()  # Reinicia el tablero simulado
            self.place_simulated_ships()  # Coloca los barcos
            hits_by_coords = self.simulate_shooting(num_shots_per_simulation)
            for coords, hits in hits_by_coords.items():
                if coords not in coords_hits:
                    coords_hits[coords] = 0
                coords_hits[coords] += hits
        
        # Encontrar las coordenadas con el máximo número de aciertos
        max_hits = max(coords_hits.values())
        best_coords = [coords for coords, hits in coords_hits.items() if hits == max_hits]
        
        # Elegir aleatoriamente entre las mejores coordenadas si hay empates
        # Convertir la lista de tuplas a un array de objetos para manejarlo con NumPy
        best_coords = np.array(best_coords, dtype=object)

        # Seleccionar un índice al azar
        indice_aleatorio = np.random.choice(len(best_coords))

        # Usar el índice para seleccionar la tupla
        tupla_seleccionada = best_coords[indice_aleatorio]
        return tupla_seleccionada
    
    def determine_best_move(self):
        """Determina el mejor movimiento basado en múltiples simulaciones."""
        best_move = self.multiple_board_simulations(1000, 100)
        return best_move

class Game:

    '''
    Class Game, allows to create a game with 2 players
    '''

    def __init__(self, AI = False):
        self.AI = AI #If the game is played against the AI
        self.player_1 = Player() #Player 1 with 10 ships
        self.player_2 = Player() if not AI else MonteCarloPlayer()
        self.player_1_turn = True #Player 1 starts
        self.over = False #Game is not over
        self.player_1_removed_positions = [] #List of removed positions of player 1
        self.player_2_removed_positions = [] #List of removed positions of player 2
        self.player_1_missed_shots = [] #List of shots of player 1
        self.player_2_missed_shots = [] #List of shots of player 2

    def make_move(self): #Make a move on the battleship board
        player = self.player_1 if self.player_1_turn else self.player_2 #Player 1 if it's player 1 turn, player 2 otherwise
        opponent = self.player_2 if self.player_1_turn else self.player_1 #Player 2 if it's player 1 turn, player 1 otherwise

        removed_positions = self.player_1_removed_positions if not self.player_1_turn else self.player_2_removed_positions #Removed positions of player 1 if it's player 1 turn, removed positions of player 2 otherwise	
        players_missed_shots = self.player_1_missed_shots if self.player_1_turn else self.player_2_missed_shots #Shots of player 1 if it's player 1 turn, shots of player 2 otherwise

        if isinstance(player, MonteCarloPlayer):
            row, col = player.determine_best_move()
            print(f"AI shot at {row, col}")
    
        else:
            row = np.random.randint(10)
            col = np.random.randint(10)
            
        if (row, col) not in removed_positions and (row, col) not in players_missed_shots: #If the position is not in the removed positions and not in the shots

            for ship in opponent.ships: #For each ship of the opponent
                if (row, col) in ship: #If the position is in the ship
                    player.update_board(row, col, "H") #Update the board of the player with a hit
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
            # if ((row, col) not in players_shots) and ((row, col) not in removed_positions): #If the position is not in the shots and not in the removed positions
            players_missed_shots.append((row, col)) #Append the position to the shots
            player.update_board(row, col, "M") #Update the board of the player with a miss
            self.player_1_turn = not self.player_1_turn #Change the turn
            return "M"  # Miss
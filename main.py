import tkinter as tk
import os
import time
from uuid import uuid4
import json
import copy

BUTTON_WIDTH = 88
BUTTON_HEIGHT = 95

EMPTY_CELL_WIDTH = 12
EMPTY_CELL_HEIGHT = 6

window = tk.Tk()


class Piece:

    def __init__(self, notation, coords, colour, owner=None):
        self.name = notation
        self.coords = coords
        self.colour = colour
        self.owner = owner
        self.image_paths = ["images/pawn_w.png", "images/pawn_b.png"]
        self.id = f"{self.colour}_{self.name}_{uuid4()}"
        if self.colour == "W":
            self.direction = -1
        else:
            self.direction = 1


    def move_piece(self, board, coords):
        valid_moves = self.get_piece_moves(board.board)
        
        
        if coords in valid_moves:
            
            if board.board[coords[0]][coords[1]]["piece"] != None:

                will_result_in_check = board.will_result_in_check(self, coords)
                print(f"Will result in check: {will_result_in_check}")
                if will_result_in_check:
                    return False
                else:
                    #print(f"Moving from {self.coords} to {coords}")

                    #print(board.board[coords[0]][coords[1]]["piece"].id)
                    #print(board.board[self.coords[0]][self.coords[1]]["piece"])#it's own cell is already empty!!??!??

                    board.remove_piece(coords)


                    board.move_piece(self, coords)

                    #TODO adjust owner params
                    self.coords = coords
                    return True
                
            else:
                will_result_in_check = board.will_result_in_check(self, coords)
                print(f"Will result in check: {will_result_in_check}")
                #print(f"Will result in check: {will_result_in_check}")
                if will_result_in_check:
                    return False
                else:
                    board.move_piece(self, coords)
                    self.coords = coords
                    return True                
        
        return False
        

    def get_piece_moves(self, board, display=False):
        
        return []



class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_move = True

    def get_piece_moves_aggressive(self, board, display=False):

        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]


        directions = [(1, 1), (-1, 1)]

        for i, direction in enumerate(directions):

            #check if moving in this direction is within the bounds of the board
            if xcoordinate + direction[0]< 0 or xcoordinate + direction[0] > 7 or ycoordinate + (direction[1] * self.direction) < 0 or ycoordinate + (direction[1] * self.direction) > 7:
                continue
            
            board_item = board[ycoordinate + (direction[1] * self.direction)][xcoordinate + direction[0]]

            coordinates = [ycoordinate + (direction[1] * self.direction), xcoordinate + direction[0]]
   

            target_cell = board_item["cell"]
            target_piece = board_item["piece"]



            if display:    
                target_cell.configure(bg="red")
                
            possible_moves.append(coordinates)

        return possible_moves

    def get_piece_moves(self, board, display=False):

        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]


        directions = [(1, 1), (-1, 1), (0, 1), (0, 2)]

        for i, direction in enumerate(directions):

            #skip pawn first move if it has moved already
            if not self.first_move and i == 3:
                continue

            #check if moving in this direction is within the bounds of the board
            if xcoordinate + direction[0]< 0 or xcoordinate + direction[0] > 7 or ycoordinate + (direction[1] * self.direction) < 0 or ycoordinate + (direction[1] * self.direction) > 7:
                continue
            
            board_item = board[ycoordinate + (direction[1] * self.direction)][xcoordinate + direction[0]]

            coordinates = [ycoordinate + (direction[1] * self.direction), xcoordinate + direction[0]]

            target_cell = board_item["cell"]
            target_piece = board_item["piece"]


            if i <= 1: #attack directions

                if target_piece != None:
                    
                    if target_piece.colour != self.colour:
                        if display:
                            target_cell.configure(bg="red")

                        possible_moves.append(coordinates)
                
                continue

            else:

                if target_piece == None:
                    if display:
                        target_cell.configure(bg="green")
                    possible_moves.append(coordinates)
                else:

                    break # Because the multi move comes after the single move and the attack checks, breaking stops the pawn from moving through an enemy pawn to a free space behind
        
        return possible_moves


class Rook(Piece):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/rook_w.png", "images/rook_b.png"]

    def get_piece_moves(self, board, display=False):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]


        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            for _ in range(1, 8):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)


                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break

                board_item = board[target_pos_y][target_pos_x]

                coordinates = [target_pos_y, target_pos_x]
                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    if display:
                        target_cell.configure(bg="green")
                    possible_moves.append(coordinates)
                else:
                    if target_piece.colour != self.colour:
                        if display:
                            target_cell.configure(bg="red")
                        possible_moves.append(coordinates)
                    break

               

        return possible_moves
    

class Bishop(Piece):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/bishop_w.png", "images/bishop_b.png"]

    def get_piece_moves(self, board, display=False):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            for _ in range(1, 9):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)
                

                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break
                
                board_item = board[target_pos_y][target_pos_x]

                coordinates = [target_pos_y, target_pos_x]

                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    if display:
                        target_cell.configure(bg="green")
                    possible_moves.append(coordinates)
                else:
                    if target_piece.colour != self.colour:
                        if display:
                            target_cell.configure(bg="red")
                        possible_moves.append(coordinates)
                    break

               

        return possible_moves


class Knight(Piece):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/knight_w.png", "images/knight_b.png"]


    def get_piece_moves(self, board, display=False):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]


        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (-1, -2), (1, -2)]

        for move in moves:
    
            target_pos_x = xcoordinate + move[1]
            target_pos_y = ycoordinate + move[0]


            if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                continue

            board_item = board[target_pos_y][target_pos_x]


            coordinates = [target_pos_y, target_pos_x]
            target_cell = board_item["cell"]
            target_piece = board_item["piece"]

            if target_piece == None:
                if display:
                    target_cell.configure(bg="green")
                possible_moves.append(coordinates)
            else:
                if target_piece.colour != self.colour:
                    if display:
                        target_cell.configure(bg="red")
                    possible_moves.append(coordinates)
                


        return possible_moves
    

class Queen(Piece):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/queen_w.png", "images/queen_b.png"]

    def get_piece_moves(self, board, display=False):
        possible_moves = []
        xcoordinate = self.coords[1]    
        ycoordinate = self.coords[0]

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            for _ in range(1, 9):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)


                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break

                board_item = board[target_pos_y][target_pos_x]


                coordinates = [target_pos_y, target_pos_x]
                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    if display:
                        target_cell.configure(bg="green")

                    possible_moves.append(coordinates)
                else:
                    if target_piece.colour != self.colour:
                        if display:
                            target_cell.configure(bg="red")
                        possible_moves.append(coordinates)
                    break

               

        return possible_moves


class King(Piece):

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/king_w.png", "images/king_b.png"]
                    

    def get_piece_moves(self, board, display=False, board_class=None):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]


        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            target_pos_x = xcoordinate + dir[0]
            target_pos_y = ycoordinate + dir[1]

            if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                continue

            board_item = board[target_pos_y][target_pos_x]

            coordinates = [target_pos_y, target_pos_x]
            target_cell = board_item["cell"]
            target_piece = board_item["piece"]
            


            if target_piece == None:
                        
                if board_class and board_class.will_result_in_check(self, coordinates):
                    continue
                if display:
                    target_cell.configure(bg="green")
                possible_moves.append(coordinates)
            else:
                if target_piece.colour != self.colour:
                                    
                    if board_class and board_class.will_result_in_check(self, coordinates):
                        continue
                    if display:
                        target_cell.configure(bg="red")
                    possible_moves.append(coordinates)
                


        return possible_moves


class ChessBoard:

    def __init__(self):
        self.board = self.generate_board()
        self.test_board = []
        self.highlighted_cells = []
        self.test_highlighted_cells = []
        self.pieces = []
        self.selected_piece = None


    def __str__(self):
        
        pieces = "\n".join([" ".join([col["piece"].id for col in row]) for row in self.board])

        return pieces

    def generate_board(self):

        board = [[" "] * 8 for _ in range(8)]
        
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                color = "#769656"
                if (j+i) % 2 == 0:
                    color = "#eeeed2"   

                
                cell = tk.Button(window, text= j + (i*len(row)), image=None, bg=color, width=EMPTY_CELL_WIDTH, height=EMPTY_CELL_HEIGHT, borderwidth=0, highlightthickness=0)
                cell.configure(command= lambda i=i, j=j: self.handle_piece_click([i, j]))
                cell.grid(row=i, column=j)
                

                board[i][j] = {"cell": cell, "piece": None} 

        return board
    

    def setup_board(self, game_manager):

        piece_layout = {
            "P": {
                "row_coords": [1, 6],
                "col_coords": [0, 1, 2, 3, 4, 5, 6, 7],
                "img_paths": ["images/pawn_w.png", "./images/pawn_b.png"],
                "piece_class": Pawn
            },
            "R": {
                "row_coords": [0, 7],
                "col_coords": [0, 7],
                "img_paths": ["images/rook_w.png", "images/rook_b.png"],
                "piece_class": Rook
            },
            "N": {
                "row_coords": [0, 7],
                "col_coords": [1, 6],
                "img_paths": ["images/knight_w.png", "images/knight_b.png"],
                "piece_class": Knight
            },
            "B": {
                "row_coords": [0, 7],
                "col_coords": [2, 5],
                "img_paths": ["images/bishop_w.png", "images/bishop_b.png"],
                "piece_class": Bishop
            },
            "Q": {
                "row_coords": [0, 7],
                "col_coords": [3],
                "img_paths": ["images/queen_w.png", "images/queen_b.png"],
                "piece_class": Queen
            },
            "K": {
                "row_coords": [0, 7], 
                "col_coords": [4],
                "img_paths": ["images/king_w.png", "images/king_b.png"],
                "piece_class": King
            },
        }

        
        start_time = time.time()
        for piece_key in list(piece_layout.keys()):
            for row in piece_layout[piece_key]["row_coords"]:
                piece_class = piece_layout[piece_key]["piece_class"]

                piece_colour = "B"

                if row > 3: 
                    piece_colour = "W"

                for col in piece_layout[piece_key]["col_coords"]:


                    piece = piece_class(piece_key, [row, col], piece_colour)

                    img_path = piece.image_paths[1]
                    if piece.colour == "W":
                        img_path = piece.image_paths[0]
                    image_abs_path = os.path.abspath(img_path)
                    img = tk.PhotoImage(file=image_abs_path)

                    piece_widget = self.board[row][col]["cell"]

                    piece_widget.configure(image=img, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
                    piece_widget.image = img

                    self.board[row][col]["piece"] = piece

        self.pieces = [cell["piece"] for row in self.board for cell in row if cell["piece"] != None]
        print(self.pieces)
        end_time = time.time()
        print(f"Setup took: {end_time - start_time} to complete")


    def handle_piece_click(self, coords):

        board_item = self.board[coords[0]][coords[1]]


        # clear highlighted_cells
        for cell_coords in self.highlighted_cells:
            cell = self.board[cell_coords[0]][cell_coords[1]]
            cell_details = cell["cell"].grid_info()
            cellx = cell_details["column"]
            celly = cell_details["row"]
            cell = self.board[celly][cellx]

            colour = "#769656"
            if (cellx+celly) % 2 == 0:
                    colour = "#eeeed2"

            self.board[celly][cellx]["cell"].configure(bg=colour)


        self.highlighted_cells = []
        piece = board_item["piece"]

        
        if piece == None: # Clicked on an empty cell
            
            if self.selected_piece != None:

                result = self.selected_piece.move_piece(self, coords)
                self.selected_piece = None
                return result
                
            else: 

                return False
            
        else: # Clicked on a piece
            if self.selected_piece != None:
                if self.selected_piece.colour != piece.colour:
                    result = self.selected_piece.move_piece(self, coords)
                    print(result)
                    self.selected_piece = None
                    return result

            self.selected_piece = piece



            if piece.name == "K":
                moves = piece.get_piece_moves(self.board, display=True, board_class=self)
            else:
                moves = piece.get_piece_moves(self.board, display=True)

            self.highlighted_cells = moves
            window.update()
             
            return False
        

    def will_result_in_check(self, piece, coords):

        current_piece_cell = self.board[piece.coords[0]][piece.coords[1]]
        
        coords_cache = piece.coords.copy()
        def test_move(piece, coords):
            board_copy = []
            for row in self.board:
                row_copy = []
                for cell in row:
                    cell_copy = cell.copy()


                    row_copy.append(cell_copy)

                board_copy.append(row_copy)

            print(f"Piece coords: {piece.coords}")
            board_copy[piece.coords[0]][piece.coords[1]]["piece"] = None
            board_copy[coords[0]][coords[1]]["piece"] = piece

            board_copy[coords[0]][coords[1]]["piece"].coords = coords


            board_str = ""

            for row in board_copy:
                row_str = ""
                for cell in row:
                    if cell["piece"] != None:
                        row_str += cell["piece"].name
                    else:
                        row_str += "_"
                board_str += row_str + "\n"

            
            print(board_str)
            king_check = self.is_king_in_check(board_copy, piece.colour)
            #print(f"King check: {king_check}")
            
            
            return king_check
        

        in_check = test_move(piece, coords)
        piece.coords = coords_cache.copy()
        
        return in_check
        


    def register_moves(self, board):
        """
        Registers all possible moves for each piece on the board and stores them in a dictionary
        
        """
        aggressive_moves = {
            "W": [],
            "B": []
        }
        board_pieces = [cell["piece"] for row in board for cell in row if cell["piece"] != None]
        for piece in board_pieces:

            if piece.name == "P":
                piece_possible_moves = piece.get_piece_moves_aggressive(board)
            else: 
                piece_possible_moves = piece.get_piece_moves(board)

            if len(piece_possible_moves) > 0:
                aggressive_moves[piece.colour].append({piece.id: piece_possible_moves})

        return aggressive_moves
    

    def clear_cell(self, cell_coords):
        print("clearing cell")
        cell = self.board[cell_coords[0]][cell_coords[1]]
        cell["piece"] = None
        cell["cell"].configure(image="", width=EMPTY_CELL_WIDTH, height=EMPTY_CELL_HEIGHT)
        window.update()
    
    def occupy_cell(self, cell_coords, piece):
        cell = self.board[cell_coords[0]][cell_coords[1]]

        image_abs_path = os.path.abspath(piece.image_paths[piece.colour == "B"])
        img = tk.PhotoImage(file=image_abs_path)

        piece_widget = cell["cell"]
        piece_widget.image = img
        piece_widget.configure(image=img, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        
        window.update()

    def remove_piece(self, coords):
        print(coords)
        piece = self.board[coords[0]][coords[1]]["piece"]
        
        self.pieces.remove(piece)
        self.clear_cell(coords)
        return

    
    def move_piece(self, piece, coords):
        self.clear_cell(piece.coords)
        self.board[coords[0]][coords[1]]["piece"] = piece
        self.occupy_cell(coords, piece)


    def is_king_in_check(self, board, colour):

        king = [item["piece"] for row in board for item in row if item["piece"] and item["piece"].name == "K" and item["piece"].colour == colour][0]
        
        other_colour = "W"
        if colour == "W":
            other_colour = "B"
    
        

        opponent_aggressive_moves = self.register_moves(board)[other_colour]


        all_aggressive_moves = [move_coords for move in opponent_aggressive_moves for move_coords_list in move.values() for move_coords in move_coords_list]

        aggressive_moves = []

        [aggressive_moves.append(move) for move in all_aggressive_moves if move not in aggressive_moves]

        aggressive_moves.sort()
        
        print(aggressive_moves)

        if king.coords in aggressive_moves:
            print("King is in check!")
            return True
        
        else: 
            return False


        
class Player:

    def __init__(self, colour, pieces, board):
        self.colour = colour
        self.pieces = pieces
        self.board = board
    
    def take_turn(self, piece, coords):
        pass
    
    def capture_piece(self, piece):
        pass
    
    def check_for_check(self):
        pass


class Game:

    
    def __init__(self):
        self.players = []
        self.current_player = 0

    def switch_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)
    

    def game_loop(self):
        player_had_turn = False
        while not player_had_turn:
            player_had_turn = self.players[self.current_player].take_turn()
            self.switch_player()
    

    

GameManager = Game()


Board = ChessBoard()
Board.setup_board(GameManager)

p1 = Player("W", [cell["piece"] for row in Board.board for cell in row if cell["piece"] != None and cell["piece"].colour == "W"], Board)
p2 = Player("B", [cell["piece"] for row in Board.board for cell in row if cell["piece"] != None and cell["piece"].colour == "B"], Board)

GameManager.players = [p1, p2]

def test_setup():

    """ 
    Board.board[5][2]["piece"] = Rook("R", (5, 2), "B")
    Board.board[5][2]["cell"].configure(bg="Yellow")

     """
    #Board.update_cell([3, 4], piece=Rook("R", [3, 4], "B"), colour="Blue")


    #Board.update_cell(Board.board[5][3], piece=King("K", [5, 3], "B"), colour="Blue")

    
"""     res = Board.move_piece(Board.board[6][4]["piece"], [5, 5])
    print(res)
 """
    
test_setup()



window.mainloop()


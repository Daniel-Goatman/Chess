import tkinter as tk
import os
import time


window = tk.Tk()

class Piece:

    def __init__(self, notation, coords, colour):
        self.name = notation
        self.coords = coords
        self.colour = colour
        self.test = 2
        self.image_paths = ["images/pawn_w.png", "images/pawn_b.png"]
        if self.colour == "W":
            self.direction = -1
        else:
            self.direction = 1
    def setup_piece(self):

        return
    
    def get_piece_moves(self, board):
        
        return []



class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_move = True


    def get_piece_moves(self, board):

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
                print('past edges!')
                continue
            
            board_item = board[ycoordinate + (direction[1] * self.direction)][xcoordinate + direction[0]]

   

            target_cell = board_item["cell"]
            target_piece = board_item["piece"]


            if i <= 1: #attack directions

                if target_piece != None:
                    
                    if target_piece.colour != self.colour:
                        target_cell.configure(bg="red")
                        print("FOUND??")
                        possible_moves.append(board_item)
                
                continue

            else:

                if target_piece == None:
                    target_cell.configure(bg="red")
                    possible_moves.append(board_item)
                else:
                    print("BREAKING")
                    break # Because the multi move comes after the single move and the attack checks, breaking stops the pawn from moving through an enemy pawn to a free space behind
        

        print(possible_moves)
        
        return possible_moves
 
class Rook(Piece):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/rook_w.png", "images/rook_b.png"]

    def get_piece_moves(self, board):
        possible_moves = []
        xcoordinate = self.coords[0]
        ycoordinate = self.coords[1]


        directions = [(0, 2), (0, 1), (1, 1), (-1, 1)]
            
        return possible_moves
    

class ChessBoard:

    def __init__(self):
        self.board = self.generate_board()

    def __str__(self):
        
        pieces = "\n".join([" ".join([col["piece"] for col in row]) for row in self.board])

        return pieces

    def generate_board(self):

        board = [[" "]*8 for _ in range(8)]
        
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                color = "#eeeed2"
                if (j+i) % 2 == 0:
                    color = "#769656"

                
                cell = tk.Button(window, text= j + (i*len(row)), image=None, bg=color, width=12, height=6, borderwidth=0, highlightthickness=0)

                cell.grid(row=i, column=j)
                
                board[i][j] = {"cell": cell, "piece": None} 

        return board
    
    
    def setup_board(self):

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
                "piece_class": Pawn
            },
            "B": {
                "row_coords": [0, 7],
                "col_coords": [2, 5],
                "img_paths": ["images/bishop_w.png", "images/bishop_b.png"],
                "piece_class": Pawn
            },
            "Q": {
                "row_coords": [0, 7],
                "col_coords": [3],
                "img_paths": ["images/queen_w.png", "images/queen_b.png"],
                "piece_class": Pawn
            },
            "K": {
                "row_coords": [0, 7], 
                "col_coords": [4],
                "img_paths": ["images/king_w.png", "images/king_b.png"],
                "piece_class": Pawn
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


                    piece = piece_class(piece_key, (row, col), piece_colour)

                    img_path = piece.image_paths[1]
                    if piece.colour == "W":
                        img_path = piece.image_paths[0]
                    image_abs_path = os.path.abspath(img_path)
                    img = tk.PhotoImage(file=image_abs_path)

                    piece_widget = self.board[row][col]["cell"]
                    piece_widget.image = img
                    piece_widget.width = 80
                    piece_widget.height = 80
                    piece_widget.configure(image=img, width=90, height=90)

                    self.board[row][col]["piece"] = piece

        end_time = time.time()

        print(f"Setup took: {end_time - start_time} to complete")



Board = ChessBoard()
Board.setup_board()

Board.board[5][3]["piece"] = Pawn("P", (5, 3), "B")
Board.board[5][3]["cell"].configure(bg="green")


Board.board[6][4]["cell"].configure(bg="blue")

Board.board[6][4]["piece"].get_piece_moves(Board.board)

window.mainloop()

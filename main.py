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
        
        return [    ]



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
                    target_cell.configure(bg="green")
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
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]
        print(self.coords)

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            for _ in range(1, 8):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)

                print([target_pos_x, target_pos_y])
                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break

                board_item = board[target_pos_y][target_pos_x]

                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    target_cell.configure(bg="green")
                    possible_moves.append(board_item)
                else:
                    if target_piece.colour != self.colour:
                        target_cell.configure(bg="red")
                        possible_moves.append(board_item)
                    break

               

        return possible_moves
    

class Bishop(Piece):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/bishop_w.png", "images/bishop_b.png"]

    def get_piece_moves(self, board):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]
        print(self.coords)

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            for _ in range(1, 8):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)

                print([target_pos_x, target_pos_y])
                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break

                board_item = board[target_pos_y][target_pos_x]

                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    target_cell.configure(bg="green")
                    possible_moves.append(board_item)
                else:
                    if target_piece.colour != self.colour:
                        target_cell.configure(bg="red")
                        possible_moves.append(board_item)
                    break

               

        return possible_moves


class Knight(Piece):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/knight_w.png", "images/knight_b.png"]


    def get_piece_moves(self, board):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]
        print(self.coords)

        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (-1, -2), (1, -2)]

        for move in moves:
    
            target_pos_x = xcoordinate + move[1]
            target_pos_y = ycoordinate + move[0]

            print([target_pos_x, target_pos_y])

            if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                continue

            board_item = board[target_pos_y][target_pos_x]

            target_cell = board_item["cell"]
            target_piece = board_item["piece"]

            if target_piece == None:
                target_cell.configure(bg="green")
                possible_moves.append(board_item)
            else:
                if target_piece.colour != self.colour:
                    target_cell.configure(bg="red")
                    possible_moves.append(board_item)
                


        return possible_moves
    

class Queen(Piece):

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/queen_w.png", "images/queen_b.png"]

    def get_piece_moves(self, board):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]
        print(self.coords)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            for _ in range(1, 8):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)

                print([target_pos_x, target_pos_y])
                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break

                board_item = board[target_pos_y][target_pos_x]

                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    target_cell.configure(bg="green")
                    possible_moves.append(board_item)
                else:
                    if target_piece.colour != self.colour:
                        target_cell.configure(bg="red")
                        possible_moves.append(board_item)
                    break

               

        return possible_moves


class Queen(Piece):

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/queen_w.png", "images/queen_b.png"]

    def get_piece_moves(self, board):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]
        print(self.coords)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            for _ in range(1, 8):
                target_pos_x = xcoordinate + (dir[0] * _)
                target_pos_y = ycoordinate + (dir[1] * _)

                print([target_pos_x, target_pos_y])
                if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                    break

                board_item = board[target_pos_y][target_pos_x]

                target_cell = board_item["cell"]
                target_piece = board_item["piece"]

                if target_piece == None:
                    target_cell.configure(bg="green")
                    possible_moves.append(board_item)
                else:
                    if target_piece.colour != self.colour:
                        target_cell.configure(bg="red")
                        possible_moves.append(board_item)
                    break

               

        return possible_moves



class King(Piece):

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = ["images/king_w.png", "images/king_b.png"]

    def get_piece_moves(self, board):
        possible_moves = []
        xcoordinate = self.coords[1]
        ycoordinate = self.coords[0]
        print(self.coords)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            target_pos_x = xcoordinate + dir[0]
            target_pos_y = ycoordinate + dir[1]

            print([target_pos_x, target_pos_y])
            if target_pos_x < 0 or target_pos_x > 7 or target_pos_y < 0 or target_pos_y > 7:
                continue

            board_item = board[target_pos_y][target_pos_x]

            target_cell = board_item["cell"]
            target_piece = board_item["piece"]

            if target_piece == None:
                target_cell.configure(bg="green")
                possible_moves.append(board_item)
            else:
                if target_piece.colour != self.colour:
                    target_cell.configure(bg="red")
                    possible_moves.append(board_item)
                

            

        return possible_moves

class ChessBoard:

    def __init__(self):
        self.board = self.generate_board()
        self.highlighted_cells = []

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
                cell.configure(command= lambda i=i, j=j: self.handle_piece_click(board[i][j]))
                cell.grid(row=i, column=j)
                

                board[i][j] = {"cell": cell, "piece": None} 

        return board
    
    def handle_piece_click(self, board_item):
        print(self.highlighted_cells)
        for cell in self.highlighted_cells:
            cell_details = cell["cell"].grid_info()
            cellx = cell_details["column"]
            celly = cell_details["row"]
            cell = self.board[celly][cellx]

            colour = "#eeeed2"
            if (cellx+celly) % 2 == 0:
                colour = "#769656"

            print(cell)
            self.board[celly][cellx]["cell"].configure(bg=colour)

            
        print(board_item)
        piece = board_item["piece"]
        print(piece)
        print("firing")
        if piece == None:
            return
         

        moves = piece.get_piece_moves(self.board)
        
        self.highlighted_cells = moves
        window.update()

        return moves
    
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
                    piece_widget.configure(image=img, width=88, height=95)

                    self.board[row][col]["piece"] = piece

        end_time = time.time()

        print(f"Setup took: {end_time - start_time} to complete")

    def update_cell(self, cell, colour=None, piece=None):

        if colour != None:
            cell["cell"].configure(bg=colour)

        cell["piece"] = piece

        if piece != None:
            image_abs_path = os.path.abspath(piece.image_paths[piece.colour == "B"])
            img = tk.PhotoImage(file=image_abs_path)

            piece_widget = cell["cell"]
            piece_widget.image = img
            piece_widget.configure(image=img, width=88, height=95)

        window.update()
    
        

Board = ChessBoard()
Board.setup_board()


def test_setup():

    """ 
    Board.board[5][2]["piece"] = Rook("R", (5, 2), "B")
    Board.board[5][2]["cell"].configure(bg="Yellow")

     """

    Board.update_cell(Board.board[5][3], piece=King("Q", (5, 3), "B"), colour="Blue")
    Board.handle_piece_click(Board.board[5][3])

    
test_setup()

window.mainloop()

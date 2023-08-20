import tkinter as tk
import os
import time


window = tk.Tk()


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
                color = "white"
                if (j+i) % 2 == 0:
                    color = "black"
                image = tk.PhotoImage(file="./images/pawn_w.png")
                cell = tk.Button(window, text= j + (i*len(row)), image=None, bg=color, width=12, height=6, borderwidth=0, highlightthickness=0)
                cell.image = image
                cell.grid(row=i, column=j)
                
                board[i][j] = cell 

        return board
    
    
    def setup_board(self):

        piece_coords = {
            "P": {
                "row_coords": [1, 6],
                "col_coords": [0, 1, 2, 3, 4, 5, 6, 7],
                "img_paths": ["images/pawn_w.png", "./images/pawn_b.png"]
            },
            "R": {
                "row_coords": [0, 7],
                "col_coords": [0, 7],
                "img_paths": ["images/rook_w.png", "images/rook_b.png"]
            }
        }
        start_time = time.time()
        for piece in list(piece_coords.keys()):
            for row in piece_coords[piece]["row_coords"]:
                row_colour = "Black"
                img_path = piece_coords[piece]["img_paths"][1]
                if row > 3: 
                    row_colour = "White"
                    img_path = piece_coords[piece]["img_paths"][0]

                image_abs_path = os.path.abspath(img_path)
                img = tk.PhotoImage(file=image_abs_path)
               
                print(image_abs_path)
                for col in piece_coords[piece]["col_coords"]:
                    piece_widget = self.board[row][col]
                    piece_widget.image = img
                    piece_widget.width = 80
                    piece_widget.height = 80
                    piece_widget.configure(image=img, width=90, height=90)

        end_time = time.time()

        print(f"Setup took: {end_time - start_time} to complete")

        

    

Board = ChessBoard()
Board.setup_board()


window.mainloop()
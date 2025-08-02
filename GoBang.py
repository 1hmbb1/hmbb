import tkinter as tk
from tkinter import messagebox

class GomokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("五子棋游戏 (Gobang)")
        self.master.resizable(False, False)

        self.frame_menu = tk.Frame(master)
        self.frame_menu.pack(padx=100, pady=50)
        
        self.label_title = tk.Label(self.frame_menu, text="五子棋", font=("Helvetica", 30))
        self.label_title.pack(pady=20)

        self.btn_start = tk.Button(self.frame_menu, text="Start", font=("Helvetica", 16), command=self.start_game)
        self.btn_start.pack(pady=10)

        self.btn_quit = tk.Button(self.frame_menu, text="Quit", font=("Helvetica", 16), command=master.quit)
        self.btn_quit.pack(pady=10)
        
        self.frame_game = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.frame_game, width=640, height=640, bg="#F0D9B5")
        
        self.board = [[0 for _ in range(15)] for _ in range(15)] 
        self.game_over = False
        self.current_player = 1 
        
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.frame_game, textvariable=self.status_var, font=("Helvetica", 14), bd=1, relief=tk.SUNKEN, anchor=tk.W)


    def start_game(self):
        self.frame_menu.destroy()
        
        self.frame_game.pack(pady=10)
        self.canvas.pack()
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        self.draw_board()
        self.update_status("黑方 (左键) 行棋")

        self.canvas.bind("<Button-1>", self.handle_left_click) 
        self.canvas.bind("<Button-3>", self.handle_right_click) 

    def draw_board(self):
        for i in range(15):
            self.canvas.create_line(40, 40 + i * 40, 600, 40 + i * 40)
            self.canvas.create_line(40 + i * 40, 40, 40 + i * 40, 600)
        
        star_points = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for i, j in star_points:
            x = 40 + i * 40
            y = 40 + j * 40
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="black")

    def handle_left_click(self, event):
        self.place_piece(event, "black", 1)

    def handle_right_click(self, event):
        self.place_piece(event, "white", 2)
        
    def place_piece(self, event, color, player_id):
        if self.game_over:
            return

        if self.current_player != player_id:
            return 

        x, y = event.x, event.y
        grid_x = round((x - 40) / 40)
        grid_y = round((y - 40) / 40)

        if not (0 <= grid_x < 15 and 0 <= grid_y < 15):
            return

        if self.board[grid_y][grid_x] != 0:
            return

        self.board[grid_y][grid_x] = player_id
        pixel_x = 40 + grid_x * 40
        pixel_y = 40 + grid_y * 40
        radius = 18
        self.canvas.create_oval(pixel_x - radius, pixel_y - radius, pixel_x + radius, pixel_y + radius, fill=color, outline=color)
        
        if self.check_win(grid_x, grid_y, player_id):
            self.game_over = True
            winner = "黑方" if color == "black" else "白方"
            self.update_status(f"游戏结束: {winner}胜利！")
            messagebox.showinfo("游戏结束", f"{winner}胜利！")
        else:
            self.current_player = 3 - self.current_player 
            next_player_name = "黑方 (左键)" if self.current_player == 1 else "白方 (右键)"
            self.update_status(f"{next_player_name} 行棋")

    def check_win(self, x, y, player_id):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < 15 and 0 <= ny < 15 and self.board[ny][nx] == player_id:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < 15 and 0 <= ny < 15 and self.board[ny][nx] == player_id:
                    count += 1
                else:
                    break
            
            if count >= 5:
                return True
        return False

    def update_status(self, message):
        self.status_var.set(message)


if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuGame(root)
    root.mainloop()
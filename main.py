import random
import time
import flet as ft

def play(page: ft.Page, against_ai=True):
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]

    def switch_player():
        nonlocal current_player
        current_player = "O" if current_player == "X" else "X"

    def check_winner():
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        if all(board[i][j] != "" for i in range(3) for j in range(3)):
            return "DRAW"
        return None

    def ai_move():
        time.sleep(0.2)

        def get_empty_cells():
            return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
        
        def can_win(player):
            for row, col in get_empty_cells():
                board[row][col] = player
                if check_winner() == player:
                    board[row][col] = ""
                    return (row, col)
                board[row][col] = ""
            return None
        
        def can_fork(player):
            fork_positions = []
            for row, col in get_empty_cells():
                board[row][col] = player
                if len([pos for pos in get_empty_cells() if can_win(player)]) > 1:
                    fork_positions.append((row, col))
                board[row][col] = ""
            if fork_positions:
                return fork_positions[0]
            return None
        
        win_move = can_win("O")
        if win_move:
            row, col = win_move
        else:
            block_move = can_win("X")
            if block_move:
                row, col = block_move
            else:
                fork_move = can_fork("O")
                if fork_move:
                    row, col = fork_move
                else:
                    block_fork_move = can_fork("X")
                    if block_fork_move:
                        row, col = block_fork_move
                    else:
                        if board[1][1] == "":
                            row, col = 1, 1
                        else:
                            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                            empty_corners = [corner for corner in corners if board[corner[0]][corner[1]] == ""]
                            if empty_corners:
                                row, col = random.choice(empty_corners)
                            else:
                                sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
                                empty_sides = [side for side in sides if board[side[0]][side[1]] == ""]
                                if empty_sides:
                                    row, col = random.choice(empty_sides)
        
        board[row][col] = "O"
        presses[row * 3 + col].text = "O"
        presses[row * 3 + col].bgcolor = "#32CD32"
        presses[row * 3 + col].update()
        result = check_winner()
        if result:
            display_winner(result)
        else:
            switch_player()
        page.update()

    def handle_click(index):
        if check_winner() is not None:
            return

        row = index // 3
        col = index % 3
        if board[row][col] == "":
            board[row][col] = current_player
            presses[index].text = current_player
            presses[index].bgcolor = "#1E90FF" if current_player == "X" else "#32CD32"
            presses[index].update()
            result = check_winner()
            if result:
                display_winner(result)
            else:
                switch_player()
                if against_ai and current_player == "O":
                    ai_move()
        page.update()

    def on_button_click(index):
        return lambda e: handle_click(index)

    presses = []
    for i in range(9):
        button = ft.ElevatedButton(
            text="",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
            width=95,
            height=95,
            bgcolor="#D3D3D3",
            color="white",
            on_click=on_button_click(i),
        )
        presses.append(button)
    
    playGround = ft.Container(
        padding=22,
        bgcolor="#1B1E22",
        height=350,
        width=350,
        content=ft.Column(
            controls=[
                ft.Row(controls=presses[:3]),
                ft.Row(controls=presses[3:6]),
                ft.Row(controls=presses[6:]),
            ]
        ),
    )
    
    winnerText = ft.Text("", size=24, color="white", weight=ft.FontWeight.BOLD)
    
    restartButton = ft.ElevatedButton(
        text="Restart",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
        bgcolor="#424242",
        color="white",
        on_click=lambda e: restart_game(page),
    )

    end = ft.Row(
        controls=[
            winnerText,
            restartButton
        ],
        alignment="center",
        spacing=10,
    )
    
    page.add(playGround)
    page.add(end)
    page.update()

    def display_winner(result):
        if result == "DRAW":
            winnerText.value = "DRAW!"
        else:
            winnerText.value = f"Winner: {result}"
        winnerText.update()
        page.update()

def restart_game(page):
    page.clean()
    start_screen(page)

def start_screen(page):
    def on_game_mode_choice(against_ai):
        page.clean()
        play(page, against_ai=against_ai)

    page.clean()
    page.add(ft.Text("Choose Game Mode", size=30, color=ft.colors.WHITE))
    page.add(
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Player vs AI",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
                    bgcolor="#1E90FF",
                    color="white",
                    on_click=lambda e: on_game_mode_choice(True),
                ),
                ft.ElevatedButton(
                    text="Player vs Player",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
                    bgcolor="#e08c38",
                    color="white",
                    on_click=lambda e: on_game_mode_choice(False),
                )
            ],
            alignment="center",
            spacing=20,
        )
    )
    page.update()

def main(page: ft.Page):
    page.title = "TicTacToe"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#22242A"
    page.window_height = 600
    page.window_width = 600
    page.window_left = 600
    page.window_top = 200
    page.update()

    start_screen(page)

ft.app(target=main)

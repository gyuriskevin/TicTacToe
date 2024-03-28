import flet as ft

def play(page: ft.Page):
    current_player = "X" 
    playGround = []
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

    def handle_click(index):
        if check_winner() is not None:
            return
        
        row = index // 3
        col = index % 3
        if board[row][col] == "":
            board[row][col] = current_player
            presses[index].text = current_player
            if current_player == "X":
                presses[index].color = "#1776FD"
            else:
                presses[index].color = "#FFFFFF"
            result = check_winner()
            if result:
                if result == "DRAW":
                    print("Draw!")
                    page.add(end)
                    winnerButton.text = "DRAW!"
                else:
                    print("Winner:", result)
                    page.add(end)
                    winnerButton.text = f"Winner: {result}"
                    
            else:
                switch_player()
        page.update()


    def on_button_click(index):
        return lambda e: handle_click(index)

    presses = []
    for i in range(9):
        button = ft.ElevatedButton(
            text="",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
            width=110,
            height=110,
            bgcolor="#4E5057",
            color="white",      
            on_click=on_button_click(i),
        )
        presses.append(button)
    playGround = ft.Container(
        padding=25,
        bgcolor="#1B1E22",
        height=400,
        width=400,
        content=ft.Column(
            controls=[
                ft.Row(controls=presses[:3]),
                ft.Row(controls=presses[3:6]),
                ft.Row(controls=presses[6:]),
            ]
        ),
    )
    winnerButton = ft.ElevatedButton(
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(),),
        bgcolor="#1777FF",  
        color="white",      
        
    )
    
    restartButton = ft.ElevatedButton(
        text="Restart",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder()),
        bgcolor="#424242",  
        color="white",      
        on_click=lambda e: restart_game(page),
    )
    
    end = ft.Row(
        controls=[
            winnerButton,
            restartButton
        ],
        alignment="center",
    )
    
    page.add(playGround)
    page.update()

def restart_game(page):
    page.clean()
    play(page)

def main(page: ft.Page):
    page.title = "TicTacToe"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#22242A"  

    play(page)

ft.app(target=main)

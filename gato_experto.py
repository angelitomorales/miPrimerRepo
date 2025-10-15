"""Programa experto para jugar gato (tic-tac-toe) en consola.

El programa utiliza un archivo de conocimiento persistente para almacenar
movimientos recomendados por posición. Si se enfrenta a una posición que no
conoce, solicita al usuario que le enseñe el movimiento correcto y lo almacena
para futuros encuentros.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


KNOWLEDGE_FILE = Path("conocimiento_gato.json")


class KnowledgeBase:
    """Gestiona los movimientos aprendidos y su persistencia."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.moves: Dict[str, int] = {}
        self._load()

    def _load(self) -> None:
        if self.file_path.exists():
            try:
                with self.file_path.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                self.moves = {str(key): int(value) for key, value in data.items()}
            except (json.JSONDecodeError, OSError, ValueError):
                # En caso de error, se conserva la base limpia para evitar datos corruptos.
                self.moves = {}

    def save(self) -> None:
        with self.file_path.open("w", encoding="utf-8") as fh:
            json.dump(self.moves, fh, ensure_ascii=False, indent=2, sort_keys=True)

    def get_move(self, board_key: str) -> Optional[int]:
        return self.moves.get(board_key)

    def learn_move(self, board_key: str, position: int) -> None:
        self.moves[board_key] = position
        self.save()


class TicTacToe:
    HUMAN = "X"
    AI = "O"
    EMPTY = " "
    WIN_PATTERNS: Tuple[Tuple[int, int, int], ...] = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontales
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Verticales
        (0, 4, 8), (2, 4, 6),  # Diagonales
    )

    def __init__(self) -> None:
        self.board: List[str] = [self.EMPTY] * 9

    def display(self) -> None:
        def row_str(start: int) -> str:
            cells = [self.board[start + i] if self.board[start + i] != self.EMPTY else str(start + i + 1) for i in range(3)]
            return " | ".join(cells)

        separator = "\n---------\n"
        print("\n" + separator.join(row_str(i) for i in range(0, 9, 3)) + "\n")

    def is_valid_move(self, position: int) -> bool:
        return 0 <= position < 9 and self.board[position] == self.EMPTY

    def apply_move(self, position: int, player: str) -> None:
        self.board[position] = player

    def check_winner(self) -> Optional[str]:
        for pattern in self.WIN_PATTERNS:
            a, b, c = pattern
            if self.board[a] == self.board[b] == self.board[c] != self.EMPTY:
                return self.board[a]
        if self.EMPTY not in self.board:
            return "Empate"
        return None

    def board_key(self) -> str:
        return "".join(self.board)

    def available_moves(self) -> List[int]:
        return [idx for idx, value in enumerate(self.board) if value == self.EMPTY]


def request_human_move(game: TicTacToe) -> int:
    while True:
        choice = input("Selecciona tu jugada (1-9): ").strip()
        if choice.isdigit():
            position = int(choice) - 1
            if game.is_valid_move(position):
                return position
        print("Jugada inválida. Intenta nuevamente.")


def ask_for_learning(game: TicTacToe, kb: KnowledgeBase) -> int:
    print("No conozco la mejor jugada para esta posición. Enséñame cuál debería jugar.")
    print("Introduce el número de la casilla (1-9) en la que debería jugar la IA.")
    while True:
        answer = input("Movimiento correcto para la IA: ").strip()
        if answer.isdigit():
            position = int(answer) - 1
            if game.is_valid_move(position):
                kb.learn_move(game.board_key(), position)
                return position
        print("Entrada inválida. Asegúrate de elegir una casilla disponible (1-9).")


def ai_move(game: TicTacToe, kb: KnowledgeBase) -> int:
    key = game.board_key()
    stored_move = kb.get_move(key)
    if stored_move is not None and game.is_valid_move(stored_move):
        return stored_move
    return ask_for_learning(game, kb)


def play_round() -> None:
    game = TicTacToe()
    kb = KnowledgeBase(KNOWLEDGE_FILE)
    current_player = TicTacToe.HUMAN

    print("Bienvenido al juego del gato experto. Tú juegas con 'X' y comienzas.")

    while True:
        game.display()

        if current_player == TicTacToe.HUMAN:
            move = request_human_move(game)
        else:
            print("Turno de la IA...")
            move = ai_move(game, kb)

        game.apply_move(move, current_player)
        winner = game.check_winner()

        if winner:
            game.display()
            if winner == "Empate":
                print("¡Empate!")
            elif winner == TicTacToe.HUMAN:
                print("¡Felicidades! Has ganado.")
            else:
                print("La IA ha ganado. Gracias por enseñarme.")
            break

        current_player = TicTacToe.AI if current_player == TicTacToe.HUMAN else TicTacToe.HUMAN


def main() -> None:
    while True:
        play_round()
        again = input("¿Quieres jugar otra partida? (s/n): ").strip().lower()
        if again != "s":
            print("Hasta luego. ¡Gracias por ayudarme a aprender!")
            break


if __name__ == "__main__":
    main()

from shape import Shape
from puzzle import Puzzle
import colors
import random

BLOCKER_LOCATIONS: list[tuple[tuple[int]]] = [
    ((0, 1), (0, 5), (2, 0), (5, 1), (5, 4)),
    ((0, 0), (0, 1), (3, 4), (4, 0), (5, 5)),
    ((0, 1), (0, 3), (4, 3), (5, 3), (5, 5))
]

REMOVE_FROM_POSITION: list[str] = ['(', ')', '']

SHAPES: dict[str, Shape] = {
    "L": Shape([[1, 0], [1, 0], [1, 1]], colors.CYAN),
    "l": Shape([[1, 0], [1, 1]], colors.RED),
    "T": Shape([[1, 1, 1], [0, 1, 0], [0, 1, 0]], colors.MAGENTA),
    "t": Shape([[1, 1, 1], [0, 1, 0]], colors.BRIGHT_MAGENTA),
    "z": Shape([[1, 1, 0], [0, 1, 1]], colors.BRIGHT_YELLOW),
    "c": Shape([[1, 1], [1, 0], [1, 1]], colors.GREEN),
    "f": Shape([[1, 1], [1, 0], [1, 1], [1, 0]], colors.YELLOW)
}

def coords_prompt(prompt: str) -> tuple[int]:
    """Prompts the user for coordinates and returns them as a tuple

    Args:
        prompt (str): The prompt to display to the user

    Returns:
        tuple[int]: A pair of 2D coordinates
    """

    position: str = input(prompt)
                
    for rem in REMOVE_FROM_POSITION:
        position = position.replace(rem, '')

    coords: list[str] = position.split(',')

    return (int(coords[0]),int(coords[1]))

def write_options(options: list) -> str:
    """Writes out a list of human-readable options

    Args:
        options (list): The options to be offered

    Returns:
        str: The options in the format "1, 2, ... or n"
    """

    if len(options) == 0:
        return ""
    elif len(options) == 2:
        return f"{options[0]} or {options[1]}"

    output: str = options[0]
    for i in range(1, len(options)):
        option = options[i]
        output += ", "
        if i == len(options) - 1:
            output += "or "
        output += f"{option}"
    return output

def main():
    puzzle: Puzzle = Puzzle(
        BLOCKER_LOCATIONS[random.randrange(0, len(BLOCKER_LOCATIONS))]
    )

    available_shapes: dict[str, Shape] = SHAPES.copy()
    placed: dict[str, Shape] = {}

    print(puzzle)
    print("Welcome to our puzzle game!")
    counter = 0
    while counter < 6:
        prompt: str = (
            "Choose one of the puzzle pieces to place "
            f"({write_options(list(available_shapes.keys()))}): "
        )
        chosen_shape: Shape
        while True:
            puzzle_piece: str = input(prompt)
            if puzzle_piece not in SHAPES:
                prompt = (
                    f"Unknown piece '{puzzle_piece}'. "
                    "Please choose one of the provided pieces: "
                )
            elif puzzle_piece in placed:
                prompt = (
                    "You have already placed that piece. Please place another."
                )
            else:
                print(f"Super! Your chosen element is: {puzzle_piece}")
                chosen_shape = available_shapes[puzzle_piece]
                break

        action: str = ''
        while not action.startswith("P"):
            print("Preview:")
            chosen_shape.draw()

            action = input((
                "\nChoose an action: "
                "\nR: Rotate the piece"
                "\nF: Flip the piece"
                "\nP: Place the piece\n"
            )).upper()

            if action.startswith("R"):
                prompt: str = (
                    "How many degrees would you like to rotate the shape by? "
                    "(Must be a multiple of 90°)\n"
                )
                while True:
                    try:
                        deg: int = int(input(prompt))
                        chosen_shape.rotate(deg)
                        break
                    except ValueError:
                        prompt = "Must be an integer divisible by 90°\n"
            elif action.startswith("F"):
                prompt: str = (
                    "Would you like to flip the shape vertically or "
                    "horizontally? (V/H)\n"
                )
                while True:
                    direction: str = input(prompt).upper()
                    if direction.startswith('V'):
                        chosen_shape.flip('x')
                        break
                    elif direction.startswith('H'):
                        chosen_shape.flip('y')
                        break
                    else:
                        prompt = "Expected H or V!\n"
            elif action.startswith("P"):
                break
            else:
                print(f"Unknown action '{action}'!")

        print(puzzle)
        print("Now it's time to place your puzzle piece!")
        prompt: str = "Please enter your position (e.g. (0, 1)): "
        while True:
            try:
                location_tuple: tuple[int] = coords_prompt(prompt)
                
                puzzle.draw(location_tuple, chosen_shape, puzzle_piece)
                placed[puzzle_piece] = chosen_shape
                counter += 1
                break
            except ValueError as e:
                prompt = f"Unable to place shape at {location_tuple}: {e}\n"
            except:
                prompt = "Invalid position syntax. Expected (row, col)\n"
        
        if counter == 6:
            break

        del available_shapes[puzzle_piece]

        action: str = ''
        while not action.startswith("P"):
            print(puzzle)

            action = input((
                "\nChoose an action: "
                "\nP: Place a new piece"
                "\nM: Move a piece"
                "\nR: Remove a piece\n"
            )).upper()

            if action.startswith("R"):
                prompt: str = (
                    "Please enter the symbol of the piece you want to remove: "
                )
                while True:
                    piece: str = input(prompt)
                    if piece in placed:
                        puzzle.remove_piece(placed[piece])
                        available_shapes[piece] = placed[piece]
                        del placed[piece]
                        print(f"The '{piece}' piece has been removed.")
                        counter += 1
                        break
                    else:
                        prompt = (
                            f"No piece with symbol '{piece}' found on the board"
                            "\n"
                        )
            elif action.startswith("M"):
                prompt: str = (
                    "Please enter the symbol of the piece you want to move: "
                )
                while True:
                    piece: str = input(prompt)
                    if piece in placed:
                        break
                    else:
                        prompt = (
                            f"No piece with symbol '{piece}' found on the board"
                            "\n"
                        )
                prompt = "Please enter the new position (e.g. (0, 1): "
                while True:
                    try:
                        location_tuple: tuple[int] = coords_prompt(prompt)
                        
                        puzzle.move_piece(placed[piece], location_tuple)
                        print(f"Moved the '{piece}' piece to {location_tuple}")
                        counter += 1
                        break
                    except ValueError as e:
                        prompt = f"Unable to move shape to {location_tuple}: {e}\n"
                    except:
                        prompt = "Invalid position syntax. Expected (row, col)\n"
                    
            elif action.startswith("P"):
                break
            else:
                print(f"Unknown action '{action}'!")

            if counter == 6:
                break

    print(puzzle)
    print(f"Final score: {puzzle.score()} points")

    moves = input("Would you like to play again? (y/n): ")
    if moves.upper().startswith("Y"):
        main()
    else:
        print("We're sad to see you go! Better luck next time.")

if __name__ == "__main__":
    main()
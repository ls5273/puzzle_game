from shape import Shape
import colors

EMPTY_SPOT = '-'
BLOCKER_SPOT = 'o'

class Cell:
    """Represents a cell in the puzzle board
    """

    __slots__ = ["__symbol", "__color"]

    def __init__(self, symbol: str, shape: Shape = None):
        """Constructs a new instance of the Puzzle class

        Args:
            symbol (str): The symbol to represent the cell on the board
            shape (Shape, optional): The shape occupying the cell

        Raises:
            ValueError: If `symbol` is not a single character
        """

        if len(symbol) != 1:
            raise ValueError("'symbol' must be a single character!")
        self.__symbol = symbol

        if shape is None:
            self.__color = colors.WHITE
        else:
            self.__color = shape.color()

    def __str__(self) -> str:
        return (
            f"{self.__color.bg()} {self.__color.text()}{self.__symbol} "
            f"{self.__color.reset()}"
        )
    
    def symbol(self) -> str:
        """str: The symbol representing the cell on the board
        """

        return self.__symbol

class Puzzle:
    """Represents a puzzle game
    """

    __slots__ = ["__board", "__shapes"]

    def __init__(self, blocker_locations: tuple[tuple[int]]):
        """Constructs a new instance of the Puzzle class

        Args:
            blocker_locations: (tuple[tuple[int]]): A tuple of tuples containing
            2D coordinates on the game board at which to place "blockers"
        """

        self.__board: list[list[str]] = []
        for y in range(6):
            self.__board.append([])
            for x in range(6):
                self.__board[y].append(
                    (y, x) in blocker_locations and Cell(BLOCKER_SPOT)
                    or None
                )
            
            self.__shapes: dict[Shape, tuple[int]] = {}

    def draw(self, position: tuple[int], shape: Shape, symbol: str):
        """Adds a shape to the board

        Args:
            position (tuple[int]): 2D coordinates for the top-left corner of the
            shape
            shape (Shape): The shape to place on the board
            symbol (str): The character used to represent the shape on the board

        Raises:
            ValueError: If the dimensions of the position coordinates are not 2
            ValueError: If the position is out of bounds
            ValueError: If the symbol is not a single character
            ValueError: If the symbol is identical to the blocker or empty char
            ValueError: If placing the shape would go out of bounds
            ValueError: If placing the shape is obstructed by a blocker
        """

        if len(position) != 2:
            raise ValueError("position must be a tuple of two integers")
        
        if position[0] > 5 or position[0] < 0:
            raise ValueError("Y-position out of bounds! (Expected 0-5)")

        if position[1] > 5 or position[1] < 0:
            raise ValueError("X-position out of bounds! (Expected 0-5)") 

        if len(symbol) != 1:
            raise ValueError("'symbol' must be a single character")
        
        if symbol == BLOCKER_SPOT:
            raise ValueError("Symbol can not be the same as the blocker spot")
        
        if symbol == EMPTY_SPOT:
            raise ValueError("Symbol can not be the same as the empty slot")
        
        shape_size: list[list[int]] = shape.get_table()
        if len(shape_size) + position[0] > 6:
            raise ValueError("Shape out of Y-bounds")
        
        if len(shape_size[0]) + position[1] > 6:
            raise ValueError("Shape out of X-bounds")
        
        add_at: list[tuple[int]] = []
        for y in range(position[0], position[0] + len(shape_size)):
            for x in range(position[1], position[1] + len(shape_size[0])):
                if shape_size[y - position[0]][x - position[1]] == 0:
                    continue

                if self.__board[y][x] != None:
                    raise ValueError(f"Shape is blocked at ({y}, {x})!")
                else:
                    add_at.append((y, x))

        shape_cell: Cell = Cell(symbol, shape)
        for pos in add_at:
            self.__board[pos[0]][pos[1]] = shape_cell
        self.__shapes[shape] = position

    def remove_piece(self, shape: Shape) -> str:
        """Removes a piece from the board

        Args:
            shape (Shape): The piece to remove

        Returns:
            str: The symbol of the shape removed

        Raises:
            ValueError: If the shape is not on the board
        """

        if shape not in self.__shapes:
            raise ValueError("Shape not found on board!")
        
        position: tuple[int] = self.__shapes[shape]
        shape_size: list[list[int]] = shape.get_table()
        symbol: str
        for y in range(position[0], position[0] + len(shape_size)):
            for x in range(position[1], position[1] + len(shape_size[0])):
                if shape_size[y - position[0]][x - position[1]] == 0:
                    continue

                symbol = self.__board[y][x].symbol()
                self.__board[y][x] = None
        del self.__shapes[shape]
        return symbol

    def move_piece(self, shape: Shape, new_position: tuple[int]):
        """Moves a piece to another position on the board

        Args:
            shape (Shape): The shape to move
            new_position (tuple[int]): The position to move the shape to

        Raises:
            ValueError: If the shape is not on the board
        """

        if shape not in self.__shapes:
            raise ValueError("Shape not found on board!")

        original_position: tuple[int] = self.__shapes[shape]
        symbol: str = self.remove_piece(shape)
        
        try:
            self.draw(new_position, shape, symbol)
        except ValueError as e:
            self.draw(original_position, shape, symbol)
            raise ValueError(e)

    def score(self) -> int:
        """Determines the score based on the number of tiles filled

        Returns:
            int: The player's score
        """

        score: int = 0
        for row in self.__board:
            for cell in row:
                if cell is None:
                    continue
                elif cell.symbol() != BLOCKER_SPOT:
                    score += 1
        return score

    def __str__(self) -> str:
        output: str = ' ' * 4
        
        for i in range(6):
            output += f" {i} "
        output += f"\n{' ' * 3}┌{'─' * 18}"
        for y in range(6):
            output += f"\n {y} │"

            for x in range(6):
                cell: str = str(self.__board[y][x])
                if cell == "None":
                    cell = f" {EMPTY_SPOT} "
                output += cell

        return output
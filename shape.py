from colors import Color

class Shape:
    """Represents a 2D shape on the game board
    """

    __slots__ = ["__table", "__position", "__color"]

    def __init__(self, table: list[list[int]], color: Color):
        """Constructs a new instance of the Shape class

        Args:
            table (list(list[int])): A 2D list containing the tiles used to make
            the shape. 0 represents an empty tile, and 1 represents a used tile.
            color (Color): The ANSI color to represent the shape
            
        Raises:
            TypeError: If `table` is not a 2D list of integers
            ValueError: If `table` contains values other than 0 or 1
        """

        for row in table:
            if type(row) is not list:
                raise TypeError("'table' must be a 2D list of integers")
            for element in row:
                if type(element) is not int:
                    raise TypeError("'table' must be a 2D list of integers")
                if not (element == 0 or element == 1):
                    raise ValueError("Rows in 'table' must only contain 0 or 1")

        self.__table: list[list[int]] = table
        self.__position: tuple[int] | None = None
        self.__color = color

    def color(self) -> Color:
        """Color: The ANSI color codes for the shape
        """

        return self.__color

    def draw(self):
        """Draws the shape in the console using full blocks
        """

        for row in self.__table:
            line: str = self.__color.fg()
            for cell in row:
                line += (cell and '█' or ' ') * 3
            print(line + self.__color.reset())

    def get_table(self) -> list[list[int]]:
        """list[list[int]]: A 2D list containing the tiles used to make the
        shape. 0 represents an empty tile, and 1 represents a used tile.
        """
        return self.__table
    

    def rotate(self, degrees: int):
        """Rotates the shape in increments of 90 degrees

        Args:
            degrees (int): The number of degrees to rotate the shape by

        Raises:
            TypeError: If `degrees` is not an `int` value
            ValueError: If `degrees` is not divisible by 90
        """

        if type(degrees) is not int:
            raise TypeError("`degrees` must contain an int value")
        if degrees % 90:
            raise ValueError("Rotations must be done in intervals of 90°")
        degrees %= 360

        if degrees == 0:
            return

        degrees -= 90
        rotated_shape: list[list[int]] = []

        rows: int = len(self.__table)
        columns: int = len(self.__table[0])

        for i in range(columns):
            row: list[int] = []
            for j in range(rows - 1, -1, -1):
                row.append(self.__table[j][i])
            rotated_shape.append(row)

        self.__table = rotated_shape
        if degrees > 0:
            self.rotate(degrees)

    def flip(self, axis: str):
        """Flips the shape over the x (vertical) or y (horizontal) axis

        Args:
            axis (str): The axis to flip the shape over

        Raises:
            TypeError: If `axis` is not a `str`˙value
            ValueError: If `axis` is not 'x' or 'y'
        """

        if type(axis) is not str:
            raise TypeError("`axis` must contain a `str` value")
        axis = axis.lower()
        if not (axis == 'x' or axis == 'y'):
            raise ValueError(f"Unexpected value '{axis}', expected 'x' or 'y'")
        
        flipped_shape: list[list[int]] = []

        rows: int = len(self.__table)
        row_operation: range = (
            axis == 'x' and range(rows - 1, -1, -1)
            or range(rows)
        )
        
        columns: int = len(self.__table[0])
        column_operation: range = (
            axis == 'y' and range(columns -1, -1, -1)
            or range(columns)
        )

        for i in row_operation:
            row: list[int] = []
            for j in column_operation:
                row.append(self.__table[i][j])
            flipped_shape.append(row)

        self.__table = flipped_shape
    
    def __hash__(self) -> int:
        size: str = ''
        for row in self.__table:
            for cell in row:
                size += str(cell)
        size += f"{len(self.__table)}{len(self.__table[0])}"
        
        return int(size)

    def __str__(self) -> str:
        return f"{self.__table} {self.__position}"
    
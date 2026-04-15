class Color:
    """Represents an ANSI color
    """
    
    __slots__ = ["__bg", "__fg", "__text"]
    
    def __init__(self, fg: str, bg: str, text: str = "\033[30m"):
        """Constructs a new ANSI Color

        Args:
            fg (str): The ANSI foreground code
            bg (str): The ANSI background code
            text (str, optional): The ANSI foreground code for text overlayed
            on the color. (Defaults to black)
        """

        self.__bg: str = bg
        self.__fg: str = fg
        self.__text: str = text

    def bg(self) -> str:
        """str: The ANSI color for the background
        """

        return self.__bg
    
    def fg(self) -> str:
        """str: The ANSI color for the foreground
        """

        return self.__fg
    
    def reset(self) -> str:
        """str: The ANSI reset code
        """

        return "\033[0m"
    
    def text(self) -> str:
        """str: The ANSI color for text overlayed over the background
        """

        return self.__text

BRIGHT_MAGENTA: Color = Color("\033[95m", "\033[105m")
BRIGHT_YELLOW: Color = Color("\033[93m", "\033[103m")
CYAN: Color = Color("\033[36m", "\033[46m")
GREEN: Color = Color("\033[32m", "\033[42m")
MAGENTA: Color = Color("\033[35m", "\033[45m")
RED: Color = Color("\033[31m", "\033[41m")
YELLOW: Color = Color("\033[33m", "\033[43m")
WHITE: Color = Color("\033[37m", "\033[47m")
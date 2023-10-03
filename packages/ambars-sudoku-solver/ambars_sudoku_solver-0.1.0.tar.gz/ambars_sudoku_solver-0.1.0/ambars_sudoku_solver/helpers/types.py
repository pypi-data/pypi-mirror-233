from enum import Enum

SudokuRow = list[int]
SudokuSquare = list[SudokuRow]
SudokuSuggestionsModel = dict[str, list[int]]
SudokuCellLocation = tuple[int, int]
SudokuCellLocations = list[SudokuCellLocation]
SudokuSuggestions = dict[SudokuCellLocation, list[int]]


class Level(Enum):
    EASY = "EASY"
    DIFFICULT = "DIFFICULT"

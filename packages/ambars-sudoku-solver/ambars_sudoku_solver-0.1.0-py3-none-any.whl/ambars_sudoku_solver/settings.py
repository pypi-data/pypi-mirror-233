import os

MAX_COUNT_OF_CELLS_TO_EMPTY: int = int(os.getenv("MAX_COUNT_OF_CELLS_TO_EMPTY", default="30"))
MAX_SUGGESTIONS_EASY: int = int(os.getenv("MAX_SUGGESTIONS_EASY", default="2"))
MAX_SUGGESTIONS_DIFFICULT: int = int(os.getenv("MAX_SUGGESTIONS_DIFFICULT", default="3"))
COUNT_OF_CELLS_TO_FILL: int = int(os.getenv("COUNT_OF_CELLS_TO_FILL", default="9"))
TIMEOUT_FOR_RECURSION: int = int(os.getenv("TIMEOUT_FOR_RECURSION", default="2"))
MAX_SOLUTIONS: int = int(os.getenv("MAX_SOLUTIONS", default="5"))

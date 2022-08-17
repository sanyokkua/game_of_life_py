"""Contains DataDto for game."""
from gameoflifeapi.logic.data.field import Field


class GameDataDto:
    """Represent main GameDataDto base class."""

    def __init__(self,
                 number_of_rows: int,
                 number_of_columns: int,
                 is_random_first_generation: bool,
                 generation: int,
                 game_field: Field) -> None:
        """__init__ Initialize Data Dto.

        Args:
            number_of_rows (int): Number of rows in field
            number_of_columns (int): Number of columns in field
            is_random_first_generation (bool): True if the first generation
                                                    should be randomized
            generation (int): Number of generation
            game_field (GameField): Game Field
        """
        self._rows: int = number_of_rows
        self._cols: int = number_of_columns
        self._is_rnd_gen: bool = is_random_first_generation
        self._generation: int = generation
        self._game_field: Field = game_field

    @property
    def number_of_rows(self) -> int:
        """Return number_of_rows Property.

        Returns:
            int: Number of rows
        """
        return self._rows

    @property
    def number_of_columns(self) -> int:
        """Return number_of_columns Property.

        Returns:
            int: Number of columns
        """
        return self._cols

    @property
    def is_random_first_generation(self) -> bool:
        """Return is_random_first_generation Property.

        Returns:
            bool: flag for random generation
        """
        return self._is_rnd_gen

    @property
    def generation(self) -> int:
        """Return generation Property.

        Returns:
            int: Number of generation
        """
        return self._generation

    @property
    def game_field(self) -> Field:
        """Return game_field Property.

        Returns:
            GameField: Game Field
        """
        return self._game_field


class NewGameDataDto(GameDataDto):
    """NewGameDataDto representation."""

    def __init__(self, number_of_rows: int,
                 number_of_columns: int,
                 is_random_first_generation: bool) -> None:
        """__init__ Initialize New Game Data Dto.

        Args:
            number_of_rows (int): Number of rows
            number_of_columns (int): Number of columns
            is_random_first_generation (bool): flag for random first
                                                generation
        """
        GameDataDto.__init__(self,
                             number_of_rows,
                             number_of_columns,
                             is_random_first_generation,
                             0,
                             None)


class LoadGameDataDto(GameDataDto):
    """LoadGameDataDto representation."""

    def __init__(self,
                 generation: int,
                 game_field: Field) -> None:
        """__init__ Initialize Load Game Data Dto.

        Args:
            generation (int): Number of generation
            game_field (GameField): Game Field
        """
        GameDataDto.__init__(self,
                             game_field.rows,
                             game_field.columns,
                             False,
                             generation,
                             game_field)


class SaveGameDataDto(GameDataDto):
    """SaveGameDataDto representation."""

    def __init__(self,
                 generation: int,
                 game_field: Field) -> None:
        """__init__ Initialize Save Game Data Dto.

        Args:
            generation (int): Number of generation
            game_field (GameField): Game Field
        """
        GameDataDto.__init__(self,
                             game_field.rows,
                             game_field.columns,
                             False,
                             generation,
                             game_field)


class GameStateDto:
    """Define DTO class to keep information about Game State."""

    def __init__(self, game_field: Field, generation: int) -> None:
        """Initialize GameState DTO object.

        Args:
            game_field (GameField): Game Field
            generation (int): Current Game Field Generation
        """
        self._game_field: Field = game_field
        self._generation: int = generation

    @property
    def game_field(self) -> Field:
        """Return GameField Value via its property.

        Returns:
            GameField: GameField instance
        """
        return self._game_field

    @property
    def generation(self) -> int:
        """Return Generation Value via its property.

        Returns:
            int: Number of generation
        """
        return self._generation

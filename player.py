from __future__ import annotations
from constants import PlayerPosition, PlayerStats
from hashy_perfection_table import HashyPerfectionTable


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N) - where N is the number of PlayerStats. Initializing other attributes are constant time operations
                                        self.reset_stats will loop through PlayerStats.
            Worst Case Complexity: O(N) - Same as best case as initializing the same PlayerStats attributes

        """
        self.name = name
        self.position = position
        self.age = age
        if self.age < 18:
            raise ValueError("Age must be 18 or higher.")

        # Initialize a hash table for statistics
        self.player_statistics = HashyPerfectionTable()

        # Set player statistics to 0
        # Setting new value for player stat key is O(hash), however the hash function is O(1).
        # So overall O(1) for other operations.
        # Complexity: O(N) where N is the number of PlayerStats to be initialized.
        self.reset_stats()

    def reset_stats(self) -> None:
        """
        Reset the stats of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N) - where N is the number of PlayerStats.
            Worst Case Complexity: O(N) - where N is the number of PlayerStats.

        """
        # Setting new value for player stat key is O(hash), however the hash function is O(1).
        # So overall O(1) for other operations.
        # Complexity: O(N) where N is the number of PlayerStats to be initialized
        for stat in PlayerStats:
            self[stat] = 0

    def get_name(self) -> str:
        """
        Get the name of the player

        Returns:
            str: The name of the player

        Complexity:
            Best Case Complexity: O(1) - Simple constant return operations
            Worst Case Complexity: O(1) - Simple constant return operations
        """
        return self.name

    def get_position(self) -> PlayerPosition:
        """
        Get the position of the player

        Returns:
            PlayerPosition: The position of the player

        Complexity:
            Best Case Complexity: O(1) - Simple constant return operations
            Worst Case Complexity: O(1) - Simple constant return operations
        """
        return self.position

    def get_statistics(self) -> HashyPerfectionTable:
        """
        Get the statistics of the player

        Returns:
            statistics: The players' statistics

        Complexity:
            Best Case Complexity: O(1) - Simple constant return operations
            Worst Case Complexity: O(1) - Simple constant return operations
        """
        return self.player_statistics
            
    def __setitem__(self, statistic: PlayerStats, value: int) -> None:
        """
        Set the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat
            value (int): The value of the stat

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) - Setting a value is constant time according to __setitem__ from HashyPerfectionTable
            Worst Case Complexity: O(1) - Since no collisions in a perfect hash table, worst case remains O(1)
        """
        self.player_statistics[statistic.value] = value

    def __getitem__(self, statistic: PlayerStats) -> int:
        """
        Get the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity: O(1) - Retrieving a value is constant time according to __getitem__ from HashyPerfectionTable
            Worst Case Complexity: O(1) - Same as best case
        """
        return self.player_statistics[statistic.value]

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Player object.
        Useful for debugging or when the Player is held in another data structure."""
        return str(self)


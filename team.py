from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from data_structures.linked_queue import LinkedQueue
from hashy_step_table import HashyStepTable
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar

T = TypeVar("T")


class Team:

    team_number = 1  # Keeps track of team numbers globally

    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity: O((S * __setitem__) + (P * __getitem__))      
                                    - where S is the number of team statistics from TeamStats
                                    - where P is the number of players in the team
                                    - where O(__setitem__) is the best case from HashyStepTable's '__setitem__' for inserting or updating
                                    - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                    - Best case for O(S * __setitem__) occurs when there are no collisions when hashing
                                    the keys (team stats). The key are mostly found in the first probe or found an empty slot.
                                    As for O(P * __getitem__), the key is found in the first probe or raises an error if
                                    it is empty.

            Worst Case Complexity: O((S * __setitem__) + (P * __getitem__))
                                    - where S is the number of team statistics from TeamStats
                                    - where P is the number of players in the team
                                    - where O(__setitem__) is the worst case from HashyStepTable's '__setitem__' for inserting or updating
                                    - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                    - Worst case for O(S * __setitem__) occurs when there multiple collisions when hashing
                                    and result in multiple probes. If the table exceeds its capacity, a rehash will occur.
                                    As for O(P * __getitem__), it is similar to __setitem__ where there are multiple probes
                                    to retrieve the value from the hashed key, but there are no rehash happening here.
        """
        self.team_name = team_name
        self.number = Team.team_number
        Team.team_number += 1

        # Initialize a hash table for team statistics is O(1)
        # According to self.reset_stats, complexity is O(S) for iterating through all team stats.
        # Complexity inside the loop depends on __setitem__ from HashyStepTable as we are setting a value with the
        # key(team stats). Best case occurs when there are no collisions and the loop hash the values efficiently.
        # Worst case occurs when collision leads to multiple probes and the full table triggers rehashing.
        self.team_statistics = HashyStepTable()
        self.reset_stats()

        # Initialize players hash table is O(1), where each position points to a LinkedList of players
        # Looping 4 times for each PlayerPosition, complexity is O(1) as this is constant.
        # Complexity inside the loop depends on __setitem__ from HashyStepTable as we are setting a value(LinkedList) with the
        # key(position). Best case occurs when there are no collisions and the loop hash the values efficiently.
        # Worst case occurs when collision leads to multiple probes and the full table triggers rehashing.
        self.players = HashyStepTable()
        for position in PlayerPosition:
            self.players[position.value] = LinkedList()

        # Group players by position and append them to their respective linked lists
        # Complexity for loop is O(P), where P is the number of players.
        # Complexity inside the loop depends on __getitem__ from HashyStepTable as we are retrieving the LinkedList.
        # Best case is retrieving the LinkedList through the position key and appending a player is O(1).
        # Worst case occurs if retrieving the list requires multiple probes to find the position.
        for player in players:
            self.players[player.position.value].append(player)

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case: O(S * __setitem__)
                                    - where S is the number of team statistics
                                    - where O(__setitem__) is the best case from HashyStepTable's '__setitem__' for inserting or updating
                                    - Best case for O(S * __setitem__) occurs when there are no collisions when hashing
                                    the keys (team stats) The key are mostly found in the first probe or found an empty slot.

            Worst Case: O(S * __setitem__)
                                    - where S is the number of team statistics
                                    - where O(__setitem__) is the worst case from HashyStepTable's '__setitem__' for inserting or updating
                                    - Worst case for O(S * __setitem__) occurs when there multiple collisions when hashing
                                    and result in multiple probes. If the table exceeds its capacity, a rehash will occur.
        """
        # Complexity: O(S) for iterating through all team stats.
        # Complexity inside the loop depends on __setitem__ from hashy_step_table as we are setting a value with the
        # key(team stats). Best case occurs when there are no collisions and the loop hash the values efficiently.
        # Worst case occurs when collision leads to multiple probes and the full table triggers rehashing.
        for stat in TeamStats:
            if stat == TeamStats.LAST_FIVE_RESULTS:
                self.team_statistics[stat.value] = LinkedQueue()  # Reset to an empty LinkedQueue
            else:
                self.team_statistics[stat.value] = 0

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(__getitem__)
                                    - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                    - Best case occurs when there are no collisions when searching the keys (positions)
                                    - The key are mostly found in the first probe, while the player is at the front of
                                     the list therefore O(1) and appending to the list is O(1)

            Worst Case Complexity: O(__getitem__ + P)
                                    - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                    - where P is the number of players to traverse through the list to find the player.
                                    - Worst case occurs when there are multiple collisions when searching and result in multiple probes.
                                    - Either the player is at the end of the list or not in the list, it has to traverse
                                    the whole list to search before adding and therefore O(P).
                                    - Appending to the end of the list is however O(1).
        """
        position_value = player.position.value
        if player not in self.players[position_value]:
            self.players[position_value].append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(__getitem__)
                                    - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                    - Best case occurs when there are no collisions when searching the keys (positions)
                                    - The key are mostly found in the first probe and remove from the front of list is O(1)
                                    - As remove involves calling index() and delete_at_index() from LinkedList and while
                                    the player is at the front of the list, it is O(1) to search and delete.

            Worst Case Complexity: O(__getitem__ + P)
                                    - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                    - where P is the number of players to traverse through the list to find the player.
                                    - Worst case occurs when there multiple collisions when searching and result in multiple probes.
                                    - Either the player is at the end of the list or not in the list, it has to traverse the whole list 
                                    to search before removing and therefore O(P).
        """
        position_value = player.position.value
        if player in self.players[position_value]:
            self.players[position_value].remove(player)

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.team_name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity: O(__getitem__)
                                        - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                        - Best case occurs when there are no collisions when searching the keys (positions)
                                        - The key are mostly found in the first probe where a specific position is
                                        provided and the players in that position is quickly returned, or the team has no players. 

            Worst Case Complexity: O(__getitem__ + N)
                                        - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                        - where N is the total number of players in the entire team.
                                        - Worst case occurs when the position is not provided, there are multiple
                                        collisions when searching and result in multiple probes.
                                        - The players in each position have to be appended into a new list which takes
                                        O(N) to traverse and retrieve all players, while appending to the new list
                                        takes O(1).
        """
        if position is not None:
            # Return players for the specific position, or None if no players are found
            # Retrieves the linkedlist of players through __getitem__ from HashyStepTable
            # Complexity: O(__getitem__)
            if len(self.players[position.value]) > 0:
                return self.players[position.value]
            else:
                return None
        else:
            # Collect all players in order by their position (Goalkeeper, Defender, Midfielder, Striker)
            # O(N) - where N is the total number of players in the entire team. 
            # When the position is None, we have to go through all the player positions and append the players in each
            # position linked list into player_collection.
            # This is representing the nested loop but not the first loop since it is fixed at a constant length of 4.
            player_collection = LinkedList()
            for pos in PlayerPosition:
                # Retrieves the linkedlist of players through __getitem__ from HashyStepTable
                # Complexity: O(__getitem__)
                players_position = self.players[pos.value]
                
                if len(players_position) > 0:
                    # O(N) - where N is the total number of players in the team's position.
                    # Appending is O(1)
                    for player in players_position:
                        player_collection.append(player)

            # If no players in team, return None
            if len(player_collection) > 0:
                return player_collection
            else:
                return None

    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity: O(1) - Simple constant return operations
            Worst Case Complexity: O(1) - Simple constant return operations
        """
        return self.team_statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specification.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(__getitem__)
                                            - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                            -  The key is found on the first probe, and either fewer than or
                                            exactly 5 games have been played, so the list is returned directly
            Worst Case Complexity: O(__getitem__)
                                            - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                            - If collisions occur during the hash table lookup and multiple probes
                                            are required to get the LAST_FIVE_RESULTS key. Other operations like length
                                            check, returning the list or serving are O(1) time.

        """
        # O(__getitem__) from HashyStepTable
        last_five_results = self.team_statistics[TeamStats.LAST_FIVE_RESULTS.value]

        # If no games have been played, return None
        if len(last_five_results) == 0:
            return None
        
        # If fewer than 5 games have been played, return the current results
        elif len(last_five_results) <= 5:
            return last_five_results

        # If exceed 5 games, delete the oldest game
        # O(1) where serving the first item from the queue is constant-time operation. 
        else:
            return last_five_results.serve()

    def update_games_played(self, result: GameResult) -> None:
        """
        Updates the number of games played per team, points, and last five results. 
        Additionally, it updates the number of games played for each player in the team.

        Args:
            result (GameResult): The result of the game (WIN, DRAW, or LOSS), which will be
                                used to update the team's points and last five results.

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N * __setitem__)
                                    - where N is the number of players in the team
                                    - where O(__setitem__) is the best case from HashyStepTable's '__setitem__' for inserting or updating
                                    - Best case occurs when there are no hash collisions, and players are updated without probings.
                                    - Other operations, like appending to the list of game results and constant additions are O(1).

            Worst Case Complexity: O(N * __setitem__)
                                    - where N is the number of players in the team
                                    - where O(__setitem__) is the worst case from HashyStepTable's `__setitem__` when
                                    hash collisions occur, and rehashing may be triggered.
                                    - Worst case occurs when the hash table approaches its load factor limit, requiring
                                    rehashing, or there are many collisions, making `__setitem__` slower.
        """
        # Increment the number of games played for the team.
        # O(__setitem__) to access the team stats and incrementing the value
        self.team_statistics[TeamStats.GAMES_PLAYED.value] += 1
        
        # Update the team's points based on the game result (3 for WIN, 1 for DRAW, 0 for LOSS).
        # O(__setitem__) to access the team stats and incrementing the value
        self.team_statistics[TeamStats.POINTS.value] += result
        
        # Update the number of games played for each player in every position.
        # O(N * __setitem__) - where N is the number of players that should update their games played statistics.
        #                    - O(__setitem__) to access the player stats and incrementing the value
        for player in self.get_players():
            player[PlayerStats.GAMES_PLAYED] += 1
                
        # Add the game result to the team's last five results.
        # O(__getitem__) to access the Last Five Results and appending is O(1)
        # Same complexity for get_last_five_results
        self.team_statistics[TeamStats.LAST_FIVE_RESULTS.value].append(result)
        self.get_last_five_results()
        
    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError
    
    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity: O(1) - When updating GOALS_FOR or GOALS_AGAINST. Simple mathematics time constant operations
            Worst Case Complexity: O(N) - where N is the number of players updated in self.update_games_played.
                                        When updating WINS, DRAWS, or LOSSES, as it requires updating all players' game played.

            Best Case Complexity: O(__setitem__ + __getitem__)
                                - where O(__setitem__) is the best case from HashyStepTable's '__setitem__' for inserting or updating
                                - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                - Best case considers when updating simple statistics like GOALS_FOR, GOALS_AGAINST, and
                                GOALS_DIFFERENCE with no hash collisions or rehashing.
                                - Updating WINS, DRAWS, LOSSES are higher complexity due to the self.update_games_played

            Worst Case Complexity: O(N * __setitem__)
                                - where N is the number of players updated in self.update_games_played.
                                - where O(__setitem__) is the worst case from HashyStepTable's `__setitem__` when
                                hash collisions occur, and rehashing may be triggered.
                                - For WINS, DRAWS, or LOSSES, updating the team and players involves N number of updates,
                                 each of which could be impacted by hash collisions or rehashing.


        """
        # O(__setitem__) from HashyStepTable, updating the value of the provided team stats with the value.
        self.team_statistics[statistic.value] = value

        # Handle cascading updates for WINS, DRAWS, LOSSES
        # Considering the complexity for self.update_games_played
        # O(N * __setitem__) where N is the number of players in the team, '__setitem__' from HashyStepTable.
        if statistic == TeamStats.WINS:
            self.update_games_played(GameResult.WIN)

        elif statistic == TeamStats.DRAWS:
            self.update_games_played(GameResult.DRAW)

        elif statistic == TeamStats.LOSSES:
            self.update_games_played(GameResult.LOSS)

        # Handle cascading updates for GOALS_FOR and GOALS_AGAINST
        # O(__setitem__) from HashyStepTable, updating the GOALS_DIFFERENCE according to provided goals for or against values.
        # O(__getitem__) from HashyStepTable, accessing the GOALS_FOR and GOALS_AGAINST values before setting.
        elif statistic == TeamStats.GOALS_FOR or statistic == TeamStats.GOALS_AGAINST:
            # Calculate goal difference after updating goals for or goals against
            self.team_statistics[TeamStats.GOALS_DIFFERENCE.value] = (self.team_statistics[TeamStats.GOALS_FOR.value] -
                                                                      self.team_statistics[TeamStats.GOALS_AGAINST.value])
            
        
    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity: O(__getitem__)
                                    - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                    - Best case occurs when there are no collisions when hashing the keys (positions)
                                    - The key are mostly found in the first probe.

            Worst Case Complexity: O(__getitem__)
                                    - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                    - Worst case occurs when there multiple collisions when hashing and result in multiple probes.
        """
        return self.team_statistics[statistic.value]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(__getitem__)
                                        - Complexity of self.get_players dominates here.
                                        - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values
                                        - Best case occurs when there are no collisions when hashing the keys (positions)
                                        - The key are mostly found in the first probe.

            Worst Case Complexity: O(__getitem__ + N)
                                        - Complexity of self.get_players dominates here.
                                        - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values
                                        - where N is the total number of players in the entire team. 
                                        - Worst case occurs when the position is not provided, there are multiple
                                        collisions when hashing and result in multiple probes.
                                        - The players in each position have to be appended into a new list which takes
                                        O(N) to traverse and retrieve all players, while taking appending to the new list
                                        takes O(1).
        """
        # Complexity of self.get_players analyzed here.
        players = self.get_players()

        if players is None:
            return 0
        else:
            return len(players)
    
    def __lt__(self, other: Team) -> bool:
        """
        Define the comparison between two Team objects based on points,
        goal difference, goals for, and team name.

        Complexity:
            Best Case Complexity: O(__getitem__)
                                - where O(__getitem__) is the best case from HashyStepTable's '__getitem__' for retrieving values


            Worst Case Complexity: O(__getitem__)
                                - where O(__getitem__) is the worst case from HashyStepTable's '__getitem__' for retrieving values

        """
        team_stats = self.team_statistics
        other_stats = other.get_statistics()

        # First: Compare points (descending)
        if team_stats[TeamStats.POINTS.value] != other_stats[TeamStats.POINTS.value]:
            return team_stats[TeamStats.POINTS.value] > other_stats[TeamStats.POINTS.value]

        # Second: Compare goal difference (descending)
        if team_stats[TeamStats.GOALS_DIFFERENCE.value] != other_stats[TeamStats.GOALS_DIFFERENCE.value]:
            return team_stats[TeamStats.GOALS_DIFFERENCE.value] > other_stats[TeamStats.GOALS_DIFFERENCE.value]

        # Third: Compare goals for (descending)
        if team_stats[TeamStats.GOALS_FOR.value] != other_stats[TeamStats.GOALS_FOR.value]:
            return team_stats[TeamStats.GOALS_FOR.value] > other_stats[TeamStats.GOALS_FOR.value]

        # Fourth: Compare team name (ascending)
        return self.get_name() < other.get_name()
    
    def __le__(self, other: Team) -> bool:
        """
        Define the less than or equal to comparison between two Team objects
        """
        return self < other or self == other

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return f"{self.get_name()}"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)



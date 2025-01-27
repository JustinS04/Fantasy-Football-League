from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from algorithms.mergesort import mergesort
from dataclasses import dataclass
from team import Team
from player import Player
from game_simulator import GameSimulator
from constants import TeamStats, ResultStats, PlayerStats
from typing import Generator, Union


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week
        self.current_game_index = 0  # Track the current game index for iteration

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity: O(1) - Assigning index to 0
        Worst Case Complexity: O(1) - Same as best case
        """
        # Initialize the game index for iteration
        self.current_game_index = 0
        return self

    def __next__(self):
        """
        Complexity:
        Best Case Complexity: O(1) - Simple index increment and access in the array.
        Worst Case Complexity: O(1) - Same as best case.
        """
        # Access the game at the current index and increment the index. 
        if self.current_game_index < len(self.games):
            game = self.games[self.current_game_index]
            self.current_game_index += 1
            return game
        else:
            # If there are no more games in the week, raise StopIteration
            raise StopIteration

class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(N^2 + N * log N) - where N is the number of teams in the season. 
                                        - O(N^2), self._generate_schedule generates all games between teams 
                                        - O(N * log N) - sorting the teams with mergesort. 
            Worst Case Complexity: O(N^2 + N * log N) - Same as best case.
        """
        self.teams: ArrayR[Team] = teams
        # Sorting the teams using mergesort O(N * log N) where N is the number of teams
        sorted_teams = mergesort(self.teams)

        self.leaderboard = LinkedList()
        # O(N) where N is the number of teams to append into leaderboard. 
        # Appending is O(1) constant-time
        for team in sorted_teams:
            self.leaderboard.append(team)

        self.schedule = LinkedList()
        # O(N^2) - where N is the number of teams in the season
        weekly_games = self._generate_schedule()
        
        # Iterating over weekly games and appending each to the schedule. 
        # O(W), where W is the number of weeks.
        for week_index, games in enumerate(weekly_games):
            week_of_games = WeekOfGames(week_index + 1, games)  # Create a WeekOfGames object
            self.schedule.append(week_of_games)  # Add to schedule, append is O(1)

    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity: O(W * G * (GS + N * __setitem__ + P)) 
                                                    - where W is the number of weeks in the schedule
                                                    - where G is the number of games per week
                                                    - where N is the number of players in a team
                                                    - where __setitem__ is the worst case complexity from team.py
                                                    - where GS is the game simulator
                                                    - where P is the number of players to update their scores
                                                    
                                                    This scenario states that players are found in the first position of the team list. 
                                                    This results in O(N * __setitem__) for updating team stats and O(P) for updating player stats.
                                                    Sorting the leaderboard remains O(T * log T).
                                                    Hence, the overall best case complexity is dominated by O(W * G * (GS + N * __setitem__ + P)).
                                                    
                                                    - Internally in __setitem__ magic method, we will be following the worst case
                                                    complexity since we not only update the goals for and against, but also updating the
                                                    WINS, DRAWS, LOSSES of the team stats.
                                                    
            Worst Case Complexity: O(W * G * (GS + (N * __setitem__) + (P * N))) 
                                                    - where W is the number of weeks in the schedule
                                                    - where G is the number of games per week
                                                    - where N is the number of players in a team
                                                    - where __setitem__ is the worst case complexity from team.py
                                                    - where GS is the game simulator
                                                    - where P is the number of players to update their scores
                                                    The worst-case scenario assumes that updating player stats takes O(P * N) for each player,
                                                    where the players are found after several iterations in update_player_stats. The simulation
                                                    becomes more time consuming when we need to traverse the player list a lot to update their stats.
                                                    
            
        """
        # Iterate over each week of games in the schedule
        # O(W) - where W is the number of weeks in the schedule

            
            # Iterate over each game in the current week
            # O(G) - where G is the number of games per week
        for game in self.get_next_game():
                
                # O(GS) - Simulate the game
            game_match = GameSimulator.simulate(game.home_team, game.away_team)
                
                # Extracting game statistics (home goals, away goals, tackles, etc.)
                # O(__getitem__), where __getitem__ is from Hash_Table, LinearProbe class. 
            home_goals = game_match[ResultStats.HOME_GOALS.value]
            away_goals = game_match[ResultStats.AWAY_GOALS.value]
                # O(1) - Constant time for assignments.
            goal_scorers = ResultStats.GOAL_SCORERS.value
            interceptions = ResultStats.INTERCEPTIONS.value
            tackles = ResultStats.TACKLES.value
            goals_assists = ResultStats.GOAL_ASSISTS.value
                
                # Update team statistics based on home goals and away goals
                # O(N * __setitem__) - where N is the number of players in the team
                #                    - O(__setitem__), where __setitem__ complexity from team class.
            self.update_team_stats(game.home_team, game.away_team, home_goals, away_goals)
                
                # Update player statistics based on game results
                # O(1) - Looping over a constant number of 4 stats (goal_scorers, interceptions, tackles, goals_assists)
            for key in (goal_scorers, interceptions, tackles, goals_assists):
                    
                    # Best case O(P) - where P is the number of players to update and it found the player in first iteration. 
                    # Worst case O(P * N) - where P is the number of players to update and N is the number of players in a team
                self.update_player_stats(game.home_team.get_players(), game_match[key], key)
                self.update_player_stats(game.away_team.get_players(), game_match[key], key)

        # Finally, update the leaderboard
        # O(T * log T) - where T is the number of teams. Mergesort complexity 
        self.get_leaderboard()

    def update_team_stats(self, home_team: Team, away_team: Team, home_goals: int, away_goals: int) -> None:
        """
        Update team stats after each game, such as goals, wins, draws, and losses.
        Most operations here utilizied the __setitem__ magic method from teams.py

        Args:
            home_team (Team): The home team.
            away_team (Team): The away team.
            home_goals (int): The number of goals scored by the home team.
            away_goals (int): The number of goals scored by the away team.
            
        Complexity:
            Best case complexity: O(N * __setitem__)
                                    - where N is the number of players in the team.
                                    - where __setitem__ is from team class
                                    - Internally in __setitem__ magic method, we will be following the worst case
                                    complexity since we not only update the goals for and against, but also updating the
                                    WINS, DRAWS, LOSSES of the team stats.
                                    - All other operations of mathematics and addition are constant.

            Worst case complexity: O(N * __setitem__) - Same as best case.
        """
        # Update goals for and against
        # O(1) - Direct mathematical constant time operations 
        home_team[TeamStats.GOALS_FOR] += home_goals
        home_team[TeamStats.GOALS_AGAINST] += away_goals
        away_team[TeamStats.GOALS_FOR] += away_goals
        away_team[TeamStats.GOALS_AGAINST] += home_goals

        # Determine the result and use the __setitem__ method to update the team stats
        # O(N) - where N is the number of players in the team. These updates call the 
        # __setitem__ method which then iterates over all players and increment their games played value.
        if home_goals > away_goals:
            # Home team wins
            home_team[TeamStats.WINS] += 1
            away_team[TeamStats.LOSSES] += 1

        elif home_goals < away_goals:
            # Away team wins
            away_team[TeamStats.WINS] += 1
            home_team[TeamStats.LOSSES] += 1

        else:
            # Draw
            home_team[TeamStats.DRAWS] += 1
            away_team[TeamStats.DRAWS] += 1

    def update_player_stats(self, players: ArrayR, player_list, key) -> None:
        """
        Updates the player statistics based on the result of the game.

        Args:
            players (list): List of players involved from home team or away team in the match.
            player_list (list): List of player names whose statistics need updating.
            key: The type of statistic to update (GOAL_SCORERS, GOAL_ASSISTS, TACKLES, INTERCEPTIONS)
            
        Complexity:
            Best Case Complexity: O(P)  - where P is the number of players in player_list, assuming the player is found
                                        immediately in the first nested loop.
                                        - HashyPerfectionTable __getitem__ and __setitem__ magic methods are O(hash), where
                                        overall are O(1).
            Worst Case Complexity: O(P * N) - where P is the number of players in the players list and N is the number
                                            of players in home team or away team. It will be a worse case if the player
                                            is in the middle or at the end of the team list.

        """
        if player_list is not None:
            # O(P) where P is the length of player_list from the results of game match
            for player_name in player_list:
                # Find the player in the list of players
                # O(N) where N is the number of players from home or away team
                for player in players:
                    if player.get_name() == player_name:
                        # O(1) operation - based on the key, update the statistic
                        if key == ResultStats.GOAL_SCORERS.value:
                            player.get_statistics()[PlayerStats.GOALS.value] += 1
                        elif key == ResultStats.GOAL_ASSISTS.value:
                            player.get_statistics()[PlayerStats.ASSISTS.value] += 1
                        elif key == ResultStats.INTERCEPTIONS.value:
                            player.get_statistics()[PlayerStats.INTERCEPTIONS.value] += 1
                        elif key == ResultStats.TACKLES.value:
                            player.get_statistics()[PlayerStats.TACKLES.value] += 1
                        # Break out once the player is found and updated
                        break 

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.
            
        Raises:
            ValueError: If the season has already started or any games have been played.

        Complexity:
            Best Case Complexity: O(W) - where W is the number of weeks.
                                        Most of the if comparison statements are O(1)
                                        But when moving a week to the end of list, it traverses the list to find the index to delete which takes O(W)
                                        and append the week to the back which takes O(1)

            Worst Case Complexity: O(W) - where W is the number of weeks. 
                                        When moving a week to the new week, it traverses the list to find the index to delete which takes O(W)
                                        and traverse again to find the correct index to insert the week which takes O(W).
                                        Overall complexity is O(W + W) --> O(W)
        """
        # Weeks in the input are starting from Week 1 (index 0), but we need to - 1 to get the actual index in the list.
        orig_week -= 1
        if new_week is not None:
            new_week -= 1

        # Obtain the games from the original week
        # Accessing the index in a linked list requires traversing to the index
        # O(W) - where W is the number of weeks
        games_to_delay = self.schedule[orig_week]

        # Moving to an existing week
        if new_week is not None:
            # Remove the games from the original week
            # O(W) - deleting from a linked list require traversing
            self.schedule.delete_at_index(orig_week)

            # Insert games_to_move at new_week
            # O(W) - inserting an item into the linked list requires traversing
            self.schedule.insert(new_week, games_to_delay)

        # Move games to the end of the season
        else:
            # Remove the games from the original week and append to the end
            # O(W) - deleting from a linked list require traversing
            self.schedule.delete_at_index(orig_week)
            
            # O(1) - appending to the tail of the linked list takes constant time
            self.schedule.append(games_to_delay)

    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: Each Yield Time Complexity: O(1)
                                        - Yielding game and incrementing the iterator in 'for game in week' loop are constant-time operations O(1).
                                        
                                  Total Time Complexity: O(W * G)
                                        - where W is the number of weeks and G is the number of games per week.
                                        - The outer loop runs len(schedule) - 1 times, and the inner loop runs the number of 
                                        games in a week per outer iteration
                                        - Each outer iteration represents processing one week and inner loop iterates
                                        over each game in the current week
                                        
            Worst Case Complexity: Same as best case. 
            
                                  Each Yield Time Complexity: O(1)
                                        - Yielding game and incrementing the iterator in 'for game in week' loop are constant-time operations O(1).
                                        
                                  Total Time Complexity: O(W * G)
                                        - where W is the number of weeks and G is the number of games per week.
                                        - The outer loop runs len(schedule) - 1 times, and the inner loop runs the number of 
                                        games in a week per outer iteration
                                        - Each outer iteration represents processing one week and inner loop iterates
                                        over each game in the current week
        """
        # Start iterating from the first week
        # O(W) - where W is the number of weeks to be iterated in self.schedule
        for week in self.schedule:
            
            # Use the WeekOfGames iterator to go through the games
            # O(G) - where G is the number of games in a week 
            for game in week:
                # Yield the current game
                yield game
                
        # The generator naturally stops when no more games are left
        
    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity: O(T * log T) -  where T is the number of teams. 
                                                If O(S * __getitem__), which is the number of statistics is small compared to O(T * log T)
                                                the overall complexity is dominated by sorting.
            Worst Case Complexity: O(T * (S * __getitem__)) 
                                            - where T is the number of teams and S is the number of statistics in team. 
                                            - where __getitem__ is the magic method __getitem__ from team.py
                                            If O(S * __getitem__) is larger compared to O(T * log T), the complexity is dominated by getting the team statistics.
                                            This is because we have to treat the number of team statistics as a variable.
        """
        # O(1) - Initialize the final leaderboard format
        final_leaderboard = LinkedList()
        
        # O(T * log T) - Sort the teams using merge sort, where T is the number of teams.
        # This sorts the teams according to the requirements of points, goals difference, goals for, and name. 
        final_sorted_teams = mergesort(self.teams)
        
        # O(T * S) - Loop over each team and append its statistics
        for team in final_sorted_teams:
            
            # O(S * __getitem__) - Get team statistics data in a list format
            team_stats = self._get_team_statistics(team)
            
            # O(1) - Append team stats to the leaderboard. Constant time as appending to the end of list. 
            final_leaderboard.append(team_stats)
        print(final_leaderboard)
        return final_leaderboard

    def _get_team_statistics(self, team: Team) -> LinkedList:
        """
        Get a linked list representation of the team's statistics for leaderboard purposes.

        Args:
            team (Team): The team for which statistics are to be fetched.

        Returns:
            LinkedList: A linked list containing the team's statistics in the following order:
                - Team name (str)
                - Each statistic defined in TeamStats (Games Played, Points, Wins, Draws, Losses, Goals For, Goals Against, Goal Difference, Last Five Results)

        Complexity:
            - Best Case Complexity: O(S * __getitem__) - Where S is the number of statistics in TeamStats.
                                                       - O(__getitem__) is the magic method complexity from team class.

            - Worst Case Complexity: O(S * __getitem__) - Same as best case.
        
        """
        # O(1) - Getting the statistics is constant time operation
        team_stats = team.get_statistics()
        team_stats_data = LinkedList() 
        
        # O(1) - Appending to the linked list is constant time operation
        team_stats_data.append(team.get_name())
        
        # Loop through each statistic in TeamStats
        # O(S) - where S is the number of stats in TeamStats
        for stat in TeamStats:
            # O(1) for hash key access and appending to the end of list.
            # O(__getitem__) from team class to access the team statistic to be appended into the list.
            team_stats_data.append(team_stats[stat.value])
            print(team_stats[stat.value])

        return team_stats_data

    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1) - Constant time return operation
            Worst Case Complexity: O(1) - Constant time return operation
        """
        return self.teams
        
    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1) - Return the length of self.teams array
            Worst Case Complexity: O(1) - Return the length of self.teams array
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""


    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)

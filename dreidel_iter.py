# dreidel.py

from random import choice
from colorama import Fore

FACES = ["Nun", "Gimel", "Hey", "Shin"]
NUM_PLAYERS = [2,4,6,8,20]
STARTING_BANK = [10,20,50]
ANTE_AMOUNT = 1
SHIN_PENALTY = 3

c = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
w = Fore.WHITE


class Player(object):
    def __init__(self, player_name: str, starting_bank: int, color_key: int) -> None:
        self.player_name = player_name
        self.bank = starting_bank
        self.color = c[color_key % len(c)]

    def is_bankrupt(self) -> bool:
        """Checks if player is bankrupt. Returns True if bank is zero or less."""
        return self.bank <= 0

    def ante(self, ante_amount: int = ANTE_AMOUNT) -> int:
        """Antes the player into the pot. Returns amount anted.

        Keyword arguments:
        ante_amount -- amount each player must ante (default set above)
        """
        if self.is_bankrupt():
            return 0
        if self.bank < ante_amount:
            money_left = self.bank
            self.bank = 0
            return money_left
        else:
            self.bank -= ante_amount
            return ante_amount

    def turn(self, pot: int) -> tuple:
        """Player spins dreidel and win/loss calculated.
        Returns tuple of spin and final pot value.

        Keyword arguments:
        pot -- starting pot value
        """
        spin = choice(FACES)
        if spin == "Nun":
            return spin, pot
        elif spin == "Gimel":
            self.bank += pot
            return spin, 0
        elif spin == "Hey":
            half_rounded_up = (pot + 1) // 2
            self.bank += half_rounded_up
            return spin, pot - half_rounded_up
        else:
            if self.bank > SHIN_PENALTY:
                self.bank -= SHIN_PENALTY
                return spin, pot + SHIN_PENALTY
            else:
                money_left = self.bank
                self.bank = 0
                return spin, pot + money_left

    def __repr__(self) -> str:
        if self.is_bankrupt():
            return f"{self.color}{self.player_name} is bankrupt."
        else:
            return f"{self.color}{self.player_name} has a bank of {self.bank}."


def check_for_winner(players) -> bool:
    """Checks all players for a single winner. Returns True if there is a winner.

    Keyword arguments:
    players -- list of player objects
    """
    return sum(map(lambda x: not x.is_bankrupt(), players)) == 1


def play_game(num_players: int = 4, starting_bank: int = 10) -> None:
    """Plays the dreidel game.

    Keyword arguments:
    ante_amount -- amount each player must ante (default set above)
    """
    players = [Player(f"Player {_ + 1}", starting_bank, _) for _ in range(num_players)]
    pot = 0
    spin_count = 0

    while True:
        for player in players:
            if pot == 0:
                pot = sum(map(lambda x: x.ante(), players))
                # print(f"{w}** Everyone must ante!  The pot is now {pot}. **")
            if check_for_winner(players):
                for player in players:
                    if player.bank > 0:
                        winner = player.player_name
                        print(
                            f"{w}For a game with {num_players} players and a starting bank of {starting_bank}, it took {spin_count} spins for {winner} to win."
                        )
                return
            if not player.is_bankrupt():
                spin, pot = player.turn(pot)
                spin_count += 1
                # print(
                    # f"{player.color}{player.player_name} spun {spin} and now has a bank of {player.bank}.  The pot is now {pot}."
                # )


if __name__ == "__main__":
    for num in NUM_PLAYERS:
        for bank in STARTING_BANK:
            play_game(num_players=num, starting_bank=bank)

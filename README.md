Lance Reinsmith, M.D. is a radiologist and programming hobbyist who lives and works in San Antonio, TX.  Dr. Reinsmith is no better at playing dreidel than random chance would indicate.

Dreidel is a game commonly played during the celebration of the Hanukkah holiday.  Each player starts with a bank of coins and takes turns spinning a four-sided top.  The results of the spins dictate how the game progresses.  For more information, check out the Wikipedia entry on dreidel.

To summarize, each player usually antes one coin into the pot to start and when it is empty.  If a player rolls a:

- נ‎ (*nun*), the player does nothing.
- ג‎ (*gimel*), the player gets everything in the pot.
- ה‎ (*hey*), the player gets half of the coins in the pot.  If there are an odd number of coins in the pot, the player takes half the pot rounded up to the nearest whole number.
- ש‎ (*shin*), the player adds one to three coins to the pot.  (For historical and geographic purposes, some dreidels have a פ‎ (*pe*y) instead of a shin, but this has the same function.)

This article reviews how to write a simple dreidel simulation script using Python.  It assumes you have intermediate familiarity with Python 3, including classes, list comprehension, lambda functions, and type hinting.

To spin the dreidel, we'll need to define our dreidel faces and import the choice method from the random module.

```python
from random import choice
FACES = ["Nun", "Gimel", "Hey", "Shin"]
```

Most dreidel games involve about 4-6 players with a starting bank of about 10 coins.  Let's set some constants for our game:

```
NUM_PLAYERS = 6
STARTING_BANK = 10
ANTE_AMOUNT = 1
SHIN_PENALTY = 3
```

Of course, you can change these.

I'll eventually want the console output to be color-coded for better readability.  The colorama package helps simplify this in Python.  Install using:

```bash
pip install colorama
```

Appending colorama color codes to strings can get quite busy and cumbersome; but, we can simplify this using lists and/or variables with short names:

```python
from colorama import Fore

c = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
w = Fore.WHITE
```

This way, we can reference the list by an index and append that to the string.  If this sounds confusing, it will be more clear below.

We'll now construct a Player class to serve as a blueprint for each player in the game.

```python
class Player(object):
    def __init__(self, player_name: str, starting_bank: int, color_key: int) -> None:
        self.player_name = player_name
        self.bank = starting_bank
        self.color = c[color_key % len(c)]
....
```

This init method assigns a name and starting bank to the Player.  It also assigns a color using a modulus to rotate through the list of colors defined above.  (The double underscores before and after "init" make this a "dunder" function--which usually means a class function run internally and not intended to be called de novo.)

```python
		def is_bankrupt(self) -> bool:
    		"""Checks if player is bankrupt. Returns True if bank is zero or less."""
    		return self.bank <= 0
....
```
Next, we create a simple method to determine if a player is bankrupt which returns a boolean based on their bank.  It returns True if the patient's bank is zero or less.

```python
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
....
```
Then, we create an ante method which takes in a parameter of the ante_amount.  (This defaults to the amount defined above.)  It first checks if the player is bankrupt.  If so, it returns 0 to the pot.  If the player is not bankrupt, it then checks if the player has enough to ante up.  If so, the ante is deducted from the player's bank and returned to the pot.  If not, the player pays its residual to the pot and the player's bank goes to zero.

```python
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
....
```
Next, it's time to spin!  The turn method takes in the current pot as a parameter.  A random choice of the faces is made.  Based on this, the player's bank and the pot are adjusted.  The method returns the spin and the final pot value as a tuple.

There are a few things to point out here:

* (pot+1) // 2 makes sure the player gets half of the pot rounded up to the nearest whole number
* The SHIN_PENALTY is defined above.  If the player cannot pay this, it adds the residual amount in their bank to the pot and sets their bank to zero.

```python
def __repr__(self) -> str:
    if self.is_bankrupt():
        return f"{self.color}{self.player_name} is bankrupt."
    else:
        return f"{self.color}{self.player_name} has a bank of {self.bank}."
....
```
Finally, we make a string representation for the Player for completeness sake.  The entire class is shown here:

```python
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
```

We then make a function to check all of the players in the game to see if there is a winner:

```python
def check_for_winner(players) -> bool:
    """Checks all players for a single winner. Returns True if there is a winner.

    Keyword arguments:
    players -- list of player objects
    """
    return sum(map(lambda x: not x.is_bankrupt(), players)) == 1
```

This can be a bit tricky if you're not used to the map function and lambda functions.  The function takes in a list of Players as a parameter, each Player with an is_bankrupt() method.  It then maps the is_bankrupt() method over all of the Players and calculates the sum of the results.  Since is_bankrupt() returns 0 for a bankrupted player, a sum of 1 means there is only a single non-bankrupt player.

Finally, we need to set up the game:

```python
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
                print(f"{w}** Everyone must ante!  The pot is now {pot}. **")
            if check_for_winner(players):
                for player in players:
                    if player.bank > 0:
                        winner = player.player_name
                        print(
                            f"\n{w}For a game with {num_players} players and a starting bank of {starting_bank}, it took {spin_count} spins for {winner} to win."
                        )
                return
            if not player.is_bankrupt():
                spin, pot = player.turn(pot)
                spin_count += 1
                print(
                    f"{player.color}{player.player_name} spun {spin} and now has a bank of {player.bank}.  The pot is now {pot}."
                )
```

This function appears complex, so we'll break it down step-by-step.

The function accepts the number of players (num_players) and starting bank amount for each player (starting_bank) as parameters.  These default to 4 and 10 by default. 

Next, the group of Players is constructed using list comprehension.  While doing so, the index of the for loop is used to assign a rotating color to the Player.  (I use "_" as an index variable, but you could use "I" or anything else.)

The pot and spin_count are then reset to zero.

Next, the script enters a loop where each player takes turns.  Prior to each turn, the function checks if the pot is zero.  If so, everyone needs to ante (see ante method above) if they can.  It then checks for a winner by passing the list of Players to the check_for_winner function defined above.

If there is a winner, it loops through the players to find the winner and prints a message in white (by prepending the text with the w variable defined with the colors) declaring the game stats, the winner name, and the number of spins it took to complete the game.  The game is then over.

If no one has won, it then checks if the current player is bankrupt.  If not, the player takes their turn spinning and the pot is updated and spin count increased.  The function then prints a message to the console in the player's color (by prepending the text with the player.color value) specifying who has spun, what the result is, and the new values of their pot and the bank.

It's now time to tell the script to set up and play the game if the script is run:

```python
if __name__ == "__main__":
    play_game(num_players=NUM_PLAYERS, starting_bank=STARTING_BANK)
```

That's it!  If you like this, try adjusting the parameters to see how the game changes.  Or, try playing a real game of dreidel with friends or family!  Here is the entire script.

```python
# dreidel.py

from random import choice
from colorama import Fore

FACES = ["Nun", "Gimel", "Hey", "Shin"]
NUM_PLAYERS = 6
STARTING_BANK = 10
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
                print(f"{w}** Everyone must ante!  The pot is now {pot}. **")
            if check_for_winner(players):
                for player in players:
                    if player.bank > 0:
                        winner = player.player_name
                        print(
                            f"\n{w}For a game with {num_players} players and a starting bank of {starting_bank}, it took {spin_count} spins for {winner} to win."
                        )
                return
            if not player.is_bankrupt():
                spin, pot = player.turn(pot)
                spin_count += 1
                print(
                    f"{player.color}{player.player_name} spun {spin} and now has a bank of {player.bank}.  The pot is now {pot}."
                )


if __name__ == "__main__":
    play_game(num_players=NUM_PLAYERS, starting_bank=STARTING_BANK)
```

Happy Holidays!
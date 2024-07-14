import random

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 10
        self.tiredness = 10
        self.happiness = 5
        self.health = 10
        self.is_sleeping = False
        self.age = 0
        self.achievements = []

    def eat(self):
        if not self.is_sleeping:
            self.hunger -= 3
            if self.hunger < 0:
                self.hunger = 0
            print(f"{self.name} has eaten. Hunger is now {self.hunger}")
        else:
            print(f"{self.name} is sleeping and can't eat.")

    def sleep(self):
        if not self.is_sleeping:
            self.is_sleeping = True
            self.tiredness -= 3
            if self.tiredness < 0:
                self.tiredness = 0
            print(f"{self.name} is sleeping. Tiredness is now {self.tiredness}")
        else:
            print(f"{self.name} is already sleeping.")

    def wake_up(self):
        if self.is_sleeping:
            self.is_sleeping = False
            print(f"{self.name} has woken up.")
        else:
            print(f"{self.name} is not sleeping.")

    def play(self):
        if not self.is_sleeping:
            self.happiness += 2
            self.tiredness += 1
            print(f"{self.name} is playing. Happiness is now {self.happiness}")
        else:
            print(f"{self.name} is sleeping and can't play.")

    def check_status(self):
        print(f"Age: {self.age}, Hunger: {self.hunger}, Tiredness: {self.tiredness}, Happiness: {self.happiness}, Health: {self.health}")
        print("Achievements:")
        for achievement in self.achievements:
            print(achievement)

    def update_status(self):
        if self.hunger > 7:
            self.health -= 1
        if self.tiredness > 7:
            self.health -= 1
        if self.happiness < 3:
            self.health -= 1
        self.age += 1

        if self.age == 10 and "Grown Up" not in self.achievements:
            self.achievements.append("Grown Up")
        if self.happiness >= 10 and "Happy Tamagotchi" not in self.achievements:
            self.achievements.append("Happy Tamagotchi")

class Player:
    def __init__(self):
        self.money = 100
        self.inventory = []

    def work(self):
        self.money += 20
        print(f"You have earned 20 dollars. You now have {self.money} dollars.")

    def buy_treat(self, treat):
        if treat == "food":
            if self.money >= 10:
                self.money -= 10
                self.inventory.append("food")
                print(f"You have bought food for 10 dollars. You now have {self.money} dollars.")
            else:
                print("You don't have enough money to buy food.")
        elif treat == "toy":
            if self.money >= 20:
                self.money -= 20
                self.inventory.append("toy")
                print(f"You have bought a toy for 20 dollars. You now have {self.money} dollars.")
            else:
                print("You don't have enough money to buy a toy.")

def chance_minigame():
    print("Welcome to the chance minigame!")
    print("You will roll a dice and if you get a 6, you will win a prize!")
    input("Press enter to roll the dice...")
    roll = random.randint(1, 6)
    print(f"You rolled a {roll}!")
    if roll == 6:
        print("Congratulations! You won a prize!")
        return True
    else:
        print("Sorry, you didn't win a prize this time.")
        return False

def guess_the_number():
    number = random.randint(1, 10)
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 10. Can you guess it?")
    guess = int(input("Enter your guess: "))
    if guess == number:
        print("Congratulations! You guessed the number correctly!")
        return True
    else:
        print(f"Sorry, the number was {number}. Better luck next time!")
        return False

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    print("Welcome to Rock Paper Scissors!")
    player_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
    print(f"Computer chose {computer_choice}!")
    if player_choice == computer_choice:
        print("It's a tie!")
        return False
    elif (player_choice == "rock" and computer_choice == "scissors") or (player_choice == "paper" and computer_choice == "rock") or (player_choice == "scissors" and computer_choice == "paper"):
        print("You win!")
        return True
    else:
        print("Computer wins!")
        return False

def main():
    name = input("Enter a name for your Tamagotchi: ")
    tama = Tamagotchi(name)
    player = Player()
    while True:
        print("\n1. Eat\n2. Sleep\n3. Wake Up\n4. Play\n5. Check Status\n6. Work\n7. Buy Treat\n8. Use Treat\n9. Chance Minigames\n10. Quit")
        choice = input("Choose an action: ")
        if choice == "1":
            tama.eat()
        elif choice == "2":
            tama.sleep()
        elif choice == "3":
            tama.wake_up()
        elif choice == "4":
            tama.play()
        elif choice == "5":
            tama.check_status()
        elif choice == "6":
            player.work()
        elif choice == "7":
            print("1. Food (10 dollars)\n2. Toy (20 dollars)")
            treat_choice = input("Choose a treat to buy: ")
            if treat_choice == "1":
                player.buy_treat("food")
            elif treat_choice == "2":
                player.buy_treat("toy")
        elif choice == "8":
            if "food" in player.inventory:
                tama.hunger -= 5
                if tama.hunger < 0:
                    tama.hunger = 0
                player.inventory.remove("food")
                print(f"You used food on {tama.name}. Hunger is now {tama.hunger}")
            elif "toy" in player.inventory:
                tama.happiness += 5
                player.inventory.remove("toy")
                print(f"You used a toy on {tama.name}. Happiness is now {tama.happiness}")
            else:
                print("You don't have any treats to use.")
        elif choice == "9":
            print("1. Roll a Dice\n2. Guess the Number\n3. Rock Paper Scissors")
            minigame_choice = input("Choose a minigame: ")
            if minigame_choice == "1":
                if chance_minigame():
                    player.money += 50
                    print(f"You won 50 dollars! You now have {player.money} dollars.")
            elif minigame_choice == "2":
                if guess_the_number():
                    player.money += 50
                    print(f"You won 50 dollars! You now have {player.money} dollars.")
            elif minigame_choice == "3":
                if rock_paper_scissors():
                    player.money += 50
                    print(f"You won 50 dollars! You now have {player.money} dollars.")
        elif choice == "10":
            break
        tama.update_status()
        if tama.health <= 0:
            print(f"{tama.name} has died. Game over.")
            break

if __name__ == "__main__":
    main()

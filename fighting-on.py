import os
import random

class fighter():
    def __init__(self, name):
        self._name = name
        self.__maxHealth = 10
        self.__health = 10
        self.__defense = 0
        self.__attack = 1
        self.__critChance = 0
        self.__critMultiplier = 0
        self.__speed = 1
        self.__wallet = 10
        self.__statsPurchased = 0
        self.__bankedMoney = 0

    def getMaxHealth(self):
        return self.__maxHealth
    def getHealth(self):
        return self.__health
    def getDefense(self):
        return self.__defense
    def getAttack(self):
        return self.__attack
    def getCritChance(self):
        return self.__critChance
    def getCritMultiplier(self):
        return self.__critMultiplier
    def getSpeed(self):
        return self.__speed
    def getNumberOfStatsPurchased(self):
        return self.__statsPurchased
    def getStats(self):
        return {
            "Health" : self.__health,
            "Defense" : self.__defense,
            "Attack" : self.__attack,
            "Critical Chance" : self.__critChance,
            "Critical Multiplier" : self.__critMultiplier,
            "Speed" : self.__speed,
            "Wallet Total" : self.__wallet,
            "Banked Total" : self.__bankedMoney
        }

    def checkWallet(self):
        return int(self.__wallet)
    
    def checkBank(self):
        return self.__bankedMoney

    def makePurchase(self, amount):
        self.__wallet -= amount
        self.__statsPurchased += 1

    def earnMoney(self, amount):
        self.__wallet += amount

    def loseMoney(self, amount):
        if amount <= self.checkWallet():
            self.__wallet -= amount
        else:
            self.__wallet = 0
    
    def bankMoney(self, amount):
        if amount > self.checkWallet():
            print(f"You Are Trying To Deposit ${amount} Which Is More Money Than You Have")
        else:
            self.loseMoney(amount)
            self.__bankedMoney += amount

    def withdrawMoney(self, amount):
        if amount > self.checkBank():
            print(f"You Are Trying To Withdraw ${amount} But You Only Have ${self.checkBank()} Banked.")
        else:
            self.earnMoney(amount)
            self.__bankedMoney -= amount

    def rest(self):
        self.__health = self.__maxHealth

    def takeDamage(self, amount):
        print(f"{self._name} Health: {self.__health}\n{self._name} Took {amount} Damage")
        self.__health += amount
        print(f"{self._name} Has {self.__health} Left\n")

    def buyStat(self, stat):
        shop = {
            "health" : 10 * self.__statsPurchased,
            "defense" : 10 * self.__statsPurchased,
            "attack" : 10 * self.__statsPurchased,
            "critChance" : 10 * self.__statsPurchased,
            "critMultiplier" : 10 * self.__statsPurchased,
            "speed" : 10 * self.__statsPurchased,
        }
        if (self.checkWallet() >= shop[stat]):
            match stat:
                case "health":
                    self.__maxHealth += 1
                    self.__health += 1
                case "defense":
                    self.__defense += 1
                case "attack":
                    self.__attack += 1
                case "critChance":
                    self.__critChance += 10
                case "critMultiplier":
                    self.__critMultiplier += 1
                case "speed":
                    self.__speed += 1
            self.makePurchase(shop[stat])
        else:
            print(f"{self._name} Does Not Have Enough Money To Buy That\n{self._name} Needs {shop[stat]} But Has {self.__wallet}")

    def battle(self, enemy):
        selfDied = False
        enemyDied = False

        selfWasCrit = True if random.random() < self.getCritChance() else False
        enemyWasCrit = True if random.random() < enemy.getCritChance() else False

        # If the current person has more speed than the enemy current person hits first
        if self.getSpeed() > enemy.getSpeed():
            # enemy health - (enemy defense - (self attack + MAYBE(self attack * self critMultiplier)))
            healthChange = enemy.getDefense() - \
                (self.getAttack() + ((self.getAttack() * self.getCritMultiplier()) if selfWasCrit else 0))
            enemy.takeDamage(healthChange)
            if enemy.getHealth() <= 0:
                print(f"{enemy._name} Died")
                enemyDied = True
            else:
                # if the enemy did not die then the enemy hits back
                healthChange = self.getDefense() - \
                    (enemy.getAttack() + ((enemy.getAttack() * enemy.getCritMultiplier()) if enemyWasCrit else 0))
                self.takeDamage(healthChange)

                if self.getHealth() <= 0:
                    print(f"{self._name} Died")
                    selfDied = True

        # If the enemy has more speed then the enemy hits first
        if self.getSpeed() < enemy.getSpeed():
            # self health - (self defense - (enemy attack + MAYBE(enemy attack * enemy critMultiplier)))
            healthChange = self.getDefense() - \
                (enemy.getAttack() + ((enemy.getAttack() * enemy.getCritMultiplier()) if enemyWasCrit else 0))
            self.takeDamage(healthChange)

            if self.getHealth() <= 0:
                print(f"{self._name} Died")
                selfDied = True
            else:
                # if current person did not die then the current person hits back
                healthChange = enemy.getDefense() - \
                    (self.getAttack() + ((self.getAttack() * self.getCritMultiplier()) if selfWasCrit else 0))
                enemy.takeDamage(healthChange)
                
                if enemy.getHealth() <= 0:
                    print(f"{enemy._name} Died")
                    enemyDied = True

        # if both the current person and the enemy have the same speed they hit at the same time
        if self.getSpeed() == enemy.getSpeed():
            # self health - (self defense - (enemy attack + MAYBE(enemy attack * enemy critMultiplier)))
            healthChange = self.getDefense() - \
                (enemy.getAttack() + ((enemy.getAttack() * enemy.getCritMultiplier()) if enemyWasCrit else 0))
            self.takeDamage(healthChange)

            # enemy health - (enemy defense - (self attack + MAYBE(self attack * self critMultiplier)))
            healthChange = enemy.getDefense() - \
                (self.getAttack() + ((self.getAttack() * self.getCritMultiplier()) if selfWasCrit else 0))
            enemy.takeDamage(healthChange)

            if self.getHealth() <= 0 and enemy.getHealth() <= 0:
                print("Both Of You Died")
                selfDied = True
                enemyDied = True
            elif self.getHealth() <= 0:
                print(f"{self._name} Died")
                selfDied = True
            elif enemy.getHealth() <= 0:
                print(f"{enemy._name} Died")
                enemyDied = True

        if selfDied:
            moneyLost = random.randint(1, self.checkWallet())
            self.loseMoney(moneyLost)
            print(f"You Died! You Lost ${moneyLost}. You Have ${self.__wallet} Left")
        if enemyDied:
            moneyEarned = random.randint(1, 10)
            self.earnMoney(moneyEarned)
            print(f"You Killed The Enemy! You Found ${moneyEarned}. You Have ${self.__wallet} Total")

def pickAFight():
    return fighter("NPC")

def createFighter():
    return fighter(input("Enter Your Fighters Name"))

def playGame(playerOne):
    possibleActions = {
        1: "Fight",
        2: "Buy Stats",
        3: "Check Stats",
        4: "Rest"
    }
    for action in possibleActions:
        print(f"{action} : {possibleActions[action]}")

    actionChoice = int(input("Enter The Number Of What You Wish To Do: "))
    match actionChoice:
        case 1:
            playerTwo = pickAFight()
            
            while(playerOne.getHealth() > 0 and playerTwo.getHealth() > 0):
                playerOne.battle(playerTwo)

        case 2:
            purchasePrice = playerOne.getNumberOfStatsPurchased() * 10
            statsToBuy = {
                1 : "health", 
                2 : "defense", 
                3 : "attack", 
                4 : "critChance", 
                5 : "critMultiplier", 
                6 : "speed"}
            for stat in statsToBuy:
                print(f"{stat} : {statsToBuy[stat]}")
            statChoice = input(f"Enter The Number Of The Stat You Want To Buy For ${purchasePrice} Or X To Exit Store:")

            if statChoice == "x" or statChoice == "X":
                print("You Have Exited The Store.")
            elif (statChoice).isnumeric() and int(statChoice) in statsToBuy:
                playerOne.buyStat(statsToBuy[int(statChoice)])
            else:
                print("Improper Input. You Have Been Kicked Out Of The Store. Try Again: ")
        
        case 3:
            print(f"\nPlayerOne Stats:")
            stats = playerOne.getStats()
            for stat in stats:
                print(f"{stat} : {stats[stat]}")
        
        case 4:
            playerOne.rest()
            print(f"You Have Rested And Returned To Full Health.")

    print("----------- End Of Round-----------")
    playGame(playerOne)
            # "health" : 10 * self.__statsPurchased,
            # "defense" : 10 * self.__statsPurchased,
            # "attack" : 10 * self.__statsPurchased,
            # "critChance" : 10 * self.__statsPurchased,
            # "critMultiplier" : 10 * self.__statsPurchased,
            # "speed" : 10 * self.__sta

def main():
    os.system("cls")

    print("------------------------------------------------------------------")

    # fighterName = input("Enter Your Fighters Name: ")
    fighterName = "Preston" # to be removed

    playerOne = fighter(fighterName)
    
    playGame(playerOne)

if __name__ == "__main__":
    main()
#!/usr/bin/env python

# In this simple RPG game, the hero fights the goblin. He has the options to:

# 1. fight goblin
# 2. do nothing - in which case the goblin will attack him anyway
# 3. flee
from random import randint as r

## Super Class

class Character:
    def __init__(self, name, health, power):
        self.name = name
        self.health = health
        self.power = power

    def alive(self):
        if self.health > 0:
            return True

    def attack(self, enemy):
        if enemy.name == "Hero":
            if enemy.armor >= 2:
                print(f"{self.name} does {(self.power - enemy.armor)} damage to the {enemy.name}.")
                enemy.takes_damage((self.power - enemy.armor))  
            else:
                enemy.takes_damage(self.power) 
        elif enemy.name == "Shadow":
            chance = r(1,10)
            if chance == 1:
                # enemy.health -= self.power
                print(f"{self.name} does {self.power} damage to the {enemy.name}.")
                enemy.takes_damage(self.power) 
        else:
            enemy.health -= self.power
            print(f"{self.name} does {self.power} damage to the {enemy.name}.")
            enemy.takes_damage(self.power)  
            # if enemy == "Medic":
            #     enemy.recuperate()
            if enemy.health <= 0:
                print(f"The {enemy.name} is dead.")
            elif self.health <= 0:
                print(f"{self.name} is dead.")
        

    def takes_damage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {damage} in damage.\n")
        

    def print_status(self):
        print(f"{self.name} has {self.health} health and {self.power} power.")
    

## Sub-classes

class Hero(Character):
    def __init__(self, name, health, power, coins, armor, evade, stake):
        super().__init__(name, health, power)
        self.coins = coins
        self.armor = armor
        self.evade = evade
        self.stake = stake


    def attack(self, enemy):
        if enemy.name == 'Zombie' and self.stake >= 1: 
            enemy.health = 0

        if enemy.name != 'Zombie':
            chance = r(1,5)
            if chance == 1:
                print(f"{self.name} does DOUBLE DAMAGE of {self.power} to the {enemy.name}.")
                enemy.takes_damage(self.power * 2) 
            else:
                enemy.takes_damage(self.power) 
            # enemy.health -= self.power
            # print(f"{self.name} does {self.power} damage to the {enemy.name}.")

    def totalBounty(self, enemy):
        self.coins += enemy.coins
        print(f"Hero recieved {enemy.coins} coins for defeating the {enemy.name}.")
        print(f"{self.name} now has {self.coins} total coins.\n")


    def evade_attack(self):
        chance = r(1,10)

        if self.evade > chance:
            return True
        else:
            return False

    def takes_damage(self, damage):
        evaded = False

        if self.evade >= 2:
            evaded = self.evade_attack()

        if evaded == True:
            print(f"{self.name} evaded the attack!")
        else:
            self.health -= damage
            print(f"{self.name} takes {damage} in damage.\n")
            

    # def takes_damage(self, enemy):
    #     if self.armor >= 2:
    #         # enemy.health -= self.power - enemy.armor
    #         self.health -= enemy.power - self.armor
    #         print(f"{self.name} takes {enemy.power - self.armor} in damage.\n")
    #     elif self.evade >= 2:
    #         self.evade_attack()

class Goblin(Character):
    def __init__(self, name, health, power, coins = 6):
        self.coins = coins
        super().__init__(name, health, power)

class Zombie(Character):
    def __init__(self, name, health, power, coins = 2):
        self.coins = coins
        super().__init__(name, health, power)

class Medic(Character):
    def __init__(self, name, health, power, coins = 10):
        self.coins = coins
        super().__init__(name, health, power)

    def recuperate(self):
        self.health += 2

    # def takes_damage(self, enemy):
    #     self.health -= enemy.power()
    #     chance = r(1,5)
    #     if chance == 1:
    #         self.name.recuperate()

class Shadow(Character):
    def __init__(self, name, health, power, coins = 9):
        self.coins = coins
        super().__init__(name, health, power)

    # def takes_damage(self, enemy):
    #     chance = r(1,10)
    #     if chance == 1:
    #         self.health -= enemy.power
    #         print(f"{enemy.name} does {enemy.power} damage to the {self.name}.")

class Spider(Character):
    def __init__(self, name, health, power, coins = 5):
        self.coins = coins
        super().__init__(name, health, power)

    def webBlock(self):
        chance = r(1,5)
        if chance == 1:
            return True
        else:
            return False
    
    def takes_damage(self, damage):
        blocked = self.webBlock()

        if blocked == True:
            print(f"{self.name} has BLOCKED the attack with a web shield.")
        else:
            self.health -= damage
            print(f"{self.name} takes {damage} in damage.\n")
        
    


class Ninja(Character):
    def __init__(self, name, health, power, coins = 7):
        self.coins = coins
        super().__init__(name, health, power)

    def knockOut(self, enemy):
        enemy.health = 0
        print(f"KNOCK OUT!")

    def attack(self, enemy):
        chance = r(1,10)
        print("Ninja Attack")
        print(chance)
        if chance == 1:
            self.knockOut(enemy)
        else:
            enemy.takes_damage(self.power) 


## Store Items

class SuperTonic:
    def buy(self, hero):
        hero.health += 10
        hero.coins -= 5
        print("Hero has bought 10 health points.")
        return hero.health

class Armor:
    def buy(self, hero):
        hero.armor += 2
        hero.coins -= 5
        print("Hero has bought 2 armor points.")
        return hero.armor

class Evade:
    def buy(self, hero):
        hero.evade += 2
        hero.coins -= 5
        print("Hero has bought 2 evade points.")
        return hero.evade

class MegaPower:
    def buy(self, hero):
        hero.power += 2
        hero.coins -= 5
        print("Hero has bought 2 power points.")
        return hero.power

class ZombieStake:
    def buy(self, hero):
        hero.coins -= 20
        hero.stake += 1
        print("Hero has bought 1 Zombie Stake.")
        return hero.stake

## Store

class Store:
    def goToStore(self, hero):
        print(f'''
Hero has entered the store!
1 -- Super Tonic (5 coins)
2 -- Armor (5 coins)
3 -- Evade (5 coins)
4 -- Mega Power (5 coins)
5 -- Zombie Stake (20 coins)
6 -- Exit the Store
        ''')
        while True:
            print(f"Hero has {hero.coins} coins.")
            print("What would you like the Hero to buy?")
            print("> ", end=' ')
            userChoice = input()
            if userChoice == "1":
                if hero.coins >= 5:
                    item = SuperTonic()
                    item.buy(hero)
                else:
                    print("Hero does not have enough coins.")
            elif userChoice == "2":
                if hero.coins >= 5:
                    item = Armor()
                    item.buy(hero)
                else:
                    print("Hero does not have enough coins.")
            elif userChoice == "3":
                if hero.coins >= 5:
                    item = Evade()
                    item.buy(hero)
                else:
                    print("Hero does not have enough coins.")
            elif userChoice == "4":
                if hero.coins >= 5:
                    item = MegaPower()
                    item.buy(hero)
                else:
                    print("Hero does not have enough coins.")
            elif userChoice == "5":
                if hero.coins >= 20:
                    item = ZombieStake()
                    item.buy(hero)
                else:
                    print("Hero does not have enough coins.")
            elif userChoice == "6":
                print("Now leaving the store.")
                break
            else:
                print(f"Invalid input {userChoice}")           

## Battle

class Battle:
    def start_battle(self, hero, enemy):
        store = Store()
        while enemy.alive() and hero.alive():
            hero.print_status()
            enemy.print_status()
            print()
            print("What do you want the Hero to do?")
            print("1 -- Fight")
            print("2 -- Do Nothing")
            print("3 -- Flee")
            print("4 -- Enter Store")
            print("> ", end=' ')
            raw_input = input()
            if raw_input == "1":
                hero.attack(enemy)
            elif raw_input == "2":
                pass
            elif raw_input == "3":
                print("Goodbye.")
                break
            elif raw_input == "4":
                store.goToStore(hero)
            else:
                print(f"Invalid input {raw_input}")
            if enemy.alive():
                enemy.attack(hero)
            else:
                print(f'{enemy.name} is dead.\n')
                hero.totalBounty(enemy)
            if not hero.alive():
                print(f"{enemy.name} has defeated {hero.name}.")
                print("YOU LOSE!")
                break

## Game

def main():

    hero = Hero("Hero", 100, 5, 0, 0, 0, 0)
    goblin = Goblin("Goblin", 6, 2)
    zombie = Zombie("Zombie", 100, 2)
    medic = Medic("Medic", 10, 2)
    shadow = Shadow("Shadow", 1, 2)
    spider = Spider("Spider", 8, 3)
    ninja = Ninja("Ninja", 5, 1)

    enemies = [goblin, medic, shadow, spider, ninja, zombie]

    battle = Battle()

    while hero.alive():
        for enemy in enemies:
            battle.start_battle(hero, enemy)
            if not hero.alive():
                break
            
        if hero.alive():
            print("YOU WIN!")
        
        break

            

main()

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
        else:
            enemy.takes_damage(self.power)  
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


class Shadow(Character):
    def __init__(self, name, health, power, coins = 9):
        self.coins = coins
        super().__init__(name, health, power)

    def takes_damage(self, damage):
        chance = r(1,10)
        if chance == 1:
            self.health -= power
            print(f"{self.name} takes {damage} in damage.\n")

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


## Store



class Store:

    def buy(self, hero, item):     
        item_price = item["price"]
        item_name = item["name"]
        item_value = item["value"]

        attr = getattr(hero, item_name)
        updatedAttr = attr + item_value
        updatedCoins = getattr(hero, "coins") - item_price

        setattr(hero, item_name, updatedAttr)
        setattr(hero, "coins", updatedCoins)
        
        print(f"Hero has bought {item_value} {item_name}")
    

    def goToStore(self, hero):
        inventory = [      
            {
                "name": "health",
                "price": 5,
                "value": 10,
            },
            {
                "name": "armor",
                "price": 20,
                "value": 2
            },
            {
                "name": "evade",
                "price": 5,
                "value": 2
            },
            {
                "name": "power",
                "price": 5,
                "value": 2
            },
            {
                "name": "stake",
                "price": 20,
                "value": 1
            }  

        ]
        print(f'''
Hero has entered the store!
1 -- Super Tonic (5 coins)
2 -- Armor (5 coins)
3 -- Evade (5 coins)
4 -- Mega Power (5 coins)
5 -- Zombie Stake (20 coins)
6 -- Exit the Store
        ''')
        stay = True
        while stay:
            print(f"Hero has {hero.coins} coins.")
            print("What would you like the Hero to buy?")
            print("> ", end=' ')
            userChoice = input()
            if (userChoice == "6"):
                print("Now leaving the store.")
                stay = False
            else:
                item = inventory[int(userChoice) - 1]

                if not int(userChoice) >= len(inventory) or not int(userChoice) <= 0:
                    if (hero.coins >= item["price"]):
                        self.buy(hero, item)
                    else:
                        print("Hero does not have enough coins.")
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
                print(
                """
                                _,.-------.,_
                            ,;~'             '~;,
                          ,;                     ;,
                         ;                         ;
                        ,'                         ',
                       ,;                           ;,
                       ; ;      .           .      ; ;
                       | ;   ______       ______   ; |
                       |  `/~"     ~" . "~     "~\'  |
                       |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
                        |   |        }:{        |   |
                        |   l       / | \       !   |
                        .~  (__,.--" .^. "--.,__)  ~.
                        |     ---;' / | \ `;---     |
                         \__.       \/^\/       .__/
                          V| \                 / |V
       __                  | |T~\___!___!___/~T| |                  _____
    .-~  ~"-.              | |`IIII_I_I_I_IIII'| |               .-~     "-.
   /         \             |  \,III I I I III,/  |              /           Y
  Y          ;              \   `~~~~~~~~~~'    /               i           |
  `.   _     `._              \   .       .   /               __)         .'
    )=~         `-.._           \.    ^    ./           _..-'~         ~"<_
 .-~                 ~`-.._       ^~~~^~~~^       _..-'~                   ~.
/                          ~`-.._           _..-'~                           Y
{        .~"-._                  ~`-.._ .-'~                  _..-~;         ;
 `._   _,'     ~`-.._                  ~`-.._           _..-'~     `._    _.-
    ~~"              ~`-.._                  ~`-.._ .-'~              ~~"~
  .----.            _..-'  ~`-.._                  ~`-.._          .-~~~~-.
 /      `.    _..-'~             ~`-.._                  ~`-.._   (        ".
Y        `=--~                  _..-'  ~`-.._                  ~`-'         |
|                         _..-'~             ~`-.._                         ;
`._                 _..-'~                         ~`-.._            -._ _.'
   "-.="      _..-'~                                     ~`-.._        ~`.
    /        `.                                                ;          Y
   Y           Y                                              Y           |
   |           ;                                              `.          /
   `.       _.'                                                 "-.____.-'

                """)
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

    print(
    """

                                      /|
                                     |\|
                                     |||
                                     |||
                                     |||
                                     |||
                                     |||
                                     |||
                                  ~-[{o}]-~
                                     |/|
                                     |/|
             ///~`     |\\_          `0'         =\\\\         . .
            ,  |='  ,))\_| ~-_                    _)  \      _/_/|
           / ,' ,;((((((    ~ \                  `~~~\-~-_ /~ (_/
         /' -~/~)))))))'\_   _/'                      \_  /'  D   |
        (       (((((( ~-/ ~-/                          ~-;  /    \--_
         ~~--|   ))''    ')  `                            `~~\_    \   )
             :        (_  ~\           ,                    /~~-     ./
              \        \_   )--__  /(_/)                   |    )    )|
    ___       |_     \__/~-__    ~~   ,'      /,_;,   __--(   _/      |
  //~~\`\    /' ~~~----|     ~~~~~~~~'        \-  ((~~    __-~        |
((()   `\`\_(_     _-~~-\                      ``~~ ~~~~~~   \_      /
 )))     ~----'   /      \                                   )       )
  (         ;`~--'        :                                _-    ,;;(
            |    `\       |                             _-~    ,;;;;)
            |    /'`\     ;                          _-~          _/
           /~   /    |    )                         /;;;''  ,;;:-~
          |    /     / | /                         |;;'   ,''
          /   /     |  \\|                         |   ,;(    
        _/  /'       \  \_)                   .---__\_    \,--._______
       ( )|'         (~-_|                   (;;'  ;;;~~~/' `;;|  `;;;
        ) `\_         |-_;;--__               ~~~----__/'    /'_______/
        `----'       (   `~--_ ~~~;;------------~~~~~ ;;;'_/'
                     `~~~~~~~~'~~~-----....___;;;____---~~



                     Initilizing new game...
    """
)
    print(
    """

  
                    |>>>                        |>>>
                    |                           |
                _  _|_  _                   _  _|_  _
               | |_| |_| |                 | |_| |_| |
               \  .      /                 \ .    .  /
                \    ,  /                   \    .  /
                 | .   |_   _   _   _   _   _| ,   |
                 |    .| |_| |_| |_| |_| |_| |  .  |
                 | ,   | .    .     .      . |    .|
                 |   . |  .     . .   .  ,   |.    |
     ___----_____| .   |.   ,  _______   .   |   , |---~_____
_---~            |     |  .   /+++++++\    . | .   |         ~---_
                 |.    | .    |+++++++| .    |   . |              ~-_
              __ |   . |   ,  |+++++++|.  . _|__   |                 ~-_
     ____--`~    '--~~__ .    |++++ __|----~    ~`---,              ___^~-__
-~--~                   ~---__|,--~'                  ~~----_____-~'   `~----~



    Welcome to the Castle! 
    We have been waiting a long time for you to arrive. 
    It seems are town has been overrun by evil creatures! 
    We need your help to kill these monsters!

    """)

    while hero.alive():
        print(
        """

                  (  (|              .
              )   )\/ ( ( (
      *  (   ((  /     ))\))  (  )    )
    (     \   )\(          |  ))( )  (|
    >)     ))/   |          )/  \((  ) 
    (     (      .        -.     V )/   )(    (
     \   /     .   \            .       \))   ))
       )(      (  | |   )            .    (  /
      )(    ,'))     \ /          \( `.    )
      (\>  ,'/__      ))            __`.  /
     ( \   | /  ___   ( \/     ___   \ | ( (
      \.)  |/  /   \__      __/   \   \|  ))
     .  \. |>  \      | __ |      /   <|  /
          )/    \____/ :..: \____/     \ <
   )   \ (|__  .      / ;: \          __| )  (
  ((    )\)  ~--_     --  --      _--~    /  ))
   \    (    |  ||               ||  |   (  /
         \.  |  ||_             _||  |  /
           > :  |  ~V+-I_I_I-+V~  |  : (.
          (  \:  T\   _     _   /T  : ./
           \  :    T^T T-+-T T^T    ;<
            \..`_       -+-       _'  )
               . `--=.._____..=--'. ./         


        """)
        for enemy in enemies:
            battle.start_battle(hero, enemy)
            if not hero.alive():
                break
            
        if hero.alive():
            print("YOU WIN!")
            break

    print("""
             .=.,
            ;c =\\
          __|  _/
        .'-'-._/-'-._
       /..   ____    \\
      /' _  [<_->] )  \\
     (  / \--\_>/-/'._ )
      \-;_/\__;__/ _/ _/
       '._}|==o==\{_\/
        /  /-._.--\  \_
       // /   /|   \ \ \\
      / | |   | \;  |  \ \\
     / /  | :/   \: \   \_\\
    /  |  /.'|   /: |    \ \\
    |  |  |--| . |--|     \_\\
    / _/   \ | : | /___--._) \\
   |_(---'-| >-'-| |       '-'
          /_/     \_\\
    """)
    print("You have saved our village! \nFinally we can go back to a life of peace! \nOur hero!")
    print(
        """
                                 .''.
       .''.             *''*    :_\/_:     . 
      :_\/_:   .    .:.*_\/_*   : /\ :  .'.:.'.
  .''.: /\ : _\(/_  ':'* /\ *  : '..'.  -=:o:=-
 :_\/_:'.:::. /)\*''*  .|.* '.\'/.'_\(/_'.':'.'
 : /\ : :::::  '*_\/_* | |  -= o =- /)\    '  *
  '..'  ':::'   * /\ * |'|  .'/.\'.  '._____
      *        __*..* |  |     :      |.   |' .---"|
       _*   .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
 ___|  '-'     '    ""       '-'   '-.'    '`      |____
jgs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
    )   


            

main()

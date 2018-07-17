# Copyright 2018 Scott Weiner
# Ascii art courtesy of James Huang
# MIT license

import random
import re
import ast
import sys

def ascii_intro():
    print("")
    print("")
    print("")
    print("     ▄████████    ▄████████    ▄████████  ▄█  ███▄▄▄▄    ▄██████▄ ")
    print("    ███    ███   ███    ███   ███    ███ ███  ███▀▀▀██▄ ███    ███")
    print("    ███    █▀    ███    ███   ███    █▀  ███▌ ███   ███ ███    ███")
    print("    ███          ███    ███   ███        ███▌ ███   ███ ███    ███")
    print("    ███        ▀███████████ ▀███████████ ███▌ ███   ███ ███    ███")
    print("    ███        ▀███████████ ▀███████████ ███▌ ███   ███ ███    ███")
    print("    ███    ███   ███    ███    ▄█    ███ ███  ███   ███ ███    ███")
    print("    ████████▀    ███    █▀   ▄████████▀  █▀    ▀█   █▀   ▀██████▀ ")
    print("")
    print("")
    print("   ▄████████    ▄████████    ▄████████    ▄███████▄    ▄████████")
    print("   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███")
    print("   ███    █▀    ███    ███   ███    ███   ███    ███   ███    █▀ ")
    print("   ███         ▄███▄▄▄▄██▀   ███    ███   ███    ███   ███       ")
    print("   ███        ▀▀███▀▀▀▀▀   ▀███████████ ▀█████████▀  ▀███████████")
    print("   ███    █▄  ▀███████████   ███    ███   ███                 ███")
    print("   ███    ███   ███    ███   ███    ███   ███           ▄█    ███")
    print("   ████████▀    ███    ███   ███    █▀   ▄████▀       ▄████████▀ ")
    print("                ███    ███                                       ")
    print("")
    print("")
    print("")

class CrapsMachine:
    def clear(self, names):
        for name in names:
            self.bets[name] = 0

    def bet(self, bet_dict):
        if bet_dict:
            for name, value in bet_dict.items():
                if (self.state['Point'] == 0 and name not in self.legalComeoutBets):
                    raise Exception('Bet ' + name + 'is not legal during the comeout roll')
                elif (self.state['Point'] != 0 and name not in self.legalPointBets):
                    raise Exception('Bet ' + name + 'is not legal during the point rolls')
                
                self.bets[name] += value

    def __payout(self, names):
        payout = 0
        for name in names:
            if ('Odds' in name or 'Horn' in name or 'Field' in name):
                payout += self.bets[(re.sub('\d',"",name)).strip()] * self.payouts[name]
            else:
                payout += self.bets[name] * self.payouts[name]

        return payout

    def __handle_point(self):
        payout = 0
        if (self.state['Point'] == self.state['Last Roll']):
            payout += self.__payout(['Pass', 'Pass Odds ' + str(self.state['Point'])])
            self.clear(['Dont Pass', 'Dont Pass Odds'])
            self.state['Point'] = 0

        return payout

    def roll(self):
        # Initialize the payout
        total_payout = 0
        one_time_keepers = []
        
        if (self.state['Point'] == 0):
            
            ############### COME OUT ROLL ###############
            self.state['D1'] = random.randint(1,6)
            self.state['D2'] = random.randint(1,6)
            self.state['Last Roll'] = self.state['D1'] + self.state['D2']

            # Payout and collect
            if (self.state['Last Roll'] == 2):
                total_payout += self.__payout(['Dont Pass', 'Any Craps', '2 Craps', 'Horn 2', 'Field 2'])
                one_time_keepers += ['Any Craps', '2 Craps', 'Horn', 'Field 2']
                self.clear(['Pass'])

            elif (self.state['Last Roll'] == 3):
                total_payout += self.__payout(['Dont Pass', 'Any Craps', '3 Craps', 'Horn 3', 'Field'])
                one_time_keepers += ['Any Craps', '3 Craps', 'Horn', 'Field']
                self.clear(['Pass']) 

            elif (self.state['Last Roll'] == 4):
                self.state['Point'] = self.state['Last Roll']
                total_payout += self.__payout(['Field'])
                one_time_keepers += ['Field']

            elif (self.state['Last Roll'] == 5):
                self.state['Point'] = self.state['Last Roll']

            elif (self.state['Last Roll'] == 6):
                self.state['Point'] = self.state['Last Roll']
                total_payout += self.__payout(['Big 6'])
                one_time_keepers += ['Big 6']

            elif (self.state['Last Roll'] == 7):
                total_payout += self.__payout(['Pass','Any 7'])
                one_time_keepers += ['Any 7']
                self.clear(['Dont Pass'])

            elif (self.state['Last Roll'] == 8):
                self.state['Point'] = self.state['Last Roll']
                total_payout += self.__payout(['Big 8'])
                one_time_keepers += ['Big 8']

            elif (self.state['Last Roll'] == 9):
                self.state['Point'] = self.state['Last Roll']
                total_payout += self.__payout(['Field'])
                one_time_keepers += ['Field']

            elif (self.state['Last Roll'] == 10):
                self.state['Point'] = self.state['Last Roll']
                total_payout += self.__payout(['Field'])
                one_time_keepers += ['Field']

            elif (self.state['Last Roll'] == 11):
                total_payout += self.__payout(['Pass','11 Yo', 'Field', 'Horn 11'])
                one_time_keepers += ['11 Yo', 'Field', 'Horn']
                self.clear(['Dont Pass'])
            
            elif (self.state['Last Roll'] == 12):
                total_payout += self.__payout(['12 Craps', 'Field 12', 'Any Craps', 'Horn 12'])
                one_time_keepers += ['12 Craps', 'Field 12', 'Horn']           

            else:
                # Can't roll this
                raise Exception('Number outside range of dice')
            
            # Clear the one time bets
            self.clear([x for x in self.oneTimeBets if x not in one_time_keepers])

            self.results.append(total_payout)
            return total_payout
        
        else:

            ############### POINT ROLL ###############
            self.state['D1'] = random.randint(1,6)
            self.state['D2'] = random.randint(1,6)
            self.state['Last Roll'] = self.state['D1'] + self.state['D2']

            # Payout and collect
            if (self.state['Last Roll'] == 2):
                total_payout += self.__payout(['Any Craps', '2 Craps', 'Horn 2', 'Field 2'])
                one_time_keepers += ['Any Craps', '2 Craps', 'Horn', 'Field']

            elif (self.state['Last Roll'] == 3):
                total_payout += self.__payout(['Any Craps', '3 Craps', 'Horn 3', 'Field'])
                one_time_keepers += ['Any Craps', '3 Craps', 'Horn', 'Field']

            elif (self.state['Last Roll'] == 4):
                total_payout += self.__handle_point()                
                total_payout += self.__payout(['Field','Place Win 4'])
                one_time_keepers += ['Field']

            elif (self.state['Last Roll'] == 5):
                total_payout += self.__handle_point() 
                total_payout += self.__payout(['Place Win 5'])

            elif (self.state['Last Roll'] == 6):
                total_payout += self.__handle_point()             
                total_payout += self.__payout(['Big 6','Place Win 6'])
                one_time_keepers += ['Big 6']

            elif (self.state['Last Roll'] == 7):
                total_payout += self.__payout(['Dont Pass', 'Dont Pass Odds ' + str(self.state['Point'])])
                self.clear(['Pass', 'Pass Odds'] + self.placeBets)

                total_payout += self.__payout(['Any 7'])
                one_time_keepers += ['Any 7']

            elif (self.state['Last Roll'] == 8):
                total_payout += self.__handle_point() 
                total_payout += self.__payout(['Big 8', 'Place Win 8'])
                one_time_keepers += ['Big 8']

            elif (self.state['Last Roll'] == 9):
                total_payout += self.__handle_point() 
                total_payout += self.__payout(['Field', 'Place Win 9'])
                one_time_keepers += ['Field']

            elif (self.state['Last Roll'] == 10):
                total_payout += self.__handle_point()
                total_payout += self.__payout(['Field','Place Win 10'])
                one_time_keepers += ['Field']

            elif (self.state['Last Roll'] == 11):
                total_payout += self.__payout(['11 Yo', 'Field', 'Horn 11'])
                one_time_keepers += ['11 Yo', 'Field', 'Horn']
            
            elif (self.state['Last Roll'] == 12):
                total_payout += self.__payout(['12 Craps', 'Field 12', 'Any Craps', 'Horn 12'])
                one_time_keepers += ['12 Craps', 'Field', 'Horn']           

            else:
                # Can't roll this
                raise Exception('Number outside range of dice')
            
            # Clear the one time bets
            self.clear([x for x in self.oneTimeBets if x not in one_time_keepers])
            self.results.append(total_payout)
            return total_payout

    def __init__(self):
        self.bets = {
            'Pass': 0, 
            'Dont Pass': 0,
            'Pass Odds': 0,
            'Dont Pass Odds': 0,
            'Place Win 4': 0,
            'Place Win 5': 0,
            'Place Win 6': 0,
            'Place Win 8': 0,
            'Place Win 9': 0,
            'Place Win 10': 0,
            'Field': 0,
            'Hard 4': 0,
            'Hard 6': 0,
            'Hard 8': 0,
            'Hard 10': 0,
            'Any 7': 0,
            'Any Craps': 0,
            '2 Craps': 0,
            '3 Craps': 0,
            '11 Yo': 0,
            '12 Craps': 0,
            'Horn': 0,
            'Big 6': 0,
            'Big 8': 0
        }
        self.payouts = {
            'Pass': 1,
            'Dont Pass': 1,
            'Pass Odds 4': 2,
            'Pass Odds 5': 3/2,
            'Pass Odds 6': 6/5,
            'Pass Odds 8': 6/5,
            'Pass Odds 9': 3/2,
            'Pass Odds 10': 2,
            'Dont Pass Odds 4': 1/2,
            'Dont Pass Odds 5': 2/3,
            'Dont Pass Odds 6': 5/6,
            'Dont Pass Odds 8': 5/6,
            'Dont Pass Odds 9': 2/3,
            'Dont Pass Odds 10': 1/2,
            'Field': 1,
            'Field 2': 2,
            'Field 12': 2,
            'Place Win 4': 9/5,
            'Place Win 5': 7/5,
            'Place Win 6': 6/5,
            'Place Win 8': 6/5,
            'Place Win 9': 7/5,
            'Place Win 10': 9/5,
            'Hard 4': 7/1,
            'Hard 6': 9/1,
            'Hard 8': 9/1,
            'Hard 10': 7/1,
            'Any 7': 4/1,
            'Any Craps': 7/1,
            '2 Craps': 30/1,
            '3 Craps': 15/1,
            '11 Yo': 15/1,
            '12 Craps': 30/1,
            'Horn 2': 7.5/1,
            'Horn 3': 3.75/1,
            'Horn 11': 3.75/1,
            'Horn 12': 7.5/1,
            'Big 6': 1,
            'Big 8': 1
        }
        self.state = {
            'Point': 0,
            'D1': 0,
            'D2': 0,
            'Last Roll': 0,
            'Hard': False
        }
        self.oneTimeBets = [
            'Field', 
            'Any 7',
            'Any Craps',
            '2 Craps',
            '12 Craps',
            'Horn',
            'Big 6',
            'Big 8'
        ]
        self.placeBets = [
            'Place Win 4',
            'Place Win 5',
            'Place Win 6',
            'Place Win 8',
            'Place Win 9',
            'Place Win 10'            
        ]
        self.legalComeoutBets = ['Pass', 'Dont Pass'] + self.oneTimeBets
        self.legalPointBets = ['Pass Odds', 'Dont Pass Odds'] + self.oneTimeBets + self.placeBets
        self.results = []

class Algorithms:
    
    @staticmethod
    def procrastinate(machine, bankroll, rolls):
        my_bet = {}
        for i in range(rolls):
            if machine.state['Point'] == 0:
                bankroll -= 5
                my_bet['Dont Pass'] = 5
                machine.bet(my_bet)
            
            bankroll += machine.roll()
            machine.clear(['Dont Pass'])

        return bankroll

if __name__ == "__main__":
    ascii_intro()
    cm = CrapsMachine()

    # Various algorithms
    alg_names = ['Scott procrastinates losing while having fun']
    alg_mapping = { 
        1 : Algorithms.procrastinate 
    }

    try:
        print('Choose an algorithm: ')
        for i, alg in enumerate(alg_names,1):
            print('  '+ str(i) + '. ' + alg)

        try:
            alg_num = int(input('Alg Number: '))
        except:
            alg_num = 1
        
        try:
            bankroll = int(input ('Bankroll: '))
        except:
            bankroll = 500

        try:
            rolls = int(input('Rolls: '))
        except:
            rolls = 200

        print(alg_mapping[alg_num](cm, bankroll, rolls))
        print(cm.results)


    except KeyboardInterrupt:
        sys.exit(0)

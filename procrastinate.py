from craps import CrapsMachine
from statistics import mean, median
import pprint
import sys

class Scott:
    
    def __init__(self):
        self.bankroll = 500
        self.rolls = 200
        self.machine = CrapsMachine()

    def reset(self):
        
        self.bankroll = 500
        self.rolls = 200
        
        # New Table
        del self.machine
        self.machine = CrapsMachine()

    def bet(self, name, amount):
        my_bet = dict()
        self.bankroll -= amount

        if self.bankroll <= 0:
            raise Exception('Out of money')

        my_bet[name] = amount
        self.machine.bet(my_bet)

    def playCrapsAtVegas(self):
        results = []
        try:
            for i in range(self.rolls):
                # If we are on the comeout roll
                if self.machine.state['Point'] == 0:
                    # Play don't pass if we don't already have a bet there
                    if not self.machine.bets['Dont Pass']:
                        self.bet('Dont Pass', 5)
                else:
                    # Play max odds on don't pass
                    if not self.machine.bets['Dont Pass Odds']:
                        if self.machine.state['Point'] == 4 or self.machine.state['Point'] == 10:
                            self.bet('Dont Pass Odds', 30)
                        elif self.machine.state['Point'] == 5 or self.machine.state['Point'] == 9:
                            self.bet('Dont Pass Odds', 30)
                        elif self.machine.state['Point'] == 6 or self.machine.state['Point'] == 8:
                            self.bet('Dont Pass Odds', 30)

                    # Put down place bets
                    if not self.machine.bets['Place Win 5']:
                        self.bet('Place Win 5', 5)
                    else:
                        # Up a unit on 5 if last roll was 5
                        if self.machine.state['Last Roll'] == 5:
                            self.bet('Place Win 5', 5)
                    if not self.machine.bets['Place Win 6']:
                        self.bet('Place Win 6', 6)
                    else:
                        # Up a unit on 6 if last roll was 6
                        if self.machine.state['Last Roll'] == 6:
                            self.bet('Place Win 6', 6)
                    if not self.machine.bets['Place Win 8']:
                        self.bet('Place Win 8', 6)
                    else:
                        # Up a unit on 8 if last roll was 8
                        if self.machine.state['Last Roll'] == 8:
                            self.bet('Place Win 8', 6)
                    if not self.machine.bets['Place Win 9']:
                        self.bet('Place Win 9', 5)
                    else:
                        # Up a unit on 9 if last roll was 9
                        if self.machine.state['Last Roll'] == 9:
                            self.bet('Place Win 9', 5)

                win = self.machine.roll()
                self.bankroll += win

                results.append({'Won': win, 'Money on Table': sum(self.machine.bets.values()), 'Bankroll': self.bankroll, 'Last Roll': self.machine.state['Last Roll']})
        
        except Exception:
            # Out of money, collect stats
            pass
            
        stats = {
            'Max Bankroll': max([x['Bankroll'] for x in results]),
            'Min Bankroll': min([x['Bankroll'] for x in results]),
            'Average Table Bankroll': mean([x['Bankroll'] for x in results]),
            'Median Table Bankroll': median([x['Bankroll'] for x in results]),
            'Max Bet on Table': max([x['Money on Table'] for x in results]),
            'Average bet on Table': mean([x['Money on Table'] for x in results]),
            'Final Bankroll': self.bankroll
        }

        return (results,stats)


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

if __name__ == "__main__":
    ascii_intro()
    scott = Scott()
    avg_stats = []

    try:
        for i in range(500):
            results, stats = scott.playCrapsAtVegas()
            avg_stats.append(stats)
            scott.reset()

        pp = pprint.PrettyPrinter()
        final_results = {
            'Average Bankroll': mean([x['Final Bankroll'] for x in avg_stats]),
            'Average Max': mean([x['Max Bankroll'] for x in avg_stats]),
            'Average Min': mean([x['Min Bankroll'] for x in avg_stats]),
            'Average Bet': mean([x['Average bet on Table'] for x in avg_stats])
        }

        pp.pprint(final_results)

    except KeyboardInterrupt:
        sys.exit(0)
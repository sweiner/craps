from shooter import Scott, NormalShooter
import pprint
from statistics import mean, median
from sys import exit
import threading

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

def getResults(avg_stats):
    final_results = {
        'Average Bankroll': mean([x['Final Bankroll'] for x in avg_stats]),
        'Average Max': mean([x['Max Bankroll'] for x in avg_stats]),
        'Average Min': mean([x['Min Bankroll'] for x in avg_stats]),
        'Average Bet': mean([x['Average bet on Table'] for x in avg_stats])
    }

    return final_results

if __name__ == "__main__":
    ascii_intro()
    
    scott = Scott()
    craig = NormalShooter()
      
    avg_stats_scott = []
    avg_stats_craig = []

    try:
        for i in range(500):
            
            t1 = threading.Thread(target=scott.play)
            t2 = threading.Thread(target=craig.play)

            t1.start()
            t2.start()
            
            t1.join()
            t2.join()

            scott_stats = scott.getStats()
            craig_stats = craig.getStats()

            avg_stats_scott.append(scott_stats)
            avg_stats_craig.append(craig_stats)

            scott.reset()
            craig.reset()

        scott_results = getResults(avg_stats_scott)
        craig_results = getResults(avg_stats_craig)

        pp = pprint.PrettyPrinter()
        pp.pprint(['Scott',scott_results,'Craig', craig_results])

    except KeyboardInterrupt:
        exit(0)
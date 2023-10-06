import argparse
from generate import generate_wordlist

def main():
    print('''
     _    _   _   _    _     _   _______   _______   ______         
    | |  | | | |  | | | |   | | |__   __| |  _____| |  __  |
    | |__| | | |  | | |  \  | |    | |    | |____   | |__| /
    |  __  | | |  | | | |\ \| |    | |    |  ____|  |  __ \ 
    | |  | | | |__| | | | \_  |    | |    | |_____  | |  \ \ 
    |_|  |_| \______/ |_|   |_|    |_|    |_______| |_|   \_\ 
             ______   ______   ______   ______
            |  __  | |  __  | |  ____| |  ____| 
            | |__| | | |__| |  \ \__    \ \__
            |  ____| |  __  |   \__ \    \__ \ 
            | |      | |  | |  ____\ \   ___\ \ 
            |_|      |_|  |_| |_______| |______|    
    ''')

    parser = argparse.ArgumentParser(
                    prog='hunterpass',
                    description='Automatic dictionary generator with AI',
                    epilog='Developed by: Rafael Rodrigues Macedo')

    generate_wordlist()

if __name__ == '__main__':
    main()

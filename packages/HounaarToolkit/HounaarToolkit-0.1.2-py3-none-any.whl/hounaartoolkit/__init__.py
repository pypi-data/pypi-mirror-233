import os
from .analyzer import main as analyzer_main
from .youtub import main as youtub_main
from .crypt import main as crypt_main
from .type_rover import main as type_rover_main
from .netscanner import main as netscanner_main
from .rootkit import main as rootkit_main


__all__ = [
    'analyzer_main',
    'youtub_main',
    'crypt_main',
    'type_rover_main',
    'netscanner_main',
    'rootkit_main',
]

def main():
    print("""


          
          WELCOME TO


 _   _                                  _____           _ _    _ _   
| | | |                                |_   _|         | | |  (_) |  
| |_| | ___  _   _ _ __   __ _  __ _ _ __| | ___   ___ | | | ___| |_ 
|  _  |/ _ \| | | | '_ \ / _` |/ _` | '__| |/ _ \ / _ \| | |/ / | __|
| | | | (_) | |_| | | | | (_| | (_| | |  | | (_) | (_) | |   <| | |_ 
\_| |_/\___/ \__,_|_| |_|\__,_|\__,_|_|  \_/\___/ \___/|_|_|\_\_|\__|
                                                                     
                                                            




 """)
    
    print("Choose from the following commands:")
    print("1> Data Analysis AI")
    print("2> Youtube Downloader")
    print("3> Cryptocurrency Price Checker")
    print("4> Type Rover")
    print("5> Network Scanner")
    print("6> Rootkit Scanner")
    print("7> Exit")

    choice = input("Enter the number of the tool you want to run: ")

    if choice == '1':
        analyzer_main()
    elif choice == '2':
        youtub_main()
    elif choice == '3':
        crypt_main()
    elif choice == '4':
        type_rover_main()
    elif choice == '5':
        netscanner_main()
    elif choice == '6':
        rootkit_main()
    elif choice == '7':
        os.system("exit")
    else:
        print("Invalid choice. Please enter a valid tool number.")

if __name__ == "__main__":
    main()

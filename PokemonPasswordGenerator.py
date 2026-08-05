from pdb import main
from bs4 import BeautifulSoup
import pandas as pd, requests, random, string, tkinter as td

def main():
# NOTE: If you are using a VPN, turn it off, as it may block the request to the website.
    try:
        r = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number")

        if r.status_code == 403:
            print("Access denied. Please check your internet connection or turn off your VPN.")
            exit()
        else:
            done = False
            listOfPasswords = []
            while not done:
                # Ask the user how many characters they want in their password.
                num_chars = int(input("How many characters do you want or need in your password? (Press Enter to continue): "))

                # Open the file in write mode with UTF-8 encoding
                file = open("pokemon.html", "w", encoding="utf-8")
                soup = BeautifulSoup(r.text, 'html.parser')
                file.write(soup.prettify())
                file.close()

                # Get the pokemon names from the HTML file and put it in a list.
                pokedexList = []

                '''
                for loop will go through all the links in the HTML file and check if the link has a title attribute and if it contains 
                '(Pokémon)' in it. If it does, it will add the title to the pokedexList
                '''
                for link in soup.find_all('a'):
                    if link.get('title') is not None and '(Pokémon)' in link.get('title') and link.parent.name == 'td':
                        pokedexList.append(str(link.get('title')).replace(' (Pokémon)', ''))

                # Removes duplicates from the list.
                pokedexList = list(dict.fromkeys(pokedexList))

                # Puts list an dataframe and adds an index to it.
                pokedex = pd.DataFrame(pokedexList, columns=['Pokémon'])
                pokedex.index += 1  # Start index at 1 instead of 0

                # Generates a random password using a random Pokémon name and a random number.
                password = pokedex["Pokémon"][random.randint(1, len(pokedex))] + str(random.randint(1, len(pokedex)))
                symbols = string.punctuation

                # If the password is not long enough, it will add random symbols to the end of the password until it is long enough.
                while len(password) < num_chars:
                    password += symbols[random.randint(0, len(symbols) - 1)]
                    
                print(password)

                listOfPasswords.append(password)

                print("Would you like to generate another password? (y/n): ")
                if input().lower() == 'n':
                    with open("pokemon_passwords.txt", "w", encoding="utf-8") as file:
                        for pwd in listOfPasswords:
                            file.write(pwd + "\n")
                    print("Thank you for using the Pokémon Password Generator! All your passwords have been saved to 'pokemon_passwords.txt'. Goodbye!")
                    done = True

    except Exception as e:
        print(f"Error occurred while writing to file: {e}")

if __name__ == "__main__":
    main()
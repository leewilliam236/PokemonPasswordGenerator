from bs4 import BeautifulSoup
import pandas as pd, requests, random, tkinter as tk

# NOTE: If you are using a VPN, turn it off, as it may block the request to the website.

try:
    r = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number")

    if r.status_code == 403:
        print("Access denied. Please check your internet connection or turn off your VPN.")
        exit()

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
            pokedexList.append(str(link.get('title')).rstrip(' (Pokémon)'))

    # Removes duplicates from the list.
    pokedexList = list(dict.fromkeys(pokedexList))

    # Puts list an dataframe and adds an index to it.
    pokedex = pd.DataFrame(pokedexList, columns=['Pokémon'])
    pokedex.index += 1  # Start index at 1 instead of 0

    # Generates a random password using a random Pokémon name and a random number.
    password = pokedex["Pokémon"][random.randint(1, len(pokedex))]
    print(f'{password}{random.randint(1, len(pokedex))}')

except Exception as e:
    print(f"Error occurred while writing to file: {e}")
from bs4 import BeautifulSoup
import pandas as pd, requests

# NOTE: If you are using a VPN, turn it off, as it may block the request to the website.

try:
    r = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number")

    # Open the file in write mode with UTF-8 encoding
    file = open("pokemon.html", "w", encoding="utf-8")
    soup = BeautifulSoup(r.text, 'html.parser')
    file.write(soup.prettify())
    file.close()

    # # Get the pokemon names from the HTML file and export into an html file.
    pokedexList = []

    for link in soup.find_all('a'):
        if link.get('title') is not None and '(Pokémon)' in link.get('title') and link.parent.name == 'td':
            pokedexList.append(str(link.get('title')).rstrip('(Pokémon)'))

    # Removes duplicates from the list.
    pokedexList = list(dict.fromkeys(pokedexList))

    pokedex = pd.DataFrame(pokedexList, columns=['Pokémon'])
    pokedex.index += 1  # Start index at 1 instead of 0

    # Use HTML file to then generate a pd.Series object.
    pokedex.to_excel("pokedex.xlsx", index=False)

except Exception as e:
    print(f"Error occurred while writing to file: {e}")
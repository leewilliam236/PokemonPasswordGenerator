from bs4 import BeautifulSoup
import pandas as pd, requests

try:
    r = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number")

    # Open the file in write mode with UTF-8 encoding
    file = open("pokemon.html", "w", encoding="utf-8")
    soup = BeautifulSoup(r.text, 'html.parser')
    file.write(soup.prettify())
    file.close()

    # # Get the pokemon names from the HTML file and export into an html file.
    file = open("pkmn.html", "w", encoding="utf-8")
    for link in soup.find_all('a'):
        if link.get('title') is not None and '(Pokémon)' in link.get('title') and link.parent.name == 'td':
            file.write(str(link.get('title')).rstrip('(Pokémon)') + '\n')
    file.close()

    # Use HTML file to then generate a list.
    pokedex = pd.read_html("pkmn.html")

except Exception as e:
    print(f"Error occurred while writing to file: {e}")

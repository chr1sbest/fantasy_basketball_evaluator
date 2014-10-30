from bs4 import BeautifulSoup
from requests import get
from json import dump

def espn_soup(start_index):
    base_url = 'http://games.espn.go.com/fba/tools/projections'
    params = {'leagueId': 271728, 'startIndex': start_index}
    response = get(base_url, params=params)
    soup = BeautifulSoup(response.text)
    return soup

def player_builder(soup):
    all_player_data = []
    players = soup.find_all('tr',{'class':'pncPlayerRow'})
    cats = ['GP', 'MIN', 'FGM', 'FGA', 'FG%', 'FTM', 'FTA', 'FT%', '3PM',\
            '3PA', 'REB', 'AST', 'A/TO', 'STL', 'BLK', 'TO', 'PTS']
    for player in players:
        player_data = {}
        tables = player.find_all('td')
        player_rank = int(tables[0].text)
        if player_rank > 350: break             # Don't handle unranked players
        player_data['RNK'] = int(player_rank)
        player_data['NAME'] = tables[1].text.split(',')[0]
        player_data['POS'] = get_positions(tables[1].text)
        for cat, value in zip(cats, tables[4:]):    # Point Values
            player_data[cat] = float(value.text)
        all_player_data.append(player_data)
    return all_player_data
    
def get_positions(unparsed_string):
    player = unparsed_string.replace(u'\xa0', u' ')
    positions = player.split(' ')[3:]
    return filter(lambda x: x not in [u'DTD', u''], positions)

if __name__ == "__main__":
    soup = espn_soup(0)
    player_data = []
    for start_index in [0, 40, 80, 120, 160, 200, 240, 280, 320]:
        soup = espn_soup(start_index)
        player_data += player_builder(soup)
    with open('player_data.json', 'wb') as player_file:
        dump(player_data, player_file)

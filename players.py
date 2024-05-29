import pandas as pd
import time
from bs4 import BeautifulSoup
import requests

from tqdm import tqdm


addurl = 'https://www.transfermarkt.com'
years = range(2000, 2024)

filenames = [f'data/Club_stats_of_the_season_{x}.csv' for x in years]

for filename in filenames:
    try:
        club_data = pd.read_csv(filename)
    except Exception as e:
        print('could not read the file')
        continue
        
    mainlinks = list(club_data['Links'])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

    player, position, ls = [], [], []
    number, date_of_birth, height, foot, joined = [], [], [], [], []
    market_value = []

    names = list(club_data['Club'])
    club_names = []
    
    season = int(filename[::-1][4:8][::-1])
    
    for l in range(len(mainlinks)):
        try:
            r = requests.get(mainlinks[l], headers = headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            for r in tqdm(soup.find_all('table', class_ = 'inline-table'), ascii= True, desc = f'The club {names[l]} - {season} season'):
                s = [x.text.strip() for x in r.find_all('td')]
                player.append(s[1])
                position.append(s[2])
                
                club_names.append(names[l])
            
            
            for elem in soup.find_all('td', class_ = 'hauptlink'):
                elem = elem.find('a')
                if elem:
                    #ls.append(str(addurl + elem['href']))
                    pass
            
            counter = 1
            for elem in soup.find_all('td', class_ = 'zentriert'):
                if counter == 1:
                    number.append(elem.text.strip())
                if counter == 2:
                    date_of_birth.append(elem.text.strip())
                if counter == 4:
                    height.append(elem.text.strip())
                if counter == 5:
                    foot.append(elem.text.strip())
                if counter == 6:
                    joined.append(elem.text.strip())
                counter += 1
                if counter == 9:
                    counter = 1

            
            for elem in soup.find_all('td', class_ = 'rechts hauptlink'):
                market_value.append(elem.text.strip())
            
            #print(f'{l+1}th link is done!!!')
            
            time.sleep(2)
            
        except Exception as e:
            print(f"The template is not working for the {l + 1}th link", '-->',e)
    
    df = pd.DataFrame({
        'Player': player,
        'Club': club_names,
        'Position': position,
        'Number': number,
        'Date of Birth': date_of_birth,
        'Height': height,
        'Foot': foot,
        'Joined': joined,
        'Market Value': market_value,
        'Season': [season for x in range(len(player))]
    })

    df.to_csv(f'data_player/Player_stats_of_the_season_{ season }.csv')
    time.sleep(2)
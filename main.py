import requests
from bs4 import BeautifulSoup

import pandas as pd

years = range(2000, 2024)
baseurls = [f'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/KAS1/plus/?saison_id={year}' for year in years]
addurl = 'https://www.transfermarkt.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
   
for baseurl in baseurls:
    year = baseurl[::-1][:4][::-1]
    try: 
        r = requests.get(baseurl, headers = headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        clubnames = []
        squad, age, foreigners = [], [], []
        market_value, total_market_value = [], []
        links = []

        classnames = ['odd', 'even']
        for cl in classnames:
            for i in soup.find_all('tr', class_ = cl):
                for elem in i.find_all('td', class_ = 'hauptlink no-border-links'):
                    clubnames.append(elem.text.strip())
                
                s = [x.text.strip() for x in i.find_all('td', class_ = 'zentriert')]
                
                if not len(s[2]):
                    break
                
                squad.append(s[1])
                age.append(s[2])
                foreigners.append(s[3])
                
                s = [x for x in i.find_all('td', class_ = 'rechts')]
                market_value.append(s[0].text.strip())
                total_market_value.append(s[1].text.strip())
                
                links.append(addurl + s[1].find('a')['href'] + '/plus/1')

        df = pd.DataFrame({'Club': clubnames, 
                        'Squad': squad, 
                        'Age': age, 
                        'Foreigners': foreigners, 
                        'Market Value': market_value, 
                        'Total Market Value': total_market_value,
                        'Links': links})
        
        df.to_csv(f'data/Club_stats_of_the_season_{ year }.csv')
        print(f"Processing {year} is done succesfully!")

    except Exception as e:
        print(f"The template is not working for the {year} season", '-->',e)
import scraper
import urllib .request as urlreq
import json

def req(url):
    request = urlreq.Request(url)

    with urlreq.urlopen(request) as resp:
        resp_text = resp.read().decode("utf-8")

    return json.loads(resp_text)

patch_url = 'https://ddragon.leagueoflegends.com/api/versions.json'
champ_url = f'http://ddragon.leagueoflegends.com/cdn/{req(patch_url)[0]}/data/en_US/championFull.json'

champ_json = req(champ_url)
keys = champ_json.get('keys')
data = champ_json.get('data')
champs = []

for key in keys:
    champ_id = keys.get(key)
    champs.append(data.get(champ_id).get('name'))

champs.sort()

def get_tags(tags):
    if tags:
        return '_tags'
    else:
        return '' 
    
def check_champ(input):
    for champ in champs:
        if input.lower() in champ.lower():

            return champ, True
        
    return input, False

def get_quotes(input=champs, tags=False):
    champ_quotes = {}
    filename = f'quotes{get_tags(tags)}.json'
    if type(input) is str:
        input = check_champ(input)
        if input[1]:
            filename = input[0].lower().replace(' ', '') + '_' + filename
            print('Started scraping ' + input[0] + '\'s quotes.')
            champ_quotes = {"name": input[0], "quotes": scraper.get_champ_quotes(input[0], tags)}
            print('Finished scraping ' + input[0] + '\'s quotes.')
        else:
            print(f"Could not find entered champion({input[0]}). Please try again.")
            return
    else:
        for champ in input: 
            print('Started scraping ' + champ + '\'s quotes.')
            champ_quotes[champ] = scraper.get_champ_quotes(champ, tags)
            print('Finished scraping ' + champ + '\'s quotes.')

    with open(filename, 'w') as file:
        file.write(json.dumps(champ_quotes))
        file.close()


from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json

def convert_champ_name(champ_name):
    champ_name = champ_name.lower()
    if 'nunu' in champ_name:
        return "Nunu"
    elif 'jarvan' in champ_name:
        return 'Jarvan_IV'
    elif 'leblanc' in champ_name:
        return 'LeBlanc'

    champ_name = champ_name.title()
    return champ_name.replace(' ', '_')

def get_champ_quotes(champ_name, tags=False):
    url = f'https://leagueoflegends.fandom.com/wiki/{convert_champ_name(champ_name)}/LoL/Audio'

    session = HTMLSession()
    response = session.get(url)
    response.html.render(timeout=30)

    soup = BeautifulSoup(response.html.html, 'html.parser')
    start = soup.find(class_='mw-parser-output').find('h2')

    if tags:
        return generate_quotes_tags(champ_name, start)
    else:
        return generate_quotes(start)

def get_quotes(tag):
    quotes=[]
    sub_tags = tag.find_all('li')
    for sub_tag in sub_tags:
        tag_element = sub_tag.find('i')
        if tag_element is not None:      
            quote = tag_element.text
            if '"' in quote and quote[-1] == '"':
                quotes.append(quote[quote.index('"'):])

    return quotes


def get_text(tags):
    if tags.name == 'dl':
        if tags.find('dt') != None:
            return tags.find('dt').text
    elif tags.name == 'h2' or tags.name == 'h3':
        return tags.find(class_='mw-headline').text 
    else:
        return None


def generate_quotes_tags(champ_name, element):
    sect_header = ''
    old_header = ''
    curr_header = ''
    curr_dict = {}
    quotes = {}
    while element is not None and get_text(element) != 'Trivia':
        temp_text = get_text(element)
        if element.name == 'h2':
            sect_header = curr_header = temp_text
        elif temp_text is not None:
            curr_header = temp_text
        elif element.name == 'ul':
            tags = element.find_all('li')
            i = 0
            for tag in tags:
                tag_element = tag.find('i')
                if tag_element is not None:
                    quote = tag_element.text
                    if '"' in quote and quote[-1] == '"':
                        curr_dict[champ_name.lower().replace(' ', '') + '-' +curr_header.lower().replace(' ', '')+str(i)] = quote[quote.index('"'):]
                        i += 1
        
            if old_header != sect_header:
                quotes[sect_header] = curr_dict.copy()
                old_header = sect_header
            else:
                old_dict = quotes[sect_header]
                new_dict = {**old_dict, **curr_dict}
                quotes[sect_header] = new_dict

            curr_dict.clear()
        elif element.has_attr('class') and element['class'] == ['tabber', 'wds-tabber']:
            sub_element = element.find(class_='wds-tab__content wds-is-current').find('h2')
            quotes = {**quotes, **generate_quotes_tags(champ_name, sub_element)}
        
        element = element.find_next_sibling()
    return quotes
    

def generate_quotes(element, quotes=[]):
    while element is not None and get_text(element) != 'Trivia': 
        if element.has_attr('class') and element['class'] == ['tabber', 'wds-tabber']:
            sub_element = element.find(class_='wds-tab__content wds-is-current').find('h2')
            generate_quotes(sub_element, quotes)
        if element.name == 'ul':
            quotes += get_quotes(element)
        element = element.find_next_sibling()

    return quotes

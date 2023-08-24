import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def convert_champ_name(champ_name):
    champ_name.lower()
    if 'nunu' in champ_name:
        return "Nunu"

    champ_name = champ_name.title()
    return champ_name.replace(' ', '_')

def get_quotes(champ_name, tag=False):
    url = f'https://leagueoflegends.fandom.com/wiki/{convert_champ_name(champ_name)}/LoL/Audio'

    opts = Options()
    opts.add_argument('-headless')

    driver = webdriver.Firefox(options=opts)
    driver.get(url)

    content = driver.find_element(By.CLASS_NAME, 'mw-parser-output')
    content_elements = content.find_elements(By.XPATH, '*')

    if tag:
        return generate_quotes_with_tags(champ_name, content_elements)
    else:
        return generate_quotes(champ_name, content_elements)

def check_for_child(element, tag=None):
    if tag == None:
        elements = element.find_elements(By.XPATH, '*')

        if len(elements) == 0:
            return False
        else:
            return True
    else:
        try:
            element.find_element(By.TAG_NAME, tag).text
        except:
            return False 
    
    return True

def generate_quotes(champ_name, content_elements):
    quotes = []
    for element in content_elements:
        if element.tag_name == 'ul':
            sub_elements = element.find_elements(By.TAG_NAME, 'li')
            for sub_element in sub_elements:
                quote = sub_element.find_element(By.TAG_NAME, 'i').text
                if quote[0] == '"':
                    quotes.append(quote)
        elif element.tag_name == 'h2':
            if element.find_element(By.CLASS_NAME, 'mw-headline').text == 'Trivia':
                break 
                
    return quotes



def generate_quotes_with_tags(champ_name, content_elements):
    champ_dict = {"name": champ_name}
    quotes = {}
    curr_header = ''
    section_header = ''
    old_header = ''
    curr_dict = {}
    for element in content_elements:
        if element.tag_name == 'h2':
            text = element.find_element(By.CLASS_NAME, 'mw-headline').text
            if text == 'Trivia':
                break
            elif text != 'Laugh':
                section_header = text.replace(' ', '')
                curr_header = text.lower().replace(' ', '')
        elif element.tag_name == 'h3':
            curr_header = element.find_element(By.CLASS_NAME, 'mw-headline').text.lower().replace(' ', '')
        elif element.tag_name == 'dl':
            if check_for_child(element, 'dt'):
                curr_header = element.find_element(By.TAG_NAME, 'dt').text.lower().replace(' ', '')
        elif element.tag_name == 'ul':
            sub_elements = element.find_elements(By.TAG_NAME, 'li')
            i = 0
            for sub_element in sub_elements:
                text = sub_element.find_element(By.TAG_NAME, 'i').text 
                if '"' in text:
                    curr_dict[champ_name.lower().replace(' ', '') + curr_header + str(i)] = text[text.index('"'):]
                    i += 1
                
            if old_header != section_header:
                quotes[section_header] = curr_dict.copy()
                old_header = section_header
            else:
                old_dict = quotes[section_header]
                new_dict = {**old_dict, **curr_dict}
                quotes[section_header] = new_dict

            curr_dict.clear()
                
    champ_dict['quotes'] = quotes
    with open(f"{champ_name.lower().replace(' ', '_')}_quotes.json", 'w') as file:
        file.write(json.dumps(champ_dict))
        file.close()

get_quotes('Camille', True)
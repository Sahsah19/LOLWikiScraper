# LOLWikiScraper

LOLWikiScraper is a webscraper that was built with the purpose of generating champion quotes from the League of Legends Wiki using Python and BeautifulSoup4. 

## Usage

Before you are able to use the scraper, some prerequisites are required. The neccessary tools to run this scraper, include Python3, requests-html, and BeautifulSoup4. To learn how to install external Python libraries, more information can be found [here](https://docs.python.org/3/installing/index.html).

usage: main.py [-h] [-t] [-c CHAMP]

  optional arguments:
  
    -h, --help                      show this help message and exit 
    -t, --tags                      generate json file with an individual key for each quote e.g. python main.py --tags
    -c CHAMP, --champ CHAMP         generate json file for a particular champion e.g. python main.py --champ "Camille"

## Credits

All code by Sahsah19

Quotes generated from the [LoL Wiki](https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki)

Project inspirtation from [LoLdle](https://loldle.net/)

import argparse
import riot

desc = '''LOLWikiScraperr is a webscraper built using Python and the BeautifulSoup libraries. This scraper generates json files with all the quotes found on the LOL Wiki 
website for each individual champion, and can be altered using the optional arguments provided below. '''

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-t', '--tags', action='store_true', help='generate json file with an individual key for each quote e.g. python main.py --tags')
parser.add_argument('-c', '--champ', type=str, help='generate json file for a particular champion e.g. python main.py --champ \"Camille\"gut')
args = parser.parse_args()

if args.champ:
    riot.get_quotes(args.champ, args.tags)
else:
    riot.get_quotes(tags=args.tags)
import requests
import pdb
import pprint
from bs4 import BeautifulSoup as bs4
import argparse
from secrets import GOODREADS_KEY
import re

pp = pprint.PrettyPrinter()


def isTitleAvailable(title: str) -> None:
    params = {
        'query': title,
        'searchType': 'title',
        'f_FORMAT': 'EBOOK',
    }

    response = requests.get('https://austin.bibliocommons.com/v2/search', params=params)
    soup = bs4(response.content, 'html.parser')

    button_wrapper = soup.find_all('div', {'class': 'item-transaction-button-wrap'})
    if len(button_wrapper) > 1:
        print(f'Multiple copies of {title} available, not sure how to distinguish')
    elif len(button_wrapper) == 0:
        print(f'Could not find {title}')
        return

    button_wrapper = button_wrapper[0]

    if 'Request this Download' in button_wrapper.text:
        print(f'{title} is not available')
    elif 'Checkout Now' in button_wrapper.text:
        print(f'{title} is currently available')
    else:
        print(f'Status for {title} is unknown')


def getGoodreadsLists():
    # shelves = requests.get('https://www.goodreads.com/shelf/list.xml', params={'key': GOODREADS_KEY})
    # pdb.set_trace()
    # return shelves

    books = requests.get('https://www.goodreads.com/review/list/10636627.xml', params={'key': GOODREADS_KEY})
    soup = bs4(books.content, 'lxml')
    xml_titles = soup.find_all('title')
    # Get the title before any ( or :
    titles = [re.split('\(|:', x.get_text(strip=True))[0].strip() for x in xml_titles]
    return titles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='The title of the book to look for', nargs='?')
    parser.add_argument('--file', help='Filename with a list of books to search for')
    args = parser.parse_args()

    if not args.file and not args.title:
        titles = getGoodreadsLists()
    elif args.file:
        with open(f'{args.file}', 'r') as infile:
            titles = []
            for title in infile:
                titles.append(title.strip())
    elif args.title:
        titles = [title.strip()]

    for title in titles:
        isTitleAvailable(title)


if __name__ == '__main__':
    main()

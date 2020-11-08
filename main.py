import requests
import pdb
import pprint
from bs4 import BeautifulSoup as bs4
import argparse

pp = pprint.PrettyPrinter()

parser = argparse.ArgumentParser()
parser.add_argument('title', help='The title of the book to look for', nargs='?')
parser.add_argument('--file', help='Filename with a list of books to search for')
args = parser.parse_args()


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
        print('Multiple copies available, not sure how to distinguish')

    button_wrapper = button_wrapper[0]

    if 'Request this Download' in button_wrapper.text:
        print(f'{title} is not available')
    elif 'Checkout Now' in button_wrapper.text:
        print(f'{title} is currently available')
    else:
        print(f'Status for {title} is unknown')


def main():
    if args.file:
        with open(f'{args.file}', 'r') as infile:
            for title in infile:
                isTitleAvailable(title.strip())
    elif args.title:
        isTitleAvailable(args.title.strip())


if __name__ == '__main__':
    main()

import argparse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class URLValidator:
    @staticmethod
    def is_valid_url(url):
        # Перевірка валідності URL-адреси
        parsed_url = urlparse(url)
        return parsed_url.scheme and parsed_url.netloc


class URLParser:
    def __init__(self, url):
        self.url = url

    def get_links(self):
        # Завантаження сторінки
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print('Error occurred while fetching the webpage:', e)
            return []

        # Парсинг HTML і отримання списку посилань
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a')]
        return links


class URLProcessor:
    def __init__(self, links):
        self.links = links

    def process_links(self):
        valid_links = []
        broken_links = []

        # Перевірка статусу кожного посилання
        for link in self.links:
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    valid_links.append(link)
                else:
                    broken_links.append(link)
            except requests.exceptions.RequestException:
                broken_links.append(link)

        return valid_links, broken_links


def save_links_to_file(filename, links):
    try:
        with open(filename, 'w') as file:
            for link in links:
                file.write(link + '\n')
    except (FileNotFoundError, PermissionError) as e:
        print('Error occurred while saving links to file:', e)


def main():
    parser = argparse.ArgumentParser(description='HTML Page Link Parser')
    parser.add_argument('-url', metavar='url', type=str, help='URL of the webpage')
    args = parser.parse_args()

    # Перевірка введення URL-адреси
    if not args.url:
        args.url = input('Enter the URL of the webpage: ')

    # Перевірка валідності URL-адреси
    if not URLValidator.is_valid_url(args.url):
        print('Invalid URL:', args.url)
        return

    # Парсинг посилань зі сторінки
    parser = URLParser(args.url)
    links = parser.get_links()

    # Перевірка наявності посилань
    if not links:
        print('No links found on the webpage.')
        return

    # Обробка посилань
    processor = URLProcessor(links)
    valid_links, broken_links = processor.process_links()

    # Збереження посилань у файли
    save_links_to_file('valid_links.txt', valid_links)
    save_links_to_file('broken_links.txt', broken_links)

    print('Link processing completed.')


if __name__ == '__main__':
    main()

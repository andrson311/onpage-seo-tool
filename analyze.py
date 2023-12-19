import argparse
import requests
from bs4 import BeautifulSoup

def get_meta(soup, meta):
    tag = soup.find('meta', {'name': meta})
    if tag:
        print(f'Meta {meta} found: {tag["content"]}')
    else:
        tag = soup.find('meta', {'property': f'og:{meta}'})
        if tag:
            print(f'Meta {meta} found: {tag["content"]}')
        else:
            print(f'No meta {meta} found.')

def analyze_metadata(response, meta_data):
    soup = BeautifulSoup(response.content, 'html.parser')
    for m in meta_data:
        get_meta(soup, m)

def lookup_elements(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    h1 = soup.find_all('h1')
    h2 = soup.find_all('h2')
    p = soup.find_all('p')

    return {
        'h1': len(h1),
        'h2': len(h2),
        'p': len(p)
    }

def check_ssl(response):
    if response.status_code != 200:
        print('Error: Could not access the website')
        return
    
    if response.url.startswith('https://'):
        print('The website has a valid SSL certificate')
    else:
        print('The website does NOT have a valid SSL certificate')

def check_images_alt_attr(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    for img in images:
        if 'alt' in img.attrs:
            print(f"Image with src: {img['src']} contains an 'alt' attribute")
        else:
            print(f"\n\tImage with src: {img['src']} does NOT contain an 'alt' attribute\n")

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Analyze on-page SEO.'
    )

    parser.add_argument(
        '-u',
        '--url',
        type=str,
        required=True,
        help='URL address of page you want to analyze.'
    )

    args = parser.parse_args()

    response = requests.get(args.url)

    print('\n---- Meta data status ---------------\n')
    meta_data = ['title', 'description']
    analyze_metadata(response, meta_data)

    print('\n---- Element occurences -------------\n')
    elements = lookup_elements(response)
    for e in elements:
        print(f"'{e}' elements found: {elements[e]}")

    print('\n---- SSL status ---------------------\n')
    check_ssl(response)

    print('\n---- Image alt attributes status ----\n')
    check_images_alt_attr(response)





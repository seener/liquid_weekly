from os import path
import requests
from bs4 import BeautifulSoup as bts
from lxml.etree import XMLSyntaxError, DocumentInvalid
import pandas as pd

def download_html(url):
    """
    Downloads the raw HTML from a webpage and returns it as a string.

    Args:
        url (str): The URL of the webpage to download.

    Returns:
        str: The raw HTML content of the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_html(content):
    """
    Parses the raw HTML content using BeautifulSoup and lxml parser.

    Args:
        content (str): The raw HTML content to be parsed.

    Returns:
        BeautifulSoup object: The parsed HTML content.
        None: If an error occurs during parsing.
    """
    try:
        parsed = bts(content, 'lxml')
        return parsed
    except (XMLSyntaxError, DocumentInvalid) as e: 
        print(f"An error occurred while parsing the HTML: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def parse_content(url, soup):
    """
    Extracts specific elements (title, head, body) from a BeautifulSoup object and returns them in a list.

    Args:
        url (str): The URL of the webpage being parsed.
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.

    Returns:
        list: A list containing the URL and the extracted elements (title, head, body).
              If an element is not found, its value will be None.
    """
    try:
        title = soup.title
    except:
        print(f'For {url} unable to find the title tag')
        title = None
    try:
        head = soup.head
    except:
        print(f'For {url} unable to find the head tag')
        head = None
    try:
        body = soup.body
    except:
        print(f'For {url} unable to find the body tag')
        body = None
    
    return [url, title, head, body, soup]
    
def run_over_list(urls):
    """
    Processes a list of URLs, downloads their HTML content, parses it, and extracts specific elements.
    Combines the extracted elements into a DataFrame.

    Args:
        urls (list): A list of URLs to be processed.

    Returns:
        DataFrame: A pandas DataFrame containing the URL and the extracted elements (title, head, body) for each URL.
    """
    cols = ['url', 'title', 'head', 'body', 'html']
    ar = []
    for url in urls:
        raw_html = download_html(url)
        soup_html = parse_html(raw_html)
        struct_html = pd.DataFrame([parse_content(url, soup_html)], columns=cols)
        ar.append(struct_html)

    df = pd.concat(ar, ignore_index=True)

    return df

def main(file_path):
    # get path to csv from user
    if file_path == False:
        file_path = input('Provide the file path to a csv with urls: ').strip()
        col_head = input('Does your csv have column headers [Y/N]: ').strip().lower()

    # process the urls
    if col_head == 'y':
        df_urls = pd.read_csv(file_path)
    else: 
        df_urls = pd.read_csv(file_path, header=None)
    url_list = df_urls.iloc[:, 0].tolist()
    # print(url_list)
    processed = run_over_list(url_list)

    # create output file name
    directory = path.dirname(file_path)
    file_name = path.splitext(path.basename(file_path))[0]
    out = directory + '/' + file_name + ' - processed.xlsx'

    # write the output
    # print(processed)
    processed.to_excel(out, index=False) 

if __name__ == "__main__":
    main(False)
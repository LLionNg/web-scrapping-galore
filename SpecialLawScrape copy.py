import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import re

def filter_thai_text(text):
    thai_char_pattern = re.compile(r'[\u0E00-\u0E7F]+')
    number_pattern = re.compile(r'(\(\d+/\d+\)|\d+/\d+|\(\d+\)|\d+)(?:\s*)')
    
    combined_text = ""
    index = 0

    while index < len(text):
        thai_match = thai_char_pattern.search(text, index)
        if thai_match:
            combined_text += thai_match.group()
            index = thai_match.end()

            while index < len(text) and text[index].isspace(): # Check forwhitespace and numbers following Thai char
                combined_text += text[index]
                index += 1
            
            number_match = number_pattern.match(text, index) # Case: numbers with optional /, (), and whitespace
            if number_match:
                combined_text += number_match.group(1)
                index += len(number_match.group(1))
            
                while index < len(text) and text[index].isspace(): # Add whitespace after number
                    combined_text += text[index]
                    index += 1
        else:
            break
    
    return combined_text

def find_links_recursive(element, base_url, keyword):
    links = []
    
    if element.name == 'a' and 'href' in element.attrs:
        href = element['href']

        if keyword in href: # href contains the keyword after "ประมวลแพ่งและพาณิชย์"
            decoded_href = unquote(href)
            full_url = urljoin(base_url, decoded_href)
            links.append(full_url)
    
    for child in element.find_all(recursive=False):
        links.extend(find_links_recursive(child, base_url, keyword))
    
    return links

def scrape_thai_law_links(url, output_file, append_mode=False):
    def scrape_page(page_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request error for {page_url}: {e}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        
        mode = 'a' if append_mode else 'w'
        with open(output_file, mode, encoding='utf-8') as file:
            for p in paragraphs:
                thai_text = filter_thai_text(p.get_text())
                if thai_text:
                    file.write(thai_text + '\n')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error for the initial page: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    content_div = soup.find('div', id='content_right_res')
    if not content_div:
        print("The <div id='content_right_res'> was not found on the page.")
        return

    base_url = 'https://www.peesirilaw.com/'
    keyword = 'ประมวลแพ่งและพาณิชย์'
    links = find_links_recursive(content_div, base_url, keyword)

    if not links:
        print("No matching links found.")
    
    for link in links:
        scrape_page(link)
        print(f"Content from {link} has been scraped and saved.")

if __name__ == "__main__":
    url = 'https://www.peesirilaw.com/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%A1%E0%B8%A7%E0%B8%A5%E0%B9%81%E0%B8%9E%E0%B9%88%E0%B8%87%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B8%9E%E0%B8%B2%E0%B8%93%E0%B8%B4%E0%B8%8A%E0%B8%A2%E0%B9%8C_page2'
    output_file = 'test.txt'
    append_mode = True  # Set to False if you want to overwrite the file
    
    scrape_thai_law_links(url, output_file, append_mode)
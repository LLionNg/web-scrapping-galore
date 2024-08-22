import requests
from bs4 import BeautifulSoup

def scrape_thai_law(url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    paragraphs = soup.find_all('p')
    mso_paragraphs = soup.find_all('p', class_='MsoNormal')
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for p in paragraphs:
            file.write(p.get_text() + '\n')
        
        for p in mso_paragraphs:
            file.write(p.get_text() + '\n')
    
    print(f"Content has been scraped and saved to {output_file}")

if __name__ == "__main__":
    url = ''
    output_file = 'test2.txt'
    
    scrape_thai_law(url, output_file)

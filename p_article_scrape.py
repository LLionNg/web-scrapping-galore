import requests
from bs4 import BeautifulSoup

# thai_arabic = str.maketrans('๑๒๓๔๕๖๗๘๙๐', '1234567890')

def scrape_thai_law(url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    article_div = soup.find('div', class_='article_detail_div')
    
    if not article_div:
        print("The <div class='article_detail_div'> was not found on the page.")
        return
    
    paragraphs = article_div.find_all('p')
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for p in paragraphs:
            text = p.get_text()
            
            # Convert Thai numbers to Arabic numbers
            # text = text.translate(thai_arabic)
            
            file.write(text + '\n')
    
    print(f"Content has been scraped and saved to {output_file}")

if __name__ == "__main__":
    url = ''
    output_file = 'test.txt'
    
    scrape_thai_law(url, output_file)

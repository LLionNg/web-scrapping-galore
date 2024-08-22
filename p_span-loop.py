import requests
from bs4 import BeautifulSoup

thai_arabic = str.maketrans('๑๒๓๔๕๖๗๘๙๐', '1234567890')

def scrape_thai_law(url, output_file, append_mode=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    content = response.content.decode('ISO-8859-11', errors='replace')
    soup = BeautifulSoup(content, 'html.parser')
    
    article_div = soup.find('div', class_='article_detail_div')
    
    if not article_div:
        print("The <div class='article_detail_div'> was not found on the page.")
        return
    
    mode = 'a' if append_mode else 'w'
    
    with open(output_file, mode, encoding='utf-8') as file:
        for p in article_div.find_all('p'):
            text_parts = []
            
            for span in p.find_all('span'):
                text_parts.append(span.get_text())
                
                if span.find_next_sibling():
                    text_parts.append('\n')

            if not p.find_all('span'):
                text_parts.append(p.get_text())
            
            text = ''.join(text_parts)
            text = text.replace(u'\xa0', ' ')  # Replace &nbsp; with space
            text = text.translate(thai_arabic).strip()
            
            text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
            
            if text:
                file.write(text + '\n')
    
    print(f"Content has been scraped and saved to {output_file}")

if __name__ == "__main__":
    url = ''
    output_file = 'test.txt'
    
    scrape_thai_law(url, output_file, append_mode=False)

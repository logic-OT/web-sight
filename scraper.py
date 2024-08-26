import requests
from bs4 import BeautifulSoup
import re

def extract_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove common noise elements
    for element in soup(['nav', 'header', 'footer', 'aside', 'script', 'style']):
        element.decompose()

    # Find the main content area (adjust as needed for specific websites)
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|body'))

    if not main_content:
        main_content = soup.body

    important_text = []
    for elem in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = elem.get_text(strip=True)
        if text:  # Ignore empty paragraphs
            important_text.append(text)
            
    return ' '.join(important_text)


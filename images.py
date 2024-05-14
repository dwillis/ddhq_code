import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to extract image URLs from a web page
def extract_image_urls(url):
    image_urls = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for img_tag in soup.find_all('img'):
                img_url = img_tag.get('src')
                if img_url:
                    absolute_img_url = urljoin(url, img_url)
                    image_urls.append(absolute_img_url)
    except Exception as e:
        print(f"Error fetching images from {url}: {e}")
    return image_urls

# Function to download images from a list of URLs
def download_images(image_urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for img_url in image_urls:
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                filename = os.path.basename(img_url)
                with open(os.path.join(output_dir, filename), 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")

# Function to extract images from web pages given a list of URLs from a file
def extract_images_from_urls_file(urls_file, output_dir):
    with open(urls_file, 'r') as f:
        urls = f.readlines()
        urls = [url.strip() for url in urls]
    extract_images_from_urls(urls, output_dir)

# Usage
if __name__ == "__main__":
    extract_images_from_urls_file("winred_urls.csv", "fundraising_images")

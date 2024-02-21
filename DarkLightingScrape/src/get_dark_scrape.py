import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def download_image(img_url, folder_name):
    try:
        response = requests.get(img_url)
        file_name = os.path.basename(img_url)
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("Image downloaded successfully:", file_path)
    except Exception as e:
        print("Error downloading image:", e)


def get_image_content(url, directory):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    images = soup.find_all("img", class_="swiper-slide-image")
    directory_name = directory
    directory_name.mkdir(parents=True, exist_ok=True)

    for image in images:
        img_url = image['src']
        download_image(img_url, directory_name)


def get_text_content(url, directory, desired_text):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    divs = soup.find_all("div", class_="elementor-widget-container")
    found_desired_text = False

    directory_name = directory
    directory_name.mkdir(exist_ok=True)

    with open(directory_name / "pendant_info.txt", "w") as f:
        for div in divs:
            text = div.text.strip()
            if desired_text in text:
                found_desired_text = True
            elif "Enquire about this product" in text:
                found_desired_text = False

            if found_desired_text:
                f.write(text + "\n")

# New Branch
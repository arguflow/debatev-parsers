import pypandoc
from bs4 import BeautifulSoup
import os
import json
import requests
import sys


def add_card_to_db(content, link, oc_file_path):
    url = "http://localhost:8090/api/card"
    payload = {
        "content": content,
        "link": link,
        "oc_file_path": oc_file_path,
        "user_id": "3572c955-d7fb-4a9c-a073-5037fa582b35"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("POST request successful!")
    else:
        print("Request:", response.status_code, response.text)


def card_exists(dictionary, link, content):
    for value in dictionary.values():
        for item in value:
            if 'link' in item and item['link'] == link:
                return True
            if 'content' in item and item['content'] == content:
                return True
    return False


def converttoHTML(filepath):
    allHtml = {}
    try:
        output = pypandoc.convert_file(filepath, 'html')
        filepath_to_save = filepath.split(
            "NSDA-Case-Files-Copy/")[1].split(".docx")[0] + ".html"

        with open('foo.html', 'w') as fp:
            fp.write(output)
            file_name = filepath.split(".docx")[0] + ".html"

        num_of_cards = 1
        with open('foo.html') as fp:
            soup = BeautifulSoup(fp, "lxml")
            all_h4_tags = soup.find_all('h4')
            all_strong_tags = soup.find_all('strong')
            if len(all_h4_tags) > len(all_strong_tags) or len(all_h4_tags) > 5:
                all_card_tags = all_h4_tags
            else:
                all_card_tags = all_strong_tags

            for element in all_card_tags:
                try:
                    text_with_link = element.find_next("p")
                    link = ""

                    for i in range(3):
                        if "http" in text_with_link.text:
                            link = next((word for word in text_with_link.text.split(
                                " ") if "http" in word), None)
                            break
                        text_with_link = text_with_link.find_next("p")

                    if link == "":
                        # print("a card was skipped because it has no link")
                        continue

                    card_content = text_with_link.find_next("p").text

                    if len(card_content.split(" ")) >= 70:
                        add_card_to_db(card_content, link, filepath_to_save)

                except AttributeError as e:
                    print("a card was skipped because attr " + str(e))
                    pass
        return allHtml
    except Exception as e:
        print("a card was skipped because e " + str(e))
        return allHtml


def traverse_directory(directory_path):
    all_html = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".docx"):
                file_path = os.path.join(root, file)
                file_link = "file://" + file_path
                file_name = os.path.splitext(file)[0]
                print("starting: " + file_path)
                converttoHTML(file_path)


def main(index):
    # Add your desired directory paths here
    base_path = "/home/skeptrune/Downloads/NSDA-Case-Files-Copy/"

    directory_paths = ["2013OpenEv/", "2014OpenEv/", "2015OpenEv/", "2016OpenEv/",
                       "2017OpenEv/", "2018OpenEv/", "2020OpenEv/", "2021OpenEv/", "2022OpenEv/",
                       "hsld22-all-2023-05-30/hsld22/", "hspf22-all-2023-05-30/hspf22/", "hspolicy22-all-2023-05-30/hspolicy22/",
                       "ndtceda22-all-2023-05-30/ndtceda22/", "nfald22-all-2023-05-30/nfald22/"]

    if index < 0 or index >= len(directory_paths):
        print("Invalid index provided.")
        return

    selected_path = directory_paths[index]
    full_path = base_path + selected_path

    # Your main process code goes here
    print("Starting process with directory:", full_path)
    traverse_directory(full_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide an index argument.")
    else:
        index = int(sys.argv[1])
        print("Starting")
        main(index)

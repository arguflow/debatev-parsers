import pypandoc
from bs4 import BeautifulSoup
def converttoHTML(filepath, filelink, types, year):
    output = pypandoc.convert_file(filepath, 'html')

    with open('test.html', 'w') as fp:
        fp.write(output)
    num_of_cards = 1
    allHtml = {}
    with open('test.html') as fp:
        soup = BeautifulSoup(fp, "lxml")
        all_card_tags = soup.find_all('h4')
        for h4 in all_card_tags:
            try:
                abstract = h4
                citation = h4.find_next("p")
                card = h4.find_next("p").find_next("p")
                full_doc = card
                doc_word_length = len(full_doc.text.split())
                if doc_word_length >= 70:
                    allHtml["card " + str(num_of_cards)] = [{"tag": str(abstract), "cite": str(citation), "cardHtml": str(abstract) + str(citation) + str(full_doc), "filepath": filelink, "dtype": types, "year": year}]
                    num_of_cards += 1
            except AttributeError as e:
                print("a card was skipped because " + str(e))
                pass
    return allHtml


import os
import pypandoc
from bs4 import BeautifulSoup

def traverse_directory(directory_path):
    all_html = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".docx"):
                file_path = os.path.join(root, file)
                file_link = "file://" + file_path
                file_name = os.path.splitext(file)[0]
                file_year = get_year_from_filename(file_name)  # Assuming you have a function to extract the year from the filename

                cards = convert_to_card_list(file_path, file_link, "docx", file_year)
                all_html[file_name] = cards

    return all_html

def convert_to_card_list(file_path, file_link, file_type, year):
    output = pypandoc.convert_file(file_path, 'html')

    with open('temp.html', 'w') as fp:
        fp.write(output)

    num_of_cards = 1
    all_html = {}

    with open('temp.html') as fp:
        soup = BeautifulSoup(fp, "lxml")
        all_card_tags = soup.find_all('h4')
        
        for h4 in all_card_tags:
            try:
                abstract = h4
                citation = h4.find_next("p")
                card = h4.find_next("p").find_next("p")
                full_doc = card
                doc_word_length = len(full_doc.text.split())
                
                if doc_word_length >= 70:
                    card_data = {
                        "tag": str(abstract),
                        "cite": str(citation),
                        "cardHtml": str(abstract) + str(citation) + str(full_doc),
                        "filepath": file_link,
                        "dtype": file_type,
                        "year": year
                    }
                    all_html["card " + str(num_of_cards)] = [card_data]
                    num_of_cards += 1
            except AttributeError as e:
                print("A card was skipped because " + str(e))
                pass

    os.remove('temp.html')  # Remove temporary HTML file
    return all_html

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import csv
import openpyxl
import json
import time
from datetime import datetime
from random import random

start_time = time.time()
print('scraping the site')
test = []
options = []
answer = ''
image_source = []
choices = None
try:
    year_error_occurred = ''
    for year in range(1978, 2020):
        print('year', year)
        for page in range(1, 11):
            print('page number', page)
            quote_page = 'https://myschool.ng/classroom/mathematics?exam_type=jamb&exam_year='+str(year) + '&page='+str(page)
            year_error_occurred = quote_page
            r = requests.get(quote_page)
            encodedText = r.text.encode("utf-8")
            soup = BeautifulSoup(encodedText, 'html.parser')
            question = soup.find_all('div', class_='question-desc')
            for item in question:
                question_id = round(random() * 10000)
                #print(item.text.strip())
                content = item.text.rstrip().lstrip()
                question = content.strip('\n')
                next_Sibling = item.find_next_sibling('ul')
                link = item.find_next_sibling('a')
                img_container = item.find_previous_sibling('div')
                image_source = []
                if img_container is not None:
                    images = img_container.findChildren('img')
                    if images is not None:
                        for img in images:
                            image_source.append(img['src'])
                #print('link to answer', link['href'])
                if link is not None:
                    link_to_answer = link['href']
                    encodedText = requests.get(link_to_answer).text.encode("utf-8")
                    soup = BeautifulSoup(encodedText, 'html.parser')
                    h5_tag = soup.find('h5', class_='text-success')
                    #print('-', h5_tag.text.strip())
                    content = h5_tag.text.rstrip().lstrip()
                    answer = content.strip('\n')
                    choices = next_Sibling.findChildren('li')
                options = []
                if choices is not None:
                    for node in choices:
                        #print(node.text.strip())
                        content = node.text.lstrip().rstrip()
                        choice = content.strip('\n')
                        options.append(choice)
                test.append({ 'id': question_id,  'year': year, 'examtype': 'Jamb', 
                'subject': 'Mathematics','qestion': question,'image_asset': image_source, 
                'options': options, 'answer': answer, 
                    'linkToanswer':link_to_answer, 'source_url': quote_page})
        time.sleep(1)
except:
    print('error occurred while try to scrap', year_error_occurred)

print('done')

with open('data.json', 'w') as outfile:
    json.dump(test, outfile)

print('executed successfully, total execution time: ', (time.time() - start_time))
    

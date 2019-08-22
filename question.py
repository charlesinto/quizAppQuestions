from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import csv
import openpyxl
import json
import time
from datetime import datetime
from random import random

class QuestionApp:
    def __init__(self):
        self.classroom_url = 'https://myschool.ng/classroom'
        self.courses = []
        self.question = {}
        self.start_time = time.time()
        pass
    def getCourses(self):
        r = requests.get(self.classroom_url)
        encodedText = r.text.encode("utf-8")
        soup = BeautifulSoup(encodedText, 'html.parser')
        courses_contanier = soup.find_all('div', class_='media-body')
        for item in courses_contanier:
            h5_tag = item.findChildren('h5')[0]
            if h5_tag is not None:
                anchor_tag = h5_tag.findChildren('a')[0]
                if anchor_tag is not None:
                    content = anchor_tag.text.rstrip().lstrip()
                    link = anchor_tag['href']
                    course = content.strip('\n')
                    self.courses.append({'title':course, 'link': link})
        self.getQuestions(self.courses)
    def printCourses(self):
        print(self.courses)

    def getQuestions(self, courses):
        print('scraping the site')
        test = []
        options = []
        answer = ''
        image_source = []
        choices = None
        for course in courses:
            year_error_occurred = ''
            test = []
            for year in range(2019, 2020):
                print('year', year, 'title',course['title'])
                
                for page in range(1, 11):
                    try:
                        print('page number', page)
                        quote_page = course['link']+'?exam_type=jamb&exam_year='+str(year) + '&page='+str(page)
                        year_error_occurred = quote_page
                        r = requests.get(quote_page)
                        encodedText = r.text.encode("utf-8")
                        soup = BeautifulSoup(encodedText, 'html.parser')
                        question = soup.find_all('div', class_='question-desc')
                        for item in question:
                            question_id = round(random() * 10000)
                            #print(item.text.strip())
                            content = item.text.rstrip().lstrip()
                            question = content.replace('\n', ' ').replace('\r', '').replace('       ','').replace('  ', ' ')
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
                                content = None
                                if h5_tag is not None:
                                    content = h5_tag.text.rstrip().lstrip()
                                answer = content
                                choices = next_Sibling.findChildren('li')
                            options = []
                            if choices is not None:
                                for node in choices:
                                    #print(node.text.strip())
                                    content = node.text.lstrip().rstrip()
                                    choice = content.replace('\n', ' ').replace('\r', '').replace('       ','').replace('  ', ' ')
                                    options.append(choice)
                            test.append({ 'id': question_id,  'year': year, 'examtype': 'Jamb', 
                            'subject': course['title'],'qestion': question,'image_asset': image_source, 
                            'options': options, 'answer': answer, 
                                'linkToanswer':link_to_answer, 'source_url': quote_page})
                        time.sleep(1)
                    except:
                        self.convert_to_json_dump_data(self.question)
                        print('error occurred while try to scrap', year_error_occurred)
            self.question[course['title']] = test
                
        self.convert_to_json_dump_data(self.question)
    def convert_to_json_dump_data(self, questions):
        with open('data2.json', 'w') as outfile:
            json.dump(questions, outfile)
        print('executed successfully, total execution time: ', (time.time() - self.start_time))

print('initiating')
app = QuestionApp()
print('getting courses')
app.getCourses()
print('courses gotten')
#app.printCourses()
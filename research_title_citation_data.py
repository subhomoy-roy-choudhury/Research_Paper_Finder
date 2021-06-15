from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import os
import glob
from zipfile import ZipFile
from os.path import basename
import requests
import json
import urllib.parse

START_PAGE = 11
END_PAGE = 20

PATH_PAPER = os.getcwd()
FOLDERNAME = f'/Research_Paper_Title_Citation_JSON_{START_PAGE}_{END_PAGE}/'
PATH_PAPER = PATH_PAPER + FOLDERNAME

if not os.path.isdir(PATH_PAPER) :
    os.mkdir(PATH_PAPER)

files=glob.glob(PATH_PAPER + '*.json')
print(len(files))
PAGE_FLAG = START_PAGE + len(files) 

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
driver = webdriver.Chrome(options = options)

i = 1

for page_num in range(PAGE_FLAG,END_PAGE + 1) :

    print('PAGE NUMBER :- ' + str(page_num))
    url = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber="+str(page_num)
    driver.get(url)
    data = []
    time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    st_divs_all = soup.find_all('div',{"class" : "List-results-items"})
    print(len(st_divs_all))

    for st_divs in st_divs_all :

        TITLE = ''
        PROFILE_URL = ''
        DOI = ''
        ABSTRACT = ''
        PAPER_CITATION = ''
        PATENT_CITATION = ''
        FULL_TEXT_VIEWS = ''

        print("*"*20 + str(i) + "*"*20)
        

        abstract = st_divs.find('i',{"class" : "icon-caret-abstract color-xplore-blue"})
        title = st_divs.find('a').text
        url_profile = st_divs.find('a')['href']
        url_profile = "https://ieeexplore.ieee.org" + url_profile
        print(title,'****',url_profile)
        TITLE = title
        PROFILE_URL = url_profile
        time.sleep(5)

        driver.get(url_profile)
        content = driver.page_source
        soup_doi = BeautifulSoup(content, "html.parser")
        soup_doi1 = soup_doi.find('div',{"class" : "abstract-desktop-div hide-mobile"})
        st_divs = soup_doi1.find('div',{"class" : "u-pb-1 stats-document-abstract-doi"})
        
        try :
            cite = soup_doi.find('div',{"class" : "document-banner-metric-container row"})
            citation_list = cite.find_all('button',{"class" : "document-banner-metric col"})
            if citation_list == [] :
                citation_list = cite.find_all('button',{"class" : "document-banner-metric single-metric"})

            for item in citation_list :
                list_type = item.find_all('div')
                if list_type[1].text.lower() == 'paper' :
                    print('Paper :- '+list_type[0].text)
                    PAPER_CITATION = list_type[0].text
                elif list_type[1].text.lower() == 'patent' :
                    print('Patent :- '+list_type[0].text)
                    PAPER_CITATION = list_type[0].text
                elif list_type[1].text.lower() == 'fulltext views' :
                    print('Full Text Views :- '+list_type[0].text)
                    FULL_TEXT_VIEWS = list_type[0].text
        
        except Exception as e :
            print(e)
            pass
            
        if abstract is not None : 
            if st_divs is not None :
                
                try :
                    abstract = soup_doi1.find('div',{"class" : "u-mb-1"}).find('div').text
                    print(abstract)
                    ABSTRACT = abstract
                except Exception as e :
                    print(e)
                    pass

                doi = st_divs.find('a',{"target" : "_blank"}).text
                DOI = doi
                print(doi)
                
        scraper_data = {}
        scraper_data['title'] = TITLE
        scraper_data['profile_url'] = PROFILE_URL
        scraper_data['doi'] = DOI
        scraper_data['abstract'] = ABSTRACT
        scraper_data['paper_citation'] = PAPER_CITATION
        scraper_data['patent_citation'] = PATENT_CITATION
        scraper_data['full_text_views'] = FULL_TEXT_VIEWS
        data.append(scraper_data)

        if i == 25 :
            i = 0
        i += 1
        time.sleep(5)

    if data == [] :
        raise Exception('The data object is empty . Please run the Python File once again ')
        break 

    JSON_FILEPATH = PATH_PAPER + str(f'{page_num}_research_paper_scraper.json')
    with open(JSON_FILEPATH,'w') as file :
        json.dump(data,file,ensure_ascii=False, indent=1)

    print("*"*40)

driver.quit()

files=glob.glob(PATH_PAPER + '*.json')
# create a ZipFile object
zipObj = ZipFile(f'{PATH_PAPER[:-1]}.zip', 'w')
# Add multiple files to the zip
for file in files :

    zipObj.write(file , basename(file))
# close the Zip File
zipObj.close()

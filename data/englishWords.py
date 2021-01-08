import requests
import time
import pandas as pd
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

url = 'http://englishprofile.org/american-english'
path="C:\\Users\\hanna\\Downloads\\geckodriver-v0.28.0-win64"
driver = webdriver.Firefox(path)
driver.get(url)
select = Select(driver.find_element_by_id('limit'))
select.select_by_visible_text('All')
time.sleep(20) #could possibly change this to a wait ?
wordsandlevels = []
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
allwords = soup.findAll('tr')
completeWords = allwords[1:]
print(len(completeWords))
for word in completeWords :
    element = list(word)
    #extract word out of html
    wordString = str(element[1])
    splitWord = 'normal'
    splitString = wordString.split(splitWord,1)
    result = splitString[1]
    pos = result.find('<')
    newWord = result[2:pos]
    #extract label out of html
    labelString = str(element[5])
    splitChar = 'label'
    labelSplit = labelString.split(splitChar,1)
    resultLabel = labelSplit[1]
    label = resultLabel[7:9]
    wordlist = [newWord, label]
    wordsandlevels.append(wordlist)
print(wordsandlevels[5])
df = pd.DataFrame(wordsandlevels, columns = ['Word', 'Level'])
df.to_csv('wordsandlevels.csv', index=False)

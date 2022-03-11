from msilib.schema import Class
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

def browser_find_scrapeurl(url):
    entry_name=input('Lutfen aramak istediginiz entry \'i giriniz:')
    browser.get(url)
    data_enter='//*[@id="search-textbox"]'
    button='//*[@id="search-form"]/button'
    input_area=browser.find_element_by_xpath(data_enter)
    button_area=browser.find_element_by_xpath(button)
    input_area.send_keys(entry_name)
    time.sleep(1)
    button_area.click()
    time.sleep(1)
    return browser,entry_name

class DataGet():
    def __init__(self,current_url):
        self.current_url=current_url
        self.entry_array=[]
        self.entry_time_array=[]

    def getContent_allPages(self,mycontent):
    
        son_sayfa=mycontent.find('a',{'title':'son sayfa'})
        content_array=[]
        sayfa_sayisi=son_sayfa.text
        for i in range(1,int(sayfa_sayisi)+1):
            
            if i!=1:
                self.current_url=self.current_url+"?p="+str(i)
                
        
            response=requests.get(self.current_url,headers={'User-Agent':'hello'})
            print(response)
            content=BeautifulSoup(response.content,'html.parser')
            content_array.append(content)
        return content_array
            
        
    def get_entry(self,mycontent_array):
        
        for mycontent in mycontent_array:
            all_entries=mycontent.find_all('div',{'class':'content'})
            entry_times=mycontent.find_all('a',{'class':'entry-date'})

            for entries in all_entries:
                self.entry_array.append(entries.text)

            for entry_time in entry_times:
                self.entry_time_array.append(entry_time.text) 

    def word_searching(self,value,word):
        
        
        if value!=str(1):
            return self.entry_array,self.entry_array
      
        else:
            searching_array=[]
            searching_array_time=[]

            for entry in self.entry_array:
                
                find_word=entry.find(word)#Eğer kelimeyi bulamazsa return -1 atar

                if find_word!=-1:

                    index_entry=self.entry_array.index(entry)
                    searching_array.append(entry)
                    searching_array_time.append(self.entry_time_array[index_entry])

                    return searching_array,searching_array_time


    def writer_function(self,writing_entry,writing_time,word):
            
        df=pd.DataFrame({'entryler':writing_entry,'zamanlar':writing_time})
        df.to_excel(f'{word}.xlsx')


           
    
browser=webdriver.Chrome()
url='https://eksisozluk.com/'

browser,entry_name=browser_find_scrapeurl(url)

url=browser.current_url
my_page_source=browser.page_source
mycontent=BeautifulSoup(my_page_source,'html.parser')

data_class=DataGet(url)
contentArray=data_class.getContent_allPages(mycontent)
data_class.get_entry(contentArray)#content içindeki tüm entryleri bulur

value=input('Kelimeye göre entry almak için 1 tüm entryleri almak için farklı bir tuşa basın.')
word=input('Aramak istediginiz kelimeyi giriniz:')

searching_array,searching_time_array=data_class.word_searching(value,word)#Değere ve kelimeye göre entry_array içindeki arrayleri,timelerini getirir 
data_class.writer_function(searching_array,searching_time_array,entry_name)#İstenen değerleri yazdırır.
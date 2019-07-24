from crawling.crawler import CrawlingThread
from selenium import webdriver
from parameters import search_query, linkedin_username, linkedin_password



thread = CrawlingThread(1, "Thread-1")

driver = webdriver.Chrome(executable_path='../static/chromedriver')


thread.crawl(driver, linkedin_username, linkedin_password, search_query, number=10, csv_name='static/userinfo.csv')



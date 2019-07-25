# test crawler with visible chrome browser
from crawler.crawler_factory import CrawlingThread
from selenium import webdriver
from crawler.parameters import search_query, linkedin_username, linkedin_password


def test_crawler():
    thread = CrawlingThread(1, "Thread-1")
    driver = webdriver.Chrome(executable_path='../static/chromedriver')
    thread.crawl(driver, linkedin_username, linkedin_password, search_query, number=10, csv_name='static/userinfo.csv')


if __name__ == '__main__':
    test_crawler()
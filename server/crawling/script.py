from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parameters import search_query,linkedin_username,linkedin_password
from parsel import Selector
import time

import pandas as pd

exitFlag = 0

def fetch_linkedin_url(driver, query, number):
    linkedin_urls = []
    # specifies the path to the chromedriver.exe
    driver.get('https://www.google.com/')

    # locate search form by_name
    search_query = driver.find_element_by_name('q')
    # send_keys() to simulate the search text key strokes
    search_query.send_keys(query)
    # .send_keys() to simulate the return key
    search_query.send_keys(Keys.RETURN)


    # locate URL by_class_name
    urls = driver.find_elements_by_class_name('iUh30')
    linkedin_urls.extend(map(lambda x: x.text.encode('utf-8'), urls))

    while len(linkedin_urls) < number:
        driver.find_elements_by_id('pnnext')[0].click()
        urls = driver.find_elements_by_class_name('iUh30')
        linkedin_urls.extend(map(lambda x: x.text.encode('utf-8'), urls))

    return linkedin_urls

def linkedin_login(driver, username, password):
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

    # fill username
    driver.find_element_by_id('username').send_keys(username)
    # fill password
    driver.find_element_by_id('password').send_keys(password)
    # locate submit button by_xpath
    log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    # .click() to mimic button click
    log_in_button.click()

def validate_field(field):
    if field:
        field = field.strip().encode('utf-8')
    else:
        field = ''
    if len(field) == 0:
        field = ''
    return field

def parse_linkedin_user(driver,url):
    #get raw html
    driver.get(url)
    sel = Selector(text=driver.page_source)

    name = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
    level = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[1]/li[2]/*/span[@class="dist-value"]/text()').extract_first()
    job = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/h2/text()').extract_first()
    location = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()
    connection = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[2]/li[2]/span/text()').extract_first()
    company = sel.xpath('//*[@class="pv-top-card-v3--experience-list-item"][1]/span/text()').extract_first()
    college = sel.xpath('//*[@class="pv-top-card-v3--experience-list-item"][2]/span/text()').extract_first()

    res = [
        validate_field(name),
        validate_field(level),
        validate_field(job),
        validate_field(location),
        validate_field(connection),
        validate_field(company),
        validate_field(college),
        url
    ]
    return res

def crawl(driver, linkedin_username, linkedin_password, search_query,csv_name='userinfo.csv', number=10):
    urls =  fetch_linkedin_url(driver,search_query,number)
    print 'fetch urls finished ---> totoal num: ' + str(len(urls))
    linkedin_login(driver,linkedin_username,linkedin_password)
    arrays = []
    idx = 1
    for url in urls:
        time.sleep(1)
        try:
            userinfo = parse_linkedin_user(driver, url)
            arrays.append(userinfo)
            print str(idx) + ' parse success ! --->' + str(userinfo)
            idx = idx + 1
        except Exception as e:
            print 'parse userinfo failed !'
            print e
    df = pd.DataFrame(arrays,columns=['name','level','job','location','connection','company','college','url'])
    df.to_csv(csv_name,index=False,sep=',')
    print 'parse finished ! ===> totoal number: '+ str(idx)



chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver')
crawl(driver,linkedin_username,linkedin_password,search_query,number=100,csv_name='userinfo_demo.csv')
driver.quit()
# Generate crawler thread based on parameters in parameters.py
# Only will delete old data, when write new data
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import pandas as pd

from parameters import search_query, linkedin_username, linkedin_password, driver_location


class CrawlingThread(threading.Thread):
    # set basic parameters
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.exitFlag = 0
        self.search_query = search_query
        self.linkedin_username = linkedin_username
        self.linkedin_password = linkedin_password
        self.driver_location = driver_location
        self.userList = []

    # collect linkedin profile urls from www.google.com
    def __fetch_linkedin_url(self, driver, query, number) :
        linkedin_urls = []
        # specifies the path to the chromedriver.exe
        driver.get('https://www.google.com/')

        # locate search form by_name
        search_query = driver.find_element_by_name('q')
        search_query.send_keys(query)
        search_query.send_keys(Keys.RETURN)

        # locate URL by_class_name
        urls = driver.find_elements_by_class_name('iUh30')
        linkedin_urls.extend(map(lambda x: x.text.encode('utf-8'), urls))

        # keeping fetching until meet the minimum number
        while len(linkedin_urls) < number:
            print 'collect url number: ' + str(len(linkedin_urls))

            # check thread stopping flag
            if self.exitFlag:
                self.driver.quit()
                return linkedin_urls

            # go to next page
            driver.find_elements_by_id('pnnext')[0].click()
            # filter invalid url
            urls = driver.find_elements_by_class_name('iUh30')
            linkedin_urls.extend(map(lambda x: x.text.encode('utf-8'), urls))

        return linkedin_urls

    # login linkedin account
    def __linkedin_login(self, driver, username, password):
        # driver.get method() will navigate to a page given by the URL address
        driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

        # fill username and password, and do login
        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
        log_in_button.click()

    # check whether need verification
    def __check_linkedin_verify(self, driver):
        try:
            driver.find_element_by_id('input__email_verification_pin')
            return True
        except:
            return False

    # validate profile field
    def __validate_field(self, field):
        if field:
            field = field.strip().encode('utf-8')
        else:
            field = ''
        if len(field) == 0:
            field = ''
        return field

    # parse single linkedin profile page
    def __parse_linkedin_user(self, driver, url):
        # get raw html
        driver.get(url)
        sel = Selector(text=driver.page_source)

        # parse content using xpath
        name = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
        level = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[1]/li[2]/*/span[@class="dist-value"]/text()').extract_first()
        job = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/h2/text()').extract_first()
        location = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()
        connection = sel.xpath('//*[@class="ph5 pb5"]/div[2]/div[1]/ul[2]/li[2]/span/text()').extract_first()
        company = sel.xpath('//*[@class="pv-top-card-v3--experience-list-item"][1]/span/text()').extract_first()
        college = sel.xpath('//*[@class="pv-top-card-v3--experience-list-item"][2]/span/text()').extract_first()


        res = [
            self.__validate_field(name),
            self.__validate_field(level),
            self.__validate_field(job),
            self.__validate_field(location),
            self.__validate_field(connection),
            self.__validate_field(company),
            self.__validate_field(college),
            url
        ]
        return res

    # control the crawling process
    def crawl(self, driver, linkedin_username, linkedin_password, search_query, csv_name='userinfo.csv', number=10):
        # collect needed urls
        urls = self.__fetch_linkedin_url(driver, search_query, number)
        print 'fetch urls finished ---> totoal num: ' + str(len(urls))

        # login linkedin account
        self.__linkedin_login(driver, linkedin_username, linkedin_password);

        # if need to be verify, stop the process
        if self.__check_linkedin_verify(driver):
            print 'need verify by email...'
            print 'please run verify script and do verification'
            return

        # collect linkedin profile
        for url in urls:
            # check stop flag
            if self.exitFlag:
                self.driver.quit()
                df = pd.DataFrame(self.userList,
                                  columns=['name', 'level', 'job', 'location', 'connection', 'company', 'college',
                                           'url'])
                # save current data to file
                df.to_csv(csv_name, index=False, sep=',')
                return
            else:
                # to act more like human
                time.sleep(1)
                try:
                    # parsing profile
                    userinfo = self.__parse_linkedin_user(driver, url)
                    if userinfo[0]:
                        self.userList.append(userinfo)
                        print str(len(self.userList)) + ' parse success ! --->' + str(userinfo)
                    else:
                        print 'invalid user info'
                except Exception as e:
                    print 'parse userinfo failed !'
                    print e

        # save all data to file
        df = pd.DataFrame(self.userList,
                          columns=['name', 'level', 'job', 'location', 'connection', 'company', 'college', 'url'])
        df.to_csv(csv_name, index=False, sep=',')
        print 'parse finished ! ===> totoal number: ' + str(len(self.userList))

    # set flag to stop process
    def stop(self):
        self.exitFlag = 1

    def run(self):
        # create web driver without GUI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(
            "user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.driver_location)

        # start crawling process
        print "Starting " + self.name
        self.crawl(self.driver, linkedin_username, linkedin_password, search_query, number=100,
                     csv_name='static/userinfo.csv')
        print "Exiting " + self.name


    def getIdx(self):
        return len(self.userList)

    def getUserList(self):
        return self.userList

# script used to quick verify by email

from selenium import webdriver
from parameters import driver_location, linkedin_username, linkedin_password

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    "user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_location)
print 'do login...'
driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
# fill username and password, and do login
driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id('password').send_keys(password)
log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()

try:
    driver.find_element_by_id('input__email_verification_pin')
    print 'please enter verdify code:'
    verify_code = raw_input("Enter your input: ")
    driver.find_element_by_id('input__email_verification_pin').send_keys(verify_code)
    driver.find_element_by_id('email-pin-submit-button').click()
    print 'success...'
except:
    print 'do not need verify...'

driver.quit()
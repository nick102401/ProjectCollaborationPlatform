import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

"""
selenium基本操作
"""


def get_color_config():
    url = 'https://blog.csdn.net/qq_27918787/article/details/52744450'

    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)

    driver.get(url=url)
    driver.implicitly_wait(10)
    driver.maximize_window()

    # js_script = 'var q = document.documentElement.scrollTop=4500'
    # driver.execute_script(js_script)
    #
    # locator = driver.find_element_by_id('passportbox')
    # # WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(locator))
    # elementsList = locator.find_elements_by_tag_name('span')
    # for element in elementsList:
    #     if element.text == '×':
    #         element.click()
    #         break
    #
    # trList = driver.find_element_by_xpath('//*[@id="content_views"]/div[3]/table/tbody').find_elements_by_xpath('//tr')
    #
    # for i in range(len(trList)):
    #     colorText = driver.find_element_by_xpath(
    #         '//*[@id="content_views"]/div[3]/table/tbody/tr[' + str(i + 2) + ']/td[1]/p//span').text
    #     colorCode = driver.find_element_by_xpath(
    #         '//*[@id="content_views"]/div[3]/table/tbody/tr[' + str(i + 2) + ']/td[2]/p//span').text
    #     print(colorText + "=" + colorCode)

    driver.close()


if __name__ == '__main__':
    pass
    for i in range(100):
        get_color_config()
        time.sleep(5)

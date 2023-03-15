from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService


def init() -> ...:
    """
    if Selenium >= 4.6 there is no need to download webdriver and configure the executable_path
    :return:
    """
    service = ChromeService(executable_path='chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def wait_elements_by_xpath(driver, x_path: str) -> ...:
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, x_path)))


def ipinfo(driver):
    driver.get('https://ipinfo.io/')
    tryit_data_li = wait_elements_by_xpath(driver, '//div[@id="tryit-data"]/ul[@class="my-2.5 space-y-2.5 w-full"]/li')
    rst = []
    for li in tryit_data_li:
        try:
            t_li = li.find_element(By.XPATH, './descendant::span[@class="text-green-05"]').text
            if t_li:
                t_li_field = li.find_element(By.XPATH, './descendant::span[@class="text-white"]').text
                if 'ip:' == t_li_field or 'city:' == t_li_field or 'region:' == t_li_field or 'country:' == t_li_field or "org:" == t_li_field:
                    rst.append(t_li)
        except NoSuchElementException:
            pass
    print('ip: {0} city: {1} region: {2} country: {3} org: {4}'.format(*rst))


if __name__ == '__main__':
    __TIMES__ = 10
    driver = init()
    with ThreadPoolExecutor(max_workers=__TIMES__) as executor:
        for _ in range(0, __TIMES__):
            executor.submit(ipinfo, driver)
    driver.quit()

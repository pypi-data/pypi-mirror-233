def load_cookies(driver, cookie_file):
    driver.delete_all_cookies()
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
        cookieList = cookies['cookies']
        for cookie in cookieList:
            cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)
        time.sleep(10)
    return driver


driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=webdriver.ChromeOptions())
driver.get('https://business.facebook.com')
time.sleep(10)
driver = load_cookies(driver, 'cookies.json')
driver.get('https://business.facebook.com/')
time.sleep(5)

# driver.find_element_by_xpath('//*[@id="mount_0_0_Vy"]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[4]/div/div/div/div/div/div/div[1]/div[2]/div').click()
# time.sleep(10)
# driver.quit()


def login_by_cookie(url, path):
    """
    url: url of connection
    path: path to cookie
    """
    try:
        driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=webdriver.ChromeOptions())
        driver.get(url)
        driver = load_cookies(driver, path)
    except Exception as e:
        print(e)
        return None

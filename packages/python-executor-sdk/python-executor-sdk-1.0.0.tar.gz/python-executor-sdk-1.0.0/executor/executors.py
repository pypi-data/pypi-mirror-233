class ExecutorsEnum:
    BASIC = 1
    SPLASH = 2
    SELENIUM_REMOTE = 3
    SELENIUM_WEBDRIVER = 4

class ExecutorHost:
    CHROME_REMOTE = 'http://127.0.0.1:4444/wd/hub'
    CHROME_VNC = 'http://localhost:7900/?autoconnect=1&resize=scale&password=secret'
    SPLASH_REMOTE = ''
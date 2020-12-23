from selenium import webdriver
from selenium.webdriver import ChromeOptions

CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'


class Chromium(object):
    """Chrome驱动"""

    ops = ChromeOptions()
    ops.set_capability('pageLoadStrategy', 'eager')
    # 浏览器不提供可视化页面
    ops.add_argument('--headless')
    ops.add_argument('--no-sandbox')
    ops.add_argument('--disable-dev-shm-usage')
    # 禁用GPU加速
    ops.add_argument('--disable-gpu')
    # 设置浏览器分辨率（窗口大小）
    ops.add_argument('window-size=1280x1000')
    # # 禁用扩展插件并实现窗口最大化
    # ops.add_argument('--ignore-certificate-errors')
    # 最大化运行（全屏窗口）,不设置，取元素会报错
    ops.add_argument('–-start-maximized')
    # 隐藏滚动条, 应对一些特殊页面
    ops.add_argument('–-hide-scrollbars')
    # 禁用浏览器正在被自动化程序控制的提示
    ops.add_argument('–-disable-infobars')
    # # 无痕模式
    # ops.add_argument('–-incognito')
    ops.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/83.0.4103.61 Safari/537.36"')
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=ops)

    @classmethod
    def init_driver(cls):
        """
        初始化驱动
        :return:
        """
        cls.driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=cls.ops)

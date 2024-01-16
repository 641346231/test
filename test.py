from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import sys
from datetime import datetime

# 检查日期是否符合规范
def is_valid_date(date_str):
    """
    TODO  检查货币类型加进去
    """
    try:
        # 尝试使用datetime.strptime解析日期字符串
        datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

date = sys.argv[1]
arg = sys.argv[2]

if is_valid_date(date):
    # 创建一个WebDriver实例
    service = Service(executable_path="D:/tools/chromedriver.exe")

    # 声明浏览器的对象
    options = webdriver.ChromeOptions()
    options.ignore_local_proxy_environment_variables()
    # 禁止打印日志
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 去除浏览器selenium监控
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless')  # 浏览器不提供可视化页面
    # 禁用GPU加速
    options.add_argument('--disable-gpu')
    # 忽略证书错误
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    # selenium 防止window.navigator.webdriver对象检测的方法
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

    # 打开网页
    driver.get("https://www.boc.cn/sourcedb/whpj/")

    currency_dict = {
        '美元': 'USD',
        '欧元': 'EUR',
        '英镑': 'GBP',
        '日元': 'JPY',
        '人民币': 'CNY',
        '加拿大元': 'CAD',
        '澳大利亚元': 'AUD',
        # 添加更多货币...
    }

    # 反转键和值
    flipped_dict = {v: k for k, v in currency_dict.items()}
    arg2 = flipped_dict[arg]
    try:
        # 起始日期
        driver.find_element(By.XPATH,"//input[@id='erectDate']").send_keys(date)
        # 结束日期
        driver.find_element(By.XPATH,"//input[@id='nothing']").send_keys(date)
        # 货币类型选择
        driver.find_element(By.XPATH,"//select[@id='pjname']").send_keys(arg2)
        time.sleep(1)
        # 点击搜索
        driver.find_element(By.XPATH,"//input[@onclick='executeSearch()']").click()
        time.sleep(1)

    except TimeoutException as e:
        print(f"Timeout: {e}")

    except NoSuchElementException as e:
        print(f"NoSuchElementException: {e}")


    tr = driver.find_element(By.XPATH,"//div[@class='BOC_main publish']//table//tr[2]")
    print(tr.text.split(" ")[3])
    # 停一下看看结果
    time.sleep(2)
    driver.quit()

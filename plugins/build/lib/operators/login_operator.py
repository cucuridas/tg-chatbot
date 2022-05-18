from selenium import webdriver
from airflow.models.baseoperator import BaseOperator

class LoginOperator(BaseOperator):
    options = webdriver.ChromeOptions()
    
    def __init__(self, task_id, login_id='sy.ha', login_pw='snow3063$', url='https://office.hiworks.com/time-gate.com/home#loginUrl=common/office_main', **kwargs) -> None:
        super().__init__(**kwargs)
        self.login_id = login_id
        self.login_pw = login_pw
        self.url = url
    
    def execute(self):
        self.options.add_argument('headless')
        self.options.add_argument('no-sandbox')
        self.options.add_argument('disable-gpu')
        self.options.add_argument("lang=ko_KR")
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=LoginOperator.options)
        driver.get(self.url)
        login_id_xpath = driver.find_element_by_xpath('/html/body/div/form/div/div/div/section/input[1]')
        login_pw_xpath = driver.find_element_by_xpath('/html/body/div/form/div/div/div/section/input[2]')
        login_id_xpath.send_keys(self.login_id, self)
        login_pw_xpath.send_keys(self.login_pw, self)
        return
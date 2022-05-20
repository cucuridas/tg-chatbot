from contextvars import Context
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from airflow.models.baseoperator import BaseOperator

class LoginOperator(BaseOperator):
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--headless') # add_argument : GUI를 지원하지 않는 리눅스 환경에서 실행하기 위함
    options.add_argument('--no-sandbox')
    options.add_argument("--single-process")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.binary_location = r'/opt/airflow/plugins/operators/chromedriver' # 바이너리 파일 인식을 위한 정보
    
    def __init__(self, login_id='sy.ha', login_pw='snow30634!', url='https://office.hiworks.com/time-gate.com/home#loginUrl=common/office_main', **kwargs) -> None:
        super().__init__(**kwargs)
        self.login_id = login_id
        self.login_pw = login_pw
        self.url = url
    
    def execute(self, context: Context):
        # self.options.add_argument('headless')
        # self.options.add_argument('no-sandbox')
        # self.options.add_argument('disable-gpu')
        # self.options.add_argument("lang=ko_KR")
        driver = webdriver.Chrome(executable_path='/opt/airflow/plugins/operators/chromedriver', options=self.options)
        try:
            driver.implicitly_wait(5)
            driver.get(self.url)
            login_id_xpath = driver.find_element_by_xpath('/html/body/div/form/div/div/div/section/input[1]')
            login_pw_xpath = driver.find_element_by_xpath('/html/body/div/form/div/div/div/section/input[2]')
            login_id_xpath.send_keys(self.login_id)
            login_pw_xpath.send_keys(self.login_pw)
            driver.find_element_by_xpath('/html/body/div/form/div/div/div/section/p[2]/label/input').click()
            print("login succeed!!")
        except Exception as e:
            print(e)
        
        driver.quit()
        return
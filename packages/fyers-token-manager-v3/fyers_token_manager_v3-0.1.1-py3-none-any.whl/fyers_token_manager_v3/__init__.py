import os
import pathlib
import pyotp

from datetime import datetime
from urllib.parse import parse_qs, urlparse

from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

response_type = "code"
state = "sample_state"
grant_type = "authorization_code"
auth_code_key = "auth_code"
sleep_time = 3600


class FyersTokenManager:
    def __init__(self, config, executable_path):
        self.username = config["username"]
        self.totp_key = config["totp_key"]
        self.pin = config["pin"]
        self.client_id = config["client_id"]
        self.secret_key = config["secret_key"]
        self.redirect_uri = config["redirect_uri"]

        self.executable_path = executable_path

        self.session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type=response_type,
        )

        self.__data_path = None
        self.__logs_path = None
        self.__file_name = None

        self.http_access_token = None
        self.ws_access_token = None

        self.__set_access_token_file_name()
        self.__initialize()

    def get_http_client(self) -> fyersModel.FyersModel:
        return fyersModel.FyersModel(
            client_id=self.client_id,
            token=self.http_access_token,
            log_path=str(self.__logs_path),
        )

    def get_ws_client(self, on_connect, on_message) -> data_ws.FyersDataSocket:
        fyers = data_ws.FyersDataSocket(
            access_token=self.ws_access_token,
            log_path=str(self.__logs_path),
            litemode=False,
            write_to_file=False,
            reconnect=True,
            on_connect=lambda: on_connect(fyers),
            on_error=lambda error: print("error", error),
            on_message=on_message,
        )

        return fyers

    def __set_access_token_file_name(self):
        home_directory = os.path.expanduser("~")

        self.__data_path = pathlib.Path(
            f"{home_directory}/fyers_token_manager/data/{self.username}"
        )

        self.__logs_path = pathlib.Path(f"{home_directory}/fyers_token_manager/logs")

        if not self.__data_path.exists():
            self.__data_path.mkdir(parents=True, exist_ok=True)

        if not self.__logs_path.exists():
            self.__logs_path.mkdir()

        self.__file_name = os.path.join(
            self.__data_path, datetime.now().strftime("%Y-%m-%d")
        )

    def __set_initial_values(self, token):
        self.http_access_token = token
        self.ws_access_token = f"{self.client_id}:{self.http_access_token}"

    def __initialize(self):
        try:
            token = self.__read_file()
            self.__set_initial_values(token)
        except FileNotFoundError:
            token = self.__setup()
            self.__set_initial_values(token)

    def __read_file(self):
        with open(f"{self.__file_name}", "r") as f:
            token = f.read()

        return token

    def __write_file(self, token):
        with open(f"{self.__file_name}", "w") as f:
            f.write(token)

    def __get_token(self):
        try:
            service = Service(executable_path=self.executable_path)
            options = Options()
            driver = webdriver.Chrome(service=service, options=options)

            get_auth_code_url = self.session.generate_authcode()

            driver.get(get_auth_code_url)

            login_by_username_input_selector = '//*[@id="fy_client_id"]'
            login_by_username_submit_selector = '//*[@id="clientIdSubmit"]'

            login_confirm_otp_form_selector = '//*[@id="confirmOtpForm"]'
            login_verify_pin_form_selector = '//*[@id="verifyPinForm"]'

            login_otp_first_selector = (
                "/html/body/section[6]/div[3]/div[3]/form/div[3]/input[1]"
            )

            login_otp_submit_selector = '//*[@id="confirmOtpSubmit"]'

            pin_1_selector = "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[1]"
            pin_2_selector = "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[2]"
            pin_3_selector = "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[3]"
            pin_4_selector = "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[4]"

            login_pin_submit_selector = '//*[@id="verifyPinSubmit"]'

            login_client_id = '//*[@id="login_client_id"]'

            driver.find_element(By.XPATH, login_client_id).click()

            driver.find_element(By.XPATH, login_by_username_input_selector).send_keys(
                self.username
            )

            driver.find_element(By.XPATH, login_by_username_submit_selector).click()

            WebDriverWait(driver, sleep_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, login_confirm_otp_form_selector)
                )
            )

            driver.find_element(By.XPATH, login_otp_first_selector).send_keys(
                pyotp.TOTP(self.totp_key).now()
            )

            driver.find_element(By.XPATH, login_otp_submit_selector).click()

            WebDriverWait(driver, sleep_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, login_verify_pin_form_selector)
                )
            )

            driver.find_element(By.XPATH, pin_1_selector).send_keys(self.pin[0])
            driver.find_element(By.XPATH, pin_2_selector).send_keys(self.pin[1])
            driver.find_element(By.XPATH, pin_3_selector).send_keys(self.pin[2])
            driver.find_element(By.XPATH, pin_4_selector).send_keys(self.pin[3])

            driver.find_element(By.XPATH, login_pin_submit_selector).click()

            WebDriverWait(driver, sleep_time).until(EC.url_contains(auth_code_key))

            parsed = urlparse(driver.current_url)

            auth_code = parse_qs(parsed.query)[auth_code_key][0]

            self.session.grant_type = grant_type

            self.session.set_token(auth_code)

            auth_token = self.session.generate_token()

            return auth_token["access_token"]
        except Exception as e:
            print(e)
        finally:
            driver.quit()

    def __setup(self):
        token = self.__get_token()
        self.__write_file(token)

        return token

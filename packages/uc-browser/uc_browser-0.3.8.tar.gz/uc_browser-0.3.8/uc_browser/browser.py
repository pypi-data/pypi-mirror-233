from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.select import Select

from time import sleep

import os
from random import choice, uniform

from .infra.undetected_webdriver import get_webdriver


class BrowserV2:
    user_agents: list = []

    @classmethod
    def get_agent(cls):
        if len(BrowserV2.user_agents) > 0:
            return choice(BrowserV2.user_agents)
        exit(1)

    @classmethod
    def delay(cls, start=3, end=6) -> None:
        Utils.time_to_sleep(start=start, end=end)

    def __init__(
            self,
            active_sleep: bool = False,
            profile_path: str = None,
            rotative_agent: bool = False,
            version_main: int = None,
            use_profile: bool = False,
            use_headless: bool = False,
            download_path: str = None,
            proxy: dict = None
    ) -> None:
        # sourcery skip: merge-duplicate-blocks, reintroduce-else, remove-redundant-if, split-or-ifs, swap-if-else-branches

        self.__version_main = version_main
        self.__active_sleep = active_sleep
        self.__rotative_agent = rotative_agent
        self.__use_profile = use_profile
        self.__use_headless = use_headless
        self.__download_path = download_path
        self.__proxy = proxy

        if profile_path is not None and not use_profile:
            raise Exception("To use profile_path, enable the use_profile option. (Eg. use_profile = True)")

        self.driver = get_webdriver(use_profile=self.__use_profile, profile_path=profile_path,
                                    download_path=self.__download_path, use_headless=self.__use_headless,
                                    version_main=self.__version_main, proxy=self.__proxy)

    def navigate(self, url: str) -> None:
        if self.__active_sleep:
            Utils.time_to_sleep()
        if self.__rotative_agent:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.get_agent()})
        self.driver.get(url)

    def close_driver(self) -> None:
        self.driver.close()

    def click(self, xpath: str):
        return self.driver.find_element(By.XPATH, xpath).click()

    def clear(self, xpath):
        self.driver.find_element(By.XPATH, xpath).clear()

    def wait_to_click(self, xpath, time=10):
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def wait_frame_switch_to(self, xpath, time=10):
        WebDriverWait(self.driver, time).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))

    def wait_element(self, xpath, time=10):
        try:
            WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return
        except Exception:
            return False

    def query_selector(self, query):
        return self.driver.execute_script(f'return {query}')

    def switch_to_frame_default(self):
        self.driver.switch_to.default_content()

    def switch_to_frame(self, frame):
        self.driver.switch_to.frame(frame)

    def screenshot(self, filename):
        return self.driver.save_screenshot(filename)

    def get_href(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).get_attribute('href')

    def get_attribute(self, xpath, attribute):
        return self.driver.find_element(By.XPATH, xpath).get_attribute(attribute)

    def select_by_option(self, xpath, option, by_text=True):
        select = Select(self.driver.find_element(By.XPATH, xpath))
        if by_text:
            select.select_by_visible_text(option)
        else:
            select.select_by_value(option)

    def input(self, xpath, send):
        self.driver.find_element(By.XPATH, xpath).send_keys(send)

    def input_like_a_human(self, xpath, send):
        element = self.driver.find_element(By.XPATH, xpath)
        for character in send:
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.click()
            actions.send_keys(character)
            actions.perform()
            sleep(uniform(0.01, 0.1))

    def get_text(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).text

    def get_elements(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    def get_cookies(self):
        selenium_cookies = self.driver.get_cookies()
        return {cookie['name']: cookie['value'] for cookie in selenium_cookies}

    def element_is_present(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except Exception:
            return False

    def waiting_ready_state(self):
        while self.driver.execute_script('return document.readyState') != 'complete':
            sleep(0.1)

    def wait_new_tab(self, time=10, number_tabs=2):
        WebDriverWait(self.driver, time).until(EC.number_of_windows_to_be(number_tabs))

    def wait_tab_with_title(self, title, time=10):
        WebDriverWait(self.driver, time).until(EC.title_contains(title))

    def wait_tab_with_url(self, url, time=10):
        WebDriverWait(self.driver, time).until(EC.url_contains(url))

    def change_recent_tab(self, original_tab):
        for window_handle in self.driver.window_handles:
            if window_handle != original_tab:
                self.driver.switch_to.window(window_handle)
                break

    def click_reCaptcha(
            self,
            iframe_selector="iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']",
            anchor='//*[@id="recaptcha-anchor"]',
            time=10):
        WebDriverWait(self.driver, time).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, iframe_selector)))
        WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable((By.XPATH, anchor))).click()

    def scroll_to_element(self, xpath, offset=100):
        element = self.driver.find_element(By.XPATH, xpath)
        scroll_origin = ScrollOrigin.from_element(element)
        ActionChains(self.driver) \
            .scroll_from_origin(scroll_origin, 0, offset) \
            .perform()


class ChecksBypass(BrowserV2):
    def __init__(self, profile_path=None, rotative_agent=None, active_sleep=False):
        self.__profile_path = profile_path
        self.__active_sleep = active_sleep
        self.__rotative_agent = rotative_agent

        super().__init__(
            active_sleep=self.__active_sleep,
            profile_path=self.__profile_path,
            rotative_agent=self.__rotative_agent)

        self.__nowsecure_url = 'https://nowsecure.nl'
        self.__sannysoft = 'https://bot.sannysoft.com/'
        self.__httpbin_headers = 'http://httpbin.org/headers'
        self.__httpbin_ip = 'http://httpbin.org/ip'
        self.__amiunique = 'https://amiunique.org/fp'
        self.__ja3er = 'https://ja3er.com/'
        self.__antoinevastel = 'http://arh.antoinevastel.com/bots/areyouheadless'
        self.__creepjs = 'https://abrahamjuliot.github.io/creepjs/'
        self.__screen = 'https://abrahamjuliot.github.io/creepjs/tests/screen.html'
        self.__scrapfly = 'https://tools.scrapfly.io/api/fp/ja3?extended=1'

    def nowsecure(self):
        """
            Checks if your browser bypass the cloudfront protection
        """
        self.navigate(self.__nowsecure_url)

    def sannysoft(self):
        """
            Antibot check
        """
        self.navigate(self.__sannysoft)

    def httpbin_headers(self):
        """
            Checks request headers
        """
        self.navigate(self.__httpbin_headers)

    def httpbin_ip(self):
        """
            Checks ip address
        """
        self.navigate(self.__httpbin_ip)

    def amiunique(self):
        """
            My browser fingerprint
        """
        self.navigate(self.__amiunique)

    def ja3er(self):
        """
            Checks JA3 SSL Fingerprint
        """
        self.navigate(self.__ja3er)

    def antoinevastel(self):
        """
            Checks with you browser is headless
        """
        self.navigate(self.__antoinevastel)

    def creepjs(self):
        """
            The purpose of this project is to shed light on weaknesses and privacy leaks among modern anti-fingerprinting
            extensions and browsers.

            1. Detect and ignore API tampering (API lies)
            2. Fingerprint lie types
            3. Fingerprint extension code
            4. Fingerprint browser privacy settings
            5. Employ large-scale validation, but allow possible inconsistencies
            6. Feature detect and fingerprint new APIs that reveal high entropy
            7. Rely only on APIs that are the most difficult to spoof when generating a pure fingerprint
        """
        self.navigate(self.__creepjs)

    def screen(self):
        """
            Monitor fingerprint
        """
        self.navigate(self.__screen)

    def scrapfly(self):
        """
            Tools create by Scrapfly with propose of retuurn information about cipher suite (TLS)
        """
        self.navigate(self.__scrapfly)


class Utils:
    @staticmethod
    def time_to_sleep(start=2, end=10):
        from time import sleep
        from random import randint
        sleep(randint(start, end))

    @staticmethod
    def get_agent_users():
        agents = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
            'Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 '
            'Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 '
            'Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 '
            'Safari/537.36 '
        )
        return agents

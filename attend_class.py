# -*- coding: utf-8 -*-
from loguru import logger
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from dotenv import load_dotenv
import time
import sys
import os


class Take_attendance:
    def __init__(self, cls: str, pin=None):
        self.pin = pin
        self.cls = self.check_class(cls)
        self.bb_username, self.bb_password, browser = self.read_env()
        # * Choose: webdriver.Safari(), webdriver.Chrome(), webdriver.Firefox()
        self.driver = webdriver.Safari()
        self.blackboard_url = "https://www.ole.bris.ac.uk"
        logger.debug(f"CLASS: {self.cls}, PIN: {self.pin}")

    def check_class(self, cl: str):
        classes = ["ca", "ifp"]
        if cl in classes:
            return cl
        else:
            raise ValueError(f"Not a valid class. Choose: {','.join(classes)}")

    def read_env(self):
        load_dotenv(verbose=True)
        BLACKBOARD_USERNAME = os.getenv("BLACKBOARD_USERNAME")
        BLACKBOARD_PASSWORD = os.getenv("BLACKBOARD_PASSWORD")
        return BLACKBOARD_USERNAME, BLACKBOARD_PASSWORD

    def login_blackboard(self):
        logger.info("Signing into blackboard...")
        blackboard_login_url = "https://sso.bris.ac.uk/sso/login?service=https%3A%2F%2Fwww.ole.bris.ac.uk%2Fwebapps%2Fbb-auth-provider-cas-bb_bb60%2Fexecute%2FcasLogin%3Fcmd%3Dlogin%26authProviderId%3D_122_1%26redirectUrl%3Dhttps%253A%252F%252Fwww.ole.bris.ac.uk%26globalLogoutEnabled%3Dtrue"
        self.driver.get(blackboard_login_url)
        time.sleep(2)
        login_info = {"username": self.bb_username, "password": self.bb_password}
        for key, value in login_info.items():
            self.driver.find_element_by_id(key).send_keys(value)
        self.driver.find_element_by_id("submit").click()

    def open_attendence_page(self):
        logger.info(f"Opening attendance page for {self.cls}...")
        if self.cls == "ca":
            attendance_uri = "webapps/blackboard/execute/blti/launchPlacement?blti_placement_id=_220_1&content_id=_4919923_1&course_id=_240775_1"
        else:
            attendance_uri = "webapps/blackboard/execute/blti/launchPlacement?blti_placement_id=_220_1&content_id=_4919929_1&course_id=_240776_1"
        url = f"{self.blackboard_url}/{attendance_uri}"
        self.driver.get(url)

    def take_attendance(self):
        try:
            logger.info("Logging attendance...")
            if self.pin:
                self.driver.find_element_by_id("check_in_pin").send_keys(self.pin)
            self.driver.find_element_by_id("student_check_in").click()
        except Exception as e:
            logger.error(
                "Attendance either not available or you have already checked in."
            )
            pass
        finally:
            logger.info("Program run complete.")

    def attend_class(self):
        self.login_blackboard()
        time.sleep(5)
        self.open_attendence_page()
        time.sleep(6)
        self.take_attendance()
        self.driver.quit()


if __name__ == "__main__":
    if len(sys.argv) > 3:
        logger.error("MORE THAN 2 ARGS GIVEN")
    else:
        if len(sys.argv) == 3:
            ta = Take_attendance(sys.argv[1], sys.argv[2])
        else:
            ta = Take_attendance(sys.argv[1])
        ta.attend_class()

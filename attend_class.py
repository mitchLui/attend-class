# -*- coding: utf-8 -*-
from loguru import logger
from selenium import webdriver
from dotenv import load_dotenv
import platform
import json
import time
import sys
import os


class Take_attendance:
    def __init__(self, cls: str, pin=None) -> None:
        self.pin = pin
        self.cls = self.check_class(cls)
        self.bb_username, self.bb_password = self.read_env()
        if platform.system() == "Darwin":
            self.driver = webdriver.Safari()
        elif platform.system() == "Windows":
            self.driver = webdriver.Edge()
        else:
            self.driver = webdriver.Firefox()
        self.config = self.load_config()
        logger.info(f"CLASS: {self.cls}, PIN: {self.pin}")

    def load_config(self, filename="config.json") -> dict:
        if os.path.isfile(filename):
            with open(filename) as f:
                data = json.load(f)
            logger.info("Config loaded")
            return data
        else:
            raise FileExistsError("File does not exist.")

    def check_class(self, cl: str) -> str:
        """Checks if the given class is available

        Args:
            cl (str): class string

        Raises:
            ValueError: if a class is unavailable

        Returns:
            str: the class itself
        """
        classes = ["ca", "ifp"]
        if cl in classes:
            return cl
        else:
            raise ValueError(f"Not a valid class. Choose: {','.join(classes)}")

    def read_env(self) -> tuple:
        """Reads .env file and returns username and password

        Returns:
            tuple: Blackboard username and password
        """
        load_dotenv(verbose=True)
        BLACKBOARD_USERNAME = os.getenv("BLACKBOARD_USERNAME")
        BLACKBOARD_PASSWORD = os.getenv("BLACKBOARD_PASSWORD")
        return BLACKBOARD_USERNAME, BLACKBOARD_PASSWORD

    def login_blackboard(self) -> None:
        """Logs into blackboard"""
        logger.info("Signing into blackboard...")
        blackboard_login_url = self.config["login"]
        self.driver.get(blackboard_login_url)
        time.sleep(2)
        login_info = {"username": self.bb_username, "password": self.bb_password}
        for key, value in login_info.items():
            self.driver.find_element_by_id(key).send_keys(value)
        self.driver.find_element_by_id("submit").click()

    def open_attendence_page(self) -> None:
        """Opens attendance page"""
        logger.info(f"Opening attendance page for {self.cls}...")
        url = f"{self.config['url']}/{self.config['classes'][self.cls]}"
        self.driver.get(url)

    def take_attendance(self) -> None:
        """Enters information and check into classes"""
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

    def attend_class(self) -> None:
        """Main function"""
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

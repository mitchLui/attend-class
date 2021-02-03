# -*- coding: utf-8 -*-
from loguru import logger
from dotenv import load_dotenv
from traceback import format_exc
from time import sleep
import pyppeteer
import argparse
import asyncio
import json
import os


class Attend_class:
    def __init__(self) -> None:
        self.config = self.load_config()

    def load_config(self, filename="config.json") -> dict:
        if os.path.isfile(filename):
            with open(filename) as f:
                data = json.load(f)
            logger.info("Config loaded")
            return data
        else:
            raise FileExistsError("File does not exist.")

    def check_unit(self, unit: str) -> str:
        """Checks if the given unit is available

        Args:
            unit (str): unit string

        Raises:
            ValueError: if a unit is unavailable

        Returns:
            str: the unit itself
        """
        units = list(self.config["units"].keys())
        if unit in units:
            return unit
        else:
            raise ValueError(f"Not a valid class. Choose: {','.join(units)}")

    def read_env(self) -> tuple:
        """Reads .env file and returns username and password

        Returns:
            tuple: Blackboard username and password
        """
        load_dotenv(verbose=True)
        BLACKBOARD_USERNAME = os.getenv("BLACKBOARD_USERNAME")
        BLACKBOARD_PASSWORD = os.getenv("BLACKBOARD_PASSWORD")
        return BLACKBOARD_USERNAME, BLACKBOARD_PASSWORD

    async def login_blackboard(
        self, page: pyppeteer.page.Page, username: str, password: str
    ) -> None:
        """Logs into blackboard"""
        logger.info("Signing into blackboard...")
        blackboard_login_url = self.config["login"]
        await page.goto(blackboard_login_url)
        login_info = {"#username": username, "#password": password}
        for key, value in login_info.items():
            await page.click(key)
            await page.keyboard.type(value)
        await page.click("#submit")

    async def open_attendence_page(self, page: pyppeteer.page.Page, unit: str) -> None:
        """Opens attendance page"""
        logger.info(f"Opening attendance page for {unit}...")
        url = f"{self.config['url']}/{self.config['units'][unit]}"
        await page.goto(url)

    async def take_attendance(self, page: pyppeteer.page.Page, pin: str) -> None:
        """Enters information and check into classes"""
        try:
            logger.info("Logging attendance...")
            if pin:
                await page.evaluate(
                    f"()=>{{docuemnt.getElementById('check_in_pin').click()}}"
                )
                await page.keyboard.type(pin)
            await page.evaluate(
                f"()=>{{docuemnt.getElementById('student_check_in').click()}}"
            )
        except Exception as e:
            logger.error(
                "Attendance either not available or you have already checked in."
            )
            pass
        finally:
            logger.info("Program run complete.")

    async def attend_class(self, unit: str, pin: str = None, headless: bool = False) -> None:
        """Main function"""
        browser = await pyppeteer.launch(headless = headless)
        try:
            page = await browser.newPage()
            username, password = self.read_env()
            unit = self.check_unit(unit)
            logger.info(f"UNIT: {unit}, PIN: {pin}")
            await self.login_blackboard(page, username, password)
            await page.waitForNavigation({"waitUntil": "networkidle0"})
            await self.open_attendence_page(page, unit)
            await page.waitForNavigation({"waitUntil": "networkidle0"})
            sleep(5)
            await self.take_attendance(page, pin)
        except Exception:
            logger.error(format_exc())
        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--unit", action="store", default="coms10015")
    parser.add_argument("--pin", action="store", type=str, default=None)
    parser.add_argument("--headless", action="store_true")
    argv = parser.parse_args()
    ac = Attend_class()
    asyncio.get_event_loop().run_until_complete(ac.attend_class(argv.unit, argv.pin, argv.headless))

if __name__ == "__main__":
    main()

import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twilio.rest import Client
from config.scraper_config import AUTH_TOKEN, ACCOUNT_SID, FROM_NUMBER, TO_NUMBER

options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

today = datetime.datetime.now()

while True:
    for i in range(0, 14):
        date = (today + datetime.timedelta(i)).strftime("%Y-%m-%d")
        url = "https://newtownparkpharmacy.simplybook.it/v2/#book/category/1/service/2/count/1/provider/any/date/" \
              + date

        browser.get(url)
        time.sleep(10)
        container = browser.find_element(By.ID, "sb_timeview_container").text

        if "No more slots available today" not in container:
            account_sid = ACCOUNT_SID
            auth_token = AUTH_TOKEN
            print("message sent: ", account_sid, auth_token)
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_=FROM_NUMBER,
                body='Appointment available: ' + url,
                to=TO_NUMBER
            )

            quit()


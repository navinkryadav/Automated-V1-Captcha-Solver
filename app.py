import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from pytesseract import pytesseract
import re
from selenium.webdriver.chrome.service import Service

s = Service('driver\\msedgedriver.exe')
options = webdriver.EdgeOptions()
options.add_argument("--disable-notifications")
driver = webdriver.Edge(options=options, service=s)


def show_otp(aadhaar_no):
    driver.implicitly_wait(10)
    print("Searching OTP......................", end="")
    driver.get('http://icdsonline.bih.nic.in/AanganLabharthi/AanganPublic/GetToken.aspx')
    driver.find_element(By.ID, 'ctl00_MainContent_txtAadhar').send_keys(aadhaar_no)
    driver.find_element(By.CLASS_NAME, 'Captcha-control').screenshot('screenshots//captcha.png')
    img = Image.open('screenshots//captcha.png')
    pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    text = pytesseract.image_to_string(img)
    captcha_ans = "".join(re.split("[^a-zA-Z0-9]*", text))
    driver.find_element(By.ID, 'ctl00_MainContent_txtCaptha').send_keys(captcha_ans.upper())
    time.sleep(4)
    driver.find_element(By.NAME, 'ctl00$MainContent$btnLogin').click()
    driver.implicitly_wait(5)
    try:
        driver.switch_to.alert.accept()

    except:
        try:
            while driver.find_element(By.ID, 'ctl00_MainContent_Label1').is_displayed():
                driver.find_element(By.ID, 'ctl00_MainContent_txtCaptha').clear()
                driver.find_element(By.CLASS_NAME, 'Captcha-control').screenshot('screenshots//captcha.png')
                img = Image.open('screenshots//captcha.png')
                pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
                text = pytesseract.image_to_string(img)
                captcha_ans = "".join(re.split("[^a-zA-Z0-9]*", text))
                driver.find_element(By.ID, 'ctl00_MainContent_txtCaptha').send_keys(captcha_ans.upper())
                time.sleep(4)
                driver.find_element(By.NAME, 'ctl00$MainContent$btnLogin').click()
                driver.implicitly_wait(5)
                try:
                    driver.switch_to.alert.accept()
                except:
                    pass
        except:
            pass


if __name__ == "__main__":
    with open('data/Std_Data.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        flag = True
        while flag:
            aadhaar = input("\nEnter last few digits of aadhaar:\t")
            csv_file.seek(0, 0)
            for line in csv_reader:
                if str(line['Aadhaar'][-len(aadhaar):]).upper() == aadhaar:
                    print(line.values())
                    show_otp(line['Aadhaar'])
                    break
            else:
                print('Data not found')
            # temp = input('To continue press 1 or to exit press any key\n')
            # if temp != '1':
            #     flag = False

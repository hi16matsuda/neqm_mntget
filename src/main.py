import os
import sys
import time
import io
import discord
import datetime
from urllib import request
from PIL import Image
from natsort import natsorted
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")
options.add_argument('--lang=ja')
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
mobile_emulation = { "deviceName": "Pixel 5" }
options.add_experimental_option("mobileEmulation", mobile_emulation)
driver_path = '.\\chromedriver.exe'
chrome_service = fs.Service(executable_path=driver_path) 
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.implicitly_wait(60)
driver.maximize_window()
wait = WebDriverWait(driver, 1000)

TOKEN = os.environ['DISTOKEN']

client = discord.Client(intents=discord.Intents.all())
continueFlag = True

@client.event
async def on_ready():
    for userId in [os.environ['DISIMO'], os.environ['DISTKT']]:
        user = client.get_user(int(userId))
        for i in natsorted(["result/" + file for file in os.listdir("result")]):  
            if i != "result/.gitignore":
                await user.send(i[i.rfind('/')+1:-4], file=discord.File(i))
    
    await client.close()

def Login():
    driver.get(os.environ['LGURL'])
    driver.find_elements(by=By.ID, value="form_id")[0].send_keys(os.environ['LGMAIL'])
    driver.find_elements(by=By.ID, value="form_pass")[0].send_keys(''.join(list(map(chr, [int((os.environ['LGPASS'][i-3:i])[::-1]) for i in range(len(os.environ['LGPASS']), 0, -3)]))))
    driver.execute_script('document.getElementsByClassName("btn--main")[0].click();')

def getSavePoint():
    with open('savepoint.txt') as f:
        for line in f:
            return int(line)

def setSavePoint(urlNum):
    with open('savepoint.txt', 'w') as f:
        f.write(urlNum + "\n" + str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))))

def searchMemont(urlNum):
    url = os.environ['TARURL'] + str(urlNum) + "/"
    driver.get(url)
    try:
        Name = driver.find_elements(by=By.CLASS_NAME, value="tit")[2].text
    except:
        setSavePoint(str(urlNum))
        return False, " "
    return True, Name

def getMoment(urlNum):
    global continueFlag
    continueFlag, Name = searchMemont(urlNum)

    if continueFlag:
        try:
            savepath = Name.replace(' ', '') + '_' + driver.find_elements(by=By.CLASS_NAME, value="date")[0].text.replace('.', '-').replace(' ', '_').replace(':', '')
            if len(driver.find_elements(by=By.TAG_NAME, value="img")) == 9:
                Image.open(io.BytesIO(request.urlopen(driver.find_elements(by=By.TAG_NAME, value="img")[2].get_attribute('src')).read())).save('result/' + savepath +'.jpg')
            else:
                driver.save_screenshot('result/' + savepath +'.png')
        except:
                print("error")
    else :
        continueFlag, Name = searchMemont(urlNum+1)

def main():
    Login()
    urlNum = getSavePoint()

    while continueFlag:
        getMoment(urlNum)
        if continueFlag:
            urlNum += 1
            time.sleep(10)

    client.run(TOKEN)

if __name__ == '__main__':
    main()
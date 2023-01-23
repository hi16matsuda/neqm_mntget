import os
import sys
import time
import io
import discord
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

@client.event
async def on_ready():
	user = client.get_user(483645421894500352)
	await user.send(file=discord.File("sample.png"))

def Login():
    url = 'https://www.rakuten.co.jp/'
    driver.get(url)
    driver.save_screenshot('sample.png')

Login()
client.run(TOKEN)
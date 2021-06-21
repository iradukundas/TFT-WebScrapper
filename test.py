# import webdriver
from selenium import webdriver
import discord

Path = "D:\samue\Python\chromedriver.exe"
driver = webdriver.Chrome(Path)

driver.get("https://lolchess.gg")

#frontpage-global-ranking__table
ranks = driver.find_elements_by_class_name('rank')
for rank in ranks:
    print(rank.text)

driver.quit()

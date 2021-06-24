from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from discord.ext import commands
from discord import Color
import discord
import os

#Setting up for webscrapping
driver = webdriver.Chrome(executable_path = "/app/.chromedriver/bin/chromedriver")

#discord side
Client = commands.Bot(command_prefix = '!')

@Client.event
async def on_ready():
    print("We have logged in as {0.user}".format(Client))

#an event is a piece of code that runs when a bot detects certain activity
driver.get("https://lolchess.gg")
 
@Client.command()
async def check(ctx, *, username):
    channel = Client.get_channel(778311945476374570)
    
    try:
        #webscraping
        driver.find_element_by_xpath('//*[@id="gnb-search-box"]/form/input').clear()
        sBox = driver.find_element_by_xpath('//*[@id="gnb-search-box"]/form/input') #looking for search box based on the xpath(obtained via inspect). stored in searchBox variable 
        sBox.send_keys(username) #entering something in the box
        searchButton = driver.find_element_by_xpath('/html/body/div[1]/header/div[3]/div/form/button')
        searchButton.click() #clicking the search button

        #changing colors for various elements on the website
        script = 'document.getElementsByClassName("profile__tier")[0].style.backgroundColor = "#2f3136";' #top part of stats
        script2 = 'document.getElementsByClassName("profile__tier__stats")[0].style.backgroundColor = "#2f3136";' #bottom part of stats
        script3 = 'document.getElementsByClassName("profile__tier__stats")[0].style.color = "#FFFFFF";' #text color
        script4 = 'document.getElementsByClassName("profile__tier")[0].style.border = "1px solid #2f3136";' #border color
        script5 = 'document.getElementsByClassName("profile__tier__info")[0].style.color = "#FFFFFF";' #LP Color
        script6 = 'for (i = 0; i < 5; i++) {document.getElementsByClassName("profile__tier__stat__text")[i].style.color = "#FFFFFF";}' #"top" color
        script7 = 'for (i = 0; i < 3; i++) {document.getElementsByClassName("profile__tier__stat__value float-right")[i].style.color = "#FFFFFF"};' #"top" color
        script8 = 'document.getElementsByClassName("text-dark-gray d-none d-md-block")[0].style.color = "#FFFFFF";' #Tier Color
        script9 = 'document.getElementsByClassName("top-percent")[0].style.color = "#FFFFFF";' #top % color
        script10 = 'document.getElementsByClassName("rank-region")[0].style.color = "#FFFFFF";' #rank region color

        #executing all the scripts
        driver.execute_script(script)
        driver.execute_script(script2)
        driver.execute_script(script3)
        driver.execute_script(script4)
        driver.execute_script(script5)
        driver.execute_script(script6)
        driver.execute_script(script7)
        driver.execute_script(script8)
        driver.execute_script(script9)
        driver.execute_script(script10)

        #taking screenshot on the stats page
        profileTierInfo = driver.find_element_by_class_name('profile__tier')
        profileTierInfo.screenshot('./stats.png')
        #locating player icon the page
        profileIcon = driver.find_element_by_class_name('profile__icon').find_element_by_tag_name('img').get_attribute('src')
        #embed
        embed = discord.Embed()
        file = discord.File('./stats.png')
        embed.set_image(url = "attachment://stats.png" )
        embed.set_author(name = username, icon_url = profileIcon)
        embed.set_footer(text ='src: lolchess.gg')
        await ctx.send(embed = embed, file = file)
        driver.get("https://lolchess.gg")

    except Exception as E:
        print(E) #printing the exception
        notFound = discord.Embed(title = '{} not found. Checking spelling and try again'.format(username))
        await ctx.send(embed=notFound)
        driver.get("https://lolchess.gg")


@Client.command()
async def lb(ctx):
    ranks = driver.find_elements_by_class_name('rank')
    ranksT = ''
    for rank in ranks:
        ranksT += rank.text + '\n'

    summoners = driver.find_elements_by_class_name('summoner')
    summonersT = ''
    for summoner in summoners:
        summonersT += summoner.text + '\n'

    regions = driver.find_elements_by_class_name('region')
    regionsT = ''
    for region in regions:
        regionsT += region.text + '\n'

    tiers = driver.find_elements_by_class_name('tier')
    tiersT = ''
    for tier in tiers:
        tiersT += tier.text + '\n'

    #not yet added
    lps = driver.find_elements_by_class_name('lp')
    lpsT = ''
    for lp in lps:
        lpsT += lp.text + '\n'

    winrates = driver.find_elements_by_class_name('winrate')
    winratesT = ''
    for winrate in winrates:
        winratesT += winrate.text + '\n'

    wins = driver.find_elements_by_class_name('wins')
    winsT = ''
    for win in wins:
        winsT += win.text + '\n'

    losses = driver.find_elements_by_class_name('losses')
    lossesT = ''
    for loss in losses:
        lossesT += loss.text + '\n'

    embed = discord.Embed(title = 'Leaderboard Data')
    embed.add_field(name = '#', value = ranksT , inline=True)
    embed.add_field(name = 'Location', value = regionsT, inline=True)
    embed.add_field(name = 'Name', value = summonersT, inline=True)
    await ctx.send(embed = embed)
    driver.get("https://lolchess.gg")


Client.run('Nzc4MzEzMDg3NzIyOTc5MzU4.X7QKjA.Sbwz4bQoRRR3dJyeI5vf71Hk-kQ')

# git add ., git commit -m "msg", git push heroku <--- for changes
#heroku logs -a discord-tft-stats --tail
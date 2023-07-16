from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

def dataobtain(quantity, url):  # Returns tuple: (played_champion, played_rune, players_champions), amount of rows = 10 + (quantity * 10)
    quantity_multiplier = quantity

    service = Service(executable_path="C:\\Users\\zlote\\Downloads\\chromedriver_win32\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    for i in range(quantity_multiplier):
        driver.find_element(By.CLASS_NAME, "see_more_ajax_button").click()
        sleep(2)

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    recent_games = soup.find(class_="data_table relative recentGamesTable inverted_rows_color")

    played_champion = []  # For data frame.
    for tab in recent_games.find_all(class_="championCellLight"):
        played_champion.append(tab.div.img["alt"])

    players_champions = []  # For data frame.
    for tab in recent_games.find_all(class_="summonerColumn"):
        team = []
        for champ in tab.contents:
            if champ == tab.contents[0]:
                continue
            team.append(champ.div.img["alt"])
        players_champions.append(team)

    played_rune = []  # For data frame.
    for tab in recent_games.find_all(class_="championCellLight"):
        played_rune.append(tab.find_all("div", class_="spell")[0].img["class"][0])
    for i in range(len(played_rune)):
        if played_rune[i] == "perk-8369-16":
            played_rune[i] = "First_Strike"
        elif played_rune[i] == "perk-8010-16":
            played_rune[i] = "Conqueror"
        elif played_rune[i] == "perk-8128-16":
            played_rune[i] = "Dark_Harvest"
        else:
            played_rune[i] = "Unknown_rune"
    return played_champion, played_rune, players_champions

def data_to_DF(data):  # Takes tuple: (played_champion, played_rune, players_champions) and produces a DF
    played_champion, played_rune, players_champions = data

    allies, enemies = [], []
    for i in range(len(played_champion)):
        if played_champion[i] in players_champions[2*i]:
            allies.append(players_champions[2*i])
            enemies.append(players_champions[2 * i + 1])
        else:
            enemies.append(players_champions[2 * i])
            allies.append(players_champions[2 * i + 1])

    df = pd.DataFrame({"Champion": played_champion,
                       "Rune": played_rune,
                       "Allies": allies,
                       "Enemies": enemies})
    return df
#df = data_to_DF(dataobtain(5, "https://www.leagueofgraphs.com/summoner/euw/SLT+Hygon"))
#print(df.to_string())
#df.to_csv("date.csv", index=False, mode='a', header=False)
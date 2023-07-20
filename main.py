#import dataobtain
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import metrics
from names_to_list import names_to_list
from sklearn.neighbors import KNeighborsClassifier

#df = dataobtain.data_to_DF(dataobtain.dataobtain(2, "https://www.leagueofgraphs.com/summoner/euw/ego+jungler"))
#print(df.to_string())
#df.to_csv("data.csv", index=False)

df = pd.read_csv("data.csv")
kayn_df = df[df["Champion"] == "Kayn"]
h = kayn_df.replace(["Conqueror", "First_Strike", "Dark_Harvest", "Unknown_rune"], [0, 1, 1, 1])
i = h[["Rune", "Enemies"]]
i = i.reset_index(drop=True)
ndf = pd.DataFrame()

feature_list = ["Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
                "Aurelion Sol", "Azir", "Bard", "BelVeth", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille",
                "Cassiopeia", "ChoGath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise",
                "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar",
                "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna",
                "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "KSante", "KaiSa", "Kalista", "Karma", "Karthus",
                "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "KhaZix", "Kindred", "Kled", "KogMaw",
                "LeBlanc", "Lee Sin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite",
                "Malzahar", "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus",
                "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu & Willump", "Olaf", "Orianna", "Ornn",
                "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "RekSai", "Rell",
                "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", "Sejuani", "Senna",
                "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona",
                "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo",
                "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus",
                "Vayne", "Veigar", "VelKoz", "Vex", "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick",
                "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri",
                "Ziggs", "Zilean", "Zoe", "Zyra"]
data1 = pd.DataFrame(columns=feature_list)
for index, row in i.iterrows():
    txt = row["Enemies"].replace("'", "")
    txt = txt.replace("[", "")
    txt = txt.replace("]", "")
    txt = txt.replace("\"", "")
    txt = txt.split(", ")
    zero_data = np.zeros(shape=(1, len(feature_list)))
    tempdf = pd.DataFrame(zero_data, columns=feature_list)
    tempdf = tempdf.astype(int)
    tempdf[txt[0]] = 1
    tempdf[txt[1]] = 1
    tempdf[txt[2]] = 1
    tempdf[txt[3]] = 1
    tempdf[txt[4]] = 1
    data1 = pd.concat([data1, tempdf])
data1 = data1.reset_index(drop=True)
data = data1.values
data = data.astype("int")

proba = data[0]
proba[16] = 0
proba[15] = 1

n_matrix = i.values
labels = n_matrix[:, 0]
labels = labels.astype("int")

split_dataset = train_test_split(data, labels)
train_data = split_dataset[0]
test_data = split_dataset[1]
train_labels = split_dataset[2]
test_labels = split_dataset[3]

reg = KNeighborsClassifier()
reg.fit(train_data, train_labels)
predictions = reg.predict(test_data)
r2 = metrics.r2_score(test_labels, predictions)

a = np.array(names_to_list("Darius", "Rammus", "Aurelion Sol", "ChoGath", "Zac"))

#print('R2: {}\n'.format(r2))



print(repr(reg.predict(a.reshape(1, -1))))
#if names_to_list("Gnar", "Zac", "Pantheon", "Ezreal", "Twitch") == data[4,:]: print("!!!")

#print(a)
#print(data[3, :])
#"Malphite", "Rammus", "Aurelion Sol", "ChoGath", "Thresh"
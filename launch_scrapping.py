
import logging
from dotenv import load_dotenv
import pandas as pd
from pandas.io.formats.format import DataFrameFormatter
import ast
import re 

load_dotenv()  # take environment variables from .env.

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler('logs.log', 'w', 'utf-8') 
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) 
root_logger.addHandler(handler)

logging.info("Identification des URL à scrapper")

df = pd.read_csv("data/alertes.csv",parse_dates=["date"])
df['content_parsed'] = df['content_parsed'].apply(ast.literal_eval)
df["nb_url"] = df.apply(lambda row: len(list(row["content_parsed"])), axis = 1)
df_grouped = df.groupby('candidat').agg({'nb_url': 'sum', 'content_parsed': 'sum'}).reset_index()

to_scrap = []

for idx,row in df_grouped.iterrows():
    for item in row["content_parsed"]:

        try: 
            media = re.search("https?:\/\/(www)?\.?(.*)\.([a-zA-Z])*\/",item[2],re.IGNORECASE).group(2)
            # pour gérer par ex les premium.figaro.fr
            if(".") in media:
                media = media.split(".")[-1]
        except:
            logging.warning("Média non identifié")
            media = "MEDIA_NON_IDENTIFIE"
        
        item_to_scrap = {
            "candidat" : row["candidat"],
            "media": media,
            "url": item[2]
        }

        to_scrap.append(item_to_scrap)

df_scrapping = pd.DataFrame(to_scrap)

df_stats_scrapping = df_scrapping.groupby("media").agg({"media": 'count'}).rename(columns={"media":"count"})
df_stats_scrapping = df_stats_scrapping.sort_values(by="count",ascending=False)


logging.info("Envoi mail récapitulatif")

import smtplib, ssl
import os 
from dotenv import load_dotenv

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST"), port, context=context) as server:
    server.login(os.environ.get("MAIL_USERNAME"), os.environ.get("MAIL_PASSWORD"))
    
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    message = """Subject: [Bot Projet Overton] Du nouveau à scraper ! \n

    Bonjour à toute l'équipe, 

    A aujourd'hui, j'ai reçu {nb_alertes} alertes Google sur les 38 personnes d'intérets que je suis. 

    Si tous mes scrapers étaient implémentés, je scrapperais {nb_scrapping} pages dont la liste est en bas de ce mail. 

    Si vous deviez implémenter les scrapper par ordre de priorité, voici ou sont les plus gros volumes :

    {stats_scrapping}

    Comme promis, voici le détail des URL à scrapper :

    {liste_to_scrap}

    Bonne implémentation à vous !

    """.format(nb_alertes = len(df), nb_scrapping=len(df_scrapping), stats_scrapping = df_stats_scrapping, liste_to_scrap = df_scrapping).encode('utf-8')

    # Send email here
    server.sendmail(sender_email, receiver_email, message)


logging.info("Email Envoyé")

#%%
# Imports
import os
import json
import logging
import csv
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler('logs.log', 'w', 'utf-8') 
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) 
root_logger.addHandler(handler)
#%%
logging.info("Mise à jour de la base d'alertes à partir de la boite mail {} ".format(os.environ.get("MAIL_USERNAME")))
from bs4 import BeautifulSoup
import json

def parse_alert(html):
    results = []
    parser = BeautifulSoup(html, features="html.parser")
    data_json = json.loads(parser.find_all('script')[0].getText())
    widgets = data_json["cards"][0]["widgets"]
    for widget in widgets:
        results.append((widget["title"], widget["description"], "https" + widget["url"].split("https")[2]))
    return results

from imap_tools import MailBox, AND
alerts = []
with MailBox(os.environ.get("IMAP_HOST")).login(os.environ.get("MAIL_USERNAME"),os.environ.get("MAIL_PASSWORD")) as mailbox:
    for msg in mailbox.fetch():  # generator: imap_tools.MailMessage

        print(msg.subject)
        if("Alerte Google" in msg.subject):
            alerte = {
                'mail_id' : msg.uid,
                'date' : msg.date,
                'candidat' : msg.subject.split(':')[1].strip(),
                'content_html' : msg.html,
                'content_raw' : msg.text,
                'content_parsed' : parse_alert(msg.html)
            }
            alerts.append(alerte)
    

with open("data/alertes.csv","w+") as f:
    writer = csv.DictWriter(f, fieldnames=["mail_id","date","candidat","content_html","content_raw","content_parsed"])
    writer.writeheader()
    [writer.writerow(row) for row in alerts]

logging.info("{} alertes exportées vers data/alertes.csv".format(len(alerts)))

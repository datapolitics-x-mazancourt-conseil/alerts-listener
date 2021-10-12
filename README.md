<div align="center" id="top"> 


  <!-- <a href="https://{{app_url}}.netlify.app">Demo</a> -->
</div>

<h1 align="center">alerts-listener</h1>

<br>

## :dart: A propos ##

Ce projet récupère des Alertes Google envoyées dans un boite mail, et identifie les URL à scrapper.


## :white_check_mark: Requirements ##

- Python 3.7+
- Docker et un compte hub.docker.com (si vous souhaitez utiliser Docker)
- L'application est conçue pour recevoir et envoyer des mails depuis un compte mail. La configuration du compte mail se fait depuis les variables d'environnement (fichier .env à la racine, par exemple). Les 5 variables suivantes sont attendues : 
  - IMAP_HOST, l'hôte sur lesquel sont reçues les alertes (par ex imap.gmail.com)
  - SMTP_HOST, l'hôte à partir duquel sont envoyés les emails de monitoring (par ex smtp.gmail.com)
  - MAIL_USERNAME, le mail ou sont reçues les alertes (par ex toto@gmail.com)
  - MAIL_PASSWORD, le mot de passe du compte mail (par ex monmotdepasseprefere)
  - SENDER_EMAIL, le mail duquel sera envoyé le récap
  - RECEIVER_EMAIL, le mail auquel sera envoyé le récap


## :white_check_mark: Lancement avec docker ##


 sudo docker run -e IMAP_HOST=IMAP_HOST -e MAIL_USERNAME=MAIL_USERNAME -e MAIL_PASSWORD=MAIL_PASSWORD -e SENDER_EMAIL=SENDER_EMAIL -e RECEIVER_EMAIL=RECEIVER_EMAIL -e SMTP_HOST=SMTP_HOST antoinebacalu/alerts-listener
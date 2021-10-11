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
- L'application est conçue pour recevoir et envoyer des mails depuis un compte mail. La configuration du compte mail se fait depuis les variables d'environnement (fichier .env à la racine, par exemple). Les 3 variables suivantes sont attendues : IMAP_HOST (par ex imap.gmail.com), MAIL_USERNAME (par ex toto@gmail.com), MAIL_PASSWORD (par ex monmotdepasseprefere).

# Lire quelques mails et publier les informations dans un tableur

## Introduction

Ce petit projet vise à initier les élèves aux API google.

Il suit trait pour trait la documentation officielle des api google et
seules quelques parties ont été modifiées depuis les fichiers `quickstart.py` des API gmail et sheet pour Python.

## Présentation

Lors de la rentrée les élèves de NSI m'ont envoyé un mail respectant un format particulier :

objet : "NSI 2020 nom prenom"
Dans le corps du message ils devaient rapidement décrire leur matériel informatique et leurs connaissances.

Ce module Python comporte deux fichiers principaux :

**gmail_to_json.py** : récupère ces informations, les stocke dans un fichier json.

**json_to_sheet.py** : lit ce fichier json et publie les informations dans
un tableur sheet.

## Principe

Les API google permettent de manipuler une grande partie des informations
hébergées sur leurs serveurs. On peut reproduire et automatiser le comportement d'un utilisateur.

Le premier script **gmail_to_json** extrait tous les mails dont l'objet répond à un critère, on filtre ceux qui ne correspondent pas.

**Attention :** ce script lira trop de messages dans le futur.

Ensuite on stocke temporairement les données dans un fichier json.

Cela évite d'avoir à solliciter trop souvent la messagerie pour relever des message dont on dispose déjà.

Les données sont formatées de manière lisible dans le json.

Le second fichier, **json_to_sheet** dépose simplement les données dans le tableur indiqué.

## Sources :

* [Api Gmail](https://developers.google.com/gmail/api/quickstart/python?authuser=2)
* [API Sheet](https://developers.google.com/sheets/api/quickstart/python?authuser=2)

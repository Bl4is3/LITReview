# LITReview 

Application Django permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

## Lancement du programme:

Créez un répertoire dédié et placez-vous dedans:

```
mkdir LITReview
cd /LITReview
```

Importez le projet:

```
git clone https://github.com/Bl4is3/LITReview.git
```

Création de l'environnement virtuel et installation des dépendances:

```
mkdir .venv
pipenv install
python manage.py runserver

```

## Fonctionnement de l'application


Un utilisateur peut :
* se connecter et s’inscrire – le site n'est pas être accessible aux utilisateurs non connectés;
* consulter un flux contenant les derniers tickets et les commentaires des utilisateurs qu'il suit; 
* créer de nouveaux tickets pour demander une critique sur un livre/article ;
* créer des critiques en réponse à des tickets;
* créer des critiques qui ne sont pas en réponse à un ticket;
* voir, modifier et supprimer ses propres tickets et commentaires; 
* suivre les autres utilisateurs en entrant leur nom d'utilisateur;
* voir qui il suit et suivre qui il veut dans l'onglet;
* cesser de suivre un utilisateur. 
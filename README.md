# SaaS Monitoring

Projet de développement d'une plateforme SaaS de monitoring destinée aux PME, agences web et petites entreprises IT.

L'objectif est de permettre aux utilisateurs de surveiller plusieurs sites web depuis un tableau de bord centralisé et de consulter leur disponibilité ainsi que leurs performances.

## Objectifs du projet

La plateforme a pour objectif de surveiller :

- La disponibilité des sites web.
- Les codes de réponse HTTP.
- Les temps de réponse.
- L'état de santé des services.
- À terme, les certificats SSL, les noms de domaine, les serveurs et les sauvegardes.

## Architecture actuelle

| Composant | Technologie | Rôle |
|---|---|---|
| Monitoring | Python | Vérification des sites web |
| Requêtes HTTP | Requests | Récupération des réponses HTTP |
| Base de données | PostgreSQL | Stockage des résultats |
| Accès à la base | Psycopg | Communication entre Python et PostgreSQL |
| Tableau de bord | Flask | Affichage de l'état des sites |
| Conteneurisation | Docker et Docker Compose | Exécution de l'ensemble des services |

Trois services sont lancés par Docker Compose :

- `db` : la base PostgreSQL, avec un volume pour conserver les données.
- `checker` : le script de monitoring, qui vérifie les sites toutes les 60 secondes.
- `web` : le tableau de bord, accessible sur le port 5000.

## Fonctionnement

Le script Python effectue les opérations suivantes :

1. Vérification de la disponibilité des sites web.
2. Récupération du code de réponse HTTP.
3. Mesure du temps de réponse.
4. Détermination de l'état de santé du site.
5. Enregistrement des résultats dans PostgreSQL.
6. Gestion des erreurs lorsqu'un site est inaccessible.
7. Répétition automatique des vérifications toutes les 60 secondes.

Le tableau de bord affiche, pour chaque site, son dernier état, son dernier temps de réponse, son temps de réponse moyen et son taux de disponibilité, ainsi que l'historique des dernières vérifications. La page se rafraîchit toutes les 30 secondes.

### Statuts surveillés

- **Online :** le serveur a répondu à la requête HTTP.
- **Healthy :** le site a retourné un code HTTP 200.
- **Offline :** aucune réponse HTTP n'a pu être obtenue.

Un site peut être accessible sans être considéré comme sain. Par exemple, une réponse HTTP 429 signifie que le serveur répond, mais limite les requêtes.

## Lancer le projet

Prérequis : Docker et Docker Compose.

1. Copier le fichier `password.env.example` en `password.env`, puis y renseigner un mot de passe.
2. Lancer l'ensemble des services :

```bash
docker compose up --build
```

3. Ouvrir le tableau de bord sur `http://127.0.0.1:5000`. Les premières données apparaissent après environ une minute.

Pour arrêter les services : `docker compose down`.

Le fichier `password.env` contient les identifiants de la base et n'est jamais envoyé sur GitHub.

## Structure du repository

```text
SaaS_monitoring/
│
├── app.py
├── checker.py
├── docker-compose.yml
├── dockerfile
├── init.sql
├── password.env.example
├── requirements.txt
└── templates/
    └── index.html
```

## Évolutions prévues

- [x] Amélioration de la configuration avec des variables d'environnement.
- [x] Conteneurisation du service de monitoring.
- [x] Mise en place de Docker Compose.
- [x] Création d'un tableau de bord web (version minimale).
- [ ] Développement d'une API REST.
- [ ] Gestion de plusieurs clients.
- [ ] Mise en place de notifications en cas de panne.
- [ ] Surveillance des certificats SSL et des domaines.
- [ ] Mise en place d'une pipeline CI/CD avec GitHub Actions.
- [ ] Déploiement sur un serveur distant avec Ansible.

## Équipe

Projet réalisé par deux étudiants :

- **Romain, développement :** backend, API REST et interface utilisateur.
- **Marcus, DevOps :** infrastructure, monitoring, conteneurisation, automatisation et déploiement.

---

*Projet en cours de développement — MVP.*

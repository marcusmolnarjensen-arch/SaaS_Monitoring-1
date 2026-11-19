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
| Environnement de base de données | Docker | Exécution de PostgreSQL dans un conteneur |

## Fonctionnement

Le script Python effectue les opérations suivantes :

1. Vérification de la disponibilité des sites web.
2. Récupération du code de réponse HTTP.
3. Mesure du temps de réponse.
4. Détermination de l'état de santé du site.
5. Enregistrement des résultats dans PostgreSQL.
6. Gestion des erreurs lorsqu'un site est inaccessible.
7. Répétition automatique des vérifications toutes les 60 secondes.

### Statuts surveillés

- **Online :** le serveur a répondu à la requête HTTP.
- **Healthy :** le site a retourné un code HTTP 200.
- **Offline :** aucune réponse HTTP n'a pu être obtenue.

Un site peut être accessible sans être considéré comme sain. Par exemple, une réponse HTTP 429 signifie que le serveur répond, mais limite les requêtes.

## Structure actuelle du repository

```text
SaaS_monitoring/
│
├── checker.py
└── requirements.txt
```

## Évolutions prévues

- [ ] Amélioration de la configuration avec des variables d'environnement.
- [ ] Conteneurisation du service de monitoring.
- [ ] Mise en place de Docker Compose.
- [ ] Développement d'une API REST.
- [ ] Création d'un tableau de bord web.
- [ ] Gestion de plusieurs clients.
- [ ] Mise en place de notifications en cas de panne.
- [ ] Surveillance des certificats SSL et des domaines.
- [ ] Mise en place d'une pipeline CI/CD avec GitHub Actions.
- [ ] Déploiement sur un serveur distant avec Ansible.

## Équipe

Projet réalisé par deux étudiants :

- **Développement :** Backend, API REST et interface utilisateur.
- **DevOps :** Infrastructure, monitoring, conteneurisation, automatisation et déploiement.

---

*Projet en cours de développement — MVP.*

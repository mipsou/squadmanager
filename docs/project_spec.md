# Modèle de Projet SquadManager

## ID
`<project_id>`

## Titre
Titre du projet

## Description
Brève description de l'objectif.

## Agents
- agent1
- agent2

## Tâches
1. draft_prompt
2. review_prompt
3. finalize_prompt

---

# Cahier des Charges – ChatBot IA

## Objectif
Permettre aux utilisateurs de poser des questions en langage naturel et d’obtenir des réponses précises.

## Fonctionnalités
- Interprétation de la requête utilisateur  
- Recherche documentaire dans la base interne  
- Génération de réponse formatée (texte, lien, image)  
- Journalisation des interactions

## Contraintes
- Temps de réponse < 200 ms  
- Sécurisation OAuth 2.0  
- Support multilingue (FR/EN)

## Livrables
- Prototype CLI  
- Documentation utilisateur  
- Tests unitaires et d’intégration

## Données requises
- Corpus FAQ interne  
- Clés API OpenAI

---

# Cahier des Charges – Gestion Inventaire IA

## Objectif
Optimiser le suivi et la répartition des stocks en temps réel pour réduire les ruptures et surstocks.

## Fonctionnalités
- Suivi automatisé des niveaux de stock
- Alertes de réapprovisionnement
- Prévision de la demande via IA
- Génération de bons de commande

## Contraintes
- Intégration ERP existant
- Mises à jour en temps réel (< 1s)
- Authentification et droits d’accès

## Livrables
- Module CLI de gestion inventaire
- Documentation d’installation
- Tests unitaires et e2e

## Données requises
- Base de données produit (SKU, quantités)
- Historique des ventes

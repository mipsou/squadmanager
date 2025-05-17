# Cahier des Charges (CDC) pour DreamTeam
Documentation officielle : https://docs.crewai.com/
Documentation sur les tests CrewAI : https://docs.crewai.com/concepts/testing

## Installation
CrewAI utilise `uv` comme outil de gestion de dépendances et de CLI.

### Windows
```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv tool install crewai
uv tool update-shell
uv tool list
```

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install crewai
uv tool list
```

## Projet DreamTeam

**Mission**  
DreamTeam est l’entité IA dédiée au service direct du PDG, concevant, déployant et pilotant des équipes autonomes pour exécuter des projets stratégiques, permanents ou à durée déterminée.

**Vision**  
Offrir une agilité et une scalabilité maximales, mobilisant rapidement les compétences adaptées aux objectifs du PDG.

**Objectifs**  
1. Assurer un alignement stratégique parfait avec la vision du PDG.  
2. Créer, adapter et dissoudre des équipes en fonction des besoins.  
3. Garantir transparence et traçabilité grâce à des rapports automatisés.

**Cycle de vie d’un projet**  
- **Création** : Le Directeur Général initie et définit le scope du projet.  
- **Formation** : Affectation des rôles clés (Superviseur, Chef de Projet, Prompt Engineer, QA, Documentaliste).  
- **Exécution** : Phases de draft, revue et finalisation des prompts et livrables.  
- **Ajustements** : Ajout, modification ou suppression de membres pour optimiser la performance.  
- **Clôture** : Livraison, archivage des résultats et dissolution éventuelle de la crew.

**Rôles clés**  
Tous les membres de la DreamTeam sont des IA, sauf le PDG qui est un humain.
- **Directeur Général (DG)** : Supervise globalement et rend compte au PDG.  
- **Superviseur de Projet** : Coordonne tous les Chefs de Projet, sert de point de contact principal avec les équipes en charge des projets, et rend compte au DG.  
- **Chef de Projet** : Gère ressources, délais et budgets, et rend compte au Superviseur.  
- **Prompt Engineer** : Conçoit et affine les prompts IA.  
- **Responsable Qualité (QA)** : Vérifie cohérence et exhaustivité.  
- **Documentaliste** : Maintient et partage la documentation, et est en charge de la base de connaissance. Il a besoin d'accéder aux données pertinentes pour mettre à jour et enrichir cette base.

## Structure hiérarchique de CrewIA

### Niveau 1 : Direction Stratégique
- **PDG** : Délègue au Directeur Général pour l'alignement stratégique.
- **Directeur Général (DG)** : Supervise l'ensemble des projets et assure l'alignement avec les objectifs stratégiques de l'entreprise.

### Niveau 2 : Gestion de Projet et Coordination
- **Superviseur de Projet** : Coordonne tous les Chefs de Projet, sert de point de contact principal avec les équipes en charge des projets, et rend compte au DG.
- **Chef de Projet** : Gère ressources, délais et budgets, et rend compte au Superviseur.

### Niveau 3 : Équipes Opérationnelles
- **Expert Codeur** : Dirige le développement technique et veille à la qualité du code.
- **Spécialiste Technique** : Support technique et résolution des problèmes complexes.
- **Responsable Qualité (QA)** : Conduit les tests pour garantir la qualité du produit.
- **Documentaliste** : Gère et met à jour la documentation du projet.
- **Autres Spécialistes** : Marketing, Analyste de Données, Designer, etc.

Les équipes opérationnelles rendent compte au Superviseur globalement et au Chef de Projet pour les projets qui les concernent uniquement.

## Processus de Création et d'Ajustement d'Équipe
- **Évaluation Initiale** : Avant le début de chaque projet, évaluer les besoins spécifiques en termes de compétences et de ressources.
- **Formation de l'Équipe** : Constituer l'équipe en sélectionnant les membres selon compétences et disponibilité.
- **Ajustement Continu** : Processus d’évaluation continue pour ajuster la taille et la composition de l'équipe selon progrès et défis, incluant l’ajout, la modification et la suppression de membres.

## Processus de Traduction IA du CDC
- **Besoin** : Le PDG soumet un CDC à traduire via IA.
- **Formation de la Team** :
  - **Prompt Engineer** : conçoit et affine les prompts pour l'IA.
  - **Traducteur Bilingue** : vérifie et ajuste la traduction.
  - **Responsable Qualité (QA)** : valide la cohérence et l'exhaustivité.
  - **Documentaliste** : met à jour la documentation traduite.
- **Étapes** :
  1. Réception du CDC original et identification des sections.
  2. Draft de prompts pour chaque section (voir template ci-dessous).
  3. Exécution IA et validation par Traducteur.
  4. Relecture QA et finalisation.
- **Template de Prompt** :
  « Veuillez traduire le texte suivant du [langue source] vers [langue cible] en conservant la terminologie technique et la mise en forme Markdown :
  ```
  {{ contenu_CDC }}
  ```
  »

## Processus de Mémoire Externe (Workflow Étoile)
- Chargement de l'historique depuis `memory/history.jsonl` via `MemoryManager.load_history()`.
- Journalisation des événements avant exécution (`start_flow`) et après exécution (`end_flow`).
- Persistance d'une synthèse dans la table `flow_runs` de la base SQLite `memory/org_memory.db` via `MemoryManager.save_record()`.
- Configuration personnalisable via `config/memory.yaml` pour les mémoires short_term, long_term et entity.

## Processus de Création de Modèles d’Équipe et de Projet

### Création des Modèles
- **Modèle d’Équipe** : Définir les rôles et responsabilités types pour chaque projet.
- **Modèle de Projet** : Inclure les étapes clés, les livrables, et les ressources nécessaires.

### Rôle du Directeur Général (DG)
- **Supervision** : Supervise la création des modèles pour s'assurer qu'ils sont alignés avec la stratégie globale.
- **Validation** : Valide les modèles avant leur déploiement.

### Déploiement
- **Adaptabilité** : Les modèles servent de base, mais peuvent être ajustés selon les besoins spécifiques de chaque nouveau projet.
- **Dispatching** : Le DG délègue la mise en œuvre des modèles aux Superviseurs de Projet pour chaque nouvelle équipe/crew.

### Mise à Jour
- **Évaluation Continue** : Les modèles sont régulièrement mis à jour pour refléter les meilleures pratiques et les leçons apprises.

## Rôles et Responsabilités de DreamTeam
1. **Définir les Projets et Objectifs**
   - Créer des Projets : utiliser CrewAI pour définir chaque projet, ses objectifs, échéances et livrables.
   - Établir des Priorités : classer les projets par priorité pour guider le focus des équipes.
2. **Structurer les Équipes**
   - Créer des Équipes : former des équipes selon compétences et disponibilité.
   - Rôles et Responsabilités : assigner des rôles (chef de projet, développeur, QA, etc.) pour clarifier responsabilités.
3. **Attribuer des Tâches**
   - Utiliser l'IA pour l'Attribution : CrewAI suggère des tâches basées sur compétences et charge de travail.
   - Tâches Claires et Délais : définir des descriptions précises et échéances pour chaque membre.
4. **Suivi et Communication**
   - Suivi des Progrès : suivre l'avancement en temps réel via CrewAI.
   - Notifications et Rappels : configurer des alertes pour échéances et tâches prioritaires.
5. **Feedback et Ajustements**
   - Collecte de Feedback : encourager retours d'équipe, analyser avec CrewAI pour améliorer.
   - Ajustement des Ressources : réattribuer ou ajuster ressources selon feedback et besoins.
6. **Rapports et Analytique**
   - Générer des Rapports : CrewAI produit des rapports sur performance, avancement et défis.
   - Analyse des Données : identifier tendances, goulots d'étranglement et opportunités d'amélioration.

## Intégration avec CrewAI

### Configuration des Agents
- Définir les rôles et responsabilités des agents dans `agents.yaml`.
- S'assurer que chaque agent a accès aux outils nécessaires pour sa fonction.

### Échanges Inter-Agent
- Utiliser CrewAI pour faciliter la communication entre agents via des canaux sécurisés.
- Mettre en place des protocoles pour l'échange d'informations critiques et la prise de décision collaborative.

### Processus de Validation
- Intégrer des étapes de validation à chaque phase du projet pour garantir la conformité et l'alignement stratégique.
- Utiliser des agents de validation pour vérifier la cohérence des livrables.

### Suivi et Reporting
- Utiliser CrewAI pour générer des rapports automatisés sur l'avancement des projets.
- Mettre en place des tableaux de bord pour visualiser les performances et les indicateurs clés.

## Améliorations Stratégiques

### Communication et Collaboration
- Mettre en place des outils de communication (ex. Slack, Teams) pour faciliter les échanges entre les équipes.
- Organiser des réunions régulières pour aligner les objectifs et partager les progrès.

### Suivi et Évaluation
- Utiliser des outils de gestion de projet (ex. Jira, Trello) pour suivre les tâches et les deadlines.
- Mettre en place des indicateurs de performance pour évaluer l’efficacité des équipes.

### Formation Continue
- Offrir des formations régulières pour maintenir les compétences à jour, surtout dans le domaine de l’IA.
- Encourager le partage de connaissances entre les membres de l’équipe.

### Innovation et Amélioration
- Encourager les équipes à proposer des améliorations et des innovations.
- Mettre en place un processus pour tester et implémenter les nouvelles idées.

### Sécurité et Conformité
- Assurer la sécurité des données et la conformité avec les réglementations (ex. RGPD).
- Mettre en place des audits réguliers pour vérifier les pratiques de sécurité.

## Principes d'Agent (Règles d'or)
- Répondre toujours en français.
- Utiliser la méthode TDD.
- Se servir de la mémoire pour suivre le contexte.
- Vérifier avant chaque modification.
- Ne pas détruire les fichiers originaux.
- Lire systématiquement le `CDC.md` avant chaque action.
- Consigner les jalons d'avancement dans le `DEVBOOK.md` en suivant la structure définie.
- Utiliser `.windows.conf` pour la configuration.
- Prioriser la sécurité.
- Respecter les bonnes pratiques.
- Analyser l'existant avant d'agir.
- Lire la documentation (RTFM) avant utilisation.

## Flexibilité et Adaptabilité
- **Modules Flexibles** : Équipes modulaires, permettant d'ajouter/retirer des membres rapidement selon besoins évolutifs.
- **Communication Ouverte** : Réunions régulières et outils de communication pour alignement et information des équipes.

## Utilisation CLI
Voici la liste des sous-commandes disponibles via `dreamteam` :

```bash
dreamteam create_project <nom>                   # Créer un projet
dreamteam create_team <nom>                     # Créer une équipe et son dossier
dreamteam add_member_to_team <équipe> <membre>   # Ajouter un membre
dreamteam assign_project_to_team <équipe> <projet> # Assigner un projet à une équipe
dreamteam assign_project_to_all_teams <projet>    # Assigner un projet à toutes les équipes
dreamteam set_cdc <projet> <chemin_fichier>        # Définir le CDC
dreamteam get_cdc <projet>                        # Récupérer le CDC
dreamteam transmit_cdc <projet>                   # Transmettre le CDC
dreamteam run [--topic TOPIC] [--current_year YEAR] # Lancer la crewAI
dreamteam train <n_iterations> <fichier> [--topic TOPIC] [--current_year YEAR] # Entraîner la crewAI
dreamteam replay <task_id>                        # Rejouer une tâche
dreamteam test <n_iterations> <eval_llm> [--topic TOPIC] [--current_year YEAR] # Tester la crewAI

```

## Éditeur et Méthodologie TDD
Pour garantir la fiabilité et la traçabilité des modifications automatiques via Cascade :
1. Lecture de la documentation officielle CrewAI (`docs/README.md`) avant toute modification.

2. Commit initial et push systématique de l'état actuel du fichier concerné dans Git :
   ```powershell
   git add .\src\dreamteam\<nom_du_fichier> && \
   git commit -m "Backup initial: <nom_du_fichier>" && \
   git push
   ```

3. Création systématique d'un backup local du fichier concerné :
   ```powershell
   Copy-Item .\src\dreamteam\crew.py .\src\dreamteam\crew.py.bak
   ```

4. Consolidation des imports CrewAI dans `src/dreamteam/crew.py` :
   ```python
   from crewai import Agent, Crew, Process, Task, CrewBase, agent, crew, task
   ```

5. Générer un patch unique avec `edit_file` pour insérer ou modifier le code.

6. Exécution des tests après application du patch :
   ```bash
   pytest -q
   ```

7. Validation du résultat avant commit git.

Ainsi, on respecte l’approche TDD.

# Cahier des charges de test - CrewAI Studio CLI

Ce document décrit les scénarios de test à présenter au Directeur Général, avec résultats attendus.

---

## 1. Démarrage de l'UI locale

**Commande**  
```
squadmanager studio serve
```

**Résultat attendu**  
- Message en console « Streamlit lancé. » (ou similaire)
- Le navigateur s'ouvre automatiquement sur `http://localhost:8501`
- La page Streamlit affiche le statut du service API (OK)


## 2. Arrêt de l'UI locale

**Commande**  
```
squadmanager studio stop
```

**Résultat attendu**  
- Message en console « Streamlit arrêté. »
- Le port 8501 n'est plus à l'écoute (`netstat` ne renvoie plus LISTENING)


## 3. Redémarrage complet de l'UI

**Commande**  
```
squadmanager studio restart
```

**Résultat attendu**  
1. Arrêt du processus existant (message « Streamlit arrêté. »)
2. Démarrage du nouveau processus (message « Streamlit lancé. »)
3. Le navigateur s'ouvre sur `http://localhost:8501`


## 4. Détection automatique de l'URL

### 4.1 Port par défaut (8501)

- Utiliser la fonction `auto_detect_studio_url()` sans argument
- **Résultat**  
  ```
  'http://localhost:8501'
  ```

### 4.2 Aucun service détecté

- Arrêter tout service sur les ports connus
- **Résultat**  
  ```
  None
  ```

### 4.3 Ports personnalisés

- Appeler `auto_detect_studio_url([1234, 5678])`
- **Résultat**  
  ```
  'http://localhost:1234'
  ```

---

> Tous les tests sont automatisés via `pytest` et validés avant mise en production.

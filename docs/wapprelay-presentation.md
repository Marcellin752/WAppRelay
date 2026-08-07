# WAppRelay
## Bot WhatsApp de transfert automatique de messages

---

## 1. Présentation

**WAppRelay** est un service backend qui reçoit n'importe quel type de message WhatsApp (texte, audio, image, vidéo, document, contact, localisation, sticker...) envoyé par un utilisateur, et le retransmet intégralement et immédiatement à un destinataire fixe prédéfini, sans perte d'information.

Le projet couvre la brique technique la plus critique d'un assistant vocal WhatsApp : la communication bidirectionnelle fiable avec l'API WhatsApp Cloud. Il ne traite aucune logique métier — pas de facturation, pas de paiement, pas de transcription — et se concentre exclusivement sur la maîtrise du canal de communication.


À terme, WAppRelay doit servir de fondation à un assistants vocaux WhatsApp plus avancés. Avant de construire ce type de produit, il faut d'abord prouver que la réception et la retransmission de messages WhatsApp — dans tous leurs formats — peuvent être faites de façon fiable, idempotente et observable. C'est l'objet de ce projet.

### 1.3 Problème résolu

Beaucoup de produits qui s'appuient sur WhatsApp comme canal d'entrée butent sur les mêmes questions techniques : comment recevoir tous les types de messages sans rien perdre, comment garantir l'idempotence face aux renvois de webhook, comment gérer les médias (téléchargement, ré-upload, tailles limites), et comment observer ce qui se passe en production. WAppRelay répond directement à ces questions avec une implémentation de référence, testée et documentée.

### 1.4 Périmètre du projet

**Inclus :**
- Réception de messages WhatsApp entrants via Webhook (`POST /webhook`)
- Support de tous les types de messages exposés par l'API : texte, audio/vocal, image, vidéo, document, contact (vCard), localisation, sticker, réaction
- Retransmission automatique et immédiate vers un destinataire unique fixe, configuré par variable d'environnement
- Fidélité maximale du contenu original (texte brut, légendes, métadonnées de fichiers)
- Journalisation structurée de chaque événement reçu et transmis
- Gestion des erreurs et des types de messages non supportés

**Hors périmètre (pour cette première version) :**
- Transcription audio-vers-texte
- Extraction d'information métier
- Génération de facture ou intégration Mobile Money
- Multi-destinataires ou routage conditionnel
- Interface d'administration graphique
- Persistance long terme en base de données
- Authentification multi-utilisateur (mono-instance, mono-compte WhatsApp Business)

---

## 2. Fonctionnalités principales

| # | Fonctionnalité | Description |
|---|---|---|
| F1 | Réception via Webhook | Endpoint `POST /webhook` appelé par WhatsApp à chaque événement, réponse `200 OK` immédiate, traitement asynchrone en arrière-plan |
| F2 | Vérification du Webhook | Handshake `GET /webhook` avec `hub.verify_token` lors de la configuration initiale côté Meta |
| F3 | Normalisation des messages | Un `MessageParser` transforme chaque type de payload WhatsApp en un objet interne unique et exploitable |
| F4 | Transfert au destinataire fixe | Un `MessageForwarder` renvoie le message normalisé (texte, média, contact...) au numéro configuré, préfixé des métadonnées de la source |
| F5 | Journalisation structurée | Logs JSON à chaque étape (réception, parsing, téléchargement média, transfert) pour le debug et l'observabilité |

Le service gère aussi les cas limites propres à WhatsApp : événements dupliqués (idempotence via cache Redis sur `message_id`), rafales de messages concurrents, échecs de téléchargement de média avec retry, médias trop volumineux, types de messages non reconnus.

---

## 3. Architecture technique

### 3.1 Vue d'ensemble

```
WhatsApp Cloud API  --(Webhook POST)-->  API Gateway (FastAPI)
                                              |
                                        Validation & Auth
                                              |
                                        Queue interne (async)
                                              |
                                        MessageParser
                                              |
                                    MediaDownloader (si média)
                                              |
                                        MessageForwarder
                                              |
                                   WhatsApp Cloud API (envoi)
```

Le service est stateless côté logique métier. Redis est utilisé pour la déduplication des `message_id` déjà traités (idempotence) et, le cas échéant, une file de tâches légère.


### 3.2 Sécurité

- Validation de la signature HMAC-SHA256 (`X-Hub-Signature-256`) de chaque requête entrante
- Secrets exclusivement chargés via variables d'environnement, jamais commités
- Aucune stack trace exposée côté client sur les routes HTTP publiques

---

## 4. Stack technique

| Technologie | Rôle |
|---|---|
| Python 3.12 | Langage principal |
| FastAPI | Framework asynchrone, validation Pydantic, OpenAPI auto-générée |
| Pydantic / pydantic-settings | Validation des payloads et de la configuration |
| httpx (async) | Client HTTP asynchrone vers l'API WhatsApp |
| Redis | Déduplication (idempotence) et cache léger |
| structlog | Logging structuré JSON |
| Pytest + pytest-asyncio | Tests unitaires et d'intégration |
| respx / pytest-httpx | Mock des appels sortants vers l'API WhatsApp |
| Docker / docker-compose | Environnement reproductible (app + Redis) |
| ngrok | Exposition HTTPS du webhook en développement local |
| WhatsApp Cloud API (Meta) | API officielle de messagerie WhatsApp |

---

## 5. Évolutions envisagées

- Interface d'administration minimale (derniers messages relayés, statut succès/échec)
- Tableau de bord de métriques (volumes par type, taux d'échec, latence)
- Pipeline CI/CD (lint, tests, build Docker à chaque push)
- Pré-commit hooks (formatage, lint, détection de secrets)
- Observabilité externe (Grafana Loki, Sentry)
- Support multi-destinataires configurables dynamiquement
- Chiffrement au repos des médias temporaires + purge automatique
- File d'attente plus robuste (Celery/RQ) si le volume augmente

---
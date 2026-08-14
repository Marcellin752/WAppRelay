# Webhook & Sécurité : Tutoriels et ressources utilisés

## Objectif de la phase

Valider le canal de communication WhatsApp : configuration d'environnement,
handshake GET /webhook, réception POST /webhook avec vérification de signature.

## Ressources utilisées

| Ressource | URL | Ce qu'elle a apporté |
|---|---|---|
| SocialHook — Receive WhatsApp Messages | https://socialhook.io/en/blog/receive-whatsapp-messages-server | Pipeline webhook complet : HMAC sur octets brutes, pattern queue, navigation entry changes |
| Medium Sanket Bodake — Smart WhatsApp Chatbot | https://medium.com/@sanket.ai/building-a-smart-whatsapp-chatbot-with-python-and-fastapi-a-step-by-step-guide-36c9c70f5715 | Setup compte Meta, tokens, ngrok, token permanent System User, paiement production |
| Docs Meta — Get Started | https://developers.facebook.com/docs/whatsapp/cloud-api/get-started | Setup complet, payloads réels, numéro de test |

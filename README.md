# ContentFlow v0.1 (FR, dark, monorepo)

## Résumé exéc’
MVP FastAPI + React (Vite + Tailwind) avec shortlink `/r/{code}`, suivi des clics, antifraude v1, ledger (balances), métriques, auth partenaire via magic-link (mode dev) + JWT. Docker multi-stage et endpoints de santé prêts pour déploiement.

## Arborescence
Voir le repo sous `contentflow/` (backend `app/`, frontend `client/`). Les assets frontend sont buildés dans `app/static/` à l’image Docker.

## Démarrage (Smoke)
- docker build -t contentflow .
- docker run -e PORT=5000 -p 5000:5000 contentflow
- GET http://localhost:5000/healthz → 200
- GET http://localhost:5000/readyz → 200 quand prêt

## Variables d’env (.env.example)
Copiez `.env.example` vers `.env` si besoin. Par défaut, DB SQLite pour dev. En prod, renseignez `DATABASE_URL` PostgreSQL.

## Flow de test (happy-path)
1) POST /api/auth/magic-link {email}
   - Le lien de connexion est affiché dans les logs (mode dev)
2) POST /api/auth/verify {token}
   - Renvoie un JWT partenaire
3) POST /api/posts (Bearer)
   - Crée un Asset + Post (contenu IA stub)
4) POST /api/links {post_id} (Bearer)
   - Renvoie l’URL courte `/r/{code}`
5) GET /r/{code}
   - 302 vers l’URL cible ; insertion d’un ClickEvent ; stats partenaire OK

Exemples curl:
```sh
curl -X POST http://localhost:5000/api/auth/magic-link -H 'content-type: application/json' -d '{"email":"test@example.com"}'
# copier le token depuis les logs: /api/auth/verify?token=...
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/verify -H 'content-type: application/json' -d '{"token":"PASTE"}' | jq -r .access_token)

POST_ID=$(curl -s -X POST http://localhost:5000/api/posts -H "authorization: Bearer $TOKEN" -H 'content-type: application/json' -d '{"target_url":"https://example.com"}' | jq -r .post_id)
SHORT=$(curl -s -X POST http://localhost:5000/api/links -H "authorization: Bearer $TOKEN" -H 'content-type: application/json' -d '{"post_id':"'$POST_ID'"}' )
```

## Observabilité
- Prometheus: `/metrics`
- Logs: format JSON simplifié via logging Python

## Notes
- Alembic initiale sous `alembic/versions/0001_init.py`. En dev SQLite, `app/main.py` crée les tables si absentes. En prod, exécutez les migrations.
- Aucune dépendance Redis n’est requise pour l’instant (vitesse antifraude en mémoire).
- Langue par défaut: FR. UI sombre Tailwind.

## Déploiement Railway
Ce repo est prêt pour Railway (Docker). Fichiers utiles:
- `railway.toml` (healthcheck, build Dockerfile)
- `Dockerfile` (multi-stage: build Vite → copie vers `app/static/`)

Étapes:
1) Créez un projet Railway et déployez ce repo (Docker auto).
2) Ajoutez un service Postgres Railway et récupérez la chaine `DATABASE_URL` (psycopg2).
3) Variables d'env à définir:
   - `DATABASE_URL` → Postgres Railway (ex: `postgresql+psycopg2://user:pass@host:5432/db`)
   - `JWT_SECRET` → secret robuste
   - `ADMIN_TOKEN` → token admin
   - Optionnel: `COUNTRY_ALLOWLIST`, `ASN_DENYLIST`, `CPC_*`
4) Domaine public Railway: `RAILWAY_PUBLIC_DOMAIN` est fourni par la plateforme. L'app ajuste automatiquement `APP_BASE_URL` et `PUBLIC_BASE_URL` vers `https://<domaine>`.
5) Healthcheck: Railway vérifiera `GET /healthz`.

Après déploiement: accédez à `/` (SPA), `/docs` (OpenAPI), `/metrics` (Prometheus).

## Légal produit
Formulez la rémunération comme « trafic qualifié via programme partenaire », éviter « payé pour cliquer ».

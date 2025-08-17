from __future__ import annotations

# Stub AI service: returns French text using a placeholder "GPT-5 low reasoning".

def generate_asset(title_hint: str | None = None) -> dict:
    title = title_hint or "Idée d'article inspirante"
    summary = (
        "Contenu généré par IA (placeholder GPT-5 low reasoning). "
        "Un court résumé en français adapté au marketing partenaire."
    )
    payload = {"model": "gpt-5-low-reasoning", "lang": "fr", "keywords": ["partenariat", "trafic qualifié"]}
    return {"title": title, "summary": summary, "payload": payload}

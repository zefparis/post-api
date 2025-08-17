import React, { useState } from "react";

export default function EmailSignInCard() {
  const [email, setEmail] = useState("");
  const [state, setState] = useState<"idle"|"loading"|"ok"|"err">("idle");
  const [msg, setMsg] = useState<string>("");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setState("loading");
    setMsg("");

    try {
      const res = await fetch("/api/auth/magic-link", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) {
        const t = await res.text();
        throw new Error(t || `HTTP ${res.status}`);
      }
      setState("ok");
      setMsg("Lien magique envoyé. Check ta boîte mail 👌");
    } catch (err: any) {
      setState("err");
      setMsg(err?.message ?? "Erreur réseau");
    }
  }

  return (
    <div className="bg-card/70 border border-white/10 rounded-2xl p-6 shadow-soft max-w-lg w-full">
      <h3 className="text-lg font-semibold text-ink mb-2">Se connecter par e-mail</h3>
      <p className="text-sm text-ink/60 mb-4">
        On t’envoie un lien magique. Pas de mot de passe.
      </p>
      <form onSubmit={onSubmit} className="flex gap-2">
        <input
          type="email"
          required
          placeholder="votre@email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="flex-1 bg-bg/60 text-ink placeholder:text-ink/40 border border-white/10 rounded-xl px-3 py-2 outline-none focus:border-accent"
        />
        <button
          type="submit"
          disabled={state === "loading"}
          className="px-4 py-2 rounded-xl bg-accent text-white font-medium disabled:opacity-60"
        >
          {state === "loading" ? "Envoi..." : "Envoyer"}
        </button>
      </form>
      {msg && (
        <div className={`mt-3 text-sm ${state === "err" ? "text-red-400" : "text-ink/80"}`}>
          {msg}
        </div>
      )}
    </div>
  );
}

import React from "react";
import NavBar from "./components/NavBar";
import EmailSignInCard from "./components/EmailSignInCard";

export default function App() {
  return (
    <div className="min-h-screen bg-bg text-ink">
      <NavBar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Smoke banner (tu peux virer quand t’es good) */}
        <div className="p-4 mb-6 rounded-2xl shadow-soft bg-accent text-white font-medium">
          TAILWIND_OK
        </div>

        <section className="grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold leading-tight">
              ContentFlow
            </h1>
            <p className="mt-3 text-ink/70">
              Générez des liens courts et suivez un trafic qualifié via notre programme partenaire.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <a href="/generate" className="px-4 py-2 rounded-xl bg-accent text-white shadow-soft">Générer un lien</a>
              <a href="/docs" className="px-4 py-2 rounded-xl border border-white/10 hover:bg-white/5">Docs</a>
            </div>
          </div>

          <div className="flex justify-center">
            <EmailSignInCard />
          </div>
        </section>
      </main>
    </div>
  );
}

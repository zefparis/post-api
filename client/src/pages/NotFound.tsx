import React from "react";
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="text-center py-24">
      <h1 className="text-5xl font-extrabold tracking-tight">404</h1>
      <p className="mt-3 text-ink/70">Page introuvable.</p>
      <div className="mt-6">
        <Link to="/" className="px-4 py-2 rounded-xl bg-accent text-white shadow-soft">
          Retour à l’accueil
        </Link>
      </div>
    </div>
  );
}

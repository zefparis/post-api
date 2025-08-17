import React from "react";

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-sm text-ink/60 flex flex-col md:flex-row items-center justify-between gap-2">
        <p>
          © {new Date().getFullYear()} ContentFlow. Tous droits réservés.
        </p>
        <nav className="flex items-center gap-4">
          <a className="hover:text-ink" href="/docs">Docs</a>
          <a className="hover:text-ink" href="/admin">Admin</a>
        </nav>
      </div>
    </footer>
  );
}

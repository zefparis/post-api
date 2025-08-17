import React from "react";

export default function NavBar() {
  return (
    <nav className="sticky top-0 z-50 bg-bg/80 backdrop-blur supports-[backdrop-filter]:bg-bg/60 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        <a href="/" className="font-semibold tracking-wide text-ink">ContentFlow</a>
        <div className="flex items-center gap-3 text-sm">
          <a href="/dashboard" className="px-3 py-1.5 rounded-lg hover:bg-white/5 text-ink/80 hover:text-ink transition">Dashboard</a>
          <a href="/generate"  className="px-3 py-1.5 rounded-lg hover:bg-white/5 text-ink/80 hover:text-ink transition">Générer lien</a>
          <a href="/admin"     className="px-3 py-1.5 rounded-lg hover:bg-white/5 text-ink/80 hover:text-ink transition">Admin</a>
        </div>
      </div>
    </nav>
  );
}

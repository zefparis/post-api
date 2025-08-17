import React from "react";
import { NavLink } from "react-router-dom";

const linkBase =
  "px-3 py-1.5 rounded-lg transition text-ink/80 hover:text-ink hover:bg-white/5";

export default function NavBar() {
  return (
    <nav className="sticky top-0 z-50 bg-bg/80 backdrop-blur supports-[backdrop-filter]:bg-bg/60 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        <NavLink to="/" className="font-semibold tracking-wide text-ink">
          ContentFlow
        </NavLink>
        <div className="flex items-center gap-3 text-sm">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `${linkBase} ${isActive ? "bg-white/5 text-ink" : ""}`
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/generate"
            className={({ isActive }) =>
              `${linkBase} ${isActive ? "bg-white/5 text-ink" : ""}`
            }
          >
            Générer lien
          </NavLink>
          <NavLink
            to="/admin"
            className={({ isActive }) =>
              `${linkBase} ${isActive ? "bg-white/5 text-ink" : ""}`
            }
          >
            Admin
          </NavLink>
        </div>
      </div>
    </nav>
  );
}

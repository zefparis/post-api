import React from "react";
import { Outlet } from "react-router-dom";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="min-h-screen bg-bg text-ink">
      {/* Decorative background */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 -z-10 opacity-40"
        style={{
          background:
            "radial-gradient(60rem 30rem at 20% -10%, rgba(124,58,237,.25), transparent 60%), radial-gradient(40rem 20rem at 80% 10%, rgba(124,58,237,.18), transparent 60%)",
        }}
      />

      <NavBar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Smoke banner (tu peux virer quand t’es good) */}
        <div className="p-4 mb-6 rounded-2xl shadow-soft bg-accent text-white font-medium">
          TAILWIND_OK
        </div>

        {/* Routed content */}
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}

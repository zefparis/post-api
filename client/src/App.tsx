import React from 'react'
import { Link, Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div className="min-h-screen bg-bg text-ink">
      <header className="container mx-auto py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-semibold">ContentFlow</Link>
        <nav className="flex gap-4">
          <Link to="/dashboard" className="hover:text-accent">Dashboard</Link>
          <Link to="/generer" className="hover:text-accent">Générer lien</Link>
          <Link to="/admin" className="hover:text-accent">Admin</Link>
        </nav>
      </header>
      <main className="container mx-auto px-4 pb-12">
        <Outlet />
      </main>
    </div>
  )
}

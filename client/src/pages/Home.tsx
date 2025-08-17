import React, { useState } from 'react'
import Card from '../components/Card'

export default function Home() {
  const [email, setEmail] = useState('')
  const [link, setLink] = useState<string | null>(null)
  const send = async () => {
    await fetch('/api/auth/magic-link', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email }) })
    setLink('Regardez les logs du serveur pour le lien magique (mode dev).')
  }
  return (
    <div className="grid gap-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold">ContentFlow</h1>
      <p className="text-white/80">Générez des liens courts et suivez un trafic qualifié via notre programme partenaire.</p>
      <Card>
        <div className="flex gap-2">
          <input className="flex-1 bg-card/80 rounded-xl px-3 py-2" placeholder="votre@email"
                 value={email} onChange={e=>setEmail(e.target.value)} />
          <button className="px-4 py-2 bg-accent rounded-xl" onClick={send}>Se connecter par e-mail</button>
        </div>
        {link && <p className="mt-2 text-sm text-white/70">{link}</p>}
      </Card>
    </div>
  )
}

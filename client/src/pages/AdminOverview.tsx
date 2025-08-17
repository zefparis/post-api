import React, { useState } from 'react'
import Card from '../components/Card'

export default function AdminOverview() {
  const [token, setToken] = useState('changeme-admin')
  const [data, setData] = useState<any>({})
  const load = async () => {
    const r = await fetch('/api/admin/overview', { headers: { Authorization: `Bearer ${token}` } })
    setData(await r.json())
  }
  return (
    <div className="grid gap-4 max-w-xl">
      <Card>
        <div className="grid gap-2">
          <label className="text-sm">Token admin (.env)</label>
          <input className="bg-card/80 rounded-xl px-3 py-2" value={token} onChange={e=>setToken(e.target.value)} />
          <button className="px-4 py-2 bg-accent rounded-xl" onClick={load}>Charger</button>
        </div>
      </Card>
      <Card>
        <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(data, null, 2)}</pre>
      </Card>
    </div>
  )
}

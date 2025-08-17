import React, { useState } from 'react'
import Card from '../components/Card'

export default function GenerateLink() {
  const [url, setUrl] = useState('https://example.com')
  const [shortUrl, setShortUrl] = useState<string>('')
  const [token, setToken] = useState(localStorage.getItem('cf_token') || '')

  const create = async () => {
    if (!token) { alert('Connectez-vous via lien magique puis collez le token ici.'); return }
    const postRes = await fetch('/api/posts', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify({ target_url: url }) })
    const post = await postRes.json()
    const linkRes = await fetch('/api/links', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify({ post_id: post.post_id }) })
    const l = await linkRes.json()
    setShortUrl(l.url)
  }

  return (
    <div className="grid gap-4 max-w-xl">
      <Card>
        <div className="grid gap-2">
          <label className="text-sm">Token (JWT) partenaire</label>
          <input className="bg-card/80 rounded-xl px-3 py-2" value={token} onChange={e=>{setToken(e.target.value); localStorage.setItem('cf_token', e.target.value)}} />
        </div>
      </Card>
      <Card>
        <div className="grid gap-2">
          <label className="text-sm">URL de destination</label>
          <input className="bg-card/80 rounded-xl px-3 py-2" value={url} onChange={e=>setUrl(e.target.value)} />
          <button onClick={create} className="mt-2 px-4 py-2 bg-accent rounded-xl">Générer un lien</button>
        </div>
      </Card>
      {shortUrl && (
        <Card>
          <div className="flex items-center gap-2">
            <input readOnly className="flex-1 bg-card/80 rounded-xl px-3 py-2" value={shortUrl} />
            <button className="px-3 py-2 bg-accent rounded-xl" onClick={()=>navigator.clipboard.writeText(shortUrl)}>Copier</button>
          </div>
        </Card>
      )}
    </div>
  )
}

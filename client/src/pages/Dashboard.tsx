import React, { useEffect, useState } from 'react'
import Card from '../components/Card'
import Stat from '../components/Stat'

export default function Dashboard() {
  const [stats, setStats] = useState<any>({ raw_clicks: 0, payable_clicks: 0, earnings: 0, epc: 0, links: 0 })
  useEffect(() => {
    const token = localStorage.getItem('cf_token')
    if (!token) return
    fetch('/api/partner/stats/summary', { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(setStats).catch(()=>{})
  }, [])
  return (
    <div className="grid gap-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card><Stat label="Clics bruts" value={stats.raw_clicks} /></Card>
        <Card><Stat label="Clics qualifiés" value={stats.payable_clicks} /></Card>
        <Card><Stat label="Gains (€)" value={stats.earnings.toFixed?.(2) ?? stats.earnings} /></Card>
        <Card><Stat label="EPC" value={stats.epc.toFixed?.(2) ?? stats.epc} /></Card>
      </div>
    </div>
  )
}

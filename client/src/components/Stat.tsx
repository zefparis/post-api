import React from 'react'

export default function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="text-center">
      <div className="text-2xl font-semibold">{value}</div>
      <div className="text-sm text-white/60">{label}</div>
    </div>
  )
}

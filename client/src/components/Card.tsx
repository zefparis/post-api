import React from 'react'

export default function Card({ children, className = '' }: { children: React.ReactNode, className?: string }) {
  return (
    <div className={`rounded-2xl bg-card/70 shadow-soft p-5 border border-white/5 ${className}`}>
      {children}
    </div>
  )
}

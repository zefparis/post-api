import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './index.css'
import App from './App'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import GenerateLink from './pages/GenerateLink'
import AdminOverview from './pages/AdminOverview'
import NotFound from './pages/NotFound'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}> 
          <Route index element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/generate" element={<GenerateLink />} />
          <Route path="/admin" element={<AdminOverview />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)

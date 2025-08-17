module.exports = {
  darkMode: 'class',
  content: ['./client/index.html','./client/src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: { bg:'#0b0f17', card:'#121826', ink:'#e5e7eb', accent:'#7c3aed' },
      boxShadow: { soft: '0 10px 30px rgba(0,0,0,.35)' }
    }
  },
  plugins: [],
}

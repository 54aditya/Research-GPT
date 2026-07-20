import { Link, Route, Routes } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import ProjectDetails from './pages/ProjectDetails'

function App() {
  return (
    <div className="min-h-screen bg-transparent text-slate-100">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <Link to="/" className="text-xl font-semibold tracking-wide">
          AI Research Presentation Generator
        </Link>
        <div className="flex gap-3">
          <Link to="/dashboard" className="rounded-full bg-cyan-500 px-4 py-2 text-sm font-medium text-slate-950">Dashboard</Link>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/projects/:projectId" element={<ProjectDetails />} />
      </Routes>
    </div>
  )
}

export default App
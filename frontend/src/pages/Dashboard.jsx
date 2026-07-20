import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function Dashboard() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState([])
  const [topic, setTopic] = useState('')
  const [slideCount, setSlideCount] = useState(8)
  const [style, setStyle] = useState('professional')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.get('/projects').then((res) => setProjects(res.data)).catch((err) => {
      console.error('Failed to load projects', err)
      setError('Failed to load projects')
    })
  }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      console.log('Creating project with:', { topic, slide_count: slideCount, presentation_style: style })
      const response = await api.post('/projects', { topic, slide_count: slideCount, presentation_style: style })
      console.log('Project created:', response.data)
      setProjects([response.data, ...projects])
      setTopic('')
      navigate(`/projects/${response.data.id}`)
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to create project'
      console.error('Error creating project:', errorMsg)
      setError(errorMsg)
    } finally {
      setLoading(true)
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-6 pb-16 pt-6">
      <div className="mb-8 rounded-3xl border border-white/10 bg-slate-900/60 p-6 backdrop-blur">
        <h1 className="text-3xl font-semibold">Create a new research presentation</h1>
        {error && <div className="mt-4 rounded-2xl border border-red-500/50 bg-red-500/10 px-4 py-3 text-red-200">{error}</div>}
        <form onSubmit={handleCreate} className="mt-6 grid gap-4 md:grid-cols-3">
          <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Research topic" className="rounded-2xl border border-white/10 bg-slate-800/70 px-4 py-3" required />
          <input type="number" min="3" max="20" value={slideCount} onChange={(e) => setSlideCount(Number(e.target.value))} className="rounded-2xl border border-white/10 bg-slate-800/70 px-4 py-3" />
          <select value={style} onChange={(e) => setStyle(e.target.value)} className="rounded-2xl border border-white/10 bg-slate-800/70 px-4 py-3">
            <option value="professional">Professional</option>
            <option value="executive">Executive</option>
            <option value="academic">Academic</option>
          </select>
          <button disabled={loading} className="md:col-span-3 rounded-2xl bg-cyan-500 px-4 py-3 font-medium text-slate-950 disabled:opacity-50">{loading ? 'Generating...' : 'Generate Presentation'}</button>
        </form>
      </div>

      <div className="grid gap-4">
        {projects.map((project) => (
          <div key={project.id} className="rounded-3xl border border-white/10 bg-white/10 p-5 backdrop-blur">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-semibold">{project.topic}</h2>
                <p className="text-sm text-slate-300">{project.slide_count} slides • {project.presentation_style}</p>
              </div>
              <span className="rounded-full bg-cyan-500/15 px-3 py-1 text-sm text-cyan-300">{project.status}</span>
            </div>
            <div className="mt-4 flex gap-3">
              <button onClick={() => navigate(`/projects/${project.id}`)} className="rounded-full border border-white/10 px-4 py-2 text-sm">Open</button>
            </div>
          </div>
        ))}
      </div>
    </main>
  )
}

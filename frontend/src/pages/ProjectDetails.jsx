import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

export default function ProjectDetails() {
  const { projectId } = useParams()
  const [project, setProject] = useState(null)

  useEffect(() => {
    let timer

    const fetchProject = async () => {
      try {
        const res = await api.get(`/projects/${projectId}`)
        setProject(res.data)
        if (res.data.status !== 'COMPLETED' && res.data.status !== 'FAILED') {
          timer = setTimeout(fetchProject, 3000)
        }
      } catch (err) {
        console.error('Failed to load project', err)
      }
    }

    fetchProject()

    return () => {
      if (timer) clearTimeout(timer)
    }
  }, [projectId])

  const handleDownloadPPT = () => {
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const downloadUrl = `${baseUrl}/projects/${projectId}/download`
    window.location.href = downloadUrl
  }

  if (!project) return <div className="px-6 py-10 text-slate-300">Loading...</div>

  return (
    <main className="mx-auto max-w-7xl px-6 pb-16 pt-6">
      <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 backdrop-blur">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold">{project.topic}</h1>
            <p className="mt-1 text-slate-300">Status: {project.status}</p>
          </div>
          <button onClick={handleDownloadPPT} disabled={!project.ppt_path} className="rounded-full bg-cyan-500 px-4 py-2 font-medium text-slate-950 disabled:opacity-50">Download PPT</button>
        </div>
        <div className="mt-8 grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
          <div className="space-y-4">
            {project.slides.map((slide, index) => (
              <div key={index} className="rounded-2xl border border-white/10 bg-white/10 p-4">
                <h2 className="text-lg font-semibold">{slide.title}</h2>
                <p className="mt-2 text-sm text-slate-300">{slide.content}</p>
                {slide.diagram ? <pre className="mt-3 overflow-x-auto rounded-xl bg-slate-950/80 p-3 text-xs">{slide.diagram}</pre> : null}
              </div>
            ))}
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/10 p-4">
            <h3 className="text-lg font-semibold">Progress</h3>
            <ul className="mt-4 space-y-2 text-sm text-slate-300">
              {project.logs.map((log, index) => <li key={index}>• {log}</li>)}
            </ul>
            <h3 className="mt-6 text-lg font-semibold">References</h3>
            <ul className="mt-4 space-y-2 text-sm text-slate-300">
              {project.references.map((reference, index) => <li key={index}>• {reference}</li>)}
            </ul>
          </div>
        </div>
      </div>
    </main>
  )
}

import { ArrowRight, Sparkles, ShieldCheck, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <main className="mx-auto flex max-w-7xl flex-col gap-10 px-6 pb-16 pt-10 lg:flex-row lg:items-center">
      <section className="max-w-2xl">
        <div className="mb-6 inline-flex items-center rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-300">
          <Sparkles className="mr-2 h-4 w-4" /> AI-powered research to presentation
        </div>
        <h1 className="text-4xl font-semibold leading-tight sm:text-6xl">
          Generate polished research presentations in minutes.
        </h1>
        <p className="mt-6 text-lg text-slate-300">
          Enter a topic, select a slide count, and let the system search papers, build a retrieval pipeline, and create a professional PowerPoint deck.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link to="/dashboard" className="inline-flex items-center rounded-full bg-cyan-500 px-5 py-3 font-medium text-slate-950">Start creating <ArrowRight className="ml-2 h-4 w-4" /></Link>
        </div>
        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/10 p-4 backdrop-blur">
            <ShieldCheck className="mb-3 h-6 w-6 text-cyan-400" />
            <h3 className="font-medium">Cited research</h3>
            <p className="mt-2 text-sm text-slate-300">Every slide includes research-backed references.</p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/10 p-4 backdrop-blur">
            <Zap className="mb-3 h-6 w-6 text-cyan-400" />
            <h3 className="font-medium">Real-time progress</h3>
            <p className="mt-2 text-sm text-slate-300">Track generation status as papers, embeddings, and slides come together.</p>
          </div>
        </div>
      </section>
      <div className="w-full max-w-xl rounded-3xl border border-white/10 bg-slate-900/60 p-8 shadow-2xl shadow-cyan-950/30 backdrop-blur">
        <h2 className="text-2xl font-semibold">What the workflow does</h2>
        <ul className="mt-6 space-y-3 text-sm text-slate-300">
          <li>• Searches research papers and downloads relevant PDFs</li>
          <li>• Extracts text, chunks documents, and builds vector embeddings</li>
          <li>• Retrieves context with RAG and generates slide content</li>
          <li>• Produces a professional PowerPoint deck with citations and notes</li>
        </ul>
      </div>
    </main>
  )
}

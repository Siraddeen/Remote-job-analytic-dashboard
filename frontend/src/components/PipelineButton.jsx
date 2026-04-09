import { useState } from 'react'
import { runPipeline } from '../services/api'

export default function PipelineButton({ onSuccess }) {
  const [status, setStatus] = useState('idle') // idle | running | done | error

  const handleRun = async () => {
    setStatus('running')
    try {
      await runPipeline()
      setStatus('done')
      setTimeout(() => setStatus('idle'), 3000)
      if (onSuccess) onSuccess()
    } catch (e) {
      setStatus('error')
      setTimeout(() => setStatus('idle'), 4000)
    }
  }

  const labels = {
    idle:    '▶ Run ETL Pipeline',
    running: '⏳ Running...',
    done:    '✅ Done!',
    error:   '❌ Error — retry?',
  }
  const colors = {
    idle:    'bg-sky-600 hover:bg-sky-500',
    running: 'bg-slate-600 cursor-not-allowed',
    done:    'bg-emerald-600',
    error:   'bg-red-600',
  }

  return (
    <button
      onClick={handleRun}
      disabled={status === 'running'}
      className={`text-sm font-mono font-semibold text-white px-4 py-2 rounded-lg transition-all ${colors[status]}`}
    >
      {labels[status]}
    </button>
  )
}

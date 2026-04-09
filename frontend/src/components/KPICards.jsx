export default function KPICards({ stats, loading }) {
  const cards = [
    { label: 'Total Jobs',       value: stats?.total_jobs,       color: 'text-sky-400',     icon: '💼' },
    { label: 'Companies',        value: stats?.total_companies,  color: 'text-emerald-400', icon: '🏢' },
    { label: 'Categories',       value: stats?.total_categories, color: 'text-violet-400',  icon: '🗂️' },
    { label: 'Added Today',      value: stats?.jobs_today,       color: 'text-amber-400',   icon: '🆕' },
  ]

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="kpi-card animate-pulse">
            <div className="h-8 w-24 bg-slate-700 rounded mb-2" />
            <div className="h-4 w-20 bg-slate-700 rounded" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((c) => (
        <div key={c.label} className="kpi-card">
          <div className="text-2xl mb-1">{c.icon}</div>
          <div className={`text-3xl font-bold font-mono ${c.color}`}>
            {c.value ?? '—'}
          </div>
          <div className="text-sm text-slate-400">{c.label}</div>
        </div>
      ))}
    </div>
  )
}

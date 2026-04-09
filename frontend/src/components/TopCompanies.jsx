export default function TopCompanies({ data, loading }) {
  if (loading) {
    return (
      <div className="card">
        <p className="section-title">Top Hiring Companies</p>
        <div className="space-y-2">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="h-8 bg-slate-800 animate-pulse rounded" />
          ))}
        </div>
      </div>
    )
  }

  const max = data[0]?.job_count || 1

  return (
    <div className="card">
      <p className="section-title">Top Hiring Companies</p>
      <div className="space-y-3">
        {data.map((c, i) => (
          <div key={i}>
            <div className="flex justify-between items-center mb-1">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 font-mono w-4">{i + 1}</span>
                <span className="text-sm text-slate-200 truncate max-w-[180px]">{c.company_name}</span>
              </div>
              <span className="text-sm font-mono text-accent">{c.job_count}</span>
            </div>
            <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-sky-500 to-emerald-400"
                style={{ width: `${(c.job_count / max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

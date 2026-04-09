const TYPE_BADGE = {
  full_time:  'badge badge-blue',
  contract:   'badge badge-amber',
  part_time:  'badge badge-green',
  freelance:  'badge badge-green',
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}

export default function LatestJobs({ data, loading }) {
  if (loading) {
    return (
      <div className="card">
        <p className="section-title">Latest Job Listings</p>
        <div className="space-y-2">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-12 bg-slate-800 animate-pulse rounded" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="card overflow-x-auto">
      <p className="section-title">Latest Job Listings</p>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border text-slate-400 text-xs uppercase tracking-wide">
            <th className="text-left pb-3 pr-4">Title</th>
            <th className="text-left pb-3 pr-4">Company</th>
            <th className="text-left pb-3 pr-4">Category</th>
            <th className="text-left pb-3 pr-4">Type</th>
            <th className="text-left pb-3 pr-4">Salary</th>
            <th className="text-left pb-3">Date</th>
          </tr>
        </thead>
        <tbody>
          {data.map((job, i) => (
            <tr
              key={i}
              className="border-b border-border/50 hover:bg-slate-800/50 transition-colors"
            >
              <td className="py-3 pr-4">
                {job.url ? (
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-accent hover:underline font-medium truncate block max-w-[220px]"
                  >
                    {job.title}
                  </a>
                ) : (
                  <span className="font-medium truncate block max-w-[220px]">{job.title}</span>
                )}
              </td>
              <td className="py-3 pr-4 text-slate-300 truncate max-w-[140px]">{job.company_name}</td>
              <td className="py-3 pr-4">
                <span className="text-xs text-slate-400">{job.category || '—'}</span>
              </td>
              <td className="py-3 pr-4">
                <span className={TYPE_BADGE[job.job_type] || 'badge badge-blue'}>
                  {job.job_type?.replace('_', ' ') || '—'}
                </span>
              </td>
              <td className="py-3 pr-4 text-slate-400 text-xs max-w-[100px] truncate">
                {job.salary && job.salary !== 'Not disclosed' ? job.salary : '—'}
              </td>
              <td className="py-3 text-slate-500 text-xs whitespace-nowrap">
                {formatDate(job.publication_date)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Area, AreaChart
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="bg-card border border-border rounded-lg px-3 py-2 text-sm">
        <p className="text-slate-400 text-xs">{label}</p>
        <p className="text-accent font-semibold">{payload[0].value} jobs</p>
      </div>
    )
  }
  return null
}

export default function TimelineChart({ data, loading }) {
  if (loading) return <div className="h-72 bg-slate-800 animate-pulse rounded-lg" />

  // Sort ascending for chart display
  const sorted = [...data].sort((a, b) => a.date > b.date ? 1 : -1)

  return (
    <div className="card">
      <p className="section-title">Jobs Published Over Time (Last 30 Days)</p>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={sorted} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <defs>
            <linearGradient id="colorJobs" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="date"
            tick={{ fill: '#94a3b8', fontSize: 10 }}
            tickFormatter={(d) => d?.slice(5)}  // show MM-DD only
            interval="preserveStartEnd"
          />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="job_count"
            stroke="#38bdf8"
            strokeWidth={2}
            fill="url(#colorJobs)"
            dot={false}
            activeDot={{ r: 5, fill: '#38bdf8' }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

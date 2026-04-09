import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from 'recharts'

const COLORS = [
  '#38bdf8','#34d399','#fb923c','#a78bfa',
  '#f472b6','#facc15','#4ade80','#60a5fa',
  '#f87171','#2dd4bf','#c084fc','#fbbf24',
]

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div className="bg-card border border-border rounded-lg px-3 py-2 text-sm">
        <p className="font-semibold text-white">{payload[0].payload.category}</p>
        <p className="text-accent">{payload[0].value} jobs</p>
      </div>
    )
  }
  return null
}

export default function CategoryChart({ data, loading }) {
  if (loading) return <div className="h-72 bg-slate-800 animate-pulse rounded-lg" />

  return (
    <div className="card">
      <p className="section-title">Jobs by Category</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="category"
            tick={{ fill: '#94a3b8', fontSize: 11 }}
            angle={-40}
            textAnchor="end"
            interval={0}
          />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="job_count" radius={[4, 4, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

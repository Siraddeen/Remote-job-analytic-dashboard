import {
  PieChart, Pie, Cell, Tooltip,
  Legend, ResponsiveContainer
} from 'recharts'

const COLORS = ['#38bdf8', '#34d399', '#fb923c', '#a78bfa', '#f472b6', '#facc15']

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div className="bg-card border border-border rounded-lg px-3 py-2 text-sm">
        <p className="font-semibold text-white">{payload[0].payload.job_type}</p>
        <p className="text-accent">{payload[0].value} jobs</p>
      </div>
    )
  }
  return null
}

const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  if (percent < 0.05) return null
  const RADIAN = Math.PI / 180
  const r = innerRadius + (outerRadius - innerRadius) * 0.55
  const x = cx + r * Math.cos(-midAngle * RADIAN)
  const y = cy + r * Math.sin(-midAngle * RADIAN)
  return (
    <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={12} fontWeight={600}>
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

export default function JobTypeChart({ data, loading }) {
  if (loading) return <div className="h-72 bg-slate-800 animate-pulse rounded-lg" />

  return (
    <div className="card">
      <p className="section-title">Job Type Distribution</p>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="job_count"
            nameKey="job_type"
            cx="50%"
            cy="50%"
            outerRadius={110}
            labelLine={false}
            label={renderLabel}
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            formatter={(val) => <span style={{ color: '#94a3b8', fontSize: 12 }}>{val}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

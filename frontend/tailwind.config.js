/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        dark: "#0f172a",
        card: "#1e293b",
        border: "#334155",
        accent: "#38bdf8",
        success: "#34d399",
        warn: "#fb923c",
      },
    },
  },
  plugins: [],
}

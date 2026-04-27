"use client";

const SEVERITY_STYLES = {
  high: {
    border: "border-red-500/40",
    bg: "bg-red-500/10",
    badge: "bg-red-500/20 text-red-400 ring-red-500/30",
    glow: "from-red-500/20",
    icon: "🔴",
    label: "High",
  },
  moderate: {
    border: "border-amber-500/40",
    bg: "bg-amber-500/10",
    badge: "bg-amber-500/20 text-amber-400 ring-amber-500/30",
    glow: "from-amber-500/20",
    icon: "🟡",
    label: "Moderate",
  },
  low: {
    border: "border-emerald-500/40",
    bg: "bg-emerald-500/10",
    badge: "bg-emerald-500/20 text-emerald-400 ring-emerald-500/30",
    glow: "from-emerald-500/20",
    icon: "🟢",
    label: "Low",
  },
  unknown: {
    border: "border-gray-500/40",
    bg: "bg-gray-500/10",
    badge: "bg-gray-500/20 text-gray-400 ring-gray-500/30",
    glow: "from-gray-500/20",
    icon: "⚪",
    label: "Unknown",
  },
};

export default function ResultCard({ result, index }) {
  const sev = SEVERITY_STYLES[result.severity?.toLowerCase()] || SEVERITY_STYLES.unknown;

  return (
    <div
      className={`group relative rounded-2xl border ${sev.border} bg-gray-900/80 backdrop-blur-lg overflow-hidden transition-all duration-500 hover:scale-[1.01] hover:shadow-2xl`}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Top glow line */}
      <div className={`absolute top-0 left-0 right-0 h-px bg-gradient-to-r ${sev.glow} via-transparent to-transparent`} />

      <div className="p-6">
        {/* Header row */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className={`flex items-center justify-center w-10 h-10 rounded-xl ${sev.bg} text-lg`}>
              {sev.icon}
            </div>
            <div>
              <h3 className="text-white font-bold text-base">
                {result.pair[0]}
                <span className="text-gray-500 mx-2">×</span>
                {result.pair[1]}
              </h3>
              <p className="text-xs text-gray-500 mt-0.5 capitalize">{result.type}</p>
            </div>
          </div>

          <div className="flex flex-col items-end gap-1.5">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ring-1 ${sev.badge}`}>
              {sev.label} Severity
            </span>
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ring-1 ${
                result.confidence === "high"
                  ? "bg-cyan-500/10 text-cyan-400 ring-cyan-500/30"
                  : "bg-gray-500/10 text-gray-400 ring-gray-500/30"
              }`}
            >
              {result.confidence === "high" ? "✓ Verified" : "⚡ AI Generated"}
            </span>
          </div>
        </div>

        {/* Interaction summary */}
        <div className={`rounded-xl p-4 ${sev.bg} mb-4`}>
          <p className="text-sm font-medium text-gray-200 leading-relaxed">
            {result.interaction}
          </p>
        </div>

        {/* Explanation */}
        <div className="mb-4">
          <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
            Explanation
          </h4>
          <p className="text-sm text-gray-300 leading-relaxed">
            {result.explanation}
          </p>
        </div>

        {/* Source badge */}
        <div className="flex items-center gap-2 mb-3">
          <span className="text-xs text-gray-500">Source:</span>
          <span
            className={`text-xs px-2 py-0.5 rounded-md ${
              result.source === "database"
                ? "bg-cyan-500/10 text-cyan-400"
                : "bg-purple-500/10 text-purple-400"
            }`}
          >
            {result.source === "database" ? "📚 Database" : "🤖 LLM"}
          </span>
        </div>

        {/* Disclaimer */}
        {result.disclaimer && (
          <div className="rounded-xl bg-amber-500/5 border border-amber-500/20 p-4">
            <div className="flex gap-2">
              <span className="text-amber-400 text-sm shrink-0">⚠️</span>
              <p className="text-xs text-amber-300/80 leading-relaxed">
                {result.disclaimer}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

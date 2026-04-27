"use client";

const SEVERITY_STYLES = {
  high: {
    border: "border-red-200",
    bg: "bg-red-50",
    badge: "bg-red-100 text-red-800 border border-red-200",
    icon: "⚠️",
    label: "High",
    accent: "text-red-600",
  },
  moderate: {
    border: "border-amber-200",
    bg: "bg-amber-50",
    badge: "bg-amber-100 text-amber-800 border border-amber-200",
    icon: "⚡",
    label: "Moderate",
    accent: "text-amber-600",
  },
  low: {
    border: "border-emerald-200",
    bg: "bg-emerald-50",
    badge: "bg-emerald-100 text-emerald-800 border border-emerald-200",
    icon: "✓",
    label: "Low",
    accent: "text-emerald-600",
  },
  unknown: {
    border: "border-gray-200",
    bg: "bg-gray-50",
    badge: "bg-gray-100 text-gray-800 border border-gray-200",
    icon: "ℹ️",
    label: "Unknown",
    accent: "text-gray-600",
  },
};

export default function ResultCard({ result, index }) {
  const sev = SEVERITY_STYLES[result.severity?.toLowerCase()] || SEVERITY_STYLES.unknown;

  return (
    <div
      className={`relative rounded-lg border ${sev.border} ${sev.bg} overflow-hidden transition-all duration-300 hover:shadow-md`}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <div className="p-6">
        {/* Header row */}
        <div className="flex items-start justify-between mb-5">
          <div className="flex items-center gap-4 flex-1">
            <div className={`flex items-center justify-center w-12 h-12 rounded-lg flex-shrink-0 font-lg ${sev.bg} ${sev.accent}`}>
              {sev.icon}
            </div>
            <div>
              <h3 className="text-gray-900 font-bold text-lg">
                {result.pair[0]}
                <span className="text-gray-400 mx-2">+</span>
                {result.pair[1]}
              </h3>
              <p className="text-xs text-gray-600 mt-1 capitalize">{result.type}</p>
            </div>
          </div>

          <div className="flex flex-col items-end gap-2 flex-shrink-0">
            <span className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-semibold ${sev.badge}`}>
              {sev.label}
            </span>
            <span
              className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium ${
                result.confidence === "high"
                  ? "bg-blue-100 text-blue-800 border border-blue-200"
                  : "bg-gray-100 text-gray-800 border border-gray-200"
              }`}
            >
              {result.confidence === "high" ? "Database" : "AI Analysis"}
            </span>
          </div>
        </div>

        {/* Interaction summary */}
        <div className="mb-5 pb-5 border-b border-gray-200">
          <p className="text-sm font-medium text-gray-900 leading-relaxed">
            {result.interaction}
          </p>
        </div>

        {/* Explanation */}
        <div className="mb-5">
          <h4 className="text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2">
            Mechanism
          </h4>
          <p className="text-sm text-gray-700 leading-relaxed">
            {result.explanation}
          </p>
        </div>

        {/* Disclaimer */}
        {result.disclaimer && (
          <div className="rounded-lg bg-amber-50 border border-amber-200 p-4 mb-4">
            <div className="flex gap-3">
              <span className="text-amber-600 text-sm shrink-0 font-bold">⚠️</span>
              <p className="text-xs text-amber-900 leading-relaxed">
                {result.disclaimer}
              </p>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200 text-xs text-gray-600">
          <span>
            Source: <strong className="text-gray-900">{result.source === "database" ? "Medical Database" : "AI Generated"}</strong>
          </span>
        </div>
      </div>
    </div>
  );
}

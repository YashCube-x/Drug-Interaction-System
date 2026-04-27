"use client";

import { useState } from "react";
import axios from "axios";
import InputBox from "./components/InputBox";
import ResultCard from "./components/ResultCard";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:1001";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const handleAnalyze = async (text) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await axios.post(`${API_URL}/analyze`, { text });
      setData(response.data);
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        err.message ||
        "An unexpected error occurred.";
      setError(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white relative overflow-hidden">
      {/* Background effects */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-cyan-500/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-purple-500/5 rounded-full blur-[120px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-pink-500/3 rounded-full blur-[150px]" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-medium mb-6 tracking-wide">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500" />
            </span>
            Powered by AI
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
            <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Drug Interaction
            </span>
            <br />
            <span className="text-white">Analyzer</span>
          </h1>
          <p className="text-gray-400 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
            Enter your medications in plain text and discover potential
            drug-drug interactions instantly with AI-powered analysis.
          </p>
        </header>

        {/* Input */}
        <section className="mb-12">
          <InputBox onAnalyze={handleAnalyze} isLoading={loading} />
        </section>

        {/* Error */}
        {error && (
          <div className="mb-8 rounded-2xl bg-red-500/10 border border-red-500/30 p-5">
            <div className="flex items-start gap-3">
              <span className="text-red-400 text-xl">⚠️</span>
              <div>
                <h3 className="text-red-400 font-semibold text-sm">
                  Analysis Failed
                </h3>
                <p className="text-red-300/80 text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading skeleton */}
        {loading && (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="rounded-2xl bg-gray-900/60 border border-white/5 p-6 animate-pulse"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-gray-800" />
                  <div className="space-y-2">
                    <div className="h-4 w-48 bg-gray-800 rounded" />
                    <div className="h-3 w-24 bg-gray-800 rounded" />
                  </div>
                </div>
                <div className="h-16 bg-gray-800/60 rounded-xl mb-4" />
                <div className="space-y-2">
                  <div className="h-3 w-full bg-gray-800 rounded" />
                  <div className="h-3 w-3/4 bg-gray-800 rounded" />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Results */}
        {data && !loading && (
          <div className="space-y-8 animate-in fade-in duration-500">
            {/* Detected drugs */}
            <div className="rounded-2xl bg-gray-900/60 backdrop-blur-lg border border-white/10 p-6">
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                Detected Drugs
              </h2>
              <div className="flex flex-wrap gap-2">
                {data.normalized_drugs.map((drug, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center px-4 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 text-sm font-medium capitalize"
                  >
                    💊 {drug}
                  </span>
                ))}
              </div>

              {data.pairs.length > 0 && (
                <p className="text-xs text-gray-500 mt-4">
                  Analyzing {data.pairs.length} drug pair
                  {data.pairs.length > 1 ? "s" : ""}
                </p>
              )}
            </div>

            {/* Interaction cards */}
            <div>
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                Interaction Results
              </h2>
              <div className="space-y-4">
                {data.results.map((result, i) => (
                  <ResultCard key={i} result={result} index={i} />
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-16 text-center">
          <p className="text-xs text-gray-600">
            ⚕️ This tool is for informational purposes only. Always consult a
            healthcare professional.
          </p>
        </footer>
      </div>
    </main>
  );
}

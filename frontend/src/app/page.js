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
    <main className="min-h-screen bg-gradient-to-b from-white via-blue-50/30 to-white">
      <div className="max-w-5xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="text-center mb-16">
          <div className="mb-8">
            <h1 className="text-5xl sm:text-6xl font-bold tracking-tight text-gray-900 mb-4">
              Drug Interaction
              <span className="block text-blue-600">Analyzer</span>
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Comprehensive drug interaction analysis with AI-powered insights. Enter your medications and get instant information about potential interactions.
            </p>
          </div>
        </header>

        {/* Input */}
        <section className="mb-12">
          <InputBox onAnalyze={handleAnalyze} isLoading={loading} />
        </section>

        {/* Error */}
        {error && (
          <div className="mb-8 rounded-lg bg-red-50 border border-red-200 p-6 animate-scale-in">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-red-900 font-semibold">
                  Analysis Failed
                </h3>
                <p className="text-red-700 text-sm mt-1">{error}</p>
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
                className="rounded-lg bg-white border border-gray-200 p-6 animate-pulse"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 rounded-lg bg-gray-200" />
                  <div className="space-y-2 flex-1">
                    <div className="h-4 w-48 bg-gray-200 rounded" />
                    <div className="h-3 w-24 bg-gray-200 rounded" />
                  </div>
                </div>
                <div className="h-16 bg-gray-200 rounded-lg mb-4" />
                <div className="space-y-2">
                  <div className="h-3 w-full bg-gray-200 rounded" />
                  <div className="h-3 w-3/4 bg-gray-200 rounded" />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Results */}
        {data && !loading && (
          <div className="space-y-8 animate-in">
            {/* Detected drugs */}
            <div className="rounded-lg bg-white border border-gray-200 p-6 shadow-sm">
              <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4">
                Detected Medications
              </h2>
              <div className="flex flex-wrap gap-2">
                {data.normalized_drugs.map((drug, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center px-4 py-2 rounded-full bg-blue-100 text-blue-800 text-sm font-medium capitalize border border-blue-200"
                  >
                    {drug}
                  </span>
                ))}
              </div>

              {data.pairs.length > 0 && (
                <p className="text-xs text-gray-600 mt-4">
                  {data.pairs.length} interaction{data.pairs.length > 1 ? "s" : ""} found
                </p>
              )}
            </div>

            {/* Interaction cards */}
            <div>
              <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4">
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

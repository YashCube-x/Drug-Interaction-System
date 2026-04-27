"use client";

import { useState } from "react";

const placeholderExamples = [
  "I take aspirin and warfarin daily...",
  "My medications include lisinopril, metformin, and atorvastatin...",
  "I'm on omeprazole, amlodipine, and simvastatin...",
  "Describe your current drug regimen here...",
];

export default function InputBox({ onAnalyze, isLoading }) {
  const [text, setText] = useState("");
  const placeholder = "Describe your current drug regimen here...";

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onAnalyze(text.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative group">
        {/* Glow border */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 rounded-2xl opacity-30 group-hover:opacity-50 blur transition-opacity duration-500" />

        <div className="relative bg-gray-900/90 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
          <label
            htmlFor="drug-input"
            className="block text-sm font-semibold text-gray-300 mb-3 tracking-wide uppercase"
          >
            Describe your medications
          </label>

          <textarea
            id="drug-input"
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={placeholder}
            className="w-full bg-gray-800/60 text-gray-100 placeholder-gray-500 rounded-xl px-5 py-4 text-base leading-relaxed border border-white/5 focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/20 focus:outline-none resize-none transition-all duration-300"
            disabled={isLoading}
          />

          <div className="flex items-center justify-between mt-4">
            <p className="text-xs text-gray-500">
              Mention at least 2 drug names in your text
            </p>

            <button
              type="submit"
              disabled={!text.trim() || isLoading}
              className="relative group/btn flex items-center gap-2 px-8 py-3 rounded-xl font-semibold text-sm tracking-wide transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {/* Button gradient bg */}
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl transition-all duration-300 group-hover/btn:from-cyan-400 group-hover/btn:to-purple-500" />
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl blur-lg opacity-40 group-hover/btn:opacity-60 transition-opacity duration-300" />

              <span className="relative text-white flex items-center gap-2">
                {isLoading ? (
                  <>
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                        fill="none"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                      />
                    </svg>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                      />
                    </svg>
                    Analyze Interactions
                  </>
                )}
              </span>
            </button>
          </div>
        </div>
      </div>
    </form>
  );
}

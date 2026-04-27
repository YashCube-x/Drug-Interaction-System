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
      <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm hover:shadow-md transition-shadow duration-300">
        <label
          htmlFor="drug-input"
          className="block text-sm font-semibold text-gray-900 mb-3"
        >
          Enter Your Medications
        </label>

        <textarea
          id="drug-input"
          rows={5}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={placeholder}
          className="w-full px-4 py-3 text-gray-900 placeholder-gray-400 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-200 focus:outline-none resize-none transition-all duration-200 text-base leading-relaxed"
          disabled={isLoading}
        />

        <div className="flex items-center justify-between mt-5">
          <p className="text-xs text-gray-600">
            Tip: Mention at least 2 medication names for interaction analysis
          </p>

            <button
              type="submit"
              disabled={!text.trim() || isLoading}
              className="inline-flex items-center justify-center px-8 py-2.5 rounded-lg font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
            >
              {isLoading ? (
                <>
                  <svg className="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" opacity="0.25" />
                    <path fill="currentColor" opacity="0.75" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Analyzing...
                </>
              ) : (
                "Analyze"
              )}
            </button>
          </div>
        </div>
    </form>
  );
}

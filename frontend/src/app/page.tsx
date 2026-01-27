"use client";

import { useState } from 'react';
import { Upload, Activity, AlertTriangle, FileText, Stethoscope } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Types
interface AnalysisResult {
  cancer_type: string;
  ml_confidence: number;
  preliminary_cri: number;
  final_cri: number;
  triage_level: string;
  explanation: string;
  recommendation: string;
  hospital_recommendation: string | null;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [cancerType, setCancerType] = useState('brain');
  const [age, setAge] = useState<number>(45);
  const [symptoms, setSymptoms] = useState('');
  const [riskFactors, setRiskFactors] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload an image.");
      return;
    }

    setAnalyzing(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    // Parse comma-separated inputs into arrays for JSON compatibility
    const symptomsList = JSON.stringify(symptoms.split(',').map(s => s.trim()).filter(Boolean));
    const risksList = JSON.stringify(riskFactors.split(',').map(s => s.trim()).filter(Boolean));

    try {
      // Assuming backend is on port 8000
      const response = await fetch('http://localhost:8000/api/v1/analyze?' + new URLSearchParams({
        cancer_type: cancerType,
        age: age.toString(),
        symptoms: symptomsList,
        risk_factors: risksList
      }), {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Analysis failed');

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("An error occurred during analysis. Please try again.");
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <main className="min-h-screen p-8 md:p-24 flex flex-col items-center gap-12">
      <header className="w-full max-w-5xl text-center space-y-4 animate-fade-in">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
          OncoDetect X
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          AI-Assisted Cancer Triage & Decision Support System
        </p>
        <div className="flex justify-center gap-4 text-sm text-gray-400">
          <span className="flex items-center gap-1"><Activity size={16} /> Multi-Organ Analysis</span>
          <span className="flex items-center gap-1"><Stethoscope size={16} /> Clinical Decision Support</span>
        </div>
      </header>

      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-8 space-y-6"
        >
          <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
            <ScanIcon /> Patient Data
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Target Organ</label>
              <select
                value={cancerType}
                onChange={(e) => setCancerType(e.target.value)}
                className="w-full glass-input"
              >
                <option value="brain">Brain (MRI)</option>
                <option value="lung">Lung (X-Ray)</option>
                <option value="breast">Breast (Mammogram)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Patient Age</label>
              <input
                type="number"
                value={age}
                onChange={(e) => setAge(Number(e.target.value))}
                className="w-full glass-input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Symptoms (comma separated)</label>
              <textarea
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="e.g. persistent headache, blurred vision"
                className="w-full glass-input h-24 resize-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Risk Factors (comma separated)</label>
              <input
                type="text"
                value={riskFactors}
                onChange={(e) => setRiskFactors(e.target.value)}
                placeholder="e.g. smoker, family history"
                className="w-full glass-input"
              />
            </div>

            <div className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-primary transition-colors cursor-pointer relative">
              <input
                type="file"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                accept="image/*"
              />
              <div className="flex flex-col items-center gap-2">
                <Upload className="text-gray-400" size={32} />
                <span className="text-sm text-gray-300">
                  {file ? file.name : "Drop medical scan or click to upload"}
                </span>
              </div>
            </div>

            <button
              type="submit"
              disabled={analyzing || !file}
              className="w-full glass-button mt-4 flex justify-center items-center gap-2"
            >
              {analyzing ? (
                <>Analyzing <Activity className="animate-spin" /></>
              ) : "Run Triage Analysis"}
            </button>
          </form>
          {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
        </motion.div>

        {/* Results Section */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="space-y-6"
        >
          <AnimatePresence mode="wait">
            {!result ? (
              <motion.div
                key="placeholder"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="glass-panel p-8 h-full flex flex-col justify-center items-center text-gray-500 text-center space-y-4"
              >
                <Activity size={64} className="opacity-20" />
                <p>Awaiting patient data and medical imagery for analysis.</p>
                <div className="text-xs max-w-xs opacity-60">
                  Note: This system provides decision support only and does not replace professional medical diagnosis.
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-6"
              >
                {/* Triage Card */}
                <div className={`glass-panel p-6 border-l-4 ${getTriageColor(result.triage_level)}`}>
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-medium text-gray-300">Triage Assessment</h3>
                      <div className="text-4xl font-bold mt-1">{result.triage_level} Risk</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-400">Cancer Risk Index</div>
                      <div className="text-3xl font-bold text-primary">{result.final_cri}<span className="text-lg text-gray-500">/100</span></div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mt-6 text-sm">
                    <div className="bg-white/5 p-3 rounded-lg">
                      <span className="block text-gray-400 text-xs">ML Confidence</span>
                      <span className="font-semibold">{Math.round(result.ml_confidence * 100)}%</span>
                    </div>
                    <div className="bg-white/5 p-3 rounded-lg">
                      <span className="block text-gray-400 text-xs">Preliminary CRI</span>
                      <span className="font-semibold">{result.preliminary_cri}</span>
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                <div className="glass-panel p-6">
                  <h3 className="text-lg font-medium mb-3 flex items-center gap-2">
                    <FileText size={20} className="text-secondary" /> Clinical Reasoning
                  </h3>
                  <p className="text-gray-300 leading-relaxed mb-4">
                    {result.explanation}
                  </p>
                  <div className="bg-primary/20 p-4 rounded-lg border border-primary/30">
                    <h4 className="text-sm font-semibold text-primary mb-1">Recommendation</h4>
                    <p className="text-sm text-gray-200">{result.recommendation}</p>
                  </div>
                </div>

                {/* Hospital Rec */}
                {result.hospital_recommendation && (
                  <div className="glass-panel p-6">
                    <h3 className="text-lg font-medium mb-3 flex items-center gap-2">
                      <Activity size={20} className="text-accent" /> Nearest Facility
                    </h3>
                    <p className="text-gray-300">{result.hospital_recommendation}</p>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </main>
  );
}

function getTriageColor(level: string) {
  switch (level.toLowerCase()) {
    case 'critical': return 'border-red-500 text-red-100';
    case 'high': return 'border-orange-500 text-orange-100';
    case 'moderate': return 'border-yellow-500 text-yellow-100';
    default: return 'border-green-500 text-green-100';
  }
}

function ScanIcon() {
  return (
    <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  );
}

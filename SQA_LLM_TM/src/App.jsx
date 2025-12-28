import './App.css'
import React, { useState } from 'react';

// Icon Components
const Upload = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
  </svg>
);

const FileText = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);

const Download = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
  </svg>
);

const Sparkles = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

function App() {
  const [file, setFile] = useState(null);
  const [pastedText, setPastedText] = useState('');
  const [generating, setGenerating] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [showPreview, setShowPreview] = useState(false);

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const reader = new FileReader();
      reader.onload = (event) => {
        setPastedText(event.target.result);
      };
      reader.readAsText(uploadedFile);
    }
  };

  const handleGenerate = async () => {
    if (!pastedText.trim()) return;
    
    setGenerating(true);
    setShowPreview(false);
    
    // Simulate API call
    setTimeout(() => {
      const sampleQuestions = [
        {
          id: 1,
          question: "What are the basic units of quantum information?",
          answer: "Qubits are the basic units of quantum information, which can be photons, ions, or electrons, enabling quantum computing and communication."
        },
        {
          id: 2,
          question: "What is quantum entanglement?",
          answer: "Quantum entanglement is a phenomenon that allows distant qubits to be correlated in a way that classical systems can't replicate, enabling secure communication and quantum computing."
        },
        {
          id: 3,
          question: "What is quantum teleportation?",
          answer: "Quantum teleportation is the transfer of quantum states across the network using entangled particles, allowing for secure and efficient communication."
        },
        {
          id: 4,
          question: "What are quantum repeaters?",
          answer: "Quantum repeaters are special nodes that extend communication distances by performing entanglement swapping and storing qubit states in quantum memory, enabling long-distance quantum communication."
        },
        {
          id: 5,
          question: "What is quantum key distribution (QKD)?",
          answer: "Quantum key distribution (QKD) is a method that enables users to exchange encryption keys securely, using the principles of quantum mechanics to prevent eavesdropping."
        }
      ];
      
      setQuestions(sampleQuestions);
      setGenerating(false);
      setShowPreview(true);
    }, 2000);
  };

  const handleDownload = () => {
    let content = "SHORT ANSWER QUESTIONS\n";
    content += "=".repeat(50) + "\n\n";
    
    questions.forEach((q, index) => {
      content += `Q${index + 1}. ${q.question}\n\n`;
      content += `Answer: ${q.answer}\n\n`;
      content += "-".repeat(50) + "\n\n";
    });
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'short-answers.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-amber-50 to-orange-50">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-amber-500 to-orange-600 rounded-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-slate-900">Short Answer Generator</h1>
              <p className="text-sm text-slate-600">Generate comprehensive Q&A from your documents</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Upload Section */}
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 mb-6">
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Upload Document</h2>
          
          <div className="space-y-6">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Upload File
              </label>
              <div className="relative">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  accept=".txt,.doc,.docx,.pdf"
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="flex items-center justify-center gap-3 p-6 border-2 border-dashed border-slate-300 rounded-xl cursor-pointer hover:border-amber-500 hover:bg-amber-50 transition-all"
                >
                  <Upload className="w-6 h-6 text-slate-400" />
                  <div className="text-center">
                    <p className="text-sm font-medium text-slate-700">
                      {file ? file.name : 'Click to upload or drag and drop'}
                    </p>
                    <p className="text-xs text-slate-500 mt-1">
                      TXT, DOC, DOCX, PDF up to 10MB
                    </p>
                  </div>
                </label>
              </div>
            </div>

            {/* Text Area */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Or Paste Your Content
              </label>
              <textarea
                value={pastedText}
                onChange={(e) => setPastedText(e.target.value)}
                placeholder="Paste your document content here..."
                className="w-full h-48 p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none text-slate-700 placeholder-slate-400"
              />
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={!pastedText.trim() || generating}
              className="w-full py-4 bg-gradient-to-r from-amber-500 to-orange-600 text-white font-semibold rounded-xl hover:from-amber-600 hover:to-orange-700 disabled:from-slate-300 disabled:to-slate-400 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
            >
              {generating ? (
                <>
                  <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Generate Short Answers
                </>
              )}
            </button>
          </div>
        </div>

        {/* Preview Section */}
        {showPreview && questions.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 mb-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <FileText className="w-6 h-6 text-amber-600" />
                <h2 className="text-xl font-semibold text-slate-900">
                  Generated Questions & Answers
                </h2>
              </div>
              <span className="px-3 py-1 bg-amber-100 text-amber-700 text-sm font-medium rounded-full">
                {questions.length} Questions
              </span>
            </div>

            <div className="space-y-6">
              {questions.map((q, index) => (
                <div
                  key={q.id}
                  className="p-6 bg-gradient-to-br from-slate-50 to-amber-50 rounded-xl border border-slate-200"
                >
                  <div className="flex items-start gap-3 mb-3">
                    <span className="px-2.5 py-1 bg-amber-600 text-white text-xs font-bold rounded-md">
                      Q{index + 1}
                    </span>
                    <p className="flex-1 text-slate-900 font-medium leading-relaxed">
                      {q.question}
                    </p>
                  </div>
                  <div className="pl-11">
                    <p className="text-slate-700 leading-relaxed">
                      <span className="font-semibold text-slate-800">Answer: </span>
                      {q.answer}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Download Button */}
            <button
              onClick={handleDownload}
              className="w-full mt-6 py-4 bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-semibold rounded-xl hover:from-emerald-600 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
            >
              <Download className="w-5 h-5" />
              Download Document
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
export default App

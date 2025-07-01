import React, { useState } from 'react';
import { Shield, Zap, Brain, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react';
import CodeEditor from './CodeEditor';
import ZetasVisualization from './ZetasVisualization';
import AIAnalysis from './AIAnalysis';
import { mockPythonCode, mockCCode, mockPythonZetas, mockCZetas } from '../data/mockData';

const KyberDebugger: React.FC = () => {
  const [pythonCode, setPythonCode] = useState(mockPythonCode);
  const [cCode, setCCode] = useState(mockCCode);
  const [pythonZetas, setPythonZetas] = useState(mockPythonZetas);
  const [cZetas, setCZetas] = useState(mockCZetas);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [aiSuggestions, setAiSuggestions] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    // Simulate AI analysis delay
    setTimeout(() => {
      setAiSuggestions(`## Analysis Results

### Issue Identified
The Montgomery reduction implementation in your Python code has subtle differences from the C reference:

1. **Integer Overflow Handling**: Python's arbitrary precision integers behave differently than C's fixed-width integers
2. **Modular Arithmetic**: The reduction step may not properly handle edge cases

### Suggested Fix
\`\`\`python
def montgomery_reduce(a):
    # Ensure proper 32-bit arithmetic behavior
    a = a & 0xFFFFFFFF  # Mask to 32 bits
    t = (a * QINV) & ((1 << 16) - 1)
    t = (a - t * Q) >> 16
    return t & 0xFFFF  # Ensure 16-bit result
\`\`\`

### Additional Recommendations
- Use explicit bit masking for consistency with C behavior
- Consider using ctypes for exact C integer behavior simulation
- Add intermediate value logging for debugging`);
      setIsAnalyzing(false);
    }, 2000);
  };

  const zetasMatch = JSON.stringify(pythonZetas) === JSON.stringify(cZetas);

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-purple-600 rounded-xl shadow-lg">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">Kyber Crypto Debugger</h1>
              <p className="text-purple-200">AI-Powered Post-Quantum Cryptography Analysis</p>
            </div>
          </div>
          
          {/* Status Badge */}
          <div className="flex items-center gap-4">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${
              zetasMatch 
                ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
                : 'bg-red-500/20 text-red-300 border border-red-500/30'
            }`}>
              {zetasMatch ? <CheckCircle className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
              <span className="font-medium">
                {zetasMatch ? 'Zetas Match!' : 'Zetas Mismatch Detected'}
              </span>
            </div>
            
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-full font-medium transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Brain className="w-4 h-4" />
                  AI Analysis
                </>
              )}
            </button>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8">
          {/* Code Editors */}
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
              <div className="px-6 py-4 bg-gradient-to-r from-orange-600/20 to-red-600/20 border-b border-white/10">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                  <h3 className="font-semibold text-white">Python Implementation</h3>
                </div>
              </div>
              <CodeEditor
                value={pythonCode}
                onChange={setPythonCode}
                language="python"
                height="400px"
              />
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
              <div className="px-6 py-4 bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border-b border-white/10">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <h3 className="font-semibold text-white">C Reference Implementation</h3>
                </div>
              </div>
              <CodeEditor
                value={cCode}
                onChange={setCCode}
                language="c"
                height="400px"
                readOnly
              />
            </div>
          </div>

          {/* Visualization Panel */}
          <div className="space-y-6">
            <ZetasVisualization
              pythonZetas={pythonZetas}
              cZetas={cZetas}
              onPythonZetasChange={setPythonZetas}
            />
            
            {aiSuggestions && (
              <AIAnalysis suggestions={aiSuggestions} />
            )}
          </div>
        </div>

        {/* Technical Info */}
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-yellow-400" />
            <h3 className="text-lg font-semibold text-white">About Kyber NTT</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <div className="bg-white/5 rounded-xl p-4">
              <h4 className="font-medium text-purple-300 mb-2">Number Theoretic Transform</h4>
              <p className="text-gray-300">
                Efficiently computes polynomial multiplication in the ring Z_q[X]/(X^n + 1) using precomputed twiddle factors (zetas).
              </p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <h4 className="font-medium text-blue-300 mb-2">Montgomery Reduction</h4>
              <p className="text-gray-300">
                Optimizes modular arithmetic by avoiding expensive division operations, crucial for cryptographic performance.
              </p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <h4 className="font-medium text-green-300 mb-2">Post-Quantum Security</h4>
              <p className="text-gray-300">
                Kyber's security relies on the hardness of the Learning With Errors (LWE) problem, resistant to quantum attacks.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KyberDebugger;
import React from 'react';
import { Brain, Lightbulb, Code, AlertCircle } from 'lucide-react';

interface AIAnalysisProps {
  suggestions: string;
}

const AIAnalysis: React.FC<AIAnalysisProps> = ({ suggestions }) => {
  // Simple markdown-like parsing for the suggestions
  const formatSuggestions = (text: string) => {
    const lines = text.split('\n');
    const formatted: JSX.Element[] = [];
    let inCodeBlock = false;
    let codeLines: string[] = [];

    lines.forEach((line, index) => {
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          // End code block
          formatted.push(
            <div key={`code-${index}`} className="bg-black/30 rounded-lg p-4 my-3 font-mono text-sm text-green-300 overflow-x-auto">
              <pre>{codeLines.join('\n')}</pre>
            </div>
          );
          codeLines = [];
          inCodeBlock = false;
        } else {
          // Start code block
          inCodeBlock = true;
        }
      } else if (inCodeBlock) {
        codeLines.push(line);
      } else if (line.startsWith('## ')) {
        formatted.push(
          <h3 key={index} className="text-lg font-semibold text-purple-300 mt-4 mb-2">
            {line.replace('## ', '')}
          </h3>
        );
      } else if (line.startsWith('### ')) {
        formatted.push(
          <h4 key={index} className="text-base font-medium text-blue-300 mt-3 mb-2">
            {line.replace('### ', '')}
          </h4>
        );
      } else if (line.startsWith('- ')) {
        formatted.push(
          <li key={index} className="text-gray-300 ml-4 mb-1">
            {line.replace('- ', '')}
          </li>
        );
      } else if (line.trim()) {
        formatted.push(
          <p key={index} className="text-gray-300 mb-2">
            {line}
          </p>
        );
      }
    });

    return formatted;
  };

  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-green-600/20 to-blue-600/20 border-b border-white/10">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-green-400" />
          <h3 className="font-semibold text-white">AI Analysis & Suggestions</h3>
        </div>
      </div>

      <div className="p-6">
        <div className="space-y-4">
          {/* Action Items */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
            <div className="flex items-center gap-3 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
              <AlertCircle className="w-5 h-5 text-yellow-400 flex-shrink-0" />
              <div>
                <div className="font-medium text-yellow-300">Issue Found</div>
                <div className="text-xs text-yellow-200">Montgomery reduction</div>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
              <Code className="w-5 h-5 text-blue-400 flex-shrink-0" />
              <div>
                <div className="font-medium text-blue-300">Fix Provided</div>
                <div className="text-xs text-blue-200">Updated algorithm</div>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
              <Lightbulb className="w-5 h-5 text-green-400 flex-shrink-0" />
              <div>
                <div className="font-medium text-green-300">Recommendations</div>
                <div className="text-xs text-green-200">Best practices</div>
              </div>
            </div>
          </div>

          {/* Detailed Analysis */}
          <div className="bg-white/5 rounded-xl p-5 max-h-96 overflow-y-auto">
            <div className="prose prose-invert max-w-none">
              {formatSuggestions(suggestions)}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4 border-t border-white/10">
            <button className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors">
              <Code className="w-4 h-4" />
              Apply Fix
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-medium transition-colors">
              <Lightbulb className="w-4 h-4" />
              More Suggestions
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysis;
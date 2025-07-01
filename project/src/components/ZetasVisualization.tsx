import React, { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import { TrendingUp, BarChart3, Shuffle } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface ZetasVisualizationProps {
  pythonZetas: number[];
  cZetas: number[];
  onPythonZetasChange: (zetas: number[]) => void;
}

const ZetasVisualization: React.FC<ZetasVisualizationProps> = ({
  pythonZetas,
  cZetas,
  onPythonZetasChange
}) => {
  const differences = useMemo(() => {
    return pythonZetas.map((val, idx) => val - cZetas[idx]);
  }, [pythonZetas, cZetas]);

  const maxDiff = Math.max(...differences.map(Math.abs));
  const mismatchCount = differences.filter(d => d !== 0).length;

  const lineChartData = {
    labels: Array.from({ length: Math.min(32, pythonZetas.length) }, (_, i) => i.toString()),
    datasets: [
      {
        label: 'Python Zetas',
        data: pythonZetas.slice(0, 32),
        borderColor: 'rgb(251, 146, 60)',
        backgroundColor: 'rgba(251, 146, 60, 0.1)',
        tension: 0.1,
      },
      {
        label: 'C Reference',
        data: cZetas.slice(0, 32),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.1,
      },
    ],
  };

  const diffChartData = {
    labels: Array.from({ length: Math.min(32, differences.length) }, (_, i) => i.toString()),
    datasets: [
      {
        label: 'Difference',
        data: differences.slice(0, 32),
        backgroundColor: differences.slice(0, 32).map(d => 
          d === 0 ? 'rgba(34, 197, 94, 0.6)' : 'rgba(239, 68, 68, 0.6)'
        ),
        borderColor: differences.slice(0, 32).map(d => 
          d === 0 ? 'rgb(34, 197, 94)' : 'rgb(239, 68, 68)'
        ),
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: 'rgb(203, 213, 225)',
          font: {
            size: 12,
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'rgb(148, 163, 184)',
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.1)',
        },
      },
      y: {
        ticks: {
          color: 'rgb(148, 163, 184)',
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.1)',
        },
      },
    },
  };

  const regenerateZetas = () => {
    // Simulate generating new zetas with some random variation
    const newZetas = pythonZetas.map(val => 
      Math.floor(val + (Math.random() - 0.5) * 200)
    );
    onPythonZetasChange(newZetas);
  };

  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-purple-600/20 to-pink-600/20 border-b border-white/10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-purple-400" />
            <h3 className="font-semibold text-white">Zetas Array Analysis</h3>
          </div>
          <button
            onClick={regenerateZetas}
            className="flex items-center gap-2 px-3 py-1 bg-purple-600/30 hover:bg-purple-600/50 text-purple-200 rounded-lg text-sm transition-colors"
          >
            <Shuffle className="w-4 h-4" />
            Regenerate
          </button>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Statistics */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white/5 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-white">{pythonZetas.length}</div>
            <div className="text-sm text-gray-400">Array Length</div>
          </div>
          <div className="bg-white/5 rounded-xl p-4 text-center">
            <div className={`text-2xl font-bold ${mismatchCount === 0 ? 'text-green-400' : 'text-red-400'}`}>
              {mismatchCount}
            </div>
            <div className="text-sm text-gray-400">Mismatches</div>
          </div>
          <div className="bg-white/5 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-yellow-400">{maxDiff}</div>
            <div className="text-sm text-gray-400">Max Diff</div>
          </div>
        </div>

        {/* Value Comparison Chart */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <BarChart3 className="w-4 h-4 text-blue-400" />
            <h4 className="font-medium text-white">Value Comparison (First 32 Elements)</h4>
          </div>
          <div className="h-64 bg-black/20 rounded-xl p-4">
            <Line data={lineChartData} options={chartOptions} />
          </div>
        </div>

        {/* Difference Visualization */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-4 h-4 text-red-400" />
            <h4 className="font-medium text-white">Differences</h4>
          </div>
          <div className="h-48 bg-black/20 rounded-xl p-4">
            <Bar data={diffChartData} options={chartOptions} />
          </div>
        </div>

        {/* Raw Data Preview */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <h5 className="font-medium text-orange-300 mb-2">Python Zetas (First 8)</h5>
            <div className="bg-black/20 rounded-lg p-3 font-mono text-sm text-gray-300">
              [{pythonZetas.slice(0, 8).join(', ')}...]
            </div>
          </div>
          <div>
            <h5 className="font-medium text-blue-300 mb-2">C Reference (First 8)</h5>
            <div className="bg-black/20 rounded-lg p-3 font-mono text-sm text-gray-300">
              [{cZetas.slice(0, 8).join(', ')}...]
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ZetasVisualization;
import React from 'react';
import { Toaster } from 'react-hot-toast';
import KyberDebugger from './components/KyberDebugger';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800">
      <Toaster position="top-right" />
      <KyberDebugger />
    </div>
  );
}

export default App;
import React from 'react';
import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  height?: string;
  readOnly?: boolean;
}

const CodeEditor: React.FC<CodeEditorProps> = ({
  value,
  onChange,
  language,
  height = '300px',
  readOnly = false
}) => {
  return (
    <Editor
      value={value}
      onChange={(val) => onChange(val || '')}
      language={language}
      height={height}
      theme="vs-dark"
      options={{
        fontSize: 13,
        fontFamily: 'JetBrains Mono, Fira Code, Monaco, monospace',
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        readOnly,
        automaticLayout: true,
        tabSize: 2,
        wordWrap: 'on',
        lineNumbers: 'on',
        folding: true,
        bracketMatching: 'always',
        autoIndent: 'full',
      }}
    />
  );
};

export default CodeEditor;
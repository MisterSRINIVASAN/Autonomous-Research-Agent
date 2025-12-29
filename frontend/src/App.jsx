import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || isProcessing) return;

    const userMessage = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery('');
    startResearchWorkflow(query);
  };

  const startResearchWorkflow = (searchQuery) => {
    setIsProcessing(true);
    setConnecting(true);

    const ws = new WebSocket('ws://localhost:8001/ws/research');

    ws.onopen = () => {
      setConnecting(false);
      ws.send(searchQuery);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'tool_call') {
        const calls = Array.isArray(data.content) ? data.content : [data.content];
        calls.forEach(call => {
          setMessages((prev) => [
            ...prev,
            { role: 'tool', content: `Executing: ${call.name || 'search'}` }
          ]);
        });
      } else if (data.type === 'message') {
        setMessages((prev) => [...prev, { role: 'agent', content: data.content }]);
      } else if (data.type === 'complete') {
        setIsProcessing(false);
        ws.close();
      } else if (data.type === 'error') {
        setMessages((prev) => [...prev, { role: 'agent', content: `**Error:** ${data.error}` }]);
        setIsProcessing(false);
        ws.close();
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket Error:', error);
      setMessages((prev) => [...prev, { role: 'agent', content: '**Connection Error**: Could not connect to agent backend. Is FastAPI running?' }]);
      setIsProcessing(false);
      setConnecting(false);
    };

    ws.onclose = () => {
      setIsProcessing(false);
      setConnecting(false);
    };
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="status-indicator" style={{ backgroundColor: isProcessing ? '#f59e0b' : '#10b981', boxShadow: `0 0 10px ${isProcessing ? '#f59e0b' : '#10b981'}` }}></div>
        <h1>Autonomous AI Researcher</h1>
        <div style={{ marginLeft: 'auto', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          {connecting ? 'Connecting...' : isProcessing ? 'Agent Active' : 'Ready'}
        </div>
      </header>

      <main className="chat-area">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '40px' }}>
            <p style={{ fontSize: '1.2rem', marginBottom: '8px', color: '#fff' }}>Welcome to the Research Agent!</p>
            <p>Ask a complex question and watch the agent independently search, scrape, and synthesize an answer.</p>
          </div>
        )}
        
        {messages.map((msg, idx) => {
          if (msg.role === 'tool') {
            return (
              <div key={idx} className="tool-call">
                <div className="spinner"></div> {msg.content}
              </div>
            );
          }
          
          return (
            <div key={idx} className={`message ${msg.role}`}>
              {msg.role === 'agent' ? (
                <div className="markdown-content">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                msg.content
              )}
            </div>
          );
        })}
        
        {isProcessing && !connecting && (
          <div className="tool-call">
            <div className="spinner"></div> Agent is thinking...
          </div>
        )}
        <div ref={chatEndRef} />
      </main>

      <form className="input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Compare the latest Q3 earnings of Microsoft and Apple..."
          disabled={isProcessing}
        />
        <button type="submit" disabled={isProcessing || !query.trim()}>
          Research
        </button>
      </form>
    </div>
  );
}

export default App;

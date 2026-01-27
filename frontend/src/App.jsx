import { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/query', { text: query });
      setResponse(res.data.response);
      setStatus(res.data.status);
      // Poll for score if needed (e.g., add another endpoint to fetch logs)
    } catch (error) {
      setStatus('Error: ' + error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Hallucination Tracker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter query"
          style={{ width: '300px', marginRight: '10px' }}
        />
        <button type="submit">Submit</button>
      </form>
      {response && <p><strong>Response:</strong> {response}</p>}
      {status && <p><strong>Status:</strong> {status}</p>}
    </div>
  );
}

export default App;import { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/query', { text: query });
      setResponse(res.data.response);
      setStatus(res.data.status);
      // Poll for score if needed (e.g., add another endpoint to fetch logs)
    } catch (error) {
      setStatus('Error: ' + error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Hallucination Tracker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter query"
          style={{ width: '300px', marginRight: '10px' }}
        />
        <button type="submit">Submit</button>
      </form>
      {response && <p><strong>Response:</strong> {response}</p>}
      {status && <p><strong>Status:</strong> {status}</p>}
    </div>
  );
}

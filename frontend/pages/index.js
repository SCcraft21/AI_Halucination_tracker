import { useState, useEffect } from "react";

export default function Home() {
  const [tab, setTab] = useState("submit");
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Failed to submit snippet" });
    } finally {
      setLoading(false);
    }
  }

  async function fetchHistory() {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/history`);
      const data = await res.json();
      setHistory(data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (tab === "history") fetchHistory();
  }, [tab]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Hallucination Tracker</h1>
      <div style={{ marginBottom: 20 }}>
        <button onClick={() => setTab("submit")}>Submit Snippet</button>
        <button onClick={() => setTab("history")} style={{ marginLeft: 10 }}>
          History
        </button>
      </div>

      {tab === "submit" && (
        <div>
          <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
            <label>
              Language:
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{ marginLeft: 10 }}
              >
                <option value="python">Python</option>
              </select>
            </label>

            <br /><br />

            <textarea
              rows={10}
              cols={80}
              placeholder="Paste your AI-generated code here..."
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
            />

            <br /><br />

            <button type="submit" disabled={loading}>
              {loading ? "Submitting..." : "Submit"}
            </button>
          </form>

          {result && (
            <div style={{ marginTop: 30, padding: 20, border: "1px solid #ccc" }}>
              <h2>Result</h2>
              {result.error ? (
                <p style={{ color: "red" }}>{result.error}</p>
              ) : (
                <>
                  <p><strong>Hash:</strong> {result.hash}</p>
                  <p><strong>Score:</strong> {result.score}</p>
                  <p><strong>IPFS CID:</strong> {result.ipfs}</p>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {tab === "history" && (
        <div>
          <h2>Stored Snippets</h2>
          {history.length === 0 ? (
            <p>No snippets yet.</p>
          ) : (
            <table border="1" cellPadding="10">
              <thead>
                <tr>
                  <th>Hash</th>
                  <th>Score</th>
                  <th>IPFS</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.hash}</td>
                    <td>{item.score}</td>
                    <td>
                      <a
                        href={`https://ipfs.io/ipfs/${item.ipfs}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        {item.ipfs}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

import React, { useState } from "react";
import "./App.css";
import scenarios from "./scenarios.js";

function ConfidenceBar({ value }) {
  return (
    <div className="confidence-bar-bg">
      <div
        className="confidence-bar-fill"
        style={{ width: `${value * 100}%` }}
      />
    </div>
  );
}

function RecommendationCard({ rec, currentPrice, raw }) {
  if (!rec || typeof rec.suggested_price !== "number") {
    return (
      <div className="card placeholder">
        <p>No recommendation yet.</p>
      </div>
    );
  }

  const delta = rec.suggested_price - currentPrice;
  const deltaPct =
    currentPrice > 0 ? ((delta / currentPrice) * 100).toFixed(1) : null;
  const up = delta > 0;
  const down = delta < 0;

  return (
    <div className="card">
      <div className="price-row">
        <span className="big-price">${rec.suggested_price.toFixed(2)}</span>
        {up && deltaPct !== null && (
          <span className="delta up">
            ▲ +{Math.abs(delta).toFixed(2)} ({Math.abs(deltaPct)}%)
          </span>
        )}
        {down && deltaPct !== null && (
          <span className="delta down">
            ▼ -{Math.abs(delta).toFixed(2)} ({Math.abs(deltaPct)}%)
          </span>
        )}
        {!up && !down && <span className="delta">No change</span>}
      </div>

      <div className="confidence-label">
        Confidence: {(rec.confidence * 100).toFixed(0)}%
      </div>
      <ConfidenceBar value={rec.confidence} />

      {typeof rec.expected_lift_pct === "number" && (
        <div className="section">
          <div className="section-title">Expected revenue lift</div>
          <div>
            {rec.expected_lift_pct > 0 ? "+" : ""}
            {rec.expected_lift_pct.toFixed(1)}%
          </div>
        </div>
      )}

      <div className="section">
        <div className="section-title">Rationale</div>
        <ul>
          {(rec.rationale || []).map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>

      <div className="section">
        <div className="section-title">Risks</div>
        <div>
          {(rec.risk_flags || []).map((risk, i) => (
            <span key={i} className="risk-tag">
              {risk}
            </span>
          ))}
        </div>
      </div>

      <details className="reasoning-details">
        <summary>Show full model response</summary>
        <pre>{JSON.stringify(raw, null, 2)}</pre>
      </details>
    </div>
  );
}

function App() {
  const [form, setForm] = useState({
    ...scenarios[0].data,
    reference_prices: scenarios[0].data.reference_prices.join(", "),
  });
  const [loading, setLoading] = useState(false);
  const [rec, setRec] = useState(null);
  const [raw, setRaw] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleScenario = (idx) => {
    if (idx === "") return;
    const s = scenarios[idx].data;
    setForm({
      ...s,
      reference_prices: s.reference_prices.join(", "),
    });
    setRec(null);
    setRaw(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRec(null);
    setRaw(null);

    const payload = {
      product_type: form.product_type,
      current_price: parseFloat(form.current_price),
      reference_prices: String(form.reference_prices)
        .split(",")
        .map((v) => parseFloat(v.trim()))
        .filter((v) => !isNaN(v)),
      demand_signal: parseFloat(form.demand_signal),
      inventory_remaining: parseInt(form.inventory_remaining, 10),
      lead_time_days: parseInt(form.lead_time_days, 10),
      context_notes: form.context_notes || "",
    };

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (!res.ok) {
        setRaw({
          error: data.detail || `HTTP ${res.status}`,
          status: res.status,
        });
        return;
      }

      setRec(data);
      setRaw(data);
    } catch (err) {
      setRaw({ error: err.toString() });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-layout">
      <div className="form-section">
        <h2>Pricing Scenario</h2>

        <div className="scenario-dropdown">
          <label>
            Load example scenario:
            <select onChange={(e) => handleScenario(e.target.value)} value="">
              <option value="" disabled>
                Select...
              </option>
              {scenarios.map((s, i) => (
                <option key={i} value={i}>
                  {s.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        <form onSubmit={handleSubmit}>
          <label>
            Product type
            <select
              name="product_type"
              value={form.product_type}
              onChange={handleChange}
            >
              <option value="hotel_room">Hotel room</option>
              <option value="event_ticket">Event ticket</option>
              <option value="short_term_rental">Short-term rental</option>
              <option value="ecom_item">E-commerce item</option>
            </select>
          </label>

          <label>
            Current price
            <input
              name="current_price"
              type="number"
              step="0.01"
              min="0"
              value={form.current_price}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Reference prices (comma separated)
            <input
              name="reference_prices"
              value={form.reference_prices}
              onChange={handleChange}
              placeholder="e.g. 100, 95, 110"
            />
          </label>

          <label>
            Demand signal ({parseFloat(form.demand_signal).toFixed(2)})
            <input
              name="demand_signal"
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={form.demand_signal}
              onChange={handleChange}
            />
          </label>

          <label>
            Inventory remaining
            <input
              name="inventory_remaining"
              type="number"
              min="0"
              value={form.inventory_remaining}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Lead time (days)
            <input
              name="lead_time_days"
              type="number"
              min="0"
              value={form.lead_time_days}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Context notes
            <textarea
              name="context_notes"
              value={form.context_notes}
              onChange={handleChange}
              rows="3"
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Get Recommendation"}
          </button>
        </form>
      </div>

      <div className="card-section">
        <RecommendationCard
          rec={rec}
          currentPrice={parseFloat(form.current_price) || 0}
          raw={raw}
        />
        {raw?.error && (
          <div className="card error">
            <strong>Error{raw.status ? ` ${raw.status}` : ""}:</strong>{" "}
            {raw.error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

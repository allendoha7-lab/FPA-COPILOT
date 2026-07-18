# 📈 Corporate FP&A Copilot: AI-Powered Variance Automation Engine

## 🏢 Executive Overview
The **FP&A Copilot** is an enterprise-grade financial business intelligence application built to automate the most time-consuming aspects of the month-end closing cycle. It eliminates manual spreadsheet wrangling by dynamically parsing unstructured 'Budget vs. Actual' ERP exports, calculating GAAP-compliant performance metrics, and utilizing Generative AI to synthesize quantitative data into boardroom-ready qualitative narratives.

Built with an "Executive First" UI philosophy, the application features a custom corporate theme, strict margin scaling, and mathematically robust visualizations designed specifically for CFO presentations.

---

## 🚀 Core Architecture & Features

### 1. Algorithmic Schema Discovery (Ingestion Layer)
* **Smart Header Detection:** Bypasses messy, un-pivoted ERP metadata using a custom Pandas weight-scoring heuristic to automatically locate transaction tables and identify exact headers.
* **Semantic Normalization:** Strips out nested subtotals, blank padding, and currency markers (₹, $) to prevent double-counting and decimal truncation.

### 2. Directional GAAP/IFRS Scorecard (Calculation Layer)
* **Stream Disaggregation:** Programmatically separates top-line revenue inflows from operational expenditures.
* **Inverted Risk Vectors:** Automatically maps cost overruns as unfavorable (Red) risk parameters while maintaining positive scaling for revenue wins (Green), ensuring bottom-line margins are calculated perfectly via absolute denominator handling.

### 3. C-Suite Data Visualization (Analytics Layer)
* **Dynamic Sensitivity Simulators:** Built-in sidebar levers allowing users to stress-test revenue and expense baselines ($\pm50\%$) with instantaneous ground-truth recalculations.
* **Risk Boundary Matrix:** Horizontal variance charts featuring hard-coded $\pm15\%$ baseline buffers and explicit $\pm10\%$ dashed risk-tolerance threshold lines to isolate operational breaches.
* **Macro Bridge Walks:** Vertical Waterfall charts powered by `Plotly Graph Objects` and Python `textwrap`, dynamically stacking long ledger names to create perfectly scaled cumulative step-walks from Initial Budget to Realized Outcomes.

### 4. Automated Boardroom Briefs (GenAI Middleware)
* **Outlier Context Binding:** Filters material anomalies and passes clean data arrays into a secure GenAI middleware pipeline (Powered by the Groq API Cloud Client).
* **Structured Narrative Synthesis:** Automatically generates a formatted, objective executive brief separating the macro-economic summary, revenue wins, and operational cost audits.

---

## 🛠️ Technology Stack
* **Language:** Python 3.13+
* **Framework:** Streamlit (Custom Executive Beige CSS Injection)
* **Data Engineering:** Pandas, NumPy
* **Data Visualization:** Plotly Express, Plotly Graph Objects (`go.Waterfall`)
* **AI Integration:** Groq SDK API (Llama-3.3 Versatile Architecture)

---

## 💼 The Business Value
In traditional finance environments, separating multi-sheet variance reports and generating qualitative narrative bridges eats up massive portions of the analytical cycle. This Copilot acts as a zero-touch pipeline—empowering leadership to stress-test performance live, instantly visualize operational milestones, and scale business visibility flawlessly.

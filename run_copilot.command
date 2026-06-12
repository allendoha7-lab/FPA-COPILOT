#!/bin/bash
# ----------------------------------------------------------------------
# Executive Startup Engine with Automated Environment Injection
# ----------------------------------------------------------------------

# 1. Inject your Groq Authentication Key permanently into local memory
export GROQ_API_KEY="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"

# 2. Navigate to your dedicated workspace root
cd "/Users/allenabraham/fpa_copilot"

# 3. Initialize background Streamlit engine safely
echo "Initializing Corporate FP&A Copilot Terminal Environment..."
python -m streamlit run app.py --server.headless=false
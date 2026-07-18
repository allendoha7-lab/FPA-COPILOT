import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import textwrap
from groq import Groq

# ----------------------------------------------------------------------
# 1. Page Configuration & Full Executive Beige Theme CSS Injection
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="FP&A Copilot - Executive Simulation Suite",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

executive_beige_css = """
<style>
    html, body, [data-testid="stSidebarUserContent"], .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 15px !important;
        color: #1E293B;
        background-color: #FDFBF7;
    }
    
    [data-testid="stSidebar"] {
        background-color: #F4F1EA !important;
        border-right: 1px solid #E4E0D5 !important;
    }
    
    h1 {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #0F172A;
        letter-spacing: -0.5px;
        padding-bottom: 14px;
        border-bottom: 1px solid #E7E5E4;
        margin-bottom: 28px !important;
    }
    
    h2 {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #44403C;
        margin-top: 30px !important;
        margin-bottom: 14px !important;
    }

    .block-container {
        padding: 3rem 4rem !important;
    }
    
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    
    .stAlert {
        margin-top: 10px !important;
        margin-bottom: 0px !important;
    }
    
    [data-testid="stWidgetLabel"] p {
        color: #44403C !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D3D1 !important;
        border-radius: 6px !important;
    }
    input {
        color: #1C1917 !important;
        font-size: 14px !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-baseweb="input"] button {
        background-color: #F5F5F4 !important;
        color: #1C1917 !important;
        border-left: 1px solid #D6D3D1 !important;
    }
    
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #A8A29E !important;
        border-radius: 8px !important;
        padding: 24px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.01) !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stFileUploader"] button {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        transition: background-color 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 20px 24px !important;
        border-radius: 8px !important;
        border: 1px solid #E7E5E4 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #1C1917 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        color: #78716C !important;
        text-transform: uppercase !important;
        letter-spacing: 0.7px !important;
        font-weight: 600 !important;
    }
    
    .stDataFrame, table {
        font-size: 13.5px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E7E5E4 !important;
        border-radius: 8px !important;
    }
    
    button[data-baseweb="tab"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #78716C !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1E3A8A !important;
        border-bottom-color: #1E3A8A !important;
    }
    
    .executive-brief-box {
        background-color: #FFFFFF;
        padding: 32px;
        border-radius: 8px;
        border-left: 6px solid #1E3A8A;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        color: #1C1917;
    }

    .brief-heading {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        text-transform: uppercase !important;
        letter-spacing: 0.7px !important;
        margin-top: 24px !important;
        margin-bottom: 12px !important;
        border-bottom: 1px dashed #E2E8F0 !important;
        padding-bottom: 6px !important;
    }
    .brief-heading:first-of-type {
        margin-top: 0px !important;
    }

    .brief-body-text {
        font-size: 15px !important;
        line-height: 1.75 !important;
        color: #334155 !important;
        margin-bottom: 20px !important;
    }

    .executive-brief-box ul {
        margin-top: 4px !important;
        margin-bottom: 20px !important;
        padding-left: 22px !important;
    }
    .executive-brief-box li {
        margin-bottom: 10px !important;
        font-size: 15px !important;
        line-height: 1.65 !important;
        color: #334155 !important;
    }
</style>
"""
st.markdown(executive_beige_css, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 2. Gatekeepers & Initialization
# ----------------------------------------------------------------------
@st.cache_resource
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

client = get_groq_client()

# ----------------------------------------------------------------------
# 3. Intelligent Classification Heuristics
# ----------------------------------------------------------------------
def infer_financial_category(item_name):
    name_lower = str(item_name).lower()
    if any(w in name_lower for w in ['tax', 'expense', 'cost', 'fee', 'charge', 'overhead', 'wage', 'salary', 'interest', 'depreciation', 'amortisation', 'lease', 'marketing', 'advertising']):
        return 'Operating Expense'
    elif any(w in name_lower for w in ['sales', 'revenue', 'income', 'turnover', 'inflow', 'grant']):
        return 'Revenue'
    else:
        return 'Operating Expense'

# ----------------------------------------------------------------------
# 4. Core Engine Pipelines
# ----------------------------------------------------------------------
def process_variance_sheet(file, threshold_pct=5.0, revenue_sim_pct=0.0, expense_sim_pct=0.0, selected_sheet=None):
    try:
        if file.name.endswith('.csv'):
            raw_df = pd.read_csv(file, header=None)
        else:
            if selected_sheet:
                raw_df = pd.read_excel(file, sheet_name=selected_sheet, header=None)
            else:
                raw_df = pd.read_excel(file, header=None)
    except Exception as parse_error:
        st.error(f"File Matrix Access Failure: {str(parse_error)}")
        return None, None

    best_row_idx = 0
    max_score = -1
    
    for idx, row in raw_df.iterrows():
        row_str = row.astype(str).str.strip().str.lower().tolist()
        score = 0
        if any(any(w in str(cell) for w in ['line item', 'item', 'particulars', 'description', 'particular']) for cell in row_str):
            score += 2
        if any(any(w in str(cell) for w in ['budget', 'planned', 'plan', 'target']) for cell in row_str):
            score += 2
        if any(any(w in str(cell) for w in ['actual', 'spent', 'realized', 'realised', 'outcome']) for cell in row_str):
            score += 2
        if score > max_score:
            max_score = score
            best_row_idx = idx
            
    if max_score < 4:
        st.error("Structure Error: Unable to automatically identify matching columns ('Line Item', 'Budget', 'Actual').")
        return None, None

    headers = raw_df.iloc[best_row_idx].astype(str).str.strip().str.lower().tolist()
    col_mapping = {'line item': None, 'budget': None, 'actual': None, 'category': None, 'operational notes': None}
    
    for i, h in enumerate(headers):
        if any(w in h for w in ['line item', 'item', 'particulars', 'description', 'particular']):
            col_mapping['line item'] = i
        if any(w in h for w in ['budget', 'planned', 'plan', 'target']):
            col_mapping['budget'] = i
        if any(w in h for w in ['actual', 'spent', 'realized', 'realised', 'outcome']):
            col_mapping['actual'] = i
        if any(w in h for w in ['category', 'type']):
            col_mapping['category'] = i
        if any(w in h for w in ['operational', 'notes', 'justification', 'comment']):
            col_mapping['operational notes'] = i

    if col_mapping['line item'] is None or col_mapping['budget'] is None or col_mapping['actual'] is None:
        st.error("Mapping Failure: Could not align metadata columns.")
        return None, None

    cleaned_rows = []
    for idx in range(best_row_idx + 1, len(raw_df)):
        row = raw_df.iloc[idx]
        if pd.isna(row[col_mapping['line item']]) or str(row[col_mapping['line item']]).strip() == '' or str(row[col_mapping['line item']]).lower() == 'nan':
            continue
            
        line_item_val = str(row[col_mapping['line item']]).strip()
        if any(w in line_item_val.lower() for w in ['total', 'summary', 'profit', 'ebitda', 'pbt', 'npat', 'gross profit', 'below the line', 'operating expenses', 'cost of revenue', 'people costs', 'sales & marketing', 'general & administrative']):
            continue
            
        budget_val = row[col_mapping['budget']]
        actual_val = row[col_mapping['actual']]
        if pd.isna(budget_val) and pd.isna(actual_val):
            continue
            
        try:
            b_num = float(str(budget_val).replace('₹', '').replace('$', '').replace(',', '').strip())
        except:
            b_num = 0.0
        try:
            a_num = float(str(actual_val).replace('₹', '').replace('$', '').replace(',', '').strip())
        except:
            a_num = 0.0
            
        if b_num == 0.0 and a_num == 0.0:
            continue

        if col_mapping['category'] is not None and col_mapping['category'] < len(row) and not pd.isna(row[col_mapping['category']]):
            cat_val = str(row[col_mapping['category']]).strip()
        else:
            cat_val = infer_financial_category(line_item_val)
            
        if col_mapping['operational notes'] is not None and col_mapping['operational notes'] < len(row) and not pd.isna(row[col_mapping['operational notes']]):
            notes_val = str(row[col_mapping['operational notes']]).strip()
        else:
            notes_val = 'No specific operational notes context provided in sheet.'

        if cat_val == 'Revenue':
            a_num = a_num * (1.0 + (revenue_sim_pct / 100.0))
        else:
            a_num = a_num * (1.0 + (expense_sim_pct / 100.0))

        abs_var = a_num - b_num
        pct_var = (abs_var / abs(b_num) * 100) if b_num != 0 else 0.0
        
        if cat_val == 'Revenue':
            status = "Favorable" if abs_var >= 0 else "Unfavorable"
        else:
            status = "Unfavorable" if abs_var > 0 else "Favorable"
            
        if abs(pct_var) >= threshold_pct:
            mat_status = status
        else:
            mat_status = "Immaterial"

        cleaned_rows.append({
            'line item': line_item_val,
            'category': cat_val,
            'budget': b_num,
            'actual': a_num,
            'absolute_variance': abs_var,
            'percentage_variance': pct_var,
            'materiality_status': mat_status,
            'operational notes': notes_val
        })

    full_df = pd.DataFrame(cleaned_rows)
    if full_df.empty:
        return full_df, full_df
        
    material_df = full_df[full_df['materiality_status'].isin(["Favorable", "Unfavorable"])].copy()
    return full_df, material_df

def generate_fp_a_commentary(material_data_df, revenue_sim_pct, expense_sim_pct):
    if material_data_df.empty:
        return "No items breached the established materiality threshold for this simulated cycle."
    
    payload_df = material_data_df[['line item', 'category', 'budget', 'actual', 'absolute_variance', 'percentage_variance', 'materiality_status', 'operational notes']]
    data_string = payload_df.to_string(index=False, formatters={'percentage_variance': '{:,.3f}%'.format})
    
    if client is None:
        return "System Diagnostic Error: Groq Environment Key integration not detected."
    
    simulation_context = ""
    if revenue_sim_pct != 0.0 or expense_sim_pct != 0.0:
        simulation_context = f"Note: This analysis incorporates real-time executive simulation parameters (Revenue scale shifted by {revenue_sim_pct:+.3f}%, Expenses scale shifted by {expense_sim_pct:+.3f}%).\n\n"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Senior FP&A Director presenting to the CFO. Speak strictly in concise, "
                        "objective analytical corporate language. Do not use emojis, conversational intros, or conclusions.\n\n"
                        "CRITICAL STRUCTURAL RULES:\n"
                        "1. Structure your output exactly like this text block blueprint, with clearly separated marker lines:\n"
                        "   [SUMMARY_START]\n"
                        "   [Write a clean, single-paragraph macro financial summary here explicitly incorporating any active simulation impacts. Do not add bold headers inside this text section]\n"
                        "   [SUMMARY_END]\n\n"
                        "   [REVENUE_START]\n"
                        "   [List of bullet points for revenue lines here]\n"
                        "   [REVENUE_END]\n\n"
                        "   [COST_START]\n"
                        "   [List of bullet points for cost/opex lines here]\n"
                        "   [COST_END]\n\n"
                        "2. Present all line-item variances as a clean bulleted list. Never mix items into continuous paragraphs.\n"
                        "3. Format each list bullet exactly like this: '* **[Line Item Name]**: [Favorable/Unfavorable] variance of ₹[Absolute Variance Value] ([Percentage Variance accompanied strictly by 3 decimal numbers, eg: 7.778]%). [Synthesized Operational Reason or highlight missing notes].'\n"
                        "4. Write all numbers and monetary figures as plain text. Never surround numbers with dollar signs ($), asterisks (*), or mathematical markdown formatting symbols."
                    )
                },
                {
                    "role": "user",
                    "content": f"{simulation_context}Synthesize these variation sets:\n\n{data_string}"
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1200
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq API Link Failure: {str(e)}"

# ----------------------------------------------------------------------
# 5. Native DataFrame CSS Styling Injectors
# ----------------------------------------------------------------------
def style_materiality_status(val):
    if val == "Favorable":
        return "background-color: rgba(16, 185, 129, 0.15); color: #065F46; font-weight: bold;"
    elif val == "Unfavorable":
        return "background-color: rgba(239, 68, 68, 0.15); color: #991B1B; font-weight: bold;"
    return "color: #6B7280;"

def style_row_by_category(df_slice):
    styles = pd.DataFrame('', index=df_slice.index, columns=df_slice.columns)
    is_rev = df_slice['category'].astype(str).str.strip().str.lower() == 'revenue'
    styles.loc[is_rev, :] = 'background-color: rgba(30, 58, 138, 0.04); font-weight: 500;'
    return styles

# ----------------------------------------------------------------------
# CHART FIX 1: Explicit "Outside" Anchoring & Enforced Axis Pads
# ----------------------------------------------------------------------
def render_horizontal_bar_chart(df, title_label):
    df_sorted = df.sort_values(by='percentage_variance', ascending=True)
    df_sorted['bar_color'] = df_sorted['materiality_status'].apply(
        lambda status: '#10B981' if status == 'Favorable' else '#EF4444'
    )
    
    min_val = df_sorted['percentage_variance'].min()
    max_val = df_sorted['percentage_variance'].max()
    
    # FIXED: Enforce a strict minimum buffer of +/- 15% so small numbers never hit the edges
    x_min = min_val * 1.5 if min_val < -10.0 else -15.0
    x_max = max_val * 1.5 if max_val > 10.0 else 15.0

    fig = px.bar(
        df_sorted,
        x="percentage_variance",
        y="line item",
        orientation='h',
        labels={"percentage_variance": "Percentage Variance (%)", "line item": "Line Item"}
    )
    
    # FIXED: Hard-code textposition="outside" so Plotly never tries to squish text into a tiny bar
    fig.update_traces(
        marker_color=df_sorted['bar_color'],
        text=df_sorted['percentage_variance'].apply(lambda x: f" {x:+.3f}% "),
        textposition="outside", 
        textfont=dict(size=11, color='#1C1917'),
        cliponaxis=False 
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True, 
            gridcolor='#E2E8F0', 
            zeroline=True, 
            zerolinecolor='#94A3B8', 
            zerolinewidth=2.0, 
            ticksuffix="%",
            range=[x_min, x_max]
        ),
        yaxis=dict(showgrid=False, autorange="reversed"),
        margin=dict(l=200, r=80, t=20, b=20),
        height=max(300, len(df_sorted) * 38),
        font=dict(family="-apple-system, BlinkMacSystemFont, sans-serif", size=12)
    )
    
    fig.add_vline(x=10.0, line_width=1.5, line_dash="dash", line_color="#EF4444")
    fig.add_vline(x=-10.0, line_width=1.5, line_dash="dash", line_color="#EF4444")
    
    return fig

# ----------------------------------------------------------------------
# CHART FIX 2: Vertical Waterfalls + Auto Text-Wrapping Line Items
# ----------------------------------------------------------------------
def render_corporate_waterfall_chart(df, is_revenue_stream=True):
    base_budget = df['budget'].sum()
    
    # FIXED: Use Python textwrap to insert HTML line-breaks (<br>) so labels stack perfectly
    raw_labels = ["Total Budget Base"] + df['line item'].tolist() + ["Realized Outcome"]
    line_labels = ["<br>".join(textwrap.wrap(str(l), width=14)) for l in raw_labels]
    
    deltas = df['absolute_variance'].tolist()
    text_stamps = [f"₹{base_budget:,.0f}"]
    
    for x in deltas:
        text_stamps.append(f"{x:+,.0f}")
        
    actual_total = df['actual'].sum()
    text_stamps.append(f"₹{actual_total:,.0f}")
    
    measure_modes = ["absolute"] + ["relative"] * len(df) + ["total"]
    value_walks = [base_budget] + deltas + [0.0]
    
    # FIXED: Orientation reverted to "v". Vertical waterfalls handle text perfectly.
    fig = go.Figure(go.Waterfall(
        name="Bridge Walk",
        orientation="v", 
        measure=measure_modes,
        x=line_labels,
        y=value_walks,
        textposition="outside",
        text=text_stamps,
        connector={"line": {"color": "#94A3B8", "width": 1.5, "dash": "dot"}},
        totals={"marker": {"color": "#1E3A8A"}},
        decreasing={"marker": {"color": "#EF4444" if is_revenue_stream else "#10B981"}},
        increasing={"marker": {"color": "#10B981" if is_revenue_stream else "#EF4444"}}
    ))

    # Calculate top ceiling so text never clips out the top of the container
    y_max = max(value_walks)
    if actual_total > y_max: y_max = actual_total
    if base_budget > y_max: y_max = base_budget

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickprefix="₹", range=[0, y_max * 1.15]),
        xaxis=dict(tickangle=0), # Keep labels flat because we wrapped them nicely!
        margin=dict(l=60, r=40, t=40, b=80), # Large bottom margin for stacked names
        height=500, # Taller canvas to let the columns breathe
        font=dict(family="-apple-system, BlinkMacSystemFont, sans-serif", size=11)
    )
    return fig

# ----------------------------------------------------------------------
# 6. UI Render Layout Loop
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Sensitivity Simulators")
    revenue_sim = st.slider("Simulated Revenue Shift (%)", min_value=-50.0, max_value=50.0, value=0.0, step=0.5, format="%.3f%%")
    expense_sim = st.slider("Simulated Expense Shift (%)", min_value=-50.0, max_value=50.0, value=0.0, step=0.5, format="%.3f%%")
    
    st.markdown("---")
    st.markdown("## 📊 Executive View Option")
    dashboard_view_mode = st.slider(
        label="Select Dashboard View Profile",
        min_value=1,
        max_value=3,
        value=1,
        step=1,
        help="1: Standard Matrix | 2: Stream Breakdown | 3: Macro CFO Deep-Dive"
    )
    view_labels = {1: "1: Standard Unified Matrix", 2: "2: Consolidated Stream Breakdown", 3: "3: Macro CFO Deep-Dive (Waterfall Walk)"}
    st.caption(f"**Active View:** `{view_labels[dashboard_view_mode]}`")

    st.markdown("---")
    st.markdown("### ⚙️ Boundary Rules")
    materiality_threshold = st.number_input("Materiality Threshold (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)

st.markdown("## Data Ingestion Portal")
uploaded_file = st.file_uploader("Upload Target 'Budget vs Actual' Spreadsheet (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file is not None:
    selected_sheet = None
    if uploaded_file.name.endswith('.xlsx'):
        try:
            xl = pd.ExcelFile(uploaded_file)
            sheet_names = xl.sheet_names
            if len(sheet_names) > 1:
                selected_sheet = st.selectbox("📊 Multi-Sheet Excel Detected: Select Target View/Scenario", sheet_names)
        except:
            pass

    full_matrix, material_matrix = process_variance_sheet(uploaded_file, materiality_threshold, revenue_sim, expense_sim, selected_sheet)
    
    if full_matrix is not None and not full_matrix.empty:
        rev_mask = full_matrix['category'].str.strip().str.lower() == 'revenue'
        exp_mask = ~rev_mask
        
        rev_budget = full_matrix.loc[rev_mask, 'budget'].sum()
        rev_actual = full_matrix.loc[rev_mask, 'actual'].sum()
        rev_variance_abs = rev_actual - rev_budget
        rev_variance_pct = (rev_variance_abs / rev_budget * 100) if rev_budget != 0 else 0.0
        
        exp_budget = full_matrix.loc[exp_mask, 'budget'].sum()
        exp_actual = full_matrix.loc[exp_mask, 'actual'].sum()
        exp_variance_abs = exp_actual - exp_budget
        exp_variance_pct = (exp_variance_abs / exp_budget * 100) if exp_budget != 0 else 0.0

        profit_budget = rev_budget - exp_budget
        profit_actual = rev_actual - exp_actual
        profit_variance_abs = profit_actual - profit_budget
        profit_variance_pct = (profit_variance_abs / abs(profit_budget) * 100) if profit_budget != 0 else 0.0

        st.markdown("## Executive Performance Scorecard")
        m1, m2, m3, m4 = st.columns(4)
        
        m1.metric(label="Gross Realized Revenue", value=f"₹{rev_actual:,.2f}", delta=f"{rev_variance_pct:+.3f}% (₹{rev_variance_abs:,.2f})", delta_color="normal")
        m2.metric(label="Total Operational Spend", value=f"₹{exp_actual:,.2f}", delta=f"{-exp_variance_pct:+.3f}% (₹{exp_variance_abs:,.2f})", delta_color="inverse")
        m3.metric(label="Net Profit Realized", value=f"₹{profit_actual:,.2f}", delta=f"Target: ₹{profit_budget:,.2f}", delta_color="off")
        m4.metric(label="Net Margin Contribution", value=f"₹{profit_variance_abs:,.2f}", delta=f"{profit_variance_pct:+.3f}% Net", delta_color="normal")
        
        st.markdown("## Performance Metrics Ledger")
        tab1, tab2, tab3 = st.tabs([
            "Material Discrepancies (Flagged Anomaly Matrix)", 
            "Visual Performance Analytics Dashboard", 
            "Complete Financial Ledger"
        ])
        
        ledger_columns_config = {
            "budget": st.column_config.NumberColumn("Budget", format="₹%,.2f"),
            "actual": st.column_config.NumberColumn("Actual", format="₹%,.2f"),
            "absolute_variance": st.column_config.NumberColumn("Absolute Variance", format="₹%,.2f"),
            "percentage_variance": st.column_config.NumberColumn("Percentage Variance (%)", format="%.3f"),
            "line item": st.column_config.TextColumn("Line Item"),
            "category": st.column_config.TextColumn("Category"),
            "materiality_status": st.column_config.TextColumn("Materiality Status"),
            "operational notes": st.column_config.TextColumn("Operational Notes")
        }
        
        display_cols = ['line item', 'category', 'budget', 'actual', 'absolute_variance', 'percentage_variance', 'materiality_status', 'operational notes']
        full_display_cols = ['line item', 'category', 'budget', 'actual', 'absolute_variance', 'percentage_variance', 'materiality_status']
        
        with tab1:
            if not material_matrix.empty:
                styled_material_df = (
                    material_matrix[display_cols]
                    .style.apply(style_row_by_category, axis=None)
                    .map(style_materiality_status, subset=['materiality_status'])
                )
                st.dataframe(styled_material_df, use_container_width=True, hide_index=True, column_config=ledger_columns_config)
            else:
                st.info("Zero variance anomalies recorded within target boundaries.")
                
        with tab2:
            if not full_matrix.empty:
                full_rev_df = full_matrix[full_matrix['category'].str.strip().str.lower() == 'revenue']
                full_exp_df = full_matrix[full_matrix['category'].str.strip().str.lower() != 'revenue']
                
                mat_rev_df = material_matrix[material_matrix['category'].str.strip().str.lower() == 'revenue']
                mat_exp_df = material_matrix[material_matrix['category'].str.strip().str.lower() != 'revenue']

                if dashboard_view_mode == 1:
                    st.markdown("### Profile 1: Standard Outlier Variance Matrix (With 10% Risk Boundaries)")
                    fig_all = render_horizontal_bar_chart(material_matrix, "All Anomalies")
                    st.plotly_chart(fig_all, use_container_width=True, config={'displayModeBar': False})
                    
                elif dashboard_view_mode == 2:
                    st.markdown("### Profile 2: Consolidated Stream Breakdown (With 10% Risk Boundaries)")
                    v_col1, v_col2 = st.columns(2)
                    with v_col1:
                        st.markdown("#### Revenue Channel Deviations")
                        if not mat_rev_df.empty:
                            fig_rev = render_horizontal_bar_chart(mat_rev_df, "Revenue")
                            st.plotly_chart(fig_rev, use_container_width=True, config={'displayModeBar': False})
                        else:
                            st.info("No standalone material revenue variances to render.")
                    with v_col2:
                        st.markdown("#### Operational Expenditure Deviations")
                        if not mat_exp_df.empty:
                            fig_exp = render_horizontal_bar_chart(mat_exp_df, "Operating Expenses")
                            st.plotly_chart(fig_exp, use_container_width=True, config={'displayModeBar': False})
                        else:
                            st.info("No standalone material expenditure variances to render.")
                            
                elif dashboard_view_mode == 3:
                    st.markdown("### Profile 3: Macro CFO Deep-Dive (Corporate Variance Waterfall Bridges)")
                    st.markdown("#### Section A: Revenue Inflow Walk Bridge (Budget to Actual)")
                    if not full_rev_df.empty:
                        fig_water_rev = render_corporate_waterfall_chart(full_rev_df, is_revenue_stream=True)
                        st.plotly_chart(fig_water_rev, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("No revenue track item arrays available to compile bridge walk figures.")
                        
                    st.markdown("#### Section B: Operational Expenditure Walk Bridge (Budget to Actual)")
                    if not full_exp_df.empty:
                        fig_water_exp = render_corporate_waterfall_chart(full_exp_df, is_revenue_stream=False)
                        st.plotly_chart(fig_water_exp, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("No cost track item arrays available to compile spend bridge walk figures.")
                        
                st.caption("💡 Note: Horizontal charts feature explicit dashed vertical target lines at ±10% points to isolate risk-tolerance breaches. Waterfall walk charts provide an interactive step-by-step visual walk tracking cumulative accounting adjustments from Budget to Realized outcomes.")
            else:
                st.info("No visual anomalies to map. All performance parameters match budget boundaries.")
                
        with tab3:
            styled_full_df = (
                full_matrix[full_display_cols]
                .style.apply(style_row_by_category, axis=None)
                .map(style_materiality_status, subset=['materiality_status'])
            )
            st.dataframe(styled_full_df, use_container_width=True, hide_index=True, column_config=ledger_columns_config)
            
        st.markdown("## Executive Narrative Synthesis")
        if st.button("Generate Senior Director Variance Commentary Brief"):
            if not client:
                st.error("Authentication Missing: Configure your background environment key script.")
            else:
                with st.spinner("Processing calculations and generating brief..."):
                    raw_brief = generate_fp_a_commentary(material_matrix, revenue_sim, expense_sim)
                    
                    try:
                        summary_text = raw_brief.split("[SUMMARY_START]")[1].split("[SUMMARY_END]")[0].strip()
                    except:
                        summary_text = raw_brief
                        
                    try:
                        revenue_text = raw_brief.split("[REVENUE_START]")[1].split("[REVENUE_END]")[0].strip()
                    except:
                        revenue_text = ""
                        
                    try:
                        cost_text = raw_brief.split("[COST_START]")[1].split("[COST_END]")[0].strip()
                    except:
                        cost_text = ""
                    
                    st.markdown("---")
                    st.markdown("### Senior FP&A Director Commentary")
                    
                    with st.container():
                        st.markdown(
                            f'<div class="executive-brief-box">'
                            f'<div class="brief-heading">Executive Summary</div>'
                            f'<div class="brief-body-text">{summary_text}</div>',
                            unsafe_allow_html=True
                        )
                        
                        if revenue_text:
                            st.markdown('<div class="brief-heading">Material Revenue Variances</div>', unsafe_allow_html=True)
                            st.markdown(revenue_text)
                            
                        if cost_text:
                            st.markdown('<div class="brief-heading">Material Cost & OPEX Variances</div>', unsafe_allow_html=True)
                            st.markdown(cost_text)
                            
                        st.markdown('</div>', unsafe_allow_html=True)
    elif full_matrix is not None and full_matrix.empty:
        st.warning("No data records could be parsed. Check that budget/actual contain numeric information lines.")

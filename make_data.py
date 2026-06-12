import pandas as pd

# Define high-fidelity corporate financial records
data = {
    'Line Item': [
        'Enterprise Cloud Subscriptions', 
        'Hardware Lease Renewals', 
        'Contract Delivery Rebates',
        'Offshore Engineering Contractor Units', 
        'Executive Headhunter Fees', 
        'Digital Acquisition Marketing',
        'Corporate Office Electricity', 
        'Travel & Entertainment (Sales)', 
        'Strategic Retainer Fees', 
        'Miscellaneous Office Supplies'
    ],
    'Category': [
        'Revenue', 'Operating Expense', 'Revenue',
        'Cost of Goods Sold', 'Operating Expense', 'Operating Expense',
        'Fixed Overhead', 'Operating Expense', 'Cost of Goods Sold', 'Fixed Overhead'
    ],
    'Budget': [1200000, 45000, 0, 450000, 30000, 180000, 12000, 65000, 80000, 4000],
    'Actual': [1140000, 48500, 15000, 525000, 0, 125000, 16800, 63200, 80000, 4100],
    'Operational Notes': [
        'Downside variance due to Q2 churn from two major legacy accounts migrating to on-premise solutions.',
        'Slightly over budget due to unexpected mid-term lease adjustment indexations linked to regional inflation.',
        'Unbudgeted revenue realized from an out-of-period vendor volume performance milestone rebate.',
        'Significant overspend driven by emergency onboarding of external engineering squads to resolve critical backend scaling issues.',
        'Zero spend incurred as executive leadership positions were successfully filled via internal promotions instead of third-party firms.',
        'Favorable variance achieved by pausing low-efficiency search engine marketing channels and optimizing organic landing page conversions.',
        'Unfavorable spike caused by summer cooling demands combined with a localized utility tariff hike of 15%.',
        'Tracked under budget due to strict regional travel pre-approval mandates enforced across the enterprise sales divisions.',
        'Aligned perfectly with contractually locked fixed quarterly vendor retainer terms.',
        'Minor variance within standard acceptable spending friction limits.'
    ]
}

# Construct DataFrame and export to target format
df = pd.DataFrame(data)
df.to_excel('budget_vs_actual.xlsx', index=False)
print(">>> SUCCESS: budget_vs_actual.xlsx has been generated.")
"""
Visualization Generator for Legal AI Survey Analysis
Creates charts and graphs to illustrate key findings
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create output directory
output_dir = Path("visualizations")
output_dir.mkdir(exist_ok=True)

# Load data
csv_path = r"c:\Users\HP\legalizeme-bi\AI in Legal Practice_ Survey on Domain-Adapted LLMs and Legal Tech in Kenya  (Responses) - Form Responses 1.csv"
df = pd.read_csv(csv_path)

print("Generating visualizations...")
print("=" * 80)

# ============================================================================
# VISUALIZATION 1: Feature Priorities (Bar Chart)
# ============================================================================
print("\n1. Creating Feature Priorities chart...")

features_col = '18. Key features I would prioritize in a legal AI tool (choose up to 3):  '
if features_col in df.columns:
    features = df[features_col].dropna()
    all_features = []
    for feature_list in features:
        feature_items = [f.strip() for f in str(feature_list).split(',')]
        all_features.extend(feature_items)

    from collections import Counter
    feature_counts = Counter(all_features)

    # Create figure
    plt.figure(figsize=(14, 8))
    features_sorted = sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)
    features_names = [f[0][:50] + '...' if len(f[0]) > 50 else f[0] for f in features_sorted]
    features_values = [f[1] for f in features_sorted]

    # Calculate percentages
    total = len(df)
    percentages = [(v/total)*100 for v in features_values]

    # Create horizontal bar chart
    bars = plt.barh(range(len(features_names)), features_values, color='#2E86AB')
    plt.yticks(range(len(features_names)), features_names)
    plt.xlabel('Number of Respondents', fontsize=12, fontweight='bold')
    plt.title('Top Prioritized Features in Legal AI Tools\n(n=7)',
              fontsize=14, fontweight='bold', pad=20)

    # Add value labels and percentages
    for i, (bar, val, pct) in enumerate(zip(bars, features_values, percentages)):
        plt.text(val + 0.1, i, f'{val} ({pct:.1f}%)',
                va='center', fontsize=10, fontweight='bold')

    # Add reference line at 100%
    if 7 in features_values:
        plt.axvline(x=7, color='red', linestyle='--', linewidth=2, alpha=0.5, label='100% (Universal)')

    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / 'feature_priorities.png', dpi=300, bbox_inches='tight')
    print(f"   Saved: {output_dir / 'feature_priorities.png'}")
    plt.close()

# ============================================================================
# VISUALIZATION 2: Trust vs Citation Importance (Scatter)
# ============================================================================
print("\n2. Creating Trust vs Citation Importance scatter plot...")

trust_col = '15. I trust AI outputs without manual verification.  '
citation_col = '16. Accurate citation and provenance (knowing where the information came from) are essential for any legal AI tool.  '

if trust_col in df.columns and citation_col in df.columns:
    plt.figure(figsize=(10, 8))

    trust_data = df[trust_col].dropna()
    citation_data = df[citation_col].dropna()

    # Create scatter plot with jitter
    x = trust_data.values + np.random.normal(0, 0.05, len(trust_data))
    y = citation_data.values + np.random.normal(0, 0.05, len(citation_data))

    plt.scatter(x, y, s=200, alpha=0.6, c='#A23B72', edgecolors='black', linewidth=2)

    # Add mean lines
    plt.axhline(y=citation_data.mean(), color='blue', linestyle='--',
                linewidth=2, label=f'Mean Citation Importance: {citation_data.mean():.2f}')
    plt.axvline(x=trust_data.mean(), color='red', linestyle='--',
                linewidth=2, label=f'Mean Trust: {trust_data.mean():.2f}')

    plt.xlabel('Trust AI Without Verification (1=Low, 5=High)', fontsize=12, fontweight='bold')
    plt.ylabel('Citation Importance (1=Low, 5=High)', fontsize=12, fontweight='bold')
    plt.title('Trust vs Citation Importance\nLow Trust + High Citation Need = RAG Essential\n(n=7)',
              fontsize=14, fontweight='bold', pad=20)

    plt.xlim(0.5, 5.5)
    plt.ylim(0.5, 5.5)
    plt.xticks([1, 2, 3, 4, 5])
    plt.yticks([1, 2, 3, 4, 5])
    plt.grid(True, alpha=0.3)
    plt.legend(loc='lower right', fontsize=10)

    # Add annotation
    plt.text(1.5, 4.5, 'Ideal for RAG:\nLow Trust + High Citation Need',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3),
             fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / 'trust_vs_citations.png', dpi=300, bbox_inches='tight')
    print(f"   Saved: {output_dir / 'trust_vs_citations.png'}")
    plt.close()

# ============================================================================
# VISUALIZATION 3: AI Adoption & Willingness to Pay (Pie Charts)
# ============================================================================
print("\n3. Creating AI Adoption and Willingness to Pay pie charts...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# AI Adoption
ai_col = '8. Do you currently use any AI tools (e.g., ChatGPT, Copilot, Claude, Gemini, Counsel AI, or others) to support legal tasks or decision-making? '
if ai_col in df.columns:
    ai_usage = df[ai_col].value_counts()
    colors1 = ['#2E86AB', '#F24236']
    explode1 = (0.1, 0)

    wedges1, texts1, autotexts1 = ax1.pie(ai_usage.values, labels=ai_usage.index, autopct='%1.1f%%',
                                            colors=colors1, explode=explode1, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})

    ax1.set_title('Current AI Tool Usage\n(n=7)', fontsize=14, fontweight='bold', pad=20)

    # Make percentage text larger
    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')

# Willingness to Pay
wtp_col = '17. If a legal AI tool saved you at least 5–10 hours per week, would you be willing to pay for it?'
if wtp_col in df.columns:
    wtp = df[wtp_col].value_counts()
    colors2 = ['#F18F01', '#2E86AB', '#A23B72']
    explode2 = tuple([0.05] * len(wtp))  # Match length of data

    wedges2, texts2, autotexts2 = ax2.pie(wtp.values, labels=wtp.index, autopct='%1.1f%%',
                                            colors=colors2[:len(wtp)], explode=explode2, startangle=90,
                                            textprops={'fontsize': 10, 'fontweight': 'bold'})

    ax2.set_title('Willingness to Pay\n(for 5-10 hrs/week savings, n=7)',
                  fontsize=14, fontweight='bold', pad=20)

    # Make percentage text larger
    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')

plt.tight_layout()
plt.savefig(output_dir / 'adoption_and_willingness.png', dpi=300, bbox_inches='tight')
print(f"   Saved: {output_dir / 'adoption_and_willingness.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 4: Pain Points Comparison (Horizontal Bar)
# ============================================================================
print("\n4. Creating Pain Points comparison chart...")

pain_points = {
    'Time Burden on\nResearch & Drafting': df['5. I spend excessive time on legal research and drafting.  '].mean(),
    'Access to Legal\nResources Challenge': df['6. Access to up-to-date case law, statutes, document templates and other relevant research material is a major challenge in my work.  '].mean(),
    'AI Time\nSavings Impact': df['12. AI tools have saved me significant time on routine tasks (e.g., research, drafting, summarization).  '].mean(),
    'Trust Without\nVerification': df['15. I trust AI outputs without manual verification.  '].mean(),
    'Citation\nImportance': df['16. Accurate citation and provenance (knowing where the information came from) are essential for any legal AI tool.  '].mean(),
}

plt.figure(figsize=(12, 8))
categories = list(pain_points.keys())
values = list(pain_points.values())

# Color code: red for problems, green for positive, blue for importance
colors_map = ['#F24236', '#F24236', '#06A77D', '#A23B72', '#2E86AB']

bars = plt.barh(categories, values, color=colors_map, edgecolor='black', linewidth=1.5)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, values)):
    # Determine severity
    if i <= 1:  # Pain points
        severity = 'HIGH' if val >= 4 else 'MEDIUM' if val >= 3 else 'LOW'
    elif i == 2:  # Positive impact
        severity = 'HIGH' if val >= 4 else 'MEDIUM' if val >= 3 else 'LOW'
    else:  # Importance/trust
        severity = 'HIGH' if val >= 4 else 'MEDIUM' if val >= 3 else 'LOW'

    plt.text(val + 0.1, i, f'{val:.2f}/5 ({severity})',
            va='center', fontsize=11, fontweight='bold')

plt.xlabel('Average Score (1-5 Likert Scale)', fontsize=12, fontweight='bold')
plt.title('Key Metrics: Pain Points, Impact & Requirements\n(n=7)',
          fontsize=14, fontweight='bold', pad=20)
plt.xlim(0, 5.5)
plt.xticks([1, 2, 3, 4, 5])
plt.axvline(x=3, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Neutral (3.0)')
plt.axvline(x=4, color='orange', linestyle='--', linewidth=1, alpha=0.5, label='High (4.0)')
plt.legend(loc='lower right')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'pain_points_comparison.png', dpi=300, bbox_inches='tight')
print(f"   Saved: {output_dir / 'pain_points_comparison.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 5: User Roles Distribution
# ============================================================================
print("\n5. Creating User Roles distribution chart...")

role_col = '1. What is your current role?'
if role_col in df.columns:
    roles = df[role_col].value_counts()

    plt.figure(figsize=(10, 8))
    colors_roles = ['#2E86AB', '#F18F01', '#A23B72', '#06A77D']
    explode_roles = [0.1 if i == 0 else 0.05 for i in range(len(roles))]

    wedges, texts, autotexts = plt.pie(roles.values, labels=roles.index, autopct='%1.1f%%',
                                        colors=colors_roles[:len(roles)], explode=explode_roles,
                                        startangle=45, textprops={'fontsize': 12, 'fontweight': 'bold'})

    plt.title('Survey Respondent Roles\n(n=7)', fontsize=14, fontweight='bold', pad=20)

    # Make percentage text larger
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')

    plt.tight_layout()
    plt.savefig(output_dir / 'respondent_roles.png', dpi=300, bbox_inches='tight')
    print(f"   Saved: {output_dir / 'respondent_roles.png'}")
    plt.close()

# ============================================================================
# VISUALIZATION 6: Issues with Current AI Tools
# ============================================================================
print("\n6. Creating Issues with Current AI Tools chart...")

# Manual categorization based on analysis
issue_categories = {
    'Accuracy/\nHallucinations': 2,
    'Citation/\nReferences': 1,
    'Speed/\nPerformance': 1,
    'Relevance to\nLocal Context': 1,
    'Comprehensiveness': 1,
    'Trust/\nReliability': 1
}

plt.figure(figsize=(12, 7))
categories_issues = list(issue_categories.keys())
values_issues = list(issue_categories.values())

# Calculate percentages (out of 4 who reported issues)
percentages_issues = [(v/4)*100 for v in values_issues]

bars = plt.bar(categories_issues, values_issues, color='#F24236',
               edgecolor='black', linewidth=1.5, alpha=0.8)

# Add value labels
for bar, val, pct in zip(bars, values_issues, percentages_issues):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{val}\n({pct:.0f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.ylabel('Number of Mentions', fontsize=12, fontweight='bold')
plt.title('Issues Reported with Current AI Tools\n(From 4 respondents who reported issues)',
          fontsize=14, fontweight='bold', pad=20)
plt.ylim(0, max(values_issues) + 0.8)
plt.xticks(rotation=0, ha='center')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'ai_issues_reported.png', dpi=300, bbox_inches='tight')
print(f"   Saved: {output_dir / 'ai_issues_reported.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 7: Key Findings Summary Dashboard
# ============================================================================
print("\n7. Creating Key Findings Summary dashboard...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# Title
fig.suptitle('Legal AI Survey - Key Findings Summary Dashboard\n(n=7, Kenya, October 2025)',
             fontsize=16, fontweight='bold', y=0.98)

# Metric 1: Citations Demand
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.7, '100%', ha='center', va='center', fontsize=48, fontweight='bold', color='#2E86AB')
ax1.text(0.5, 0.3, 'Demand Accurate\nCitations', ha='center', va='center', fontsize=14, fontweight='bold')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#2E86AB', linewidth=3))

# Metric 2: Kenya-Specific Coverage
ax2 = fig.add_subplot(gs[0, 1])
ax2.text(0.5, 0.7, '86%', ha='center', va='center', fontsize=48, fontweight='bold', color='#F18F01')
ax2.text(0.5, 0.3, 'Need Kenya-Specific\nCoverage', ha='center', va='center', fontsize=14, fontweight='bold')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
ax2.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#F18F01', linewidth=3))

# Metric 3: Willing to Pay
ax3 = fig.add_subplot(gs[0, 2])
ax3.text(0.5, 0.7, '100%', ha='center', va='center', fontsize=48, fontweight='bold', color='#06A77D')
ax3.text(0.5, 0.3, 'Willing to Pay\n(5-10 hrs/week)', ha='center', va='center', fontsize=14, fontweight='bold')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#06A77D', linewidth=3))

# Metric 4: AI Adoption
ax4 = fig.add_subplot(gs[1, 0])
ax4.text(0.5, 0.7, '86%', ha='center', va='center', fontsize=48, fontweight='bold', color='#A23B72')
ax4.text(0.5, 0.3, 'Already Use\nAI Tools', ha='center', va='center', fontsize=14, fontweight='bold')
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')
ax4.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#A23B72', linewidth=3))

# Metric 5: Accuracy Issues
ax5 = fig.add_subplot(gs[1, 1])
ax5.text(0.5, 0.7, '50%', ha='center', va='center', fontsize=48, fontweight='bold', color='#F24236')
ax5.text(0.5, 0.3, 'Report Accuracy\nIssues', ha='center', va='center', fontsize=14, fontweight='bold')
ax5.set_xlim(0, 1)
ax5.set_ylim(0, 1)
ax5.axis('off')
ax5.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#F24236', linewidth=3))

# Metric 6: Trust Score
ax6 = fig.add_subplot(gs[1, 2])
ax6.text(0.5, 0.7, '2.29/5', ha='center', va='center', fontsize=40, fontweight='bold', color='#C73E1D')
ax6.text(0.5, 0.3, 'Trust Without\nVerification', ha='center', va='center', fontsize=14, fontweight='bold')
ax6.text(0.5, 0.15, '(LOW)', ha='center', va='center', fontsize=12, fontweight='bold', color='red')
ax6.set_xlim(0, 1)
ax6.set_ylim(0, 1)
ax6.axis('off')
ax6.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#C73E1D', linewidth=3))

# Bottom section: Key implications
ax7 = fig.add_subplot(gs[2, :])
ax7.axis('off')

implications_text = """
KEY IMPLICATIONS FOR DOMAIN-ADAPTED LLMs WITH RAG:

1. RAG IS ESSENTIAL: 100% demand citations + 71% don't trust without verification
   → Retrieval-Augmented Generation provides grounded, verifiable responses

2. DOMAIN ADAPTATION NECESSARY: 86% need Kenya-specific coverage + 50% accuracy issues
   → Generic LLMs trained on Western law insufficient for African legal practice

3. MARKET READY: 100% willing to pay + 86% already use AI + 4.14/5 time savings
   → Economic viability proven; strong ROI potential

4. ACCURACY CRITICAL: 50% report issues + 2.29/5 trust + 4.14/5 citation importance
   → RAG + domain adaptation essential for professional-grade reliability

5. INFRASTRUCTURE MATTERS: 57% want offline mode + African context constraints
   → Solution must work in low-bandwidth, infrastructure-constrained environments
"""

ax7.text(0.05, 0.5, implications_text, ha='left', va='center',
        fontsize=11, family='monospace',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, pad=1))

plt.savefig(output_dir / 'key_findings_dashboard.png', dpi=300, bbox_inches='tight')
print(f"   Saved: {output_dir / 'key_findings_dashboard.png'}")
plt.close()

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 80)
print(f"\nAll visualizations saved to: {output_dir.absolute()}")
print("\nGenerated files:")
print("  1. feature_priorities.png - Top requested features")
print("  2. trust_vs_citations.png - Trust vs Citation importance scatter")
print("  3. adoption_and_willingness.png - AI adoption & willingness to pay")
print("  4. pain_points_comparison.png - Key metrics comparison")
print("  5. respondent_roles.png - User role distribution")
print("  6. ai_issues_reported.png - Problems with current AI")
print("  7. key_findings_dashboard.png - Summary dashboard")
print("\nThese visualizations are ready to use in:")
print("  - Research papers")
print("  - Presentations")
print("  - Grant proposals")
print("  - Product pitches")
print("\n" + "=" * 80)

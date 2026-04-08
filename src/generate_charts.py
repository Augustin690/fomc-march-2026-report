import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'charts')
os.makedirs(OUTPUT, exist_ok=True)

# --- Style constants ---
BG = '#0a1628'
CARD = '#0f1f38'
TEXT = '#e8edf5'
MUTED = '#8899b4'
TEAL = '#00d4aa'
RED = '#ff6b6b'
GOLD = '#ffd700'
BLUE = '#4e9fff'
PURPLE = '#a78bfa'
FONT = 'DejaVu Sans'
DPI = 200

def style_ax(ax, fig, title, ylabel=None, xlabel=None):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(MUTED)
    ax.spines['bottom'].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.yaxis.grid(True, color='#1a2d4d', linewidth=0.5)
    ax.xaxis.grid(False)
    ax.set_title(title, color=TEXT, fontsize=13, fontfamily=FONT, fontweight='bold', pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED, fontsize=9, fontfamily=FONT)
    if xlabel:
        ax.set_xlabel(xlabel, color=MUTED, fontsize=9, fontfamily=FONT)


# ========== CHART 1: Inflation ==========
def chart_inflation():
    months = ['Mar 25','Apr 25','May 25','Jun 25','Jul 25','Aug 25','Sep 25','Oct 25','Nov 25','Dec 25','Jan 26','Feb 26']
    cpi_idx = [312.345,313.023,313.175,313.044,313.569,314.062,314.732,315.631,316.528,317.604,318.961,319.679,
               319.785,320.302,320.620,321.435,322.169,323.291,324.245,325.063,326.031,326.588,327.460]
    cpi_yoy = [(cpi_idx[i+12] - cpi_idx[i]) / cpi_idx[i] * 100 for i in range(11)]  # Mar25-Jan26 = 11 values? No, 12-0..10 = 11
    # index 12 is Mar 25 vs index 0 Mar 24. We have indices 0..22, so 12..22 = 11 YoY values for Mar25..Jan26
    # But x-axis has 12 labels (Mar25..Feb26). CPI YoY: Mar25..Jan26 = 11 values (no Feb26 CPI YoY since we have 23 vals)
    # Actually: 23 values, indices 0-22. YoY from index 12 to 22 = 11 values. But wait:
    # index 12 = Mar 25 vs index 0 = Mar 24 ... index 22 = Jan 26 vs index 10 = Jan 25
    # That gives Mar25 through Jan26 = 11 months. No Feb26 YoY (would need index 23 which doesn't exist).
    # Wait, we have 23 values. 23-12=11. So 11 YoY values for Mar25-Jan26.
    # But the user says "Compute YoY% starting at index 12 (Mar 25 vs Mar 24)". Let me recount:
    # Indices 0..22 = 23 values. YoY: i in range(12, 23) → 11 values.
    # Actually re-read: there are 23 CPI values. Index 0=Mar24, index 12=Mar25, index 22=Jan26.
    # So CPI YoY has 11 values: Mar25..Jan26. Missing Feb26.

    cpi_yoy = [(cpi_idx[i] - cpi_idx[i-12]) / cpi_idx[i-12] * 100 for i in range(12, 23)]

    # Core PCE: 24 values, Feb 2024 to Jan 2026. Index 0=Feb24, index 12=Feb25, index 23=Jan26
    pce_idx = [121.537,122.009,122.304,122.383,122.677,122.911,123.128,123.466,123.832,123.962,124.196,124.587,
               125.145,125.267,125.502,125.790,126.121,126.430,126.714,126.954,127.245,127.473,127.929,128.394]
    pce_yoy = [(pce_idx[i] - pce_idx[i-12]) / pce_idx[i-12] * 100 for i in range(12, 24)]
    # 12 YoY values: Feb25..Jan26. Skip first (Feb25), keep Mar25..Jan26 = 11 values
    pce_yoy_aligned = pce_yoy[1:]  # Mar25..Jan26 = 11 values

    fig, ax = plt.subplots(figsize=(12, 6))
    style_ax(ax, fig, "Inflation: CPI vs Core PCE (YoY%)")

    x = np.arange(len(months))
    # CPI: 11 values → months[0:11] = Mar25..Jan26
    ax.plot(x[:11], cpi_yoy, color=GOLD, linewidth=2, marker='o', markersize=4, label='CPI YoY%')
    # Core PCE: 11 values → months[0:11] = Mar25..Jan26
    ax.plot(x[:11], pce_yoy_aligned, color=RED, linewidth=2.5, marker='o', markersize=4, label='Core PCE YoY%')
    ax.axhline(2.0, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.text(x[-1], 2.05, "Fed 2% Target", color=RED, fontsize=8, fontfamily=FONT, ha='right', va='bottom')

    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=7)
    ax.legend(facecolor=CARD, edgecolor=MUTED, labelcolor=TEXT, fontsize=9)
    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_inflation.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_inflation.png done")


# ========== CHART 2: Unemployment ==========
def chart_unemployment():
    months = ['Mar 24','Apr 24','May 24','Jun 24','Jul 24','Aug 24','Sep 24','Oct 24','Nov 24','Dec 24',
              'Jan 25','Feb 25','Mar 25','Apr 25','May 25','Jun 25','Jul 25','Aug 25','Sep 25',
              'Nov 25','Dec 25','Jan 26','Feb 26']
    data = [3.9,3.9,3.9,4.1,4.2,4.2,4.1,4.1,4.2,4.1,4.0,4.2,4.2,4.2,4.3,4.1,4.3,4.3,4.4,4.5,4.4,4.3,4.4]

    fig, ax = plt.subplots(figsize=(12, 6))
    style_ax(ax, fig, "Unemployment Rate (%)")

    x = np.arange(len(months))
    ax.plot(x, data, color=GOLD, linewidth=2, marker='o', markersize=4)
    ax.axhline(4.5, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.text(x[-1], 4.52, "Sahm Rule Proximity", color=RED, fontsize=8, fontfamily=FONT, ha='right', va='bottom')
    ax.set_ylim(3.6, 4.8)
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=7)
    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_unemployment.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_unemployment.png done")


# ========== CHART 3: NFP ==========
def chart_nfp():
    nfp = [157466,157530,157608,157695,157748,157757,157912,157945,158079,158316,158268,158310,
           158377,158485,158498,158478,158542,158472,158548,158408,158449,158432,158558,158466]
    changes = [nfp[i+1] - nfp[i] for i in range(len(nfp)-1)]
    months = ['Apr 24','May 24','Jun 24','Jul 24','Aug 24','Sep 24','Oct 24','Nov 24','Dec 24',
              'Jan 25','Feb 25','Mar 25','Apr 25','May 25','Jun 25','Jul 25','Aug 25','Sep 25',
              'Oct 25','Nov 25','Dec 25','Jan 26','Feb 26']

    fig, ax = plt.subplots(figsize=(12, 6))
    style_ax(ax, fig, "Nonfarm Payrolls — Monthly Change (Thousands)")

    colors = [TEAL if c >= 0 else RED for c in changes]
    x = np.arange(len(months))
    ax.bar(x, changes, color=colors, width=0.6)
    ax.axhline(0, color=MUTED, linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=7)
    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_nfp.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_nfp.png done")


# ========== CHART 4: GDP ==========
def chart_gdp():
    quarters = ['Q1 23','Q2 23','Q3 23','Q4 23','Q1 24','Q2 24','Q3 24','Q4 24','Q1 25','Q2 25','Q3 25','Q4 25']
    data = [2.9,2.5,4.7,3.4,0.8,3.6,3.3,1.9,-0.6,3.8,4.4,0.7]

    def gdp_color(v):
        if v < 0: return RED
        elif v < 1.5: return GOLD
        else: return TEAL

    colors = [gdp_color(v) for v in data]

    fig, ax = plt.subplots(figsize=(12, 6))
    style_ax(ax, fig, "Real GDP Growth Rate (% QoQ Annualized)")

    x = np.arange(len(quarters))
    ax.bar(x, data, color=colors, width=0.6)
    ax.axhline(0, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, rotation=45, ha='right', fontsize=7)
    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_gdp.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_gdp.png done")


# ========== CHART 5: Fed Funds ==========
def chart_fedfunds():
    months = ['Oct 23','Nov 23','Dec 23','Jan 24','Feb 24','Mar 24','Apr 24','May 24','Jun 24','Jul 24',
              'Aug 24','Sep 24','Oct 24','Nov 24','Dec 24','Jan 25','Feb 25','Mar 25','Apr 25','May 25',
              'Jun 25','Jul 25','Aug 25','Sep 25','Oct 25','Nov 25','Dec 25','Jan 26','Feb 26','Mar 26']
    data = [5.33,5.33,5.33,5.33,5.33,5.33,5.33,5.33,5.33,5.33,5.33,5.13,4.83,4.64,4.48,4.33,4.33,4.33,
            4.33,4.33,4.33,4.33,4.33,4.22,4.09,3.88,3.72,3.64,3.64,3.64]

    fig, ax = plt.subplots(figsize=(12, 6))
    style_ax(ax, fig, "Effective Federal Funds Rate (%)")

    x = np.arange(len(months))
    ax.step(x, data, color=PURPLE, linewidth=2, where='mid')

    # Shade cutting phase: Sep 24 (index 11) to Dec 25 (index 26)
    ax.axvspan(11, 26, alpha=0.1, color=TEAL)
    # Shade pause phase: Jan 26 (index 27) to Mar 26 (index 29)
    ax.axvspan(27, 29, alpha=0.1, color=GOLD)

    # Annotations
    ax.annotate("Cuts Begin", xy=(11, data[11]), xytext=(8, data[11]+0.25),
                color=TEAL, fontsize=9, fontfamily=FONT, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.2))
    ax.annotate("Pause", xy=(27, data[27]), xytext=(27, data[27]+0.35),
                color=GOLD, fontsize=9, fontfamily=FONT, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.2))

    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=6)
    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_fedfunds.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_fedfunds.png done")


# ========== CHART 6: Dot Plot ==========
def chart_dotplot():
    dot_data = {
        '2026': {3.625:7, 3.375:7, 3.125:2, 2.875:2, 2.625:1},
        '2027': {3.875:1, 3.625:3, 3.375:4, 3.125:6, 2.875:3, 2.625:1, 2.375:1},
        '2028': {3.875:1, 3.625:3, 3.375:3, 3.125:7, 2.875:3, 2.625:2},
        'Longer Run': {3.875:1, 3.750:1, 3.625:1, 3.500:1, 3.375:2, 3.250:1, 3.125:3, 3.000:5, 2.875:2, 2.625:2},
    }
    medians = {'2026': 3.375, '2027': 3.125, '2028': 3.125, 'Longer Run': 3.0625}
    years = ['2026', '2027', '2028', 'Longer Run']

    fig, ax = plt.subplots(figsize=(12, 8))
    style_ax(ax, fig, "FOMC Dot Plot — March 2026 SEP")

    x_positions = {y: i for i, y in enumerate(years)}
    dot_spread = 0.08  # horizontal spread per dot (matches ECharts 0.08 offset)

    for year, rates in dot_data.items():
        xc = x_positions[year]
        for rate, count in rates.items():
            offsets = np.linspace(-(count-1)*dot_spread/2, (count-1)*dot_spread/2, count)
            for off in offsets:
                ax.plot(xc + off, rate, 'o', color=BLUE, markersize=10,
                        markeredgecolor=(1, 1, 1, 0.2), markeredgewidth=0.8,
                        alpha=0.85, zorder=3)

    # Medians
    for year, med in medians.items():
        xc = x_positions[year]
        ax.plot(xc, med, 'D', color=GOLD, markersize=14, markeredgecolor='white',
                markeredgewidth=1.5, zorder=4)

    ax.set_ylim(2.25, 4.0)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.125))
    ax.yaxis.grid(True, which='major', color=(1, 1, 1, 0.04), linewidth=0.5)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f'{v:.2f}%' if v % 0.25 == 0 else ''))
    ax.xaxis.grid(True, color=(1, 1, 1, 0.04), linewidth=0.5)

    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, fontsize=12, fontweight='bold', color=TEXT)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0],[0], marker='o', color='w', markerfacecolor=BLUE, markersize=10,
               markeredgecolor=(1, 1, 1, 0.2), label='Participant', linestyle='None'),
        Line2D([0],[0], marker='D', color='w', markerfacecolor=GOLD, markersize=12,
               markeredgecolor='white', label='Median', linestyle='None'),
    ]
    ax.legend(handles=legend_elements, facecolor=CARD, edgecolor=MUTED, labelcolor=TEXT,
              fontsize=10, loc='upper right')

    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_dotplot.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_dotplot.png done")


# ========== CHART 7: Risk Balance ==========
def chart_risk_balance():
    categories = ['GDP Growth', 'Unemployment', 'PCE Inflation', 'Core PCE']
    downside = [14, 0, 0, 0]
    balanced = [5, 3, 2, 3]
    upside = [0, 16, 17, 16]

    fig, ax = plt.subplots(figsize=(12, 6))
    style_ax(ax, fig, "FOMC Risk Assessment Balance — March 2026")

    y = np.arange(len(categories))
    bar_h = 0.5

    # Downside as negative
    ax.barh(y, [-d for d in downside], height=bar_h, color=RED, label='Downside')
    # Balanced: starts at -downside, goes right
    # Actually center around zero: downside goes left from 0, balanced right from 0, upside right from balanced
    # Re-read: "Center the chart around zero" with downside as negative direction
    ax.barh(y, balanced, height=bar_h, left=[0]*4, color=GOLD, label='Balanced')
    ax.barh(y, upside, height=bar_h, left=balanced, color=TEAL, label='Upside')

    # Value labels
    for i in range(len(categories)):
        if downside[i] > 0:
            ax.text(-downside[i]/2, i, str(downside[i]), ha='center', va='center', color=TEXT, fontsize=9, fontweight='bold', fontfamily=FONT)
        if balanced[i] > 0:
            ax.text(balanced[i]/2, i, str(balanced[i]), ha='center', va='center', color=BG, fontsize=9, fontweight='bold', fontfamily=FONT)
        if upside[i] > 0:
            ax.text(balanced[i] + upside[i]/2, i, str(upside[i]), ha='center', va='center', color=BG, fontsize=9, fontweight='bold', fontfamily=FONT)

    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=10, color=TEXT, fontfamily=FONT)
    ax.axvline(0, color=MUTED, linewidth=0.8)
    ax.legend(facecolor=CARD, edgecolor=MUTED, labelcolor=TEXT, fontsize=9, loc='lower right')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT}/chart_risk_balance.png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    print("chart_risk_balance.png done")


if __name__ == '__main__':
    chart_inflation()
    chart_unemployment()
    chart_nfp()
    chart_gdp()
    chart_fedfunds()
    chart_dotplot()
    chart_risk_balance()
    # Verify
    files = os.listdir(OUTPUT)
    pngs = [f for f in files if f.endswith('.png')]
    print(f"\nGenerated {len(pngs)} PNGs in {OUTPUT}:")
    for f in sorted(pngs):
        print(f"  {f}")

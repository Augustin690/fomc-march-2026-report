# March 2026 FOMC Meeting — Macro Context & SEP Analysis

A comprehensive analysis of the March 17-18, 2026 Federal Open Market Committee meeting, covering the macroeconomic backdrop (inflation, labor market, GDP) and a detailed spotlight on the Summary of Economic Projections (SEP) and dot plot.

## Structure

```
├── report/
│   └── fomc-march-2026-report.html   # Interactive scrollytelling report (ECharts + GSAP)
├── charts/
│   ├── chart_inflation.png            # CPI YoY vs Core PCE YoY
│   ├── chart_unemployment.png         # Unemployment rate trend
│   ├── chart_nfp.png                  # Monthly nonfarm payroll changes
│   ├── chart_gdp.png                  # Quarterly GDP growth
│   ├── chart_fedfunds.png             # Fed funds rate path
│   ├── chart_dotplot.png              # FOMC dot plot
│   └── chart_risk_balance.png         # Risk assessment balance
├── source_docs/
│   ├── fomc_statement_mar2026.pdf     # Official FOMC statement
│   └── fomc_projections_mar2026.pdf   # Official SEP materials
├── src/
│   └── generate_charts.py             # Matplotlib chart generation script
├── requirements.txt
└── README.md
```

## Key Findings

- **Rates held** at 3.50-3.75% with one dissent (Miran, favoring a 25bp cut)
- **Core PCE** re-accelerated to 3.06% YoY — well above the 2% target
- **GDP** slowed to 0.7% in Q4 2025 — near stall speed
- **Dot plot** split 7-7 between holding and cutting once more in 2026
- **Risk assessment** is the most stagflationary since March 2022

## Usage

Open `report/fomc-march-2026-report.html` in a browser for the interactive report, or view the static charts in `charts/`.

To regenerate charts:

```bash
pip install -r requirements.txt
python src/generate_charts.py
```

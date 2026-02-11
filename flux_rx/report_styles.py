# Flux-RX Report Styles: CSS for HTML reports

BASE_CSS = """
:root {
    --bg-primary: #09090b;
    --bg-secondary: #18181b;
    --bg-tertiary: #27272a;
    --bg-elevated: #3f3f46;
    --text-primary: #fafafa;
    --text-secondary: #a1a1aa;
    --text-muted: #71717a;
    --border: #27272a;
    --border-hover: #3f3f46;
    --accent: #3b82f6;
    --accent-hover: #60a5fa;
    --positive: #22c55e;
    --positive-bg: rgba(34, 197, 94, 0.1);
    --negative: #ef4444;
    --negative-bg: rgba(239, 68, 68, 0.1);
    --warning: #f59e0b;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.5;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
}

.app { display: flex; min-height: 100vh; }
.sidebar {
    width: 280px;
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
    padding: 24px 0;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    z-index: 100;
}
.sidebar-header { padding: 0 24px 24px; border-bottom: 1px solid var(--border); }
.logo { font-size: 20px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; }
.logo span { color: var(--accent); }
.sidebar-nav { padding: 16px 12px; }
.nav-section { margin-bottom: 24px; }
.nav-section-title { font-size: 10px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; padding: 0 12px; margin-bottom: 8px; }
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 8px;
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.15s ease;
    cursor: pointer;
}
.nav-item:hover { background: var(--bg-tertiary); color: var(--text-primary); }
.nav-item.active { background: var(--accent); color: white; }
.nav-icon { width: 18px; height: 18px; opacity: 0.7; }
.main { flex: 1; margin-left: 280px; min-height: 100vh; }
.topbar {
    height: 64px;
    background: rgba(24, 24, 27, 0.9);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    position: sticky;
    top: 0;
    z-index: 50;
    backdrop-filter: blur(8px);
}
.ticker-header { display: flex; align-items: center; gap: 16px; }
.ticker-symbol { font-size: 24px; font-weight: 700; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }
.ticker-name { font-size: 14px; color: var(--text-secondary); text-overflow: ellipsis; white-space: nowrap; overflow: hidden; max-width: 300px; }
.ticker-badge { padding: 4px 10px; background: var(--bg-tertiary); border-radius: 6px; font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; }
.price-display { text-align: right; }
.current-price { font-size: 28px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: var(--text-primary); }
.price-change { display: flex; align-items: center; justify-content: flex-end; gap: 8px; margin-top: 2px; }
.change-value { font-size: 14px; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.change-badge { padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.positive { color: var(--positive); }
.negative { color: var(--negative); }
.positive-bg { background: var(--positive-bg); }
.negative-bg { background: var(--negative-bg); }
.content { padding: 24px 32px; }
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.metric-card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: all 0.2s ease; }
.metric-card:hover { border-color: var(--border-hover); transform: translateY(-2px); }
.metric-label { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.metric-value { font-size: 24px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.metric-subtext { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.section { margin-bottom: 24px; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.section-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }
.chart-container { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 20px; overflow: hidden; }
.info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.info-card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
.info-card-title { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border); }
.info-row:last-child { border-bottom: none; }
.info-label { font-size: 13px; color: var(--text-secondary); }
.info-value { font-size: 13px; font-weight: 600; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }
.footer { padding: 32px; text-align: center; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 12px; }
.footer a { color: var(--accent); text-decoration: none; }

@media (max-width: 1200px) { .metrics-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 900px) {
    .sidebar { display: none; }
    .main { margin-left: 0; }
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .info-grid { grid-template-columns: 1fr; }
}
"""

COMPARISON_CSS = """
:root {
    --bg-primary: #09090b;
    --bg-secondary: #18181b;
    --bg-tertiary: #27272a;
    --text-primary: #fafafa;
    --text-secondary: #a1a1aa;
    --text-muted: #71717a;
    --border: #27272a;
    --accent: #3b82f6;
    --positive: #22c55e;
    --negative: #ef4444;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Inter', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.5;
    min-height: 100vh;
}
.container { max-width: 1400px; margin: 0 auto; padding: 32px; }
.header { margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.title { font-size: 32px; font-weight: 700; margin-bottom: 8px; }
.subtitle { color: var(--text-secondary); }
.tickers { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
.ticker-badge { padding: 8px 16px; background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 8px; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.section { margin-bottom: 32px; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; }
.card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 24px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px 16px; text-align: right; border-bottom: 1px solid var(--border); }
th { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; background: var(--bg-tertiary); }
td { font-family: 'JetBrains Mono', monospace; font-size: 13px; }
td:first-child, th:first-child { text-align: left; }
.positive { color: var(--positive); }
.negative { color: var(--negative); }
.footer { padding: 32px 0; text-align: center; color: var(--text-muted); font-size: 12px; border-top: 1px solid var(--border); margin-top: 32px; }
@media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
"""

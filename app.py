import json, os, glob, datetime, re, base64, random, calendar as pycal, urllib.request, urllib.error, urllib.parse
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title='BUSHIDO ANALYSIS — Dashboard Dealer', page_icon='🐺', layout='wide')
st.markdown("""<style>
[data-testid="stSidebar"] { background-color: #3B18FF !important; min-width: 245px !important; max-width: 265px !important; }
[data-testid="stSidebar"] > div:first-child { padding: 1.2rem 1.1rem 0 1.1rem !important; }
[data-testid="stSidebar"] *:not([data-testid="stIconMaterial"]):not(.material-icons) { color: #FFFFFF !important; }
[data-testid="stSidebar"] hr { margin: 12px 0px !important; border: none !important; border-top: 1px solid rgba(255,255,255,0.22) !important; }
[data-testid="stSidebar"] h3 { font-size: 16.5px !important; font-weight: 800 !important; margin: 2px 0 6px 0 !important; padding-bottom: 0px !important; letter-spacing: 0.3px; }
[data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px !important; }
[data-testid="stSidebar"] div[role="radiogroup"] label { padding: 3px 4px !important; margin: 0px !important; border: none !important; font-size: 13.5px !important; font-weight: 700 !important; min-height: 28px !important; align-items: center !important; }
[data-testid="stSidebar"] div[role="radiogroup"] label p { font-size: 13.5px !important; font-weight: 700 !important; margin: 0px !important; line-height: 1.2 !important; }
[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background-color: rgba(255,255,255,0.1) !important; border-radius: 5px !important; }
[data-testid="stSidebar"] div[data-testid="stDateInput"] label p { font-size: 12.5px !important; font-weight: 700 !important; margin-bottom: 4px !important; color: #FFFFFF !important; }
[data-testid="stSidebar"] div[data-baseweb="input"] { background-color: #FFFFFF !important; border: 1.5px solid #0E1117 !important; border-radius: 7px !important; min-height: 36px !important; }
[data-testid="stSidebar"] div[data-baseweb="input"] input { color: #0E1117 !important; -webkit-text-fill-color: #0E1117 !important; font-weight: 800 !important; font-size: 13.5px !important; background-color: #FFFFFF !important; padding: 6px 10px !important; }
[data-testid="stSidebar"] div[data-baseweb="calendar"] * { color: #0E1117 !important; }
[data-testid="stSidebar"] div[data-baseweb="textarea"], [data-testid="stSidebar"] div[data-baseweb="textarea"] textarea { background-color: #FFFFFF !important; color: #0E1117 !important; -webkit-text-fill-color: #0E1117 !important; font-weight: 700 !important; font-size: 12.5px !important; }
.azura-logo-box { display: flex; flex-direction: column; align-items: flex-start; justify-content: center; margin: -8px 0 10px 0; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.22); }
.azura-logo-img { max-width: 195px; max-height: 90px; width: auto; height: auto; object-fit: contain; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.35); background-color: transparent; }
.azura-fallback-badge { width: 72px; height: 72px; border-radius: 12px; background: radial-gradient(circle, #0051FF 0%, #050B14 85%); border: 2px solid #94A3B8; box-shadow: 0 0 10px rgba(0,0,0,0.45); display: flex; flex-direction: column; align-items: center; justify-content: center; }
.target-ideal-caption { font-size: 12.5px !important; font-weight: 700 !important; color: rgba(255,255,255,0.85) !important; margin-top: 6px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.22); }
.main-title { font-size: 44px !important; font-weight: 800 !important; color: #4318FF !important; margin-bottom: 2px; line-height: 1.1; }
.sub-title { font-size: 15px; font-weight: 600; color: #475569 !important; margin-bottom: 15px; }
.section-title { font-size: 22px !important; font-weight: 700 !important; color: #4318FF !important; margin: 20px 0 10px 0; }
.cap-title-banner { background: linear-gradient(90deg, #4318FF 0%, #1E293B 100%); color: #FFFFFF !important; font-family: 'Source Sans Pro', sans-serif; font-size: 15px; font-weight: 800; padding: 9px 14px; border-bottom: 2px solid #3B18FF; letter-spacing: 0.4px; text-align: left; }
.compact-table-wrap { width: 100%; overflow-x: auto; margin-bottom: 4px; border-radius: 8px; border: 1px solid #2D3748; background-color: #0E1117; }
table.compact-tbl { width: 100%; border-collapse: collapse; font-family: 'Source Sans Pro', sans-serif; font-size: 13px; background-color: #0E1117; }
table.compact-tbl th { background-color: #1A202C; color: #CBD5E1; font-weight: 700; padding: 7px 6px; border-bottom: 1px solid #2D3748; border-right: 1px solid #1E293B; text-align: right; white-space: nowrap; }
table.compact-tbl th:first-child, table.compact-tbl td:first-child { text-align: left; padding-left: 10px; }
table.compact-tbl td { padding: 6px 6px; border-bottom: 1px solid #1E293B; border-right: 1px solid #1E293B; text-align: right; white-space: nowrap; font-weight: 600; }
table.compact-tbl tr:hover td, table.ultra-compact-tbl tr:hover td { background-color: rgba(255,255,255,0.04); }
.ultra-compact-wrap { width: 100%; overflow-x: hidden; margin-bottom: 4px; border-radius: 8px; border: 1px solid #2D3748; background-color: #0E1117; }
table.ultra-compact-tbl { width: 100%; table-layout: fixed; border-collapse: collapse; font-family: 'Source Sans Pro', sans-serif; font-size: 13.5px; background-color: #0E1117; }
table.ultra-compact-tbl th { background-color: #1A202C; color: #CBD5E1; font-weight: 800; padding: 6px 3px; border-bottom: 1px solid #2D3748; border-right: 1px solid #1E293B; text-align: center; white-space: normal; line-height: 1.15; font-size: 11.5px; word-break: break-word; }
table.ultra-compact-tbl th:first-child, table.ultra-compact-tbl td:first-child { width: 17.5%; text-align: left; padding-left: 8px; font-size: 12px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
table.ultra-compact-tbl td { padding: 5px 5px; border-bottom: 1px solid #1E293B; border-right: 1px solid #1E293B; text-align: right; white-space: nowrap; font-weight: 700; font-size: 13.5px; overflow: hidden; }
table.narrative-tbl { width: 100%; border-collapse: collapse; font-family: 'Source Sans Pro', sans-serif; font-size: 13.5px; background-color: #0E1117; }
table.narrative-tbl th { background-color: #4318FF; color: #FFFFFF; font-weight: 700; padding: 10px 14px; border: 1px solid #2D3748; text-align: left; font-size: 13.5px; }
table.narrative-tbl td { padding: 10px 14px; border: 1px solid #2D3748; text-align: left; vertical-align: top; color: #E2E8F0; line-height: 1.55; font-weight: 400; white-space: normal; }
table.narrative-tbl td.item-col { width: 15%; color: #E2E8F0; text-align: left; background-color: #161B26; white-space: nowrap; font-weight: 600; }
table.narrative-tbl td.cond-col { width: 42.5%; background-color: #0E1117; }
table.narrative-tbl td.plan-col { width: 42.5%; background-color: #111622; }
p.nar-p { margin: 0 0 6px 0; padding: 0; color: #E2E8F0; font-weight: 400; line-height: 1.55; text-align: left; }
p.nar-p:last-of-type { margin-bottom: 4px; }
.focus-alert-box { margin-top: 14px; padding: 11px 16px; background: linear-gradient(90deg, rgba(255,0,127,0.14) 0%, rgba(14,17,23,0.95) 100%); border-left: 4px solid #FF007F; border-top: 1px solid #2D3748; border-right: 1px solid #2D3748; border-bottom: 1px solid #2D3748; border-radius: 6px; font-size: 13.5px; line-height: 1.65; color: #E2E8F0; }
.unmapped-sales-box { margin: 4px 0 12px 0; padding: 10px 14px; background: linear-gradient(90deg, rgba(255,234,0,0.12) 0%, rgba(14,17,23,0.96) 100%); border-left: 4px solid #FFEA00; border-top: 1px solid #2D3748; border-right: 1px solid #2D3748; border-bottom: 1px solid #2D3748; border-radius: 6px; font-size: 13px; line-height: 1.6; color: #E2E8F0; }
.unmapped-badge { display: inline-block; background-color: #1E293B; color: #FFEA00; border: 1px solid #475569; border-radius: 4px; padding: 2px 8px; margin: 2px 4px 2px 0; font-size: 12px; font-weight: 700; }
</style>""", unsafe_allow_html=True)
st.markdown("""<style>
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) { background-color: rgba(255,255,255,0.20) !important; border-radius: 6px !important; box-shadow: inset 3px 0 0 #FFEA00 !important; padding-left: 9px !important; }
div[data-testid="stTabs"] button[data-baseweb="tab"], .stTabs button[data-baseweb="tab"] { padding: 10px 16px !important; }
div[data-testid="stTabs"] button[data-baseweb="tab"] p, .stTabs button[data-baseweb="tab"] p { font-size: 15px !important; font-weight: 700 !important; }
div[data-testid="stTabs"] button[aria-selected="true"] p, .stTabs button[aria-selected="true"] p { color: #9F8CFF !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-highlight"] { background-color: #4318FF !important; height: 3px !important; }
@media (max-width: 768px) { .main-title { font-size: 28px !important; } .section-title { font-size: 18px !important; } .block-container { padding: 1rem 0.8rem 3rem 0.8rem !important; } }
</style>""", unsafe_allow_html=True)

# ====================================================================================================
# ===================== UI v2 — grafik interaktif, kartu progres, insight, leaderboard ==============
# (tanpa dependensi baru: grafik dibuat sebagai HTML/SVG ringan & dirender lewat components.html)
# ====================================================================================================
import html as _html

BSG_GRN, BSG_YEL, BSG_RED, BSG_CYN, BSG_PUR = '#00FF66', '#FFEA00', '#FF4D8D', '#00E5FF', '#4318FF'
_bsg_fragment = getattr(st, 'fragment', None) or getattr(st, 'experimental_fragment', None) or (lambda f: f)

def _esc(x): return _html.escape(str(x), quote=True)

def bsg_num(x, default=0.0):
    try:
        if x is None: return default
        if isinstance(x, str):
            s = x.replace('%', '').replace(',', '').strip()
            return float(s) if s not in ('', 'nan', 'NaN', 'None') else default
        v = float(x)
        return default if v != v else v
    except Exception: return default

def bsg_stat_color(v, good, warn): return BSG_GRN if v >= good else (BSG_YEL if v >= warn else BSG_RED)

def bsg_ach_bar(v, ideal):
    """Skala bar kartu: 0..1,5x ideal (marker ideal di 66,7%)."""
    try: return (max(0.0, min(float(v) / float(ideal), 1.5)) / 1.5 * 100.0, 66.67)
    except Exception: return (None, None)

def bsg_safe(fn, *a, label='Visual', **kw):
    try: return fn(*a, **kw)
    except Exception as e:
        try: st.caption(f'⚠️ {label} tidak dapat ditampilkan ({type(e).__name__}: {str(e)[:90]}).')
        except Exception: pass
        return None

def bsg_toast(msg, icon='✅'):
    try: st.toast(msg, icon=icon)
    except Exception: pass

def bsg_toast_once(key, msg, icon='✅'):
    flag = f'_toast_{key}'
    if not st.session_state.get(flag):
        st.session_state[flag] = True
        bsg_toast(msg, icon)

def bsg_segmented(label, options, key, default=None):
    default = default if default is not None else options[0]
    try:
        if hasattr(st, 'segmented_control'):
            v = st.segmented_control(label, options, default=default, key=key, label_visibility='collapsed')
            return v if v in options else default
    except Exception: pass
    return st.radio(label, options, index=options.index(default), horizontal=True, key=key, label_visibility='collapsed')

# ---------------------------------------------------------------- kartu dengan progress bar ----
def bsg_prog_bar(prog, color, ref=None):
    try: p = max(0.0, min(100.0, float(prog)))
    except Exception: return ''
    mk = ''
    if ref is not None:
        try: mk = f'<div title="Acuan ideal" style="position:absolute;left:{max(0.0, min(100.0, float(ref))):.1f}%;top:-3px;bottom:-3px;width:2px;background:#FFFFFF;opacity:.9;border-radius:1px;"></div>'
        except Exception: mk = ''
    return (f'<div style="position:relative;height:6px;border-radius:4px;background:#1E293B;margin-top:8px;">'
            f'<div style="width:{p:.1f}%;height:100%;border-radius:4px;background:{color};"></div>{mk}</div>')

def bsg_card(icon, label, value, sub, color, prog=None, ref=None):
    bar = bsg_prog_bar(prog, color, ref) if prog is not None else ''
    return (f'<div style="background:linear-gradient(160deg,#151B2B 0%,#0E1117 100%);border:1px solid #232B3E;border-top:3px solid {color};border-radius:12px;padding:12px 14px;min-height:98px;box-sizing:border-box;">'
            f'<div style="font-size:11.5px;font-weight:700;letter-spacing:0.6px;color:#94A3B8;text-transform:uppercase;white-space:nowrap;">{icon} {label}</div>'
            f'<div style="font-size:27px;font-weight:800;color:{color};line-height:1.2;margin:4px 0 2px 0;">{value}</div>'
            f'<div style="font-size:12px;font-weight:500;color:#CBD5E1;line-height:1.45;">{sub}</div>{bar}</div>')

# ---------------------------------------------------------------- kerangka iframe grafik ----
_BSG_FRAME = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:transparent;font-family:'Source Sans Pro','Segoe UI',Arial,sans-serif;color:#E2E8F0}
.card{background:linear-gradient(160deg,#151B2B 0%,#0E1117 100%);border:1px solid #232B3E;border-radius:12px;padding:12px 14px 10px 14px;width:100%}
.ttl{font-size:14px;font-weight:800;color:#E2E8F0;line-height:1.25}
.sub{font-size:11.5px;color:#94A3B8;margin:2px 0 8px 0;line-height:1.4}
.lg{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:#94A3B8;margin:0 12px 6px 0}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block}
.mk{display:inline-block;width:2px;height:11px;background:#fff;opacity:.9}
.ds{display:inline-block;width:16px;height:0;border-top:2px dashed #94A3B8}
.chip{display:inline-block;font-size:11.5px;font-weight:700;padding:2px 8px;border-radius:999px;background:#1B2336;border:1px solid #2D3748;margin:0 6px 6px 0;color:#CBD5E1}
#tip{position:fixed;left:0;top:0;pointer-events:none;background:#0B1020;border:1px solid #475569;border-radius:8px;padding:6px 9px;font-size:12px;line-height:1.5;opacity:0;transition:opacity .08s;z-index:99;max-width:280px;color:#E2E8F0}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
__CSS__
</style></head><body>__INNER__<div id="tip"></div>
<script>(function(){var t=document.getElementById('tip');if(!t)return;
document.querySelectorAll('[data-tip]').forEach(function(e){
e.addEventListener('mousemove',function(ev){t.innerHTML=e.getAttribute('data-tip');t.style.opacity=1;var x=ev.clientX+14,y=ev.clientY+14;
if(x+t.offsetWidth>window.innerWidth-6)x=Math.max(4,ev.clientX-t.offsetWidth-14);if(y+t.offsetHeight>window.innerHeight-4)y=Math.max(4,ev.clientY-t.offsetHeight-10);
t.style.left=x+'px';t.style.top=y+'px';});
e.addEventListener('mouseleave',function(){t.style.opacity=0;});});})();</script>
<script>(function(){function fit(){try{var c=document.querySelector('.card');if(!c)return;var h=Math.ceil(c.getBoundingClientRect().height)+4;var fe=window.frameElement;
if(fe&&Math.abs(fe.getBoundingClientRect().height-h)>2){fe.style.height=h+'px';fe.setAttribute('height',h);}}catch(e){}}
fit();window.addEventListener('resize',function(){setTimeout(fit,60);});setTimeout(fit,200);setTimeout(fit,800);})();</script>
__JS__</body></html>"""

def _bsg_frame(inner, css='', js=''):
    return _BSG_FRAME.replace('__CSS__', css).replace('__INNER__', inner).replace('__JS__', js)

def bsg_show(res):
    if not res: return
    html_str, h = res
    components.html(html_str, height=int(h), scrolling=False)

def _hdr(title, subtitle=''):
    return f'<div class="ttl">{_esc(title)}</div>' + (f'<div class="sub">{_esc(subtitle)}</div>' if subtitle else '<div style="height:8px"></div>')

# ---------------------------------------------------------------- 1. ranking bar horizontal ----
_RANK_CSS = """.rk{display:flex;align-items:center;gap:8px;height:26px}
.rk-n{flex:0 0 36%;max-width:215px;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#E2E8F0}
.rk-t{position:relative;flex:1;height:14px;border-radius:7px;background:#1B2336}
.rk-f{height:100%;border-radius:7px;transform-origin:left center;animation:grow .7s ease-out both}
.rk-m{position:absolute;top:-3px;bottom:-3px;width:2px;background:#fff;opacity:.9;border-radius:1px}
.rk-v{flex:0 0 58px;text-align:right;font-size:12px;font-weight:800}
.rk:hover .rk-t{background:#242E45}
.rk:hover .rk-n{color:#fff}"""

def bsg_chart_rank(title, subtitle, rows, ideal=None, ideal_label='Ideal', unit='%', max_rows=None, fixed_color=None, ascending=False):
    """rows: list dict(name, val, label=None, tip=None). Warna otomatis terhadap ideal (hijau ≥ ideal, kuning ≥ 85%, merah di bawahnya)."""
    rows = [r for r in rows if r is not None]
    if not rows: return None
    rows = sorted(rows, key=lambda r: r['val'], reverse=not ascending)
    if max_rows: rows = rows[:max_rows]
    mx = max([r['val'] for r in rows] + ([ideal * 1.15] if ideal else []) + [1.0])
    def _c(v):
        if fixed_color: return fixed_color
        if ideal is None: return BSG_CYN
        return BSG_GRN if v >= ideal else (BSG_YEL if v >= 0.85 * ideal else BSG_RED)
    body = ''
    for i, r in enumerate(rows):
        v = max(0.0, r['val']); c = _c(v)
        lab = r.get('label') or f'{v:.1f}{unit}'
        tip = r.get('tip') or f"<b>{_esc(r['name'])}</b><br>{lab}"
        mk = f'<div class="rk-m" style="left:{min(100.0, ideal / mx * 100.0):.2f}%"></div>' if ideal else ''
        body += (f'<div class="rk" data-tip="{_esc(tip)}"><div class="rk-n" title="{_esc(r["name"])}">{_esc(r["name"])}</div>'
                 f'<div class="rk-t"><div class="rk-f" style="width:{min(100.0, v / mx * 100.0):.2f}%;background:{c};animation-delay:{min(i, 12) * 40}ms"></div>{mk}</div>'
                 f'<div class="rk-v" style="color:{c}">{_esc(lab)}</div></div>')
    leg = ''
    if ideal and not fixed_color:
        leg = (f'<span class="lg"><span class="mk"></span>{_esc(ideal_label)} {ideal:.0f}{unit}</span><span class="lg"><span class="dot" style="background:{BSG_GRN}"></span>≥ ideal</span>'
               f'<span class="lg"><span class="dot" style="background:{BSG_YEL}"></span>85–99%</span><span class="lg"><span class="dot" style="background:{BSG_RED}"></span>&lt; 85%</span>')
    inner = f'<div class="card">{_hdr(title, subtitle)}{leg}{body}</div>'
    h = 59 + (22 if leg else 0) + (14 if subtitle else 0) + 26 * len(rows)
    return _bsg_frame(inner, css=_RANK_CSS), h

# ---------------------------------------------------------------- 2. funnel ----
def bsg_chart_funnel(title, subtitle, stages):
    """stages: list (label, value, color). Lebar bar relatif terhadap tahap pertama; tampil konversi antar tahap."""
    st_ = [(l, max(0.0, float(v)), c) for l, v, c in stages]
    if not st_ or st_[0][1] <= 0: return None
    base = st_[0][1]; body = ''
    for i, (l, v, c) in enumerate(st_):
        w = max(v / base * 100.0, 12.0) if v > 0 else 8.0
        if i > 0:
            prev = st_[i - 1][1]
            conv = (v / prev * 100.0) if prev > 0 else 0.0
            body += f'<div class="fn-c">↓ {conv:.1f}% dari {_esc(st_[i - 1][0])}</div>'
        tip = f'<b>{_esc(l)}</b><br>{int(v):,} ({v / base * 100.0:.1f}% dari {_esc(st_[0][0])})'
        body += (f'<div class="fn-r" data-tip="{_esc(tip)}"><div class="fn-l" title="{_esc(l)}">{_esc(l)}</div><div class="fn-t">'
                 f'<div class="fn-b" style="width:{w:.1f}%;background:linear-gradient(90deg,{c},{c}CC);animation-delay:{i * 90}ms">{int(v):,}</div></div></div>')
    css = (".fn-r{display:flex;align-items:center;gap:8px;height:28px}"
           ".fn-l{flex:0 0 38%;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#E2E8F0}"
           ".fn-t{flex:1;display:flex;justify-content:center}"
           ".fn-b{height:26px;border-radius:7px;display:flex;align-items:center;justify-content:center;color:#06101F;font-size:12.5px;font-weight:900;"
           "transform-origin:center;animation:grow .6s ease-out both;white-space:nowrap;min-width:46px}"
           ".fn-r:hover .fn-b{filter:brightness(1.18)}"
           ".fn-c{margin-left:calc(38% + 8px);text-align:center;font-size:10.5px;color:#94A3B8;height:16px;line-height:16px}")
    inner = f'<div class="card">{_hdr(title, subtitle)}{body}</div>'
    n = len(st_)
    return _bsg_frame(inner, css=css), 60 + (14 if subtitle else 0) + n * 28 + (n - 1) * 16

# ---------------------------------------------------------------- 3. heatmap ----
def _bsg_heat_color(s):
    """skor 0..100+ → merah → kuning → hijau."""
    stops = [(0.0, (255, 77, 141)), (50.0, (255, 176, 32)), (100.0, (0, 230, 118))]
    s = max(0.0, min(100.0, float(s)))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if s <= b:
            t = (s - a) / (b - a) if b > a else 0.0
            return '#%02X%02X%02X' % tuple(int(round(ca[k] + (cb[k] - ca[k]) * t)) for k in range(3))
    return '#00E676'

def bsg_chart_heat(title, subtitle, row_names, col_names, cells, max_rows=24):
    """cells[(row, col)] = (skor | None, label, tip)."""
    row_names = list(row_names)[:max_rows]
    if not row_names: return None
    css = (".ht{width:100%;border-collapse:separate;border-spacing:3px}.ht th{font-size:11.5px;font-weight:800;color:#CBD5E1;padding:4px 2px;text-align:center}"
           ".ht td.n{font-size:12px;font-weight:700;color:#E2E8F0;white-space:nowrap;max-width:190px;overflow:hidden;text-overflow:ellipsis;padding-right:6px}"
           ".ht td.c{height:26px;text-align:center;font-size:12.5px;font-weight:800;border-radius:6px;color:#06101F}.ht td.c:hover{filter:brightness(1.15);outline:1px solid #fff}"
           ".ht td.na{background:#1B2336;color:#64748B}")
    th = '<tr><th></th>' + ''.join(f'<th>{_esc(c)}</th>' for c in col_names) + '</tr>'
    rows_html = ''
    for rn in row_names:
        tds = f'<td class="n" title="{_esc(rn)}">{_esc(rn)}</td>'
        for cn in col_names:
            sc, lab, tip = cells.get((rn, cn), (None, '–', ''))
            if sc is None: tds += f'<td class="c na" data-tip="{_esc(tip or "Tidak ada data")}">–</td>'
            else: tds += f'<td class="c" style="background:{_bsg_heat_color(sc)}" data-tip="{_esc(tip)}">{_esc(lab)}</td>'
        rows_html += f'<tr>{tds}</tr>'
    leg = ('<div style="display:flex;align-items:center;gap:8px;margin-top:6px;font-size:10.5px;color:#94A3B8;">Skor vs ideal:'
           f'<span style="width:120px;height:8px;border-radius:4px;background:linear-gradient(90deg,{_bsg_heat_color(0)},{_bsg_heat_color(50)},{_bsg_heat_color(100)})"></span>0% → 100%+</div>')
    inner = f'<div class="card">{_hdr(title, subtitle)}<table class="ht">{th}{rows_html}</table>{leg}</div>'
    return _bsg_frame(inner, css=css), 67 + (14 if subtitle else 0) + 30 * (len(row_names) + 1)

# ---------------------------------------------------------------- 4. donut ----
def bsg_chart_donut(title, subtitle, items, center_label='Total'):
    """items: list (label, value, color)."""
    its = [(l, float(v), c) for l, v, c in items if v is not None and float(v) > 0]
    total = sum(v for _, v, _ in its)
    if total <= 0: return None
    R, SW = 44.0, 16.0; C = 2 * 3.141592653589793 * R; off = 0.0; segs = ''
    for l, v, c in its:
        ln = v / total * C; gap = 0.8 if len(its) > 1 else 0.0
        tip = f'<b>{_esc(l)}</b><br>{int(v):,} ({v / total * 100.0:.1f}%)'
        segs += (f'<circle class="sg" cx="60" cy="60" r="{R}" fill="none" stroke="{c}" stroke-width="{SW}" stroke-dasharray="{max(ln - gap, 0.1):.3f} {C - max(ln - gap, 0.1):.3f}" '
                 f'stroke-dashoffset="{-off:.3f}" data-tip="{_esc(tip)}"/>')
        off += ln
    leg = ''.join(f'<div class="dl"><span class="dot" style="background:{c}"></span><span class="dn">{_esc(l)}</span><b>{int(v):,}</b><i>{v / total * 100.0:.0f}%</i></div>' for l, v, c in its)
    css = (".dw{display:flex;align-items:center;gap:14px}.dc{flex:0 0 132px}.sg{transition:stroke-width .12s}.sg:hover{stroke-width:20}"
           ".dlg{flex:1;min-width:0}.dl{display:flex;align-items:center;gap:7px;font-size:12px;height:22px}.dn{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#CBD5E1}"
           ".dl b{font-weight:800}.dl i{font-style:normal;color:#94A3B8;width:34px;text-align:right}")
    svg = (f'<svg class="dc" viewBox="0 0 120 120" width="132" height="132"><circle cx="60" cy="60" r="{R}" fill="none" stroke="#1B2336" stroke-width="{SW}"/>'
           f'<g transform="rotate(-90 60 60)">{segs}</g><text x="60" y="61" text-anchor="middle" font-size="17" font-weight="800" fill="#E2E8F0">{int(total):,}</text>'
           f'<text x="60" y="76" text-anchor="middle" font-size="9" fill="#94A3B8">{_esc(center_label)}</text></svg>')
    inner = f'<div class="card">{_hdr(title, subtitle)}<div class="dw">{svg}<div class="dlg">{leg}</div></div></div>'
    return _bsg_frame(inner, css=css), 60 + (14 if subtitle else 0) + max(132, 22 * len(its))

# ---------------------------------------------------------------- 5. kurva target ideal vs realisasi (JS, responsif) ----
_CURVE_JS = """<script>(function(){
var CFG=__CFG__, wrap=document.getElementById('cv'), tip=document.getElementById('tip'), H=CFG.h;
function nice(x){var p=Math.pow(10,Math.floor(Math.log10(x||1)));var f=x/p;return (f<=1?1:f<=2?2:f<=5?5:10)*p;}
function fmt(v){return (Math.round(v*10)/10).toLocaleString('id-ID');}
function draw(){
 var W=wrap.clientWidth||600, m={l:46,r:16,t:12,b:26}, iw=W-m.l-m.r, ih=H-m.t-m.b, D=CFG.maxd;
 var vs=CFG.ideal.slice(); CFG.real.forEach(function(p){vs.push(p[1]);}); CFG.proj.forEach(function(p){vs.push(p[1]);}); vs.push(CFG.target);
 var mx=Math.max.apply(null,vs)*1.06; if(!(mx>0)) mx=1; var step=nice(mx/4), top=Math.ceil(mx/step)*step;
 function X(d){return m.l+(d-1)/Math.max(1,D-1)*iw;} function Y(v){return m.t+ih-v/top*ih;}
 var s='<svg width="'+W+'" height="'+H+'" style="display:block">';
 for(var v=0; v<=top+1e-9; v+=step){var y=Y(v); s+='<line x1="'+m.l+'" x2="'+(W-m.r)+'" y1="'+y+'" y2="'+y+'" stroke="#1E293B"/><text x="'+(m.l-7)+'" y="'+(y+4)+'" text-anchor="end" font-size="10.5" fill="#64748B">'+fmt(v)+'</text>';}
 var xs=D>20?3:(D>10?2:1);
 for(var d=1; d<=D; d++){ if(d===1||d%xs===0||d===D){ s+='<text x="'+X(d)+'" y="'+(H-8)+'" text-anchor="middle" font-size="10.5" fill="#64748B">'+d+'</text>'; } }
 if(CFG.target>0){ s+='<line x1="'+m.l+'" x2="'+(W-m.r)+'" y1="'+Y(CFG.target)+'" y2="'+Y(CFG.target)+'" stroke="#475569" stroke-dasharray="2 4"/><text x="'+(W-m.r)+'" y="'+(Y(CFG.target)-5)+'" text-anchor="end" font-size="10.5" fill="#94A3B8">Target '+fmt(CFG.target)+'</text>'; }
 var p=''; CFG.ideal.forEach(function(v,i){p+=(i?'L':'M')+X(i+1)+','+Y(v);});
 s+='<path d="'+p+'" fill="none" stroke="#94A3B8" stroke-width="2" stroke-dasharray="6 4"/>';
 if(CFG.proj.length>1){ p=''; CFG.proj.forEach(function(q,i){p+=(i?'L':'M')+X(q[0])+','+Y(q[1]);}); s+='<path d="'+p+'" fill="none" stroke="#00E5FF" stroke-width="2.2" stroke-dasharray="2 4" stroke-linecap="round"/>'; }
 if(CFG.real.length){
  p=''; CFG.real.forEach(function(q,i){p+=(i?'L':'M')+X(q[0])+','+Y(q[1]);});
  var last=CFG.real[CFG.real.length-1], first=CFG.real[0];
  s+='<path d="'+p+'L'+X(last[0])+','+Y(0)+'L'+X(first[0])+','+Y(0)+'Z" fill="rgba(0,255,102,0.10)"/>';
  s+='<path d="'+p+'" fill="none" stroke="#00FF66" stroke-width="2.8" stroke-linejoin="round"/>';
  s+='<circle cx="'+X(last[0])+'" cy="'+Y(last[1])+'" r="5" fill="#00FF66" stroke="#0E1117" stroke-width="2"/>';
 }
 s+='<line x1="'+X(CFG.today)+'" x2="'+X(CFG.today)+'" y1="'+m.t+'" y2="'+(m.t+ih)+'" stroke="#FFEA00" stroke-dasharray="3 3" stroke-opacity=".7"/><text x="'+X(CFG.today)+'" y="'+(m.t+9)+'" text-anchor="middle" font-size="10" fill="#FFEA00" font-weight="700" dx="'+(CFG.today>D-3?-16:16)+'">Tgl '+CFG.today+'</text>';
 s+='<line id="hl" y1="'+m.t+'" y2="'+(m.t+ih)+'" stroke="#E2E8F0" stroke-opacity=".35" style="display:none"/><circle id="h1" r="4.5" fill="#94A3B8" style="display:none"/><circle id="h2" r="5" fill="#00FF66" stroke="#0E1117" stroke-width="2" style="display:none"/>';
 s+='<rect id="ov" x="'+m.l+'" y="'+m.t+'" width="'+iw+'" height="'+ih+'" fill="transparent"/></svg>';
 wrap.innerHTML=s;
 var ov=document.getElementById('ov'), hl=document.getElementById('hl'), h1=document.getElementById('h1'), h2=document.getElementById('h2');
 var rmap={}; CFG.real.forEach(function(q){rmap[q[0]]=q[1];});
 ov.addEventListener('mousemove',function(ev){
  var r=ov.getBoundingClientRect(), d=Math.round((ev.clientX-r.left)/iw*(D-1))+1; d=Math.max(1,Math.min(D,d));
  var idv=CFG.ideal[d-1], rv=rmap[d], x=X(d);
  hl.setAttribute('x1',x); hl.setAttribute('x2',x); hl.style.display='';
  h1.setAttribute('cx',x); h1.setAttribute('cy',Y(idv)); h1.style.display='';
  var t='<b>Tgl '+d+'</b><br>Target ideal: <b>'+fmt(idv)+'</b>';
  if(rv!==undefined){ var g=rv-idv; h2.setAttribute('cx',x); h2.setAttribute('cy',Y(rv)); h2.style.display=''; t+='<br>Realisasi STU: <b style="color:#00FF66">'+fmt(rv)+'</b><br>Gap: <b style="color:'+(g>=0?'#00FF66':'#FF4D8D')+'">'+(g>=0?'+':'')+fmt(g)+'</b>'; } else { h2.style.display='none'; }
  tip.innerHTML=t; tip.style.opacity=1; var tx=ev.clientX+14, ty=ev.clientY+14; if(tx+tip.offsetWidth>window.innerWidth-6) tx=ev.clientX-tip.offsetWidth-14; tip.style.left=tx+'px'; tip.style.top=ty+'px';
 });
 ov.addEventListener('mouseleave',function(){hl.style.display='none';h1.style.display='none';h2.style.display='none';tip.style.opacity=0;});
}
draw(); var rt; window.addEventListener('resize',function(){clearTimeout(rt); rt=setTimeout(draw,80);});
})();</script>"""

def bsg_chart_curve(title, subtitle, df_stu, target, tgl_akhir, max_day, forc=None, h=280):
    """Kurva kumulatif STU: target ideal harian (dari tabel_target_harian) vs realisasi + proyeksi (forecast closing)."""
    target = bsg_num(target)
    if target <= 0: return None
    days = list(range(1, int(max_day) + 1))
    ideal = [round(target * tabel_target_harian.get(d, 0.0) / 100.0, 2) for d in days]
    cnt = {}
    if df_stu is not None and not df_stu.empty and 'hari' in df_stu.columns:
        for hh, cc in df_stu['hari'].dropna().astype(int).value_counts().items(): cnt[int(hh)] = int(cc)
    real, run = [], 0
    for d in range(1, int(tgl_akhir) + 1):
        run += cnt.get(d, 0); real.append([d, run])
    proj = [[int(tgl_akhir), run], [int(max_day), float(forc)]] if (forc is not None and bsg_num(forc) > 0 and int(tgl_akhir) < int(max_day)) else []
    gap = run - ideal[int(tgl_akhir) - 1]
    gcol = BSG_GRN if gap >= 0 else BSG_RED
    chips = (f'<span class="chip">Realisasi <b style="color:{BSG_GRN}">{run:,}</b></span><span class="chip">Ideal tgl {int(tgl_akhir)} <b>{ideal[int(tgl_akhir) - 1]:,.0f}</b></span>'
             f'<span class="chip">Gap <b style="color:{gcol}">{gap:+,.0f}</b></span><span class="chip">Target <b>{int(target):,}</b></span>'
             + (f'<span class="chip">Forecast closing <b style="color:{BSG_CYN}">{int(bsg_num(forc)):,}</b></span>' if proj else ''))
    leg = (f'<span class="lg"><span class="ds"></span>Target ideal</span><span class="lg"><span class="dot" style="background:{BSG_GRN}"></span>Realisasi STU</span>'
           + (f'<span class="lg"><span class="dot" style="background:{BSG_CYN}"></span>Proyeksi</span>' if proj else ''))
    cfg = json.dumps({'maxd': int(max_day), 'ideal': ideal, 'real': real, 'proj': proj, 'today': int(tgl_akhir), 'target': target, 'h': int(h)})
    inner = f'<div class="card">{_hdr(title, subtitle)}<div>{chips}</div><div>{leg}</div><div id="cv" style="width:100%;height:{int(h)}px"></div></div>'
    return _bsg_frame(inner, js=_CURVE_JS.replace('__CFG__', cfg)), 104 + (14 if subtitle else 0) + int(h) + 6

# ---------------------------------------------------------------- 6. podium / leaderboard & insight otomatis ----
def bsg_html_podium(rows, ideal):
    """rows: list dict(name, stu, target, pct) terurut dari terbaik."""
    if not rows: return ''
    medals = ['🥇', '🥈', '🥉']
    def _row(i, r, warn=False):
        col = bsg_stat_color(r['pct'], ideal, 0.85 * ideal) if ideal else BSG_CYN
        tag = '⚠️' if warn else (medals[i] if i < 3 else f'#{i + 1}')
        bar = bsg_prog_bar(min(r['pct'], 100.0), col, ideal if ideal else None)
        return (f'<div style="display:flex;align-items:center;gap:10px;background:linear-gradient(160deg,#151B2B 0%,#0E1117 100%);border:1px solid #232B3E;border-left:4px solid {col};border-radius:10px;padding:7px 12px;">'
                f'<div style="font-size:20px;width:26px;text-align:center;">{tag}</div>'
                f'<div style="flex:1;min-width:0;"><div style="font-size:12.5px;font-weight:800;color:#E2E8F0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="{_esc(r["name"])}">{_esc(r["name"])}</div>'
                f'<div style="font-size:11px;color:#94A3B8;">STU {int(r["stu"]):,} / Target {int(r["target"]):,}</div>{bar}</div>'
                f'<div style="font-size:20px;font-weight:900;color:{col};min-width:62px;text-align:right;">{r["pct"]:.1f}%</div></div>')
    top = rows[:3]; top_names = {r['name'] for r in top}
    bottom = [r for r in rows[::-1][:3] if r['name'] not in top_names]
    out = '<div style="font-size:13px;font-weight:800;color:#E2E8F0;margin:2px 0 6px 0;">🏅 Leaderboard Pencapaian</div>'
    out += '<div style="display:grid;gap:7px;">' + ''.join(_row(i, r) for i, r in enumerate(top)) + '</div>'
    if bottom:
        out += '<div style="font-size:13px;font-weight:800;color:#E2E8F0;margin:12px 0 6px 0;">🚨 Perlu Perhatian</div>'
        out += '<div style="display:grid;gap:7px;">' + ''.join(_row(i, r, True) for i, r in enumerate(bottom)) + '</div>'
    return out

def bsg_build_insights(ctx, rows):
    """rows: list dict(name, stu, target, ideal_u, pct) terurut dari terbaik. Mengembalikan list (warna, ikon, html)."""
    out = []
    r_p, tgl, ideal = ctx['r_tot_p'], ctx['tanggal_akhir'], float(ctx['ideal_pct'])
    stu, ideal_u, targ = bsg_num(r_p.get('STU')), bsg_num(r_p.get('IDEAL')), bsg_num(r_p.get('TARGET'))
    if targ > 0:
        gap = stu - ideal_u; col = BSG_GRN if gap >= 0 else (BSG_YEL if stu >= 0.85 * ideal_u else BSG_RED)
        out.append((col, '🎯', f"<b>Pace tgl {tgl}:</b> STU {int(stu):,} vs ideal {int(ideal_u):,} → <b style='color:{col}'>{gap:+,.0f} unit</b> ({stu / targ * 100:.1f}% dari target {int(targ):,})."))
        sisa, ha = int(ctx.get('sisa_hari', 0) or 0), max(1, int(ctx.get('hari_aktif', 1) or 1)); butuh = max(0.0, targ - stu)
        if butuh > 0 and sisa > 0: out.append((BSG_CYN, '⏱️', f"Untuk menutup target butuh <b>{butuh / sisa:.1f} STU/hari kerja</b> selama {sisa} hari kerja tersisa (rata-rata saat ini {stu / ha:.1f}/hari)."))
        elif butuh > 0: out.append((BSG_RED, '⏱️', f"Hari kerja habis, target masih kurang <b>{int(butuh):,} unit</b>."))
        else: out.append((BSG_GRN, '🏆', f"Target bulanan <b>sudah terlampaui</b> (+{int(stu - targ):,} unit)."))
    if rows:
        below = [r for r in rows if r['pct'] < ideal]
        out.append((BSG_YEL if below else BSG_GRN, '📉' if below else '✅', f"<b>{len(below)} dari {len(rows)}</b> {_esc(ctx.get('kol_label', 'entitas'))} berada di bawah pace ideal ({ideal:.0f}%)."))
        lag = rows[::-1][:3]
        out.append((BSG_RED, '🚨', '<b>Paling tertinggal:</b> ' + '; '.join(f"{_esc(r['name'])} ({r['pct']:.1f}%, {r['stu'] - r['ideal_u']:+,.0f} vs ideal)" for r in lag)))
        b = rows[0]
        out.append((BSG_GRN, '🌟', f"<b>Terbaik:</b> {_esc(b['name'])} — {b['pct']:.1f}% ({int(b['stu']):,}/{int(b['target']):,})."))
    for lbl, key, ideal_q, flt in ctx.get('quality_checks', []):
        try:
            cand = [(n, v) for n, v, ok in key if ok]
            if cand:
                n, v = min(cand, key=lambda t: t[1])
                out.append((bsg_stat_color(v, ideal_q, 0.7 * ideal_q), '🔎', f"<b>{lbl} terendah:</b> {_esc(n)} ({v:.1f}% vs ideal {ideal_q:.0f}%)."))
        except Exception: pass
    return out

def bsg_html_insights(items):
    if not items: return ''
    cells = ''.join(f'<div style="border-left:4px solid {c};background:linear-gradient(90deg,rgba(255,255,255,0.04) 0%,rgba(14,17,23,0.95) 100%);border-top:1px solid #2D3748;border-right:1px solid #2D3748;border-bottom:1px solid #2D3748;border-radius:6px;padding:8px 12px;font-size:13px;line-height:1.55;color:#E2E8F0;">{ic} {tx}</div>' for c, ic, tx in items)
    return '<div style="font-size:13px;font-weight:800;color:#E2E8F0;margin:2px 0 6px 0;">💡 Insight Otomatis</div><div style="display:grid;grid-template-columns:1fr;gap:7px;">' + cells + '</div>'

def bsg_celebrate(key, achieved, msg='🎉 Target tercapai!'):
    """Efek balon + toast sekali saja per kunci (scope + bulan + tanggal)."""
    flag = f'_celeb_{key}'
    if achieved and not st.session_state.get(flag):
        st.session_state[flag] = True
        try: st.balloons()
        except Exception: pass
        bsg_toast(msg, '🏆')

# ---------------------------------------------------------------- tabel interaktif (alternatif tabel capture) ----
_PROG_METRIC = {'_pct': 'Progress', '_pct_val': 'Progress', '_stu_pct': 'Progress STU%', '_acc_val': 'Progress ACC%'}

def bsg_render_interactive_table(df_items, df_full, columns, name_col, metric_col, key_suffix, title_text):
    try:
        cols = [c for c in columns if c in df_full.columns]
        if name_col not in cols or not hasattr(st, 'column_config'): return False
        d = df_full[cols].copy(); cfg = {}
        for c in cols:
            if c == name_col: continue
            s = d[c]
            if s.dtype == object:
                ss = s.astype(str).str.strip()
                if ss.str.endswith('%').all():
                    d[c] = pd.to_numeric(ss.str.rstrip('%'), errors='coerce'); cfg[c] = st.column_config.NumberColumn(c, format='%.2f%%')
                else:
                    num = pd.to_numeric(ss.str.replace(',', '', regex=False), errors='coerce')
                    if num.notna().all(): d[c] = num
        if metric_col in _PROG_METRIC and metric_col in df_full.columns:
            lbl = _PROG_METRIC[metric_col]; pv = pd.to_numeric(df_full[metric_col], errors='coerce').fillna(0.0)
            d.insert(1, lbl, pv.values)
            cfg[lbl] = st.column_config.ProgressColumn(lbl, format='%.1f%%', min_value=0.0, max_value=float(max(100.0, pv.max())))
        h = min(max(120, calc_table_height(d)), 900)
        st.dataframe(d, hide_index=True, use_container_width=True, column_config=cfg, height=h, key=f'itbl_{re.sub(r"[^a-zA-Z0-9]", "_", key_suffix)}')
        st.caption('⚡ Mode interaktif: klik header kolom untuk mengurutkan, ikon kaca pembesar untuk mencari. Pilih **🖼️ Capture** di sidebar bila ingin menyalin tabel sebagai gambar.')
        return True
    except Exception:
        return False

# ---------------------------------------------------------------- drill-down (fragment: tidak me-rerun seluruh halaman) ----
@_bsg_fragment
def bsg_drilldown(ctx, names):
    kol, ideal = ctx['kol_nm'], float(ctx['ideal_pct'])
    df_p, df_pr, df_s = ctx['df_p_disp'], ctx['df_pr_disp'], ctx['df_s_disp']
    sk = re.sub(r'[^A-Za-z0-9]', '_', str(ctx['scope_key']))
    P = {str(r[kol]): r for _, r in df_p.iterrows()}
    PR = {str(r[kol]): r for _, r in df_pr.iterrows()} if (df_pr is not None and not df_pr.empty) else {}
    SP = {str(r[kol]): r for _, r in df_s.iterrows()} if (df_s is not None and not df_s.empty) else {}
    names = [n for n in names if n in P]
    if not names: st.caption('Tidak ada baris untuk ditampilkan pada filter saat ini.'); return
    recs = []
    for n in names:
        r, pr, sp = P[n], PR.get(n), SP.get(n)
        recs.append({kol: n, 'TARGET': int(bsg_num(r.get('TARGET'))), 'STU': int(bsg_num(r.get('STU'))), 'IDEAL': int(bsg_num(r.get('IDEAL'))),
                     'GAP vs IDEAL': int(bsg_num(r.get('STU')) - bsg_num(r.get('IDEAL'))), 'Pencapaian': round(bsg_num(r.get('_pct')), 2),
                     'DB Q (%)': round(bsg_num(pr.get('DB Q')) if pr is not None else 0.0, 2), 'STU% (%)': round(bsg_num(pr.get('STU%')) if pr is not None else 0.0, 2),
                     'ACC% (%)': round(bsg_num(sp.get('_acc_val')) if sp is not None else 0.0, 2)})
    view = pd.DataFrame(recs)
    cfg = {}
    try:
        cfg = {'Pencapaian': st.column_config.ProgressColumn('Pencapaian', format='%.1f%%', min_value=0.0, max_value=float(max(100.0, view['Pencapaian'].max()))),
               'DB Q (%)': st.column_config.NumberColumn('DB Q', format='%.1f%%'), 'STU% (%)': st.column_config.NumberColumn('STU%', format='%.1f%%'),
               'ACC% (%)': st.column_config.NumberColumn('ACC%', format='%.1f%%')}
    except Exception: cfg = {}
    sel_name = None
    try:
        ev = st.dataframe(view, hide_index=True, use_container_width=True, column_config=cfg, on_select='rerun', selection_mode='single-row', key=f'bsg_dd_{sk}', height=min(max(120, calc_table_height(view)), 420))
        rows_sel = list(ev.selection.rows) if hasattr(ev, 'selection') else []
        if rows_sel and rows_sel[0] < len(view): sel_name = str(view.iloc[rows_sel[0]][kol])
        else: st.caption('👆 Klik satu baris untuk melihat kartu detail & kurva harian-nya.')
    except Exception:
        st.dataframe(view, hide_index=True, use_container_width=True, column_config=cfg)
        sel_name = st.selectbox('Pilih untuk detail:', ['—'] + names, key=f'bsg_dd_sel_{sk}')
        sel_name = None if sel_name == '—' else sel_name
    if not sel_name: return
    r, pr, sp = P[sel_name], PR.get(sel_name), SP.get(sel_name)
    stu, targ, idl, pct = bsg_num(r.get('STU')), bsg_num(r.get('TARGET')), bsg_num(r.get('IDEAL')), bsg_num(r.get('_pct'))
    dbq, stup = (bsg_num(pr.get('DB Q')) if pr is not None else 0.0), (bsg_num(pr.get('STU%')) if pr is not None else 0.0)
    acc = bsg_num(sp.get('_acc_val')) if sp is not None else 0.0
    st.markdown(f'<div class="section-title" style="font-size:18px !important;">🔎 Detail — {_esc(sel_name)}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 3])
    with c1:
        cards = [bsg_card('🎯', 'Target vs Result', f'{int(targ):,} / {int(stu):,}', f'<b>{pct:.1f}%</b> tercapai · Ideal {int(idl):,}', bsg_stat_color(stu, idl, 0.85 * idl) if idl > 0 else BSG_CYN, min(pct, 100.0), ideal),
                 bsg_card('✨', 'DB Quality', f'{dbq:.1f}%', 'Ideal 30%', bsg_stat_color(dbq, 30, 20), *bsg_ach_bar(dbq, 30)),
                 bsg_card('📈', 'STU Ratio', f'{stup:.1f}%', 'Ideal 10%', bsg_stat_color(stup, 10, 7), *bsg_ach_bar(stup, 10)),
                 bsg_card('✅', 'Approval', f'{acc:.1f}%', 'Ideal 50%', bsg_stat_color(acc, 50, 40), *bsg_ach_bar(acc, 50))]
        st.markdown('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;">' + ''.join(cards) + '</div>', unsafe_allow_html=True)
    with c2:
        f_c = ctx.get('f_c'); col = 'Nama Dealer' if ctx['is_total'] else 'Koor'
        sub = f_c[f_c[col] == sel_name] if (f_c is not None and not f_c.empty and col in f_c.columns) else None
        bsg_show(bsg_chart_curve(f'Kurva STU — {sel_name}', 'Kumulatif harian vs target ideal', sub, targ, ctx['tanggal_akhir'], ctx['max_day'], forc=bsg_num(r.get('FORC')) or None, h=230))

# ---------------------------------------------------------------- halaman "Ringkasan Visual" tab STU ----
def bsg_render_ringkasan(ctx):
    kol, ideal, tgl = ctx['kol_nm'], float(ctx['ideal_pct']), ctx['tanggal_akhir']
    df_p, df_pr, df_s = ctx['df_p_disp'], ctx['df_pr_disp'], ctx['df_s_disp']
    r_p, r_pr, r_s = ctx['r_tot_p'], ctx['r_tot_pr'], ctx['r_tot_s']
    sk = re.sub(r'[^A-Za-z0-9]', '_', str(ctx['scope_key']))
    if df_p is None or df_p.empty:
        st.info('ℹ️ Belum ada data penjualan untuk divisualisasikan pada periode ini.'); return
    P = {str(r[kol]): r for _, r in df_p.iterrows()}
    PR = {str(r[kol]): r for _, r in df_pr.iterrows()} if (df_pr is not None and not df_pr.empty) else {}
    SP = {str(r[kol]): r for _, r in df_s.iterrows()} if (df_s is not None and not df_s.empty) else {}
    names_all = list(P.keys())

    # ---- filter interaktif ----
    c_f1, c_f2 = st.columns([2, 3])
    with c_f1:
        st.caption('Tampilkan baris:')
        mode = bsg_segmented('Tampilkan', ['Semua', 'Di bawah ideal', 'Di atas ideal'], f'bsg_mode_{sk}')
    with c_f2:
        pick = st.multiselect('Filter baris (kosongkan = semua)', names_all, key=f'bsg_pick_{sk}')
    keep = []
    for n in names_all:
        if pick and n not in pick: continue
        pc = bsg_num(P[n].get('_pct'))
        if mode == 'Di bawah ideal' and not pc < ideal: continue
        if mode == 'Di atas ideal' and not pc >= ideal: continue
        keep.append(n)

    rows_all = []   # untuk leaderboard & insight (hanya yang punya target), terurut dari terbaik
    for n in names_all:
        r = P[n]; targ = bsg_num(r.get('TARGET'))
        if targ > 0: rows_all.append({'name': n, 'stu': bsg_num(r.get('STU')), 'target': targ, 'ideal_u': bsg_num(r.get('IDEAL')), 'pct': bsg_num(r.get('_pct'))})
    rows_all.sort(key=lambda x: x['pct'], reverse=True)

    # ---- celebrate bila target total tercapai ----
    try: bsg_celebrate(f"{sk}_{ctx['period_key']}", bsg_num(r_p.get('TARGET')) > 0 and bsg_num(r_p.get('STU')) >= bsg_num(r_p.get('TARGET')), '🎉 Target STU bulan ini tercapai!')
    except Exception: pass

    # ---- insight + leaderboard ----
    qchecks = []
    try:
        qchecks = [('DB Quality', [(n, bsg_num(PR[n].get('DB Q')), bsg_num(PR[n].get('DB')) >= 10) for n in names_all if n in PR], 30.0, None),
                   ('STU Ratio', [(n, bsg_num(PR[n].get('_stu_pct')), bsg_num(PR[n].get('DB')) >= 10) for n in names_all if n in PR], 10.0, None),
                   ('Approval SPK', [(n, bsg_num(SP[n].get('_acc_val')), bsg_num(SP[n].get('_spk_val')) >= 3) for n in names_all if n in SP], 50.0, None)]
    except Exception: qchecks = []
    cctx = dict(ctx); cctx['quality_checks'] = qchecks
    cctx['kol_label'] = 'dealer' if ctx['is_total'] else 'koordinator/counter'
    c_i1, c_i2 = st.columns([3, 2])
    with c_i1: st.markdown(bsg_html_insights(bsg_build_insights(cctx, rows_all)), unsafe_allow_html=True)
    with c_i2: st.markdown(bsg_html_podium(rows_all, ideal), unsafe_allow_html=True)

    # ---- kurva target vs realisasi ----
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    bsg_show(bsg_safe(bsg_chart_curve, f'Kurva Pencapaian STU — {ctx["dlr_label"]}', 'Arahkan kursor ke grafik untuk membaca nilai per tanggal. Garis putus-putus abu = target ideal harian.',
                      ctx.get('f_c'), bsg_num(r_p.get('TARGET')), tgl, ctx['max_day'], forc=bsg_num(r_p.get('FORC')) or None, label='Kurva pencapaian'))

    # ---- ranking + funnel ----
    c_r, c_f = st.columns([3, 2])
    with c_r:
        rank_rows = []
        for n in keep:
            r = P[n]; targ = bsg_num(r.get('TARGET'))
            if targ <= 0: continue
            pct, stu, idu = bsg_num(r.get('_pct')), bsg_num(r.get('STU')), bsg_num(r.get('IDEAL'))
            rank_rows.append({'name': n, 'val': pct, 'tip': f"<b>{_esc(n)}</b><br>STU <b>{int(stu):,}</b> / Target {int(targ):,}<br>Ideal tgl {tgl}: {int(idu):,} → <b>{stu - idu:+,.0f}</b><br>Pencapaian <b>{pct:.1f}%</b>"})
        res = bsg_safe(bsg_chart_rank, 'Ranking Pencapaian Target', f'% STU terhadap target bulanan · garis putih = ideal tgl {tgl} ({ideal:.0f}%)', rank_rows, ideal=ideal, label='Ranking')
        if res: bsg_show(res)
        else: st.caption('Belum ada baris bertarget pada filter ini.')
    with c_f:
        regs = 0; f_c = ctx.get('f_c')
        if f_c is not None and not f_c.empty and 'Status_Registrasi_Rating' in f_c.columns: regs = int((f_c['Status_Registrasi_Rating'] == 'SUDAH REGISTRASI').sum())
        stages = [('Database (DB)', bsg_num(r_pr.get('DB')), '#4318FF'), ('Hot Prospect', bsg_num(r_pr.get('HOT')), '#6D4DFF'), ('STU', bsg_num(r_p.get('STU')), '#00B8D9')]
        if regs > 0: stages.append(('Sudah Registrasi', float(regs), '#00E5FF'))
        bsg_show(bsg_safe(bsg_chart_funnel, 'Funnel Konversi Prospek', 'DB → Hot → STU (→ registrasi rating)', stages, label='Funnel'))
        s_c = ctx.get('s_c')
        if s_c is not None and not s_c.empty and 'Status_SPK_Clean' in s_c.columns:
            vc = s_c['Status_SPK_Clean'].value_counts()
            bsg_show(bsg_safe(bsg_chart_donut, 'Status SPK Leasing', 'Disetujui vs ditolak vs terbuka',
                              [('Disetujui', int(vc.get('DISETUJUI', 0)), '#00E676'), ('Ditolak', int(vc.get('DITOLAK', 0)), '#FF4D8D'), ('Terbuka', int(vc.get('TERBUKA', 0)), '#FFB020')], 'SPK', label='Donut SPK'))

    # ---- heatmap kualitas ----
    cols = ['Target', 'DB Quality', 'STU Ratio', 'Approval']
    cells, hr = {}, []
    for n in keep:
        r = P[n]; pr, sp = PR.get(n), SP.get(n); hr.append(n)
        targ = bsg_num(r.get('TARGET')); pc = bsg_num(r.get('_pct'))
        if targ > 0: cells[(n, 'Target')] = (pc / ideal * 100.0 if ideal > 0 else 0.0, f'{pc:.0f}%', f'<b>{_esc(n)}</b><br>Pencapaian {pc:.1f}% (ideal {ideal:.0f}%)')
        if pr is not None and bsg_num(pr.get('DB')) > 0:
            v = bsg_num(pr.get('DB Q')); cells[(n, 'DB Quality')] = (v / 30.0 * 100.0, f'{v:.0f}%', f'<b>{_esc(n)}</b><br>DB Quality {v:.1f}% (ideal 30%)')
            v = bsg_num(pr.get('_stu_pct')); cells[(n, 'STU Ratio')] = (v / 10.0 * 100.0, f'{v:.1f}%', f'<b>{_esc(n)}</b><br>STU Ratio {v:.1f}% (ideal 10%)')
        if sp is not None and bsg_num(sp.get('_spk_val')) > 0:
            v = bsg_num(sp.get('_acc_val')); cells[(n, 'Approval')] = (v / 50.0 * 100.0, f'{v:.0f}%', f'<b>{_esc(n)}</b><br>Approval {v:.1f}% (ideal 50%)')
    bsg_show(bsg_safe(bsg_chart_heat, 'Peta Panas Kualitas — capaian vs acuan ideal', 'Merah = jauh di bawah ideal · hijau = memenuhi/melampaui ideal (Target vs pace, DB Q 30%, STU% 10%, ACC% 50%)', hr, cols, cells, label='Heatmap'))

    # ---- drill-down ----
    st.markdown('<div class="section-title" style="font-size:18px !important;">🔎 Drill-down Interaktif</div>', unsafe_allow_html=True)
    bsg_safe(bsg_drilldown, ctx, keep, label='Drill-down')

# ---------------------------------------------------------------- grafik tambahan per tab ----
def bsg_render_leasing_charts(df_s, r_tot_s, kol_nm):
    """Tab STU › SPK & Leasing: ranking ACC% per baris + porsi SPK per leasing."""
    rows = []
    if df_s is not None and not df_s.empty:
        for _, r in df_s.iterrows():
            if bsg_num(r.get('_spk_val')) <= 0: continue
            acc = bsg_num(r.get('_acc_val'))
            rows.append({'name': str(r[kol_nm]), 'val': acc, 'tip': f"<b>{_esc(r[kol_nm])}</b><br>ACC% <b>{acc:.1f}%</b><br>SPK {int(bsg_num(r.get('_spk_val'))):,} (LM {int(bsg_num(r.get('_spk_lm_val'))):,}) · Terbuka {int(bsg_num(r.get('TERBUKA'))):,}"})
    c1, c2 = st.columns([3, 2])
    with c1:
        res = bsg_chart_rank('Approval Rate (ACC%) per baris', 'Garis putih = acuan ideal ACC% 50%', rows, ideal=50.0)
        if res: bsg_show(res)
        else: st.caption('Belum ada SPK pada periode ini.')
    with c2:
        items = [(k, bsg_num(r_tot_s.get(k)), c) for k, c in [('BAF', '#4318FF'), ('ADIRA', '#00E5FF'), ('SOF', '#FFB020'), ('IMFI', '#FF4D8D')]]
        bsg_show(bsg_chart_donut('Porsi SPK per Leasing', 'Total periode berjalan', items, 'SPK'))

def bsg_render_type_charts(df_td_i, ideal):
    """Tab STU › Per Type: komposisi STU per type + capaian terhadap target type."""
    if df_td_i is None or df_td_i.empty or 'TYPE' not in df_td_i.columns: return
    pal = {'AT PREMIUM': '#4318FF', 'AT CLASSY': '#00E5FF', 'AT LPM': '#FFB020', 'MOPED': '#FF4D8D', 'OTHERS': '#94A3B8'}
    items = [(str(r['TYPE']), bsg_num(r.get('STU')), pal.get(str(r['TYPE']), '#64748B')) for _, r in df_td_i.iterrows()]
    rows = []
    for _, r in df_td_i.iterrows():
        tg = bsg_num(r.get('TARGET'))
        if tg <= 0: continue
        ach = bsg_num(r.get('ACHIEV'))
        rows.append({'name': str(r['TYPE']), 'val': ach, 'tip': f"<b>{_esc(r['TYPE'])}</b><br>STU <b>{int(bsg_num(r.get('STU'))):,}</b> / Target {int(tg):,}<br>Capaian <b>{ach:.1f}%</b> · LM {int(bsg_num(r.get('LM'))):,}"})
    c1, c2 = st.columns([2, 3])
    with c1: bsg_show(bsg_chart_donut('Komposisi STU per Type', 'Porsi unit terjual periode berjalan', items, 'STU'))
    with c2:
        res = bsg_chart_rank('Capaian per Type vs Target Type', f'Garis putih = ideal tgl {int(bsg_num(ideal))} ({ideal:.0f}%)', rows, ideal=float(ideal))
        if res: bsg_show(res)

def bsg_render_salesman_charts(df_smi, ideal, n=10):
    """Tab STU › Salesman: top-N dan N salesman perlu dorongan (hanya yang bertarget)."""
    if df_smi is None or df_smi.empty or '_pct_val' not in df_smi.columns: return
    rows = []
    for _, r in df_smi.iterrows():
        tg = bsg_num(r.get('TARGET'))
        if tg <= 0: continue
        pc = bsg_num(r.get('_pct_val'))
        rows.append({'name': str(r['NAMA SALESMAN']), 'val': pc, 'tip': f"<b>{_esc(r['NAMA SALESMAN'])}</b><br>STU <b>{int(bsg_num(r.get('STU'))):,}</b> / Target {int(tg):,} ({pc:.1f}%)<br>DB {int(bsg_num(r.get('DB'))):,} · DB Q {_esc(r.get('DB Q', '-'))} · STU% {_esc(r.get('STU%', '-'))}"})
    if not rows: return
    c1, c2 = st.columns(2)
    with c1: bsg_show(bsg_chart_rank(f'Top {min(n, len(rows))} Salesman', f'% STU terhadap target · ideal {ideal:.0f}%', rows, ideal=float(ideal), max_rows=n))
    with c2: bsg_show(bsg_chart_rank(f'{min(n, len(rows))} Salesman Perlu Dorongan', 'Capaian terendah (hanya yang punya target)', rows, ideal=float(ideal), max_rows=n, ascending=True))

def bsg_render_reg_donut(sudah, belum):
    c1, c2 = st.columns([2, 3])
    with c1: bsg_show(bsg_chart_donut('Status Registrasi Rating (MYDR)', 'Konsumen faktur periode berjalan', [('Sudah Registrasi', sudah, '#00E676'), ('Belum Registrasi', belum, '#FF4D8D')], 'Konsumen'))

def bsg_render_spk_online_charts(df_sit, df_bwi, df_lsg_full):
    """Menu SPK ONLINE: ranking ACC%, growth SPK vs bulan lalu, dan porsi leasing."""
    d = pd.concat([x for x in (df_sit, df_bwi) if x is not None and not x.empty], ignore_index=True) if (df_sit is not None or df_bwi is not None) else pd.DataFrame()
    if d.empty: return
    acc_rows, grw_rows = [], []
    for _, r in d.iterrows():
        nm = str(r['NAMA DEALER']); spk, lm = bsg_num(r.get('_spk_val')), bsg_num(r.get('_spk_lm_val'))
        if spk > 0: acc_rows.append({'name': nm, 'val': bsg_num(r.get('_acc_val')), 'tip': f"<b>{_esc(nm)}</b><br>ACC% <b>{bsg_num(r.get('_acc_val')):.1f}%</b><br>SPK {int(spk):,} · Terbuka {int(bsg_num(r.get('TERBUKA'))):,}"})
        if lm > 0: grw_rows.append({'name': nm, 'val': spk / lm * 100.0, 'tip': f"<b>{_esc(nm)}</b><br>SPK {int(spk):,} vs LM {int(lm):,}<br>Growth <b>{spk / lm * 100.0:.1f}%</b>"})
    st.markdown('<div class="section-title">📊 Visual Ringkas Leasing</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        res = bsg_chart_rank('Approval Rate (ACC%) per Dealer', 'Putih = ideal 50%', acc_rows, ideal=50.0)
        if res: bsg_show(res)
    with c2:
        res = bsg_chart_rank('Growth SPK vs Bulan Lalu', 'Putih = sama dengan bulan lalu (100%)', grw_rows, ideal=100.0)
        if res: bsg_show(res)
    with c3:
        tot = df_lsg_full.iloc[-1] if (df_lsg_full is not None and not df_lsg_full.empty) else {}
        items = [(k, bsg_num(tot.get(k)), c) for k, c in [('BAF', '#4318FF'), ('ADIRA', '#00E5FF'), ('SOF', '#FFB020'), ('IMFI', '#FF4D8D')]]
        bsg_show(bsg_chart_donut('Porsi SPK per Leasing', 'Total seluruh dealer', items, 'SPK'))

def bsg_render_master_kpi_cards(tot_d, ideal):
    """Kartu ringkas Master KPI dengan progress bar; warna status mengacu pada pace ideal tanggal berjalan."""
    g = lambda k: bsg_num(tot_d.get(k))
    pc = lambda r, t: (r / t * 100.0) if t > 0 else 0.0
    idl = float(ideal) if ideal else 100.0
    p_stu, p_max, p_mp, p_acc = pc(g('R. STU'), g('T. STU')), pc(g('R. MAXI'), g('T. MAXI')), pc(g('R. MP'), g('T. MP')), pc(g('R. ACC%'), g('T. ACC%'))
    pace = lambda p: bsg_stat_color(p, idl, 0.85 * idl)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(bsg_card('🎯', 'KPI STU Dealer', f"{int(g('R. STU')):,} / {int(g('T. STU')):,}", f'<b>{p_stu:.1f}%</b> Tercapai · ideal {idl:.0f}%', pace(p_stu), min(p_stu, 100.0), idl), unsafe_allow_html=True)
    k2.markdown(bsg_card('🏍️', 'KPI MAXI & CLASSY', f"MAXI: {int(g('R. MAXI'))}/{int(g('T. MAXI'))}", f"<b>CLASSY: {int(g('R. CLASSY'))} / {int(g('T. CLASSY'))} Unit</b> · MAXI {p_max:.0f}%", pace(p_max), min(p_max, 100.0), idl), unsafe_allow_html=True)
    k3.markdown(bsg_card('👥', 'KPI MP & INCOMING', f"MP: {int(g('R. MP'))}/{int(g('T. MP'))}", f"<b>INC: {int(g('R. INC'))} / {int(g('T. INC'))} SPK</b> · MP {p_mp:.0f}%", pace(p_mp), min(p_mp, 100.0), idl), unsafe_allow_html=True)
    k4.markdown(bsg_card('✅', 'KPI ACC% & MYDR/GREV', f"ACC: {g('R. ACC%'):.1f}%", f"<b>Target ACC {g('T. ACC%'):.1f}% · MYDR: {int(g('R. MYDR'))}/{int(g('T. MYDR'))} | G.REV: {int(g('R. G REV'))}/{int(g('T. G REV'))}</b>", bsg_stat_color(p_acc, 100, 85), min(p_acc, 100.0), None), unsafe_allow_html=True)


DEFAULT_SHARED_API_KEY = ""   # JANGAN isi key di kode. Pakai st.secrets["GEMINI_API_KEY"] / env GEMINI_API_KEY / kolom API Key di menu Analisa.
IDEAL_DBQ_PCT, IDEAL_STU_PCT, IDEAL_ACC_PCT, MAX_NARRATIVE_WORDS = 30.0, 10.0, 50.0, 35
SUBTOTAL_ROW_LABELS = {'SUB SITUBONDO', 'SUB BANYUWANGI', 'JEMBER', 'BONDOWOSO', 'SITUBONDO', 'BANYUWANGI'}
tabel_target_harian = {1:0.0, 2:1.0, 3:2.0, 4:5.0, 5:8.0, 6:12.0, 7:18.0, 8:21.0, 9:24.0, 10:29.0, 11:34.0, 12:36.0, 13:40.0, 14:44.0, 15:48.0, 16:51.0, 17:54.0, 18:57.0, 19:60.0, 20:63.0, 21:67.0, 22:70.0, 23:73.0, 24:77.0, 25:79.0, 26:82.0, 27:84.0, 28:88.0, 29:92.0, 30:100.0, 31:100.0}
FIXED_COUNTER_TARGETS = {'IIN BARIROH': 25, 'SITI NURJANAH': 25, 'TRIA DAMAYANTI': 25, 'MUHAMMAD HAMDAN WAHDI': 15, 'DESVIN NURUL PRISTANTINI': 15, 'RIKA DWI ASTUTI': 15, 'NURUL FADILAH': 15}
FOKUS_KATEGORI_TYPE = ['AT PREMIUM', 'AT CLASSY', 'AT LPM']
daftar_dealer = ['SIP PANJI', 'SIP BESUKI', 'SIP A. YANI', 'SIP SRONO', 'SIP SIAGA', 'SIP SOBO', 'SIP GIRI']
TARGET_DEALER_FILE, TARGET_KOOR_FILE, KPI_SAVED_FILE, AI_CONFIG_FILE, UPLOAD_DIR = 'dealer_targets_saved.json', 'koor_targets_saved.json', 'kpi_targets_saved.json', 'ai_config.json', 'saved_raw_files'
DB_Multi_DIR, RATING_Multi_DIR, RAW_META_FILE = os.path.join(UPLOAD_DIR, 'database_files'), os.path.join(UPLOAD_DIR, 'rating_files'), os.path.join(UPLOAD_DIR, 'metadata.json')
os.makedirs(DB_Multi_DIR, exist_ok=True)
os.makedirs(RATING_Multi_DIR, exist_ok=True)

DEFAULT_KPI_DEALER = {
    'SIP PANJI':   {'T. STU': 85, 'T. MAXI': 35, 'T. CLASSY': 7,  'T. MP': 24, 'T. INC': 85, 'T. ACC%': 50.0, 'T. MYDR': 0, 'T. G REV': 0},
    'SIP BESUKI':  {'T. STU': 40, 'T. MAXI': 20, 'T. CLASSY': 8,  'T. MP': 7,  'T. INC': 48, 'T. ACC%': 54.0, 'T. MYDR': 0, 'T. G REV': 0},
    'SIP A. YANI': {'T. STU': 35, 'T. MAXI': 22, 'T. CLASSY': 4,  'T. MP': 6,  'T. INC': 13, 'T. ACC%': 55.0, 'T. MYDR': 0, 'T. G REV': 0},
    'SIP SRONO':   {'T. STU': 90, 'T. MAXI': 50, 'T. CLASSY': 12, 'T. MP': 26, 'T. INC': 70, 'T. ACC%': 50.0, 'T. MYDR': 0, 'T. G REV': 0},
    'SIP SIAGA':   {'T. STU': 60, 'T. MAXI': 36, 'T. CLASSY': 9,  'T. MP': 11, 'T. INC': 30, 'T. ACC%': 50.0, 'T. MYDR': 0, 'T. G REV': 0},
    'SIP SOBO':    {'T. STU': 50, 'T. MAXI': 34, 'T. CLASSY': 9,  'T. MP': 10, 'T. INC': 30, 'T. ACC%': 50.0, 'T. MYDR': 0, 'T. G REV': 0},
    'SIP GIRI':    {'T. STU': 35, 'T. MAXI': 7,  'T. CLASSY': 3,  'T. MP': 5,  'T. INC': 15, 'T. ACC%': 50.0, 'T. MYDR': 0, 'T. G REV': 0},
}

def clean_str(val): return '' if pd.isna(val) else ' '.join(str(val).split()).upper()
def nospace_str(val): return '' if pd.isna(val) else ''.join(str(val).split()).upper()
def alnum_str(val): return '' if pd.isna(val) else ''.join(c for c in str(val).upper() if c.isalnum())
FIXED_COUNTER_TARGETS_NS = {alnum_str(k): v for k, v in FIXED_COUNTER_TARGETS.items()}

def normalize_dealer_name(val):
    s = clean_str(val)
    if not s or s in ['NAN', 'NONE'] or s in daftar_dealer: return s
    if any(k in s for k in ['A YANI', 'A. YANI', 'AYANI', 'A.YANI']): return 'SIP A. YANI'
    for k, v in [('BESUKI', 'SIP BESUKI'), ('PANJI', 'SIP PANJI'), ('SRONO', 'SIP SRONO'), ('SIAGA', 'SIP SIAGA'), ('SOBO', 'SIP SOBO'), ('GIRI', 'SIP GIRI')]:
        if k in s: return v
    return s

def safe_int(val, default=0):
    try: return default if pd.isna(val) else int(float(str(val).replace(',', '').replace('%', '').strip()))
    except Exception: return default

def safe_float(val, default=0.0):
    try: return default if pd.isna(val) else float(str(val).replace(',', '').replace('%', '').strip())
    except Exception: return default

def strip_formatting_tags(text):
    return ' '.join(re.sub(r'<[^>]+>', '', str(text).replace('<br>', ' ').replace('<br/>', ' ').replace('</p>', ' ')).split()) if text else ''

def limit_words(text, max_words=MAX_NARRATIVE_WORDS):
    clean_txt = strip_formatting_tags(text)
    if not clean_txt: return ''
    words = clean_txt.split()
    if len(words) <= max_words: return clean_txt
    truncated = ' '.join(words[:max_words]).rstrip(',;:-')
    return truncated if truncated.endswith('.') else truncated + '.'

def format_paragraphs_html(text):
    clean_txt = limit_words(text, MAX_NARRATIVE_WORDS)
    return f'<p class="nar-p">{clean_txt}</p>' if clean_txt else ''

def calc_rational_7d_addition(curr_stu, monthly_targ, curr_day, next_day, pct_curr_dec, pct_next_dec, active_mp=1):
    sisa_hr, hr_jalan, delta_pct = max(1, next_day - curr_day), max(1, curr_day), max(0.12, pct_next_dec - pct_curr_dec)
    normal_period_quota = monthly_targ * delta_pct if monthly_targ > 0 else max(2.0, active_mp * 1.5)
    stretch_from_rate = ((curr_stu / hr_jalan) * sisa_hr * 1.8) + max(1.0, active_mp * 0.6)
    ideal_now = monthly_targ * pct_curr_dec
    if ideal_now > 0 and curr_stu < (ideal_now * 0.5):
        add_stu = min(round((normal_period_quota * 0.65) + (stretch_from_rate * 0.35)), max(curr_stu + 4, round(normal_period_quota * 1.15), round(active_mp * 1.5)))
    else: add_stu = round(normal_period_quota + (max(0.0, ideal_now - curr_stu) * 0.30))
    add_stu = max(max(2, round(active_mp * 0.8)) if monthly_targ >= 10 else 1, add_stu)
    return int(add_stu), int(curr_stu + add_stu)

def calc_table_height(df, row_h=35, head_h=38): return 150 if (df is None or df.empty) else (len(df) * row_h) + head_h + 3
def get_compact_col_config(columns, name_col, editable_col=None):
    return {c: (st.column_config.TextColumn(c, width="medium") if c == name_col else (st.column_config.NumberColumn(c, width="small", format="%d") if c == editable_col else st.column_config.Column(c, width="small"))) for c in columns}

def get_neon_gradient_hex(ratio):
    r = max(0.0, min(1.0, float(ratio)))
    return '#{:02X}{:02X}{:02X}'.format(255, int((r/0.5)*234), int(127*(1.0-r/0.5))) if r <= 0.5 else '#{:02X}{:02X}{:02X}'.format(int(255*(1.0-(r-0.5)/0.5)), int(234+((r-0.5)/0.5)*21), int(((r-0.5)/0.5)*102))

def build_compact_html_string(df_items, df_full, columns, name_col, metric_col, table_dom_id, header_labels=None, ultra_compact=False, title_text=None, highlight_names=None, wrap_first=False):
    if df_full is None or df_full.empty: return ''
    hdrs = header_labels if (header_labels is not None and len(header_labels) == len(columns)) else columns
    min_v = float(df_items[metric_col].min()) if (df_items is not None and not df_items.empty and metric_col in df_items.columns) else 0.0
    max_v = float(df_items[metric_col].max()) if (df_items is not None and not df_items.empty and metric_col in df_items.columns) else 0.0
    n_items = len(df_items) if df_items is not None else 0
    wrap_cls, tbl_cls = ('ultra-compact-wrap', 'ultra-compact-tbl') if ultra_compact else ('compact-table-wrap', 'compact-tbl')
    banner_html = f'<div class="cap-title-banner">🐺 {title_text}</div>' if title_text else ''
    html = [f'<div id="{table_dom_id}" class="{wrap_cls}">{banner_html}<table class="{tbl_cls}"><thead><tr>'] + [(f'<th style="white-space:normal;font-size:11px;padding:5px 4px;text-align:left;line-height:1.2;">{h}</th>' if wrap_first == 'all' else f'<th>{h}</th>') for h in hdrs] + ['</tr></thead><tbody>']
    for _, row in df_full.iterrows():
        nm = str(row[name_col])
        style = 'background-color: #4318FF; color: #FFFFFF; font-weight: 800;' if (nm.startswith('TOTAL') or nm.startswith('CREDIT SHARE')) else ('background-color: #1E293B; color: #FFFFFF; font-weight: 800;' if (nm in SUBTOTAL_ROW_LABELS or nm.startswith('SUB ') or (highlight_names is not None and nm in highlight_names)) else '')
        if not style and '_row_ratio' in df_full.columns and pd.notna(row['_row_ratio']):
            style = f'color: {get_neon_gradient_hex(float(row["_row_ratio"]))};'
        if not style and df_items is not None and not df_items.empty and metric_col in df_items.columns:
            m_idx = df_items.index[df_items[name_col] == nm].tolist()
            if m_idx:
                v = float(df_items.loc[m_idx[0], metric_col])
                style = f'color: {get_neon_gradient_hex(((v - min_v) / (max_v - min_v)) if max_v > min_v else (m_idx[0] / max(1, n_items - 1)))};'
        if wrap_first == 'all' and nm.startswith('TOTAL') and '_summary' in df_full.columns and pd.notna(row['_summary']):   # baris total: 1 sel gabungan selebar tabel agar terbaca
            html.append(f'<tr style="{style}"><td colspan="{len(columns)}" style="white-space:normal;text-align:center;font-size:12.5px;padding:9px 8px;line-height:1.4;letter-spacing:0.3px;">{row["_summary"]}</td></tr>')
            continue
        html.append(f'<tr style="{style}">' + ''.join((f'<td style="white-space:normal;word-break:break-word;font-size:11.5px;padding:4px 5px;text-align:left;line-height:1.25;{"width:30px;" if ci_c == 0 else ""}">{row[c]}</td>' if wrap_first == 'all' else (f'<td style="white-space:normal;word-break:break-word;min-width:150px;max-width:260px;line-height:1.25;">{row[c]}</td>' if (wrap_first and ci_c == 0) else f'<td>{row[c]}</td>')) for ci_c, c in enumerate(columns)) + '</tr>')
    return ''.join(html + ['</tbody></table></div>'])

def render_table_image_buttons(table_dom_id, file_label, standalone_html=None):
    safe_fname, hidden_payload = re.sub(r'[^a-zA-Z0-9_-]', '_', file_label), json.dumps(standalone_html or '')
    components.html(f"""<html><head><script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script><style>
        body {{ margin: 0; padding: 2px 0; background: transparent; font-family: 'Source Sans Pro', sans-serif; display: flex; align-items: center; gap: 8px; }}
        .act-btn {{ background-color: #1E293B; color: #E2E8F0; border: 1px solid #334155; border-radius: 6px; padding: 5px 11px; font-size: 12px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; transition: all 0.15s; }}
        .act-btn:hover {{ background-color: #4318FF; color: #FFFFFF; border-color: #4318FF; }}
        #status_msg {{ font-size: 12px; color: #00FF66; font-weight: 600; margin-left: 6px; }}
        #offscreen_holder {{ position: fixed; left: -9999px; top: 0; background: #0E1117; padding: 10px; z-index: -1; }}
        .compact-table-wrap, .ultra-compact-wrap {{ border-radius: 8px; border: 1px solid #2D3748; background-color: #0E1117; overflow: hidden; }}
        .cap-title-banner {{ background: linear-gradient(90deg, #4318FF 0%, #1E293B 100%); color: #FFFFFF !important; font-family: 'Source Sans Pro', sans-serif; font-size: 15px; font-weight: 800; padding: 9px 14px; border-bottom: 2px solid #3B18FF; letter-spacing: 0.4px; text-align: left; }}
        table.compact-tbl, table.ultra-compact-tbl {{ border-collapse: collapse; font-family: 'Source Sans Pro', sans-serif; font-size: 13.5px; background-color: #0E1117; width: 100%; }}
        table.compact-tbl th, table.ultra-compact-tbl th {{ background-color: #1A202C; color: #CBD5E1; font-weight: 800; padding: 6px 6px; border: 1px solid #2D3748; text-align: right; white-space: nowrap; }}
        table.compact-tbl th:first-child, table.compact-tbl td:first-child, table.ultra-compact-tbl th:first-child, table.ultra-compact-tbl td:first-child {{ text-align: left; padding-left: 8px; }}
        table.compact-tbl td, table.ultra-compact-tbl td {{ padding: 5px 6px; border: 1px solid #1E293B; text-align: right; white-space: nowrap; font-weight: 700; }}
    </style></head><body>
    <button class="act-btn" onclick="captureTbl('copy')">📸 Copy Tabel (Gambar)</button>
    <button class="act-btn" onclick="captureTbl('jpg')">📥 Download JPG</button>
    <span id="status_msg"></span><div id="offscreen_holder"></div>
    <script>
    const fallbackHtml = {hidden_payload};
    async function captureTbl(mode) {{
        const msg = document.getElementById('status_msg'); msg.style.color = '#FFEA00'; msg.innerText = 'Memproses gambar...';
        try {{
            const holder = document.getElementById('offscreen_holder');
            let targetEl = fallbackHtml ? (holder.innerHTML = fallbackHtml, holder.firstElementChild) : window.parent.document.getElementById('{table_dom_id}');
            if (!targetEl) {{ msg.style.color = '#FF007F'; msg.innerText = 'Tabel tidak ditemukan.'; return; }}
            const canvas = await html2canvas(targetEl, {{ backgroundColor: '#0E1117', scale: 2, useCORS: true, logging: false }});
            if (mode === 'copy') {{
                canvas.toBlob(async (blob) => {{
                    try {{
                        await navigator.clipboard.write([new ClipboardItem({{ 'image/png': blob }})]);
                        msg.style.color = '#00FF66'; msg.innerText = '✅ Gambar berhasil disalin ke Clipboard! (Siap Ctrl+V di WA/Excel)';
                    }} catch (err) {{
                        const a = document.createElement('a'); a.href = canvas.toDataURL('image/jpeg', 0.95); a.download = '{safe_fname}.jpg'; a.click();
                        msg.style.color = '#00E5FF'; msg.innerText = '📥 Browser membatasi clipboard, gambar otomatis diunduh sebagai JPG.';
                    }}
                    setTimeout(() => msg.innerText = '', 4500);
                }}, 'image/png');
            }} else {{
                const a = document.createElement('a'); a.href = canvas.toDataURL('image/jpeg', 0.95); a.download = '{safe_fname}.jpg'; a.click();
                msg.style.color = '#00FF66'; msg.innerText = '✅ File {safe_fname}.jpg berhasil diunduh!';
                setTimeout(() => msg.innerText = '', 4000);
            }}
            holder.innerHTML = '';
        }} catch (e) {{ msg.style.color = '#FF007F'; msg.innerText = 'Gagal membuat gambar: ' + e.message; }}
    }}
    </script></body></html>""", height=36)

def render_compact_html_table(df_items, df_full, columns, name_col, metric_col, key_suffix='tbl', header_labels=None, ultra_compact=False, title_text=None, custom_capture_html=None, highlight_names=None, wrap_first=False):
    if df_full is None or df_full.empty: return
    if st.session_state.get('tbl_mode') == 'interaktif' and bsg_render_interactive_table(df_items, df_full, columns, name_col, metric_col, key_suffix, title_text): return
    dom_id = f"Capture_{re.sub(r'[^a-zA-Z0-9]', '_', key_suffix)}"
    html_display_str = build_compact_html_string(df_items, df_full, columns, name_col, metric_col, dom_id, header_labels=header_labels, ultra_compact=ultra_compact, title_text=None, highlight_names=highlight_names, wrap_first=wrap_first)
    cap_title = title_text if title_text else key_suffix.replace('_', ' ')
    html_capture_str = custom_capture_html if custom_capture_html is not None else build_compact_html_string(df_items, df_full, columns, name_col, metric_col, f"{dom_id}_cap", header_labels=header_labels, ultra_compact=ultra_compact, title_text=cap_title, highlight_names=highlight_names, wrap_first=wrap_first)
    if ultra_compact:
        safe_fname, comp_height, hidden_uc_payload = re.sub(r'[^a-zA-Z0-9_-]', '_', key_suffix), (len(df_full) * 29) + 100, json.dumps(html_capture_str)
        components.html(f"""<html><head><script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script><style>
            body {{ margin: 0; padding: 0; background: transparent; font-family: 'Source Sans Pro', sans-serif; color: #E2E8F0; }}
            .ultra-compact-wrap {{ width: 100%; overflow-x: hidden; margin-bottom: 6px; border-radius: 8px; border: 1px solid #2D3748; background-color: #0E1117; }}
            .cap-title-banner {{ background: linear-gradient(90deg, #4318FF 0%, #1E293B 100%); color: #FFFFFF !important; font-family: 'Source Sans Pro', sans-serif; font-size: 15px; font-weight: 800; padding: 9px 14px; border-bottom: 2px solid #3B18FF; letter-spacing: 0.4px; text-align: left; }}
            table.ultra-compact-tbl {{ width: 100%; table-layout: fixed; border-collapse: collapse; font-family: 'Source Sans Pro', sans-serif; font-size: 13.5px; background-color: #0E1117; }}
            table.ultra-compact-tbl th {{ background-color: #1A202C; color: #CBD5E1; font-weight: 800; padding: 6px 3px; border-bottom: 1px solid #2D3748; border-right: 1px solid #1E293B; text-align: center; white-space: normal; line-height: 1.15; font-size: 11.5px; word-break: break-word; }}
            table.ultra-compact-tbl th:first-child, table.ultra-compact-tbl td:first-child {{ width: 17.5%; text-align: left; padding-left: 8px; font-size: 12px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            table.ultra-compact-tbl td {{ padding: 5px 5px; border-bottom: 1px solid #1E293B; border-right: 1px solid #1E293B; text-align: right; white-space: nowrap; font-weight: 700; font-size: 13.5px; overflow: hidden; }}
            table.ultra-compact-tbl tr:hover td {{ background-color: rgba(255,255,255,0.04); }}
            .toolbar {{ display: flex; align-items: center; gap: 8px; padding-top: 2px; }}
            .act-btn {{ background-color: #1E293B; color: #E2E8F0; border: 1px solid #334155; border-radius: 6px; padding: 5px 11px; font-size: 12px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; transition: all 0.15s; }}
            .act-btn:hover {{ background-color: #4318FF; color: #FFFFFF; border-color: #4318FF; }}
            #status_msg {{ font-size: 12px; color: #00FF66; font-weight: 600; margin-left: 6px; }}
            #offscreen_uc {{ position: fixed; left: -9999px; top: 0; width: 1350px; background: #0E1117; padding: 10px; z-index: -1; }}
        </style></head><body>{html_display_str}
        <div class="toolbar"><button class="act-btn" onclick="captureUC('copy')">📸 Copy Tabel (Gambar)</button><button class="act-btn" onclick="captureUC('jpg')">📥 Download JPG</button><span id="status_msg"></span></div>
        <div id="offscreen_uc"></div>
        <script>
        const ucCaptureHtml = {hidden_uc_payload};
        async function captureUC(mode) {{
            const msg = document.getElementById('status_msg'); msg.style.color = '#FFEA00'; msg.innerText = 'Memproses gambar...';
            try {{
                const holder = document.getElementById('offscreen_uc'); holder.innerHTML = ucCaptureHtml;
                const canvas = await html2canvas(holder.firstElementChild, {{ backgroundColor: '#0E1117', scale: 2, useCORS: true, logging: false }});
                holder.innerHTML = '';
                if (mode === 'copy') {{
                    canvas.toBlob(async (blob) => {{
                        try {{
                            await navigator.clipboard.write([new ClipboardItem({{ 'image/png': blob }})]);
                            msg.style.color = '#00FF66'; msg.innerText = '✅ Gambar tabel + Judul disalin ke Clipboard! (Siap Ctrl+V di WA/Excel)';
                        }} catch (err) {{
                            const a = document.createElement('a'); a.href = canvas.toDataURL('image/jpeg', 0.95); a.download = '{safe_fname}.jpg'; a.click();
                            msg.style.color = '#00E5FF'; msg.innerText = '📥 Gambar otomatis diunduh sebagai JPG.';
                        }}
                        setTimeout(() => msg.innerText = '', 4500);
                    }}, 'image/png');
                }} else {{
                    const a = document.createElement('a'); a.href = canvas.toDataURL('image/jpeg', 0.95); a.download = '{safe_fname}.jpg'; a.click();
                    msg.style.color = '#00FF66'; msg.innerText = '✅ File {safe_fname}.jpg berhasil diunduh!';
                    setTimeout(() => msg.innerText = '', 4000);
                }}
            }} catch (e) {{ msg.style.color = '#FF007F'; msg.innerText = 'Gagal membuat gambar: ' + e.message; }}
        }}
        </script></body></html>""", height=comp_height, scrolling=False)
    else:
        st.markdown(html_display_str, unsafe_allow_html=True)
        render_table_image_buttons(dom_id, key_suffix, standalone_html=html_capture_str)

def load_json(f):
    if os.path.exists(f):
        try:
            with open(f, 'r') as fp: return json.load(fp)
        except Exception: return {}
    return {}

def save_json(data, f):
    try:
        with open(f, 'w') as fp: json.dump(data, fp)
    except Exception: pass

def resolve_gemini_api_key():
    if st.session_state.get('shared_gemini_api_key'): return st.session_state['shared_gemini_api_key'].strip()
    cfg_k = load_json(AI_CONFIG_FILE).get('gemini_api_key', '').strip()
    if cfg_k: return cfg_k
    try:
        for k_sec in ['GEMINI_API_KEY', 'gemini_api_key', 'GOOGLE_API_KEY']:
            if k_sec in st.secrets and str(st.secrets[k_sec]).strip(): return str(st.secrets[k_sec]).strip()
    except Exception: pass
    return os.environ.get('GEMINI_API_KEY', DEFAULT_SHARED_API_KEY).strip()

def save_raw_file(up_file, prefix):
    ext = os.path.splitext(up_file.name)[1].lower()
    for old in glob.glob(os.path.join(UPLOAD_DIR, f"{prefix}_*")):
        try: os.remove(old)
        except Exception: pass
    fpath = os.path.join(UPLOAD_DIR, f"{prefix}_latest{ext}")
    with open(fpath, 'wb') as f: f.write(up_file.getbuffer())
    meta = load_json(RAW_META_FILE)
    meta[prefix] = {'original_name': up_file.name, 'saved_path': fpath, 'updated_at': datetime.datetime.now().strftime('%d %b %Y, %H:%M WIB')}
    save_json(meta, RAW_META_FILE)

def save_database_files(up_files):
    meta = load_json(RAW_META_FILE)
    now_str = datetime.datetime.now().strftime('%d %b %Y, %H:%M WIB')
    file_times = meta.get('database_multi', {}).get('file_times', {})
    updated_dealers = []
    for uf in up_files:
        new_dlr = normalize_dealer_name(os.path.splitext(uf.name)[0])
        for old_p in glob.glob(os.path.join(DB_Multi_DIR, "*.*")):
            old_bname = os.path.basename(old_p)
            old_dlr = normalize_dealer_name(os.path.splitext(old_bname)[0])
            if (new_dlr in daftar_dealer and old_dlr == new_dlr) or (old_bname.upper() == uf.name.upper()):
                try: os.remove(old_p)
                except Exception: pass
        p = os.path.join(DB_Multi_DIR, uf.name)
        with open(p, 'wb') as f: f.write(uf.getbuffer())
        file_times[uf.name] = now_str
        updated_dealers.append(f"{uf.name} ({new_dlr})")
    all_saved_paths = sorted(glob.glob(os.path.join(DB_Multi_DIR, "*.*")))
    all_names = [os.path.basename(p) for p in all_saved_paths]
    file_times = {k: file_times.get(k, now_str) for k in all_names}
    meta['database_multi'] = {'file_names': all_names, 'saved_paths': all_saved_paths, 'file_times': file_times, 'count': len(all_names), 'updated_at': now_str}
    save_json(meta, RAW_META_FILE)
    return updated_dealers, len(all_names)

def get_saved_file_path(prefix):
    meta = load_json(RAW_META_FILE)
    if prefix in meta and os.path.exists(meta[prefix].get('saved_path', '')): return meta[prefix]['saved_path']
    m = glob.glob(os.path.join(UPLOAD_DIR, f"{prefix}_latest.*"))
    return m[0] if m else None

def get_saved_database_paths():
    return sorted(glob.glob(os.path.join(DB_Multi_DIR, "*.*")))

def save_rating_files(up_files):
    meta = load_json(RAW_META_FILE)
    now_str = datetime.datetime.now().strftime('%d %b %Y, %H:%M WIB')
    file_times = meta.get('rating_multi', {}).get('file_times', {})
    updated_dealers = []
    for uf in up_files:
        new_dlr = normalize_dealer_name(os.path.splitext(uf.name)[0])
        for old_p in glob.glob(os.path.join(RATING_Multi_DIR, "*.*")):
            old_bname = os.path.basename(old_p)
            old_dlr = normalize_dealer_name(os.path.splitext(old_bname)[0])
            if (new_dlr in daftar_dealer and old_dlr == new_dlr) or (old_bname.upper() == uf.name.upper()):
                try: os.remove(old_p)
                except Exception: pass
        p = os.path.join(RATING_Multi_DIR, uf.name)
        with open(p, 'wb') as f: f.write(uf.getbuffer())
        file_times[uf.name] = now_str
        updated_dealers.append(f"{uf.name} ({new_dlr})")
    all_saved_paths = sorted(glob.glob(os.path.join(RATING_Multi_DIR, "*.*")))
    all_names = [os.path.basename(p) for p in all_saved_paths]
    file_times = {k: file_times.get(k, now_str) for k in all_names}
    meta['rating_multi'] = {'file_names': all_names, 'saved_paths': all_saved_paths, 'file_times': file_times, 'count': len(all_names), 'updated_at': now_str}
    save_json(meta, RAW_META_FILE)
    return updated_dealers, len(all_names)

def get_saved_rating_paths():
    return sorted(glob.glob(os.path.join(RATING_Multi_DIR, "*.*")))

def get_azura_logo_path():
    saved_logo = get_saved_file_path('azura_logo')
    if saved_logo and os.path.exists(saved_logo): return saved_logo
    for cand in ['AZURA.jpg', 'AZURA.png', 'AZURA.jpeg', 'azura.jpg', 'azura.png', 'logo_azura.jpg', 'logo_azura.png']:
        if os.path.exists(cand): return cand
    for m in (glob.glob('*AZURA*.*') + glob.glob('*azura*.*')):
        if m.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): return m
    return None

def render_sidebar_azura_logo():
    logo_p = get_azura_logo_path()
    if logo_p and os.path.exists(logo_p):
        try:
            with open(logo_p, 'rb') as img_f: b64_str = base64.b64encode(img_f.read()).decode('utf-8')
            mime = 'image/png' if logo_p.lower().endswith('.png') else 'image/jpeg'
            st.sidebar.markdown(f'<div class="azura-logo-box"><img src="data:{mime};base64,{b64_str}" class="azura-logo-img" alt="AZURA"></div>', unsafe_allow_html=True)
            return
        except Exception: pass
    st.sidebar.markdown('<div class="azura-logo-box"><div class="azura-fallback-badge"><div style="font-size:22px; line-height:1;">🐺</div><div style="font-size:10px; font-weight:900; letter-spacing:1px; color:#00E5FF; margin-top:2px;">AZURA</div></div></div>', unsafe_allow_html=True)

def call_gemini_ai_table(api_key, raw_context_str):
    clean_key = api_key.strip()
    prompt = f"""Anda adalah Senior Sales Manager & Data Analyst Dealer Motor Yamaha.
Berikut adalah DATA MENTAH LENGKAP dari Tabel 1 s.d 5, Data Alasan Reject SPK, serta TARGET RASIONAL 7 HARI KE DEPAN:
{raw_context_str}

TUGAS ANDA:
Lakukan analisa silang yang tajam (temukan akar masalah/bottleneck tersembunyi dari data di atas) dan susun Action Plan taktis terukur dalam format JSON murni dengan 16 key berikut.

ATURAN WAJIB (SANGAT KETAT):
1. MAKSIMAL 35 KATA UNTUK SETIAP KEY! Buat kalimat yang super padat, to-the-point, langsung ke akar masalah dan angka sasaran (1 paragraf pendek saja per key, maksimal 35 kata).
2. GUNAKAN ANGKA TARGET RASIONAL yang sudah disediakan di dalam konteks data (JANGAN membuat target tidak masuk akal seperti memaksa STU dari 2 langsung ke 25 dalam 7 hari; gunakan angka sasaran rasional & menantang yang telah dihitung di data konteks).
3. JANGAN gunakan tag HTML apa pun (teks polos murni).
4. Gunakan kata 'dealer' (bukan cabang) dan istilah 'zona kritis'.
5. Pada setiap key plan (kecuali plan_leasing), WAJIB sertakan frasa: TANPA MENURUNKAN KUALITAS DATABASE.
6. Gunakan acuan standar ideal: DB Quality (HOT/DB) = 30%, STU% (STU/DB) = 10%, Approval Leasing ACC% = 50%.
7. Untuk Leasing: bedah masalah bottleneck konversi SPK ke Faktur Kredit (BAF/ADIRA/SOF), risiko SPK Terbuka, serta sebutkan alasan penolakan (Reject) tertinggi beserta solusinya.

Format JSON:
{{
  "cond_dealer": "Maks 35 kata: diagnosa tajam akar masalah STU Dealer vs Ideal/LM & bottleneck konversi DB->HOT (ideal 30%) atau HOT->STU (ideal 10%).",
  "plan_dealer": "Maks 35 kata: target rasional tambahan STU (sesuai konteks), STU/hari, & DB/MP/hari TANPA MENURUNKAN KUALITAS DATABASE.",
  "cond_type": "Maks 35 kata: bedah segmen type terburuk (AT PREMIUM/CLASSY/LPM), penyebab anjloknya dilihat dari DB Q, ACC%, atau STU%.",
  "plan_type": "Maks 35 kata: target rasional tambahan STU, SPK, & DB harian fokus segmen terburuk TANPA MENURUNKAN KUALITAS DATABASE.",
  "cond_leasing": "Maks 35 kata: bedah gap SPK vs Faktur Kredit (BAF/ADIRA/SOF), bahaya SPK Terbuka, & alasan Reject tertinggi.",
  "plan_leasing": "Maks 35 kata: target eksekusi SPK Terbuka 1x24 jam, alokasi aplikasi ke leasing terkuat, & solusi mengatasi alasan Reject utama.",
  "cond_koor": "Maks 35 kata: diagnosa kelemahan utama Koordinator terburuk (apakah kurang DB lapangan, rendah DB Q <30%, atau macet di ACC%/STU%).",
  "plan_koor": "Maks 35 kata: target rasional tambahan STU, SPK, & DB/MP/hari tim koordinator tersebut TANPA MENURUNKAN KUALITAS DATABASE.",
  "cond_counter": "Maks 35 kata: diagnosa kelemahan Counter terburuk dari sisi konversi walk-in/leads digital (DB Q vs 30%, STU% vs 10%, ACC% vs 50%).",
  "plan_counter": "Maks 35 kata: target rasional tambahan STU, follow-up SPK terbuka, & input DB harian counter TANPA MENURUNKAN KUALITAS DATABASE.",
  "cond_mp": "Maks 35 kata: diagnosa pola masalah Salesman lapangan di zona kritis (target besar tapi STU/DB Q/ACC% rendah).",
  "plan_mp": "Maks 35 kata: kuota rasional +1 s.d +2 STU, SPK, & 4-5 DB/hari per salesman kritis TANPA MENURUNKAN KUALITAS DATABASE.",
  "cond_md": "Maks 35 kata: analisa aktifitas MD KHUSUS prospect type Event; sebutkan sub prospect Event yang TERLEMAH (DB, HOT/DB Q, STU/STU%) dan penyebabnya.",
  "plan_md": "Maks 35 kata: target rasional STU & follow-up HOT untuk sub Event terlemah TANPA MENURUNKAN KUALITAS DATABASE.",
  "cond_sosmed": "Maks 35 kata: analisa prospect dari Media Sosial (DB, HOT/DB Q, STU/STU%) vs standar 30% dan 10%.",
  "plan_sosmed": "Maks 35 kata: target rasional STU & follow-up HOT Media Sosial TANPA MENURUNKAN KUALITAS DATABASE."
}}"""
    if clean_key.startswith('AIza'):
        auth_variants = [
            ({'Content-Type': 'application/json', 'x-goog-api-key': clean_key}, f"?key={urllib.parse.quote(clean_key)}"),
            ({'Content-Type': 'application/json', 'x-goog-api-key': clean_key}, "")
        ]
    else:
        auth_variants = [
            ({'Content-Type': 'application/json', 'Authorization': f'Bearer {clean_key}'}, ""),
            ({'Content-Type': 'application/json', 'x-goog-api-key': clean_key}, ""),
            ({'Content-Type': 'application/json', 'x-goog-api-key': clean_key}, f"?key={urllib.parse.quote(clean_key)}")
        ]
    candidate_models = [('v1beta', 'gemini-2.5-flash'), ('v1beta', 'gemini-2.0-flash'), ('v1beta', 'gemini-1.5-flash'), ('v1', 'gemini-2.5-flash'), ('v1', 'gemini-2.0-flash'), ('v1', 'gemini-1.5-flash')]
    last_err = None
    for api_ver, model_name in candidate_models:
        for hdrs, q_str in auth_variants:
            url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{model_name}:generateContent{q_str}"
            gen_cfg = {"temperature": 0.45, "responseMimeType": "application/json"} if api_ver == 'v1beta' else {"temperature": 0.45}
            try:
                req = urllib.request.Request(url, data=json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": gen_cfg}).encode('utf-8'), headers=hdrs)
                with urllib.request.urlopen(req, timeout=25) as resp:
                    txt = json.loads(resp.read().decode('utf-8'))['candidates'][0]['content']['parts'][0]['text'].strip()
                    if txt.startswith("```"): txt = txt.strip("`").replace("json", "", 1).strip()
                    s_i, e_i = txt.find('{'), txt.rfind('}')
                    if s_i != -1 and e_i != -1: txt = txt[s_i:e_i+1]
                    return {k: limit_words(v, MAX_NARRATIVE_WORDS) for k, v in json.loads(txt).items()}
            except urllib.error.HTTPError as he:
                err_body = ""
                try: err_body = he.read().decode('utf-8')
                except Exception: pass
                last_err = f"HTTP {he.code} ({api_ver}/{model_name}): {err_body[:160] or he.reason}"
                continue
            except Exception as e:
                last_err = f"{model_name}: {str(e)}"
                continue
    raise RuntimeError(last_err or "Gagal menghubungi Gemini API.")

render_sidebar_azura_logo()
st.sidebar.markdown('### ⚔️ BUSHIDO ANALYSIS')
MAIN_TABS, UPLOAD_TAB, MASTER_TAB = ['🏢 STU', '🏦 SPK ONLINE', '📊 DASHBOARD KPI'], '📁 UPLOAD FILE', '🎯 MASTER KPI'
UPLOAD_MENU = [UPLOAD_TAB, MASTER_TAB]
if st.session_state.get('active_menu_tab') not in MAIN_TABS + UPLOAD_MENU:
    st.session_state['active_menu_tab'] = '🏢 STU'
if st.session_state.get('nav_main_radio') not in MAIN_TABS + [None]:
    del st.session_state['nav_main_radio']

def on_main_nav_change():
    if st.session_state.get('nav_main_radio') is not None: st.session_state['active_menu_tab'], st.session_state['nav_upload_radio'] = st.session_state['nav_main_radio'], None
def on_upload_nav_change():
    if st.session_state.get('nav_upload_radio') is not None: st.session_state['active_menu_tab'], st.session_state['nav_main_radio'] = st.session_state['nav_upload_radio'], None

st.sidebar.radio('Menu Bushido Analysis:', MAIN_TABS, index=MAIN_TABS.index(st.session_state['active_menu_tab']) if st.session_state['active_menu_tab'] in MAIN_TABS else None, key='nav_main_radio', on_change=on_main_nav_change, label_visibility='collapsed')
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
st.sidebar.radio('Menu Upload File:', UPLOAD_MENU, index=UPLOAD_MENU.index(st.session_state['active_menu_tab']) if st.session_state['active_menu_tab'] in UPLOAD_MENU else None, key='nav_upload_radio', on_change=on_upload_nav_change, label_visibility='collapsed')
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
st.sidebar.markdown('### 🧰 Tampilan Tabel')
st.sidebar.radio('Mode tabel:', ['🖼️ Capture (gambar)', '⚡ Interaktif'], key='tbl_mode_radio', label_visibility='collapsed', help='Capture: tabel statis + tombol salin/unduh gambar. Interaktif: tabel yang bisa diurutkan & dicari.')
st.session_state['tbl_mode'] = 'interaktif' if str(st.session_state.get('tbl_mode_radio', '')).startswith('⚡') else 'capture'
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
menu_pilihan = st.session_state['active_menu_tab']

def smart_parse_datetime(s):
    if s is None or len(s) == 0 or pd.api.types.is_datetime64_any_dtype(s): return pd.to_datetime(s, errors='coerce')
    s_str = s.dropna().astype(str).str.strip()
    if s_str.empty: return pd.to_datetime(s, errors='coerce')
    return pd.to_datetime(s, errors='coerce', yearfirst=True) if s_str.str.match(r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}').mean() > 0.5 else pd.to_datetime(s, errors='coerce', dayfirst=True)

def make_unique_columns(cols):
    seen, res = {}, []
    for i, c in enumerate(cols):
        cs = str(c).strip()
        if not cs or cs.upper() in ['NAN', 'NONE']: cs = f'UNNAMED_{i}'
        seen[cs] = seen.get(cs, -1) + 1
        res.append(f"{cs}_{seen[cs]}" if seen[cs] > 0 else cs)
    return res

def parse_date_cols(df):
    if df is None or df.empty: return df
    cu = [str(c).strip().upper() for c in df.columns]
    idx = next((i for i, x in enumerate(cu) if x in ['TANGGAL', 'TGL PENGAJUAN', 'TGL NOTA', 'TGL FAKTUR', 'TGL SPK', 'TANGGAL SPK', 'SPK DATE', 'DATE', 'TGL', 'PROSPECT DATE', 'TGL INPUT', 'TGL DATABASE', 'TANGGAL INPUT', 'TGL PROSPEK']), None)
    if idx is None: idx = next((i for i, c in enumerate(cu) if any(k in c for k in ['TGL', 'TANGGAL', 'DATE']) and 'LAHIR' not in c), 4 if df.shape[1] > 4 else None)
    if idx is not None:
        df['Tanggal_Parsed'] = smart_parse_datetime(df.iloc[:, idx])
        df['bulan'], df['hari'], df['tahun'] = df['Tanggal_Parsed'].dt.month, df['Tanggal_Parsed'].dt.day, df['Tanggal_Parsed'].dt.year
    return df

def normalize_leasing_val(val):
    s = clean_str(val)
    if not s or s in ['NAN', 'NONE', '-']: return ''
    if s in ['CASH', 'TUNAI', 'KSM MANDIRI', 'KSMBCA', 'MICROFINANCE INDO MOBILE FINANCE INDONESIA'] or any(k in s for k in ['MICROFINANCE', 'KSM MANDIRI', 'KSMBCA', 'KSM BCA', 'CASH', 'TUNAI']): return 'CASH'
    if s in ['ADIRA', 'ADIRA FINANCE'] or 'ADIRA' in s: return 'ADIRA'
    if s in ['BAF', 'BUSSAN AUTO FINANCE'] or any(k in s for k in ['BAF', 'BUSSAN']): return 'BAF'
    if s in ['SOF', 'SUMMIT OTO FINANCE'] or any(k in s for k in ['SOF', 'SUMMIT', 'OTO MULTIARTHA']): return 'SOF'
    if s in ['IMFI', 'INDOMOBIL FINANCE INDONESIA'] or any(k in s for k in ['IMFI', 'INDOMOBIL']): return 'IMFI'
    return 'OTHERS'

def assign_leasing_faktur(df):
    if df is None or df.empty:
        if df is not None: df['Leasing_Faktur_Clean'] = ''
        return df
    cu = [str(c).strip().upper() for c in df.columns]
    best_c = df.columns[cu.index('LEASING')] if 'LEASING' in cu else (df.columns[20] if df.shape[1] > 20 else None)
    if best_c is None:
        ign = {'NAMA DEALER', 'TANGGAL_PARSED', 'BULAN', 'HARI', 'TAHUN', 'KOOR', 'TYPE_CLEAN', 'LEASING_FAKTUR_CLEAN', 'SALESMAN_CLEAN'}
        best_sc = 0
        for i, cn in enumerate(df.columns):
            if str(cn).strip().upper() in ign: continue
            sc = int(df.iloc[:, i].dropna().astype(str).apply(normalize_leasing_val).isin(['BAF', 'ADIRA', 'SOF', 'IMFI', 'OTHERS', 'CASH']).sum())
            if sc > best_sc: best_sc, best_c = sc, cn
    if best_c is None: best_c = next((df.columns[cu.index(c)] for c in ['LEASING', 'NAMA LEASING', 'FINCOY', 'FINANCE COMPANY', 'NAMA FINCOY', 'KREDITUR', 'PEMBIAYAAN', 'VIA'] if c in cu), None)
    if best_c is None: best_c = next((df.columns[i] for i, c in enumerate(cu) if any(k in c for k in ['LEASING', 'FINCOY', 'FINANCE', 'PEMBIAYAAN', 'KREDIT'])), None)
    s_t = df[best_c].iloc[:, 0] if (best_c is not None and isinstance(df[best_c], pd.DataFrame)) else (df[best_c] if best_c is not None else None)
    df['Leasing_Faktur_Clean'] = s_t.apply(normalize_leasing_val) if s_t is not None else ''
    return df

def detect_type_col(df, map_d, map_ns):
    if df is None or df.empty: return None
    ign = {'NAMA_DEALER_CLEAN', 'DATA_TYPE_CLEAN', 'TANGGAL_PARSED', 'BULAN', 'HARI', 'TAHUN', 'KOOR', 'KOOR_SPK', 'NAMA_DEALER_SPK', 'LEASING_SPK_CLEAN', 'STATUS_SPK_CLEAN', 'ALASAN_REJECT_CLEAN', 'SALESMAN_CLEAN', 'TYPE_CLEAN', 'DATA TYPE', 'LEASING_FAKTUR_CLEAN'}
    cu = [str(c).strip().upper() for c in df.columns]
    if map_d:
        ku, kns, best_c, best_sc = set(map_d.keys()), set(map_ns.keys()), None, 0
        for i, cn in enumerate(df.columns):
            if cu[i] in ign or 'DATA TYPE' in cu[i]: continue
            s = df.iloc[:, i].dropna().astype(str)
            if s.empty: continue
            sc = max(len(set(s.str.split().str.join(' ').str.upper().unique()).intersection(ku)), len(set(s.str.split().str.join('').str.upper().unique()).intersection(kns)))
            if sc > best_sc: best_sc, best_c = sc, cn
        if best_sc > 0: return best_c
    for cand in ['TYPE', 'TIPE', 'NAMA TYPE', 'NAMA TIPE', 'TYPE MOTOR', 'TIPE MOTOR', 'MODEL', 'MODEL NAME', 'PRODUCT NAME', 'UNIT', 'NAMA UNIT', 'DESKRIPSI UNIT', 'DESKRIPSI', 'NAMA BARANG', 'TYPE UNIT', 'TIPE UNIT', 'INTERESTED MODEL', 'PRODUCT', 'MOTOR', 'SERIES']:
        if cand in cu: return df.columns[cu.index(cand)]
    return next((df.columns[i] for i, c in enumerate(cu) if c not in ign and not any(x in c for x in ['DATA TYPE', 'PAYMENT', 'BAYAR', 'TRANSAKSI']) and any(k in c for k in ['TYPE', 'TIPE', 'MODEL', 'PRODUK', 'PRODUCT', 'UNIT', 'MOTOR'])), None)

def assign_type_from_lookup(df, map_d, map_ns, unmapped=None):
    if df is None or df.empty:
        if df is not None: df['Type_Clean'] = 'LAIN-LAIN'
        return df
    tc = detect_type_col(df, map_d, map_ns)
    if tc is not None and map_d:
        def map_fn(val):
            k = clean_str(val)
            if not k or k in ['NAN', 'NONE', '', 'NA', '-', 'TOTAL', 'JUMLAH']: return 'LAIN-LAIN'
            if k in map_d: return map_d[k]
            k_ns = nospace_str(val)
            if k_ns in map_ns: return map_ns[k_ns]
            if unmapped is not None: unmapped.add(k)
            return 'LAIN-LAIN'
        s_t = df[tc].iloc[:, 0] if isinstance(df[tc], pd.DataFrame) else df[tc]
        df['Type_Clean'] = s_t.apply(map_fn)
    else: df['Type_Clean'] = 'LAIN-LAIN'
    return df

def get_file_mtime(fpath):
    try: return os.path.getmtime(fpath) if fpath and os.path.exists(fpath) else 0.0
    except Exception: return 0.0

@st.cache_data(show_spinner=False)
def read_single_db_file_cached(fpath, mtime):
    df_raw = pd.read_csv(fpath, header=None) if fpath.lower().endswith('.csv') else pd.read_excel(fpath, header=None)
    df_raw = smart_text_to_columns(df_raw)
    if df_raw is None or df_raw.empty: return pd.DataFrame()
    h_idx = next((r for r in range(min(25, len(df_raw))) if any(m in [clean_str(v) for v in df_raw.iloc[r].values if pd.notna(v)] for m in ['CUSTOMER NAME', 'POINT NAME', 'PROSPECT DATE', 'DATA TYPE', 'KTP NO.', 'POINT CODE'])), 0)
    df = df_raw.iloc[h_idx + 1:].copy()
    df.columns = make_unique_columns([str(c).strip() for c in df_raw.iloc[h_idx].values])
    df = df.dropna(how='all').reset_index(drop=True)
    cu = [c.upper() for c in df.columns]
    s_chk = df.iloc[:, cu.index('CUSTOMER NAME')] if 'CUSTOMER NAME' in cu else df.iloc[:, 0]
    nm_up = s_chk.astype(str).str.strip().str.upper()
    _keep_hdr = ~nm_up.isin(['CUSTOMER NAME', 'NO', 'NO.', 'TOTAL', 'JUMLAH'])   # baris judul/total dibuang
    df = df[_keep_hdr.values].reset_index(drop=True)
    nm_up = nm_up[_keep_hdr.values].reset_index(drop=True)
    df['Nama_Dealer_Clean'] = normalize_dealer_name(os.path.splitext(os.path.basename(fpath))[0]) or 'TIDAK DIKETAHUI'
    col_k = df.iloc[:, cu.index('POINT NAME')].astype(str).str.strip().str.upper() if 'POINT NAME' in cu else (df.iloc[:, 10].astype(str).str.strip().str.upper() if df.shape[1] > 10 else None)
    if col_k is not None: df.loc[col_k == 'SIP PANJI BESUKI', 'Nama_Dealer_Clean'] = 'SIP BESUKI'
    df['Data_Type_Clean'] = df.iloc[:, cu.index('DATA TYPE')].astype(str).str.strip().str.upper() if 'DATA TYPE' in cu else (df.iloc[:, 5].astype(str).str.strip().str.upper() if df.shape[1] > 5 else '')
    df = parse_date_cols(df)
    _nm_ok = ~nm_up.isin(['NAN', 'NONE', '']).values
    # baris tanpa Customer Name tetap dihitung bila tanggal prospek valid (sama seperti hitung manual dari file asli)
    df = df[_nm_ok | df['Tanggal_Parsed'].notna().values].reset_index(drop=True) if 'Tanggal_Parsed' in df.columns else df[_nm_ok].reset_index(drop=True)
    return df

@st.cache_data(show_spinner=False)
def db_file_rawcount(fpath, mtime):
    """Jumlah baris data mentah di file Database (di luar judul kolom) — untuk rekonsiliasi."""
    try:
        df_raw = pd.read_csv(fpath, header=None) if fpath.lower().endswith('.csv') else pd.read_excel(fpath, header=None)
        df_raw = smart_text_to_columns(df_raw)
        if df_raw is None or df_raw.empty: return 0
        h_idx = next((r for r in range(min(25, len(df_raw))) if any(m in [clean_str(v) for v in df_raw.iloc[r].values if pd.notna(v)] for m in ['CUSTOMER NAME', 'POINT NAME', 'PROSPECT DATE', 'DATA TYPE', 'KTP NO.', 'POINT CODE'])), 0)
        return int(len(df_raw.iloc[h_idx + 1:].dropna(how='all')))
    except Exception: return 0

def read_single_db_file(fpath):
    return read_single_db_file_cached(fpath, get_file_mtime(fpath)).copy()

def smart_text_to_columns(df):
    if df is not None and df.shape[1] == 1 and len(df) > 0:
        sample_str = str(df.iloc[0, 0])
        for delim in ['\t', ';', ',', '|']:
            if delim in sample_str:
                df_split = df.iloc[:, 0].str.split(delim, expand=True)
                if df_split.shape[1] > 1:
                    return df_split
    return df

@st.cache_data(show_spinner=False)
def read_single_rating_file_cached(fpath, mtime):
    df_raw = pd.read_csv(fpath, header=None) if fpath.lower().endswith('.csv') else pd.read_excel(fpath, header=None)
    df_raw = smart_text_to_columns(df_raw)
    if df_raw is None or df_raw.empty: return pd.DataFrame()
    rating_markers = ['KODE DEALER', 'DEALER CODE', 'POINT CODE', 'POINT NAME', 'CUSTOMER NAME', 'NAMA CUSTOMER', 'NAMA KONSUMEN', 'RATING', 'REVIEW', 'STAR', 'BINTANG', 'SCORE', 'NILAI', 'SALESMAN', 'NAMA SALES', 'NAMA PEGAWAI', 'PRAMUNIAGA', 'TANGGAL', 'DATE', 'PROSPECT DATE']
    h_idx = next((r for r in range(min(25, len(df_raw))) if any(m in [clean_str(v) for v in df_raw.iloc[r].values if pd.notna(v)] for m in rating_markers)), 0)
    df = df_raw.iloc[h_idx + 1:].copy()
    df.columns = make_unique_columns([str(c).strip() for c in df_raw.iloc[h_idx].values])
    df = df.dropna(how='all').reset_index(drop=True)
    if df.empty: return pd.DataFrame()
    cu = [c.upper() for c in df.columns]
    chk_col = next((df.columns[cu.index(c)] for c in ['CUSTOMER NAME', 'NAMA CUSTOMER', 'NAMA KONSUMEN', 'NAMA PELANGGAN', 'NAMA SALES', 'SALESMAN', 'KODE DEALER', 'DEALER CODE', 'POINT CODE'] if c in cu), df.columns[0])
    s_chk = df[chk_col].iloc[:, 0] if isinstance(df[chk_col], pd.DataFrame) else df[chk_col]
    df = df[s_chk.notna() & ~s_chk.astype(str).str.strip().str.upper().isin(['CUSTOMER NAME', 'NAMA CUSTOMER', 'NAMA KONSUMEN', 'KODE DEALER', 'DEALER CODE', 'POINT CODE', 'NO', 'NO.', 'TOTAL', 'JUMLAH', 'NAN', 'NONE', ''])].reset_index(drop=True)
    fallback_dlr = normalize_dealer_name(os.path.splitext(os.path.basename(fpath))[0])
    df['Nama_Dealer_Clean'] = fallback_dlr if fallback_dlr in daftar_dealer else (fallback_dlr or 'TIDAK DIKETAHUI')
    return parse_date_cols(df)

def read_single_rating_file(fpath):
    return read_single_rating_file_cached(fpath, get_file_mtime(fpath)).copy()

def assign_rating_dealer_and_koor(df, map_dlr_code):
    if df is None or df.empty:
        if df is not None:
            df['Kode_Dealer_Clean'] = ''
            df['Salesman_Clean'] = None
            df['Koor'] = 'LAIN-LAIN'
            df['Nama_Dealer_Clean'] = 'TIDAK DIKETAHUI'
        return df
    
    df.columns = make_unique_columns([str(c).strip() for c in df.columns])
    cu = [str(c).strip().upper() for c in df.columns]
    fallback_file_dlr = df['Nama_Dealer_Clean'].iloc[0] if ('Nama_Dealer_Clean' in df.columns and len(df) > 0) else 'TIDAK DIKETAHUI'
    
    # Deteksi cerdas kolom Salesman dengan mencocokkan isi kolom terhadap daftar nama Salesman di Data Lookup
    sm_col = next((df.columns[cu.index(c)] for c in ['SALESMAN/TEKNISI', 'NAMA SALESMAN', 'SALESMAN', 'NAMA SALES', 'NAMA PEGAWAI', 'PRAMUNIAGA', 'SALES NAME', 'PIC'] if c in cu), None)
    if sm_col is None and (mapping_salesman_koor or mapping_salesman_dealer):
        known_sm_set = set(mapping_salesman_koor.keys()) | set(mapping_salesman_dealer.keys())
        known_sm_ns = {alnum_str(k) for k in known_sm_set if alnum_str(k)}
        best_c, best_sc = None, 0
        for i, cn in enumerate(df.columns):
            if cu[i] in {'NAMA_DEALER_CLEAN', 'TANGGAL_PARSED', 'BULAN', 'HARI', 'TAHUN'}: continue
            s_vals = df.iloc[:, i].dropna().astype(str).apply(clean_str)
            if s_vals.empty: continue
            sc = int(s_vals.isin(known_sm_set).sum()) + int(s_vals.apply(alnum_str).isin(known_sm_ns).sum())
            if sc > best_sc:
                best_sc, best_c = sc, cn
        if best_sc > 0:
            sm_col = best_c
    if sm_col is None and df.shape[1] > 9: sm_col = df.columns[9]
    if sm_col is None:
        sm_col = next((df.columns[i] for i, c in enumerate(cu) if any(k in c for k in ['SALES', 'PEGAWAI', 'PRAMUNIAGA', 'TEKNISI'])), None)

    kd_col = next((df.columns[cu.index(c)] for c in ['KODE DEALER', 'DEALER CODE', 'POINT CODE', 'KODE CABANG', 'BRANCH CODE', 'KD DEALER', 'KODE_DEALER', 'DEALER ID', 'OUTLET CODE', 'KODE OUTLET'] if c in cu), None)
    if kd_col is None and df.shape[1] > 2: kd_col = df.columns[2]
    
    dn_col = next((df.columns[cu.index(c)] for c in ['NAMA DEALER', 'DEALER', 'POINT NAME', 'CABANG'] if c in cu), None)
    if dn_col is None and df.shape[1] > 3: dn_col = df.columns[3]

    map_sm_dlr_ns = {alnum_str(k): v for k, v in mapping_salesman_dealer.items() if alnum_str(k)} if mapping_salesman_dealer else {}
    map_sm_koor_ns = {alnum_str(k): v for k, v in mapping_salesman_koor.items() if alnum_str(k)} if mapping_salesman_koor else {}

    def resolve_koor_from_sm(sm_c):
        if not sm_c or sm_c in ['NAN', 'NONE', '', '-']: return 'LAIN-LAIN'
        if mapping_salesman_koor:
            if sm_c in mapping_salesman_koor: return clean_str(mapping_salesman_koor[sm_c])
            sm_ns = alnum_str(sm_c)
            if sm_ns and sm_ns in map_sm_koor_ns: return clean_str(map_sm_koor_ns[sm_ns])
            for k_s, v_k in mapping_salesman_koor.items():
                if len(k_s) >= 4 and (k_s in sm_c or sm_c in k_s): return clean_str(v_k)
        return 'LAIN-LAIN'

    def resolve_dlr_and_koor(kd_val, dn_val, sm_val, kr_resolved):
        sm_c = clean_str(sm_val)
        # 1. Prioritas Utama: Lookup Dealer langsung dari Nama Salesman
        if sm_c and mapping_salesman_dealer:
            if sm_c in mapping_salesman_dealer: return mapping_salesman_dealer[sm_c]
            sm_ns = alnum_str(sm_c)
            if sm_ns and sm_ns in map_sm_dlr_ns: return map_sm_dlr_ns[sm_ns]
            for sm_k, dlr_v in mapping_salesman_dealer.items():
                if len(sm_k) >= 4 and (sm_k in sm_c or sm_c in sm_k): return dlr_v

        # 2. Prioritas Kedua: Lookup Dealer dari Koordinator Salesman tersebut
        if kr_resolved and kr_resolved != 'LAIN-LAIN':
            if 'mapping_koor_dealer' in globals() and kr_resolved in mapping_koor_dealer:
                return mapping_koor_dealer[kr_resolved]
            norm_kr = normalize_dealer_name(kr_resolved)
            if norm_kr in daftar_dealer:
                return norm_kr

        # 3. Fallback: Kode Dealer atau Nama Dealer di baris file
        k_code = clean_str(kd_val)
        if k_code.endswith('.0'): k_code = k_code[:-2].strip()
        k_alnum = alnum_str(k_code)
        if k_code:
            if k_code in map_dlr_code: dl = map_dlr_code[k_code]
            elif k_alnum in map_dlr_code: dl = map_dlr_code[k_alnum]
            elif k_code == 'SIP PANJI BESUKI': dl = 'SIP BESUKI'
            else: dl = normalize_dealer_name(k_code)
            if dl in daftar_dealer: return dl
            
        d_name = clean_str(dn_val)
        if d_name:
            if d_name == 'SIP PANJI BESUKI': return 'SIP BESUKI'
            norm_dn = normalize_dealer_name(d_name)
            if norm_dn in daftar_dealer: return norm_dn
                
        return fallback_file_dlr if fallback_file_dlr in daftar_dealer else (normalize_dealer_name(d_name) or 'TIDAK DIKETAHUI')

    dealers, sm_cleans, koors, kode_dealers = [], [], [], []
    for _, row in df.iterrows():
        kd_v = row[kd_col] if kd_col is not None and kd_col in df.columns else ''
        dn_v = row[dn_col] if dn_col is not None and dn_col in df.columns else ''
        sm_v = row[sm_col] if sm_col is not None and sm_col in df.columns else ''
        
        if isinstance(kd_v, pd.Series): kd_v = kd_v.iloc[0]
        if isinstance(dn_v, pd.Series): dn_v = dn_v.iloc[0]
        if isinstance(sm_v, pd.Series): sm_v = sm_v.iloc[0]
        
        sm_clean = clean_str(sm_v)
        sm_clean = sm_clean if (sm_clean and sm_clean not in ['NAN', 'NONE', '', '-']) else None
        kr_val = resolve_koor_from_sm(sm_clean)
        if not kr_val or kr_val in ['NAN', 'NONE', '-']: kr_val = 'LAIN-LAIN'
        dlr_res = resolve_dlr_and_koor(kd_v, dn_v, sm_clean, kr_val)
                
        dealers.append(dlr_res)
        sm_cleans.append(sm_clean)
        koors.append(kr_val)
        kode_dealers.append(clean_str(kd_v)[:-2].strip() if clean_str(kd_v).endswith('.0') else clean_str(kd_v))

    df['Nama_Dealer_Clean'] = dealers
    df['Salesman_Clean'] = sm_cleans
    df['Koor'] = koors
    df['Kode_Dealer_Clean'] = kode_dealers
    return df

def load_employee_targets(fpath):
    t_exact, t_ns = dict(FIXED_COUNTER_TARGETS), dict(FIXED_COUNTER_TARGETS_NS)
    if not fpath or not os.path.exists(fpath): return t_exact, t_ns
    try:
        df_e = pd.read_csv(fpath, header=None) if fpath.lower().endswith('.csv') else pd.read_excel(fpath, header=None)
        if df_e is not None and df_e.shape[1] >= 6:
            for i in range(len(df_e)):
                nm, pos = clean_str(df_e.iloc[i, 2]), clean_str(df_e.iloc[i, 5])
                if not nm or nm in ['NAMA', 'NAN', 'NONE'] or nm in FIXED_COUNTER_TARGETS or alnum_str(nm) in FIXED_COUNTER_TARGETS_NS: continue
                tv = 5 if 'PLATINUM' in pos else (3 if 'GOLD' in pos else (2 if 'TRAINING' in pos else None))
                if tv is not None: t_exact[nm], t_ns[alnum_str(nm)] = tv, tv
    except Exception as e: st.error(f'Error File Employee: {e}')
    return t_exact, t_ns

if menu_pilihan == '📁 UPLOAD FILE':
    st.markdown('<div class="main-title">UPLOAD FILE</div><div class="sub-title">Unggah file sumber data sesuai kelompoknya (tersimpan otomatis &amp; permanen)</div>', unsafe_allow_html=True)
    meta_info = load_json(RAW_META_FILE)

    def _status_line(kp, lbl):
        m_ = meta_info.get(kp)
        if m_ and os.path.exists(m_.get('saved_path', '')):
            st.markdown(f"<div style='font-size:12px;color:#94A3B8;line-height:1.5;'>📌 <b>Aktif:</b> <code style='font-size:11px;'>{m_['original_name']}</code> · {m_['updated_at']}</div>", unsafe_allow_html=True)
        else: st.markdown("<div style='font-size:12px;color:#FBBF24;'>⚠️ Belum ada file.</div>", unsafe_allow_html=True)

    # ---------- Grup 1: Data Penjualan & Master ----------
    with st.container(border=True):
        st.markdown("#### 📒 Data Penjualan & Master")
        st.caption('Diupload oleh admin MD')
        up_defs = [('Faktur', 'faktur', ['xls', 'xlsx'], 'File Faktur penjualan (.xls / .xlsx).'),
                   ('Nota', 'nota', ['xls', 'xlsx'], 'File Nota (.xls / .xlsx).'),
                   ('SPK', 'spk', ['xls', 'xlsx', 'csv'], 'File SPK leasing (.xls / .xlsx / .csv).'),
                   ('Master Employee', 'employee', ['xls', 'xlsx', 'csv'], 'Target otomatis salesman — Kolom C: Nama, Kolom F: Posisi.'),
                   ('Data Lookup', 'lookup', ['xls', 'xlsx'], 'Mapping type, salesman, koordinator & dealer (.xls / .xlsx).')]
        for col_u, (lbl, kp, exts, hlp) in zip(st.columns(len(up_defs)), up_defs):
            with col_u:
                uf = st.file_uploader(lbl, type=exts, key=f'{kp}_up', help=hlp)
                if uf: save_raw_file(uf, kp); st.success(f"✅ {lbl} diperbarui: **{uf.name}**"); bsg_toast_once(f'up_{kp}_{uf.name}_{uf.size}', f'{lbl} diperbarui: {uf.name}'); meta_info = load_json(RAW_META_FILE)
                _status_line(kp, lbl)

    # ---------- Grup 2: Data Operasional Dealer ----------
    with st.container(border=True):
        st.markdown("#### 🗂️ Data Operasional Dealer")
        st.caption('Diupload setiap sore oleh admin dealer')
        col_db, col_rt = st.columns(2)
        with col_db:
            db_ups = st.file_uploader('Database — 1 file (parsial) atau 6 file sekaligus (.xls / .xlsx / .csv)', type=['xls', 'xlsx', 'csv'], accept_multiple_files=True, key='db_up')
            if db_ups:
                upd_list, total_active = save_database_files(db_ups)
                st.success(f"✅ **Update Parsial Berhasil!** File diperbarui: `{', '.join(upd_list)}`. File dealer lainnya tetap aman (Total **{total_active} File Database** aktif).")
                bsg_toast_once('up_db_' + '|'.join(f'{u.name}{u.size}' for u in db_ups), f'Database diperbarui ({len(db_ups)} file)')
            saved_db_paths_now = get_saved_database_paths()
            if saved_db_paths_now:
                ftimes = load_json(RAW_META_FILE).get('database_multi', {}).get('file_times', {})
                badge_items = [f"`{os.path.basename(p)}` → **{normalize_dealer_name(os.path.splitext(os.path.basename(p))[0])}** ({ftimes.get(os.path.basename(p), 'Tersimpan')})" for p in saved_db_paths_now]
                st.info(f"📌 **Database Aktif ({len(saved_db_paths_now)} File):** " + " | ".join(badge_items))
                if st.button('🗑️ Reset Semua DB', key='btn_rst_all_db', help='Hapus seluruh file database jika ingin mulai dari 0'):
                    for old_p in saved_db_paths_now:
                        try: os.remove(old_p)
                        except Exception: pass
                    meta_info.pop('database_multi', None); save_json(meta_info, RAW_META_FILE); st.rerun()
            else: st.warning("⚠️ Belum ada file Database.")
        with col_rt:
            rt_ups = st.file_uploader('Rating Dealer — 1 file (parsial) atau 6 file sekaligus (.xls / .xlsx / .csv)', type=['xls', 'xlsx', 'csv'], accept_multiple_files=True, key='rating_up')
            if rt_ups:
                upd_rt_list, total_rt_active = save_rating_files(rt_ups)
                st.success(f"✅ **Update Parsial Rating Berhasil!** File diperbarui: `{', '.join(upd_rt_list)}`. File dealer lainnya tetap aman (Total **{total_rt_active} File Rating** aktif).")
                bsg_toast_once('up_rt_' + '|'.join(f'{u.name}{u.size}' for u in rt_ups), f'Rating diperbarui ({len(rt_ups)} file)')
            saved_rt_paths_now = get_saved_rating_paths()
            if saved_rt_paths_now:
                rt_ftimes = load_json(RAW_META_FILE).get('rating_multi', {}).get('file_times', {})
                rt_badge_items = [f"`{os.path.basename(p)}` → **{normalize_dealer_name(os.path.splitext(os.path.basename(p))[0])}** ({rt_ftimes.get(os.path.basename(p), 'Tersimpan')})" for p in saved_rt_paths_now]
                st.info(f"📌 **File Rating Aktif ({len(saved_rt_paths_now)} File):** " + " | ".join(rt_badge_items))
                if st.button('🗑️ Reset Semua Rating', key='btn_rst_all_rt', help='Hapus seluruh file rating jika ingin mulai dari 0'):
                    for old_p in saved_rt_paths_now:
                        try: os.remove(old_p)
                        except Exception: pass
                    meta_info.pop('rating_multi', None); save_json(meta_info, RAW_META_FILE); st.rerun()
            else: st.warning("⚠️ Belum ada file Rating.")

    # ---------- Logo ----------
    with st.expander('🐺 Logo AZURA (pojok kiri atas)'):
        logo_uf = st.file_uploader('Upload Logo AZURA (.jpg / .png)', type=['jpg', 'jpeg', 'png'], key='azura_logo_up')
        if logo_uf: save_raw_file(logo_uf, 'azura_logo'); st.success(f"✅ Logo AZURA berhasil diperbarui: **{logo_uf.name}**"); st.rerun()

path_faktur, path_nota, path_lookup = get_saved_file_path('faktur'), get_saved_file_path('nota'), get_saved_file_path('lookup')
paths_database, paths_rating, path_spk = get_saved_database_paths(), get_saved_rating_paths(), get_saved_file_path('spk')
path_employee = get_saved_file_path('employee') or (glob.glob('*EMPLOYEE*.xls*')[0] if glob.glob('*EMPLOYEE*.xls*') else None)
mapping_emp_target, mapping_emp_target_ns = load_employee_targets(path_employee)

def get_fixed_counter_target(name_val):
    s = clean_str(name_val)
    if s in FIXED_COUNTER_TARGETS: return FIXED_COUNTER_TARGETS[s]
    s_no_prefix = clean_str(s.replace('COUNTER', '').replace('-', ' '))
    if s_no_prefix in FIXED_COUNTER_TARGETS: return FIXED_COUNTER_TARGETS[s_no_prefix]
    return next((v_fix for k_fix, v_fix in FIXED_COUNTER_TARGETS.items() if k_fix in s), None)

def is_counter_personnel(name_val):
    s = clean_str(name_val)
    return False if not s else (True if (s.startswith('COUNTER') or get_fixed_counter_target(s) is not None) else clean_str(mapping_salesman_koor.get(s, '')).startswith('COUNTER'))

def get_auto_sales_target(sm):
    fix_c = get_fixed_counter_target(sm)
    return fix_c if fix_c is not None else mapping_emp_target.get(clean_str(sm), mapping_emp_target_ns.get(alnum_str(clean_str(sm)), 0))

def get_koor_or_counter_target(ent_name, saved_tk_dict):
    fix_c = get_fixed_counter_target(ent_name)
    return fix_c if fix_c is not None else safe_int(saved_tk_dict.get(ent_name, 0))

mapping_salesman_koor, mapping_salesman_dealer, mapping_dealer_spk, mapping_type_lookup, mapping_type_lookup_nospace, daftar_kategori_type = {}, {}, {}, {}, {}, []
if path_lookup:
    try:
        xl_lk = pd.ExcelFile(path_lookup)
        sh_lk = next((s for s in xl_lk.sheet_names if 'LOOKUP' in s.strip().upper()), xl_lk.sheet_names[0])
        df_lk = pd.read_excel(path_lookup, sheet_name=sh_lk, header=None)
        if df_lk.shape[1] >= 2:
            skip_h = {'TYPE', 'TIPE', 'NAMA TYPE', 'NAMA TIPE', 'UNIT', 'MODEL', 'KATEGORI', 'GROUP TYPE', 'JENIS', 'ROW LABELS', 'NAN', 'NONE', ''}
            for i in range(len(df_lk)):
                ra, rb = clean_str(df_lk.iloc[i, 0]), clean_str(df_lk.iloc[i, 1])
                if ra and rb and ra not in skip_h and rb not in skip_h:
                    mapping_type_lookup[ra] = mapping_type_lookup_nospace[nospace_str(ra)] = rb
                    if rb not in daftar_kategori_type: daftar_kategori_type.append(rb)
        sc, kc, dc, hr = None, None, None, None
        for r in range(min(50, len(df_lk))):
            for c, val in enumerate(df_lk.iloc[r]):
                vs = clean_str(val)
                if any(k in vs for k in ['NAMA SALES', 'SALESMAN', 'PRAMUNIAGA', 'PEGAWAI']): sc = c
                elif 'KOOR' in vs: kc = c
                elif any(k in vs for k in ['DEALER', 'NAMA DEALER', 'CABANG', 'POINT NAME', 'OUTLET']): dc = c
            if sc is not None: hr = r; break
        if sc is not None:
            for i in range(hr + 1, len(df_lk)):
                sm = clean_str(df_lk.iloc[i, sc]) if sc is not None and sc < df_lk.shape[1] else ''
                kr = clean_str(df_lk.iloc[i, kc]) if kc is not None and kc < df_lk.shape[1] else ''
                dlr_lk = clean_str(df_lk.iloc[i, dc]) if dc is not None and dc < df_lk.shape[1] else ''
                if sm and sm not in ['NAN', 'NONE']:
                    if kr and kr not in ['NAN', 'NONE']: mapping_salesman_koor[sm] = kr
                    if dlr_lk and dlr_lk not in ['NAN', 'NONE']:
                        norm_dlr = normalize_dealer_name(dlr_lk)
                        if norm_dlr in daftar_dealer:
                            mapping_salesman_dealer[sm] = norm_dlr
        if df_lk.shape[1] > 9:
            for i in range(len(df_lk)):
                ri, rj = clean_str(df_lk.iloc[i, 8]), clean_str(df_lk.iloc[i, 9])
                if ri.endswith('.0'): ri = ri[:-2].strip()
                if rj.endswith('.0'): rj = rj[:-2].strip()
                if ri and rj and ri not in ['NAN', 'NONE'] and rj not in ['NAN', 'NONE']:
                    ni, nj = normalize_dealer_name(ri), normalize_dealer_name(rj)
                    if nj in daftar_dealer:
                        mapping_dealer_spk[ri] = mapping_dealer_spk[alnum_str(ri)] = nj
                    elif ni in daftar_dealer:
                        mapping_dealer_spk[rj] = mapping_dealer_spk[alnum_str(rj)] = ni
                    else:
                        mapping_dealer_spk[ri] = nj
        for c_idx in range(df_lk.shape[1] - 1):
            for r_idx in range(len(df_lk)):
                v1, v2 = clean_str(df_lk.iloc[r_idx, c_idx]), clean_str(df_lk.iloc[r_idx, c_idx + 1])
                if v1.endswith('.0'): v1 = v1[:-2].strip()
                if v2.endswith('.0'): v2 = v2[:-2].strip()
                if not v1 or not v2 or v1 in ['NAN', 'NONE'] or v2 in ['NAN', 'NONE']: continue
                n1, n2 = normalize_dealer_name(v1), normalize_dealer_name(v2)
                if n2 in daftar_dealer and v1 not in daftar_dealer:
                    mapping_dealer_spk[v1] = mapping_dealer_spk[alnum_str(v1)] = n2
                elif n1 in daftar_dealer and v2 not in daftar_dealer:
                    mapping_dealer_spk[v2] = mapping_dealer_spk[alnum_str(v2)] = n1
    except Exception as e: st.error(f'Error Lookup: {e}')

unmapped_types_all, sales_tanpa_koor, sales_tanpa_koor_db, sales_tanpa_koor_spk, sales_tanpa_koor_rating = set(), set(), set(), set(), set()

def assign_koor_and_sales(df, col_idx_override=None, tracker=None, koor_col_name='Koor'):
    if df is None: return df
    if df.empty:
        df['Salesman_Clean'], df[koor_col_name] = None, 'LAIN-LAIN'
        return df
    cu = [str(c).strip().upper() for c in df.columns]
    ign_col_kw = {'CUSTOMER', 'KONSUMEN', 'PELANGGAN', 'RATING', 'REVIEW', 'STAR', 'BINTANG', 'SCORE', 'NILAI', 'KOMENTAR', 'TANGGAL', 'DATE', 'KODE', 'PHONE', 'TELP', 'ALAMAT'}
    sc_name = df.columns[col_idx_override] if (col_idx_override is not None and df.shape[1] > col_idx_override) else None
    if sc_name is None:
        valid_cands = [x for x in ['NAMA PEGAWAI', 'NAMA SALES', 'NAMA PRAMUNIAGA', 'SALESMAN', 'PRAMUNIAGA', 'SALES', 'SALES NAME', 'NAMA SALESMAN', 'SALES PERSON', 'SALESPERSON', 'PIC', 'EMPLOYEE NAME', 'SALESMAN NAME', 'CREATED BY', 'USER INPUT'] if x in cu]
        if valid_cands: sc_name = df.columns[cu.index(valid_cands[0])]
    if sc_name is None:
        # Search columns that don't match ignored keywords
        for i, c_str in enumerate(cu):
            if not any(kw in c_str for kw in ign_col_kw) and any(k in c_str for k in ['NAMA', 'SALES', 'PEGAWAI', 'PRAMUNIAGA', 'PIC']):
                sc_name = df.columns[i]
                break
    if sc_name is not None:
        s_s = df[sc_name].iloc[:, 0] if isinstance(df[sc_name], pd.DataFrame) else df[sc_name]
        s_cl = s_s.astype(str).str.split().str.join(' ').str.upper()
        df['Salesman_Clean'] = s_cl.where(~s_cl.isin(['NAN', 'NONE', '', 'NA', '-', 'TOTAL', 'JUMLAH']), None)
        def map_kr(s):
            if s and pd.notna(s):
                kr_val = clean_str(mapping_salesman_koor.get(s, '')) if mapping_salesman_koor else ''
                if not kr_val or kr_val in ['NAN', 'NONE', '-', 'LAIN-LAIN']:
                    if tracker is not None: tracker.add(s)
                    return 'LAIN-LAIN'
                return kr_val
            return 'LAIN-LAIN'
        df[koor_col_name] = df['Salesman_Clean'].apply(map_kr)
    else: df['Salesman_Clean'], df[koor_col_name] = None, 'LAIN-LAIN'
    return df

df_faktur, df_faktur_all = None, None
if path_faktur:
    try:
        df_faktur_raw = pd.read_excel(path_faktur, header=8)
        if 'Tanggal' not in df_faktur_raw.columns and 'Tgl Pengajuan' not in df_faktur_raw.columns: df_faktur_raw = pd.read_excel(path_faktur, header=0)
        df_faktur_raw = assign_leasing_faktur(parse_date_cols(df_faktur_raw))
        df_faktur_all = df_faktur_raw.copy()
        df_faktur = df_faktur_raw[df_faktur_raw['Nama Dealer'].isin(daftar_dealer)].reset_index(drop=True) if 'Nama Dealer' in df_faktur_raw.columns else df_faktur_raw.copy()
        df_faktur = assign_koor_and_sales(assign_type_from_lookup(df_faktur, mapping_type_lookup, mapping_type_lookup_nospace, unmapped_types_all), tracker=sales_tanpa_koor)
    except Exception as e: st.error(f'Error Faktur: {e}')

df_nota = None
if path_nota:
    try:
        df_nt = pd.read_excel(path_nota, header=5)
        df_nota = parse_date_cols(pd.read_excel(path_nota, header=0) if not any(k in df_nt.columns for k in ['Nama Dealer', 'Dealer', 'Tanggal']) else df_nt)
        cd = 'Nama Dealer' if 'Nama Dealer' in df_nota.columns else ('Dealer' if 'Dealer' in df_nota.columns else None)
        if cd: df_nota = df_nota[df_nota[cd].isin(daftar_dealer)].reset_index(drop=True)
        df_nota = assign_koor_and_sales(assign_type_from_lookup(df_nota, mapping_type_lookup, mapping_type_lookup_nospace, unmapped_types_all), tracker=sales_tanpa_koor)
    except Exception as e: st.error(f'Error Nota: {e}')

df_database = None
if paths_database:
    l_db = [assign_type_from_lookup(read_single_db_file(p), mapping_type_lookup, mapping_type_lookup_nospace, unmapped_types_all) for p in paths_database]
    l_db = [d for d in l_db if not d.empty]
    if l_db: df_database = assign_koor_and_sales(pd.concat(l_db, ignore_index=True), tracker=sales_tanpa_koor_db)
df_database_alldlr = df_database   # sebelum difilter (untuk rekonsiliasi)
if df_database is not None and not df_database.empty and 'Nama_Dealer_Clean' in df_database.columns and df_database['Nama_Dealer_Clean'].isin(daftar_dealer).any():
    df_database = df_database[df_database['Nama_Dealer_Clean'].isin(daftar_dealer)].reset_index(drop=True)   # KPI & Proses memakai basis data yang sama

def strip_sub_code(v):
    """Buang kode di depan nama sub prospect (mis. '03 - Pameran' / 'EV01: Pameran' -> 'PAMERAN')."""
    t = clean_str(v)
    t2 = re.sub(r'^[\[\(]?[A-Z]{0,5}[-_./]?\d+[A-Z0-9._/-]*[\]\)]?\s*[-–:.)|]\s*', '', t).strip()
    t2 = t2 or re.sub(r'^[\[\(]?[A-Z]{0,5}[-_./]?\d+[A-Z0-9._/-]*[\]\)]?\s+', '', t).strip()
    return t2 or t

def ktp_norm(v):
    if v is None or (not isinstance(v, str) and pd.isna(v)): return ''
    t = str(v).strip()
    if t.endswith('.0'): t = t[:-2]
    t = re.sub(r'\D', '', t)
    return t if len(t) >= 10 else ''

# Kolom STU otomatis di Database: KTP (kolom C Database) dicocokkan dengan KTP kolom I file Faktur -> keterangan 'STU'
if df_database is not None and not df_database.empty:
    df_database['STU'] = ''
    if df_database.shape[1] > 2 and df_faktur_all is not None and not df_faktur_all.empty and df_faktur_all.shape[1] > 8:
        _ktp_fak = set(k for k in df_faktur_all.iloc[:, 8].apply(ktp_norm) if k)
        _ktp_db = df_database.iloc[:, 2].apply(ktp_norm)
        df_database['STU'] = ['STU' if (k and k in _ktp_fak) else '' for k in _ktp_db]

df_spk = None
if path_spk:
    try:
        df_sr = pd.read_csv(path_spk, header=None) if path_spk.lower().endswith('.csv') else pd.read_excel(path_spk, sheet_name=next((s for s in pd.ExcelFile(path_spk).sheet_names if s.strip().upper() == 'SPK'), 0), header=None)
        if df_sr is not None and not df_sr.empty:
            hi = next((r for r in range(min(25, len(df_sr))) if len([v for v in df_sr.iloc[r].values if pd.notna(v)]) >= 4 and any(k in ' '.join(clean_str(v) for v in df_sr.iloc[r].values if pd.notna(v)) for k in ['NAMA DEALER', 'NO TRANSAKSI', 'TGL', 'LEASING', 'STATUS'])), 0)
            df_spk = df_sr.iloc[hi + 1:].copy()
            df_spk.columns = make_unique_columns([str(c).strip() for c in df_sr.iloc[hi].values])
            df_spk = df_spk.dropna(how='all').reset_index(drop=True)
            df_spk['Nama_Dealer_SPK'] = df_spk.iloc[:, 3].apply(lambda x: mapping_dealer_spk.get(clean_str(x), mapping_dealer_spk.get(normalize_dealer_name(x), normalize_dealer_name(x)))) if df_spk.shape[1] > 3 else 'TIDAK DIKETAHUI'
            df_spk = df_spk[df_spk['Nama_Dealer_SPK'].isin(daftar_dealer)].reset_index(drop=True)
            df_spk['Leasing_SPK_Clean'] = df_spk.iloc[:, 16].apply(normalize_leasing_val) if df_spk.shape[1] > 16 else ''
            df_spk['Alasan_Reject_Clean'] = df_spk.iloc[:, 18].apply(lambda x: clean_str(x) if clean_str(x) not in ['', 'NAN', 'NONE', '-'] else 'TANPA KETERANGAN') if df_spk.shape[1] > 18 else 'TANPA KETERANGAN'
            if df_spk.shape[1] > 17:
                df_spk['Status_SPK_Clean'] = df_spk.iloc[:, 17].apply(clean_str)
                df_spk = df_spk[df_spk['Status_SPK_Clean'].isin(['DISETUJUI', 'DITOLAK', 'TERBUKA'])].reset_index(drop=True)
            else: df_spk['Status_SPK_Clean'] = ''
            if df_spk.shape[1] > 5:
                df_spk['Tanggal_Parsed'] = smart_parse_datetime(df_spk.iloc[:, 5])
                df_spk['bulan'], df_spk['hari'], df_spk['tahun'] = df_spk['Tanggal_Parsed'].dt.month, df_spk['Tanggal_Parsed'].dt.day, df_spk['Tanggal_Parsed'].dt.year
            df_spk = assign_type_from_lookup(assign_koor_and_sales(df_spk, col_idx_override=25, tracker=sales_tanpa_koor_spk, koor_col_name='Koor_SPK'), mapping_type_lookup, mapping_type_lookup_nospace, unmapped_types_all)
    except Exception as e: st.error(f'Error SPK: {e}')

# Lengkapi mapping_salesman_dealer dan mapping_koor_dealer dari seluruh sumber data (Database, Faktur, Nota, SPK)
mapping_koor_dealer = {'ADI MOKHTAR': 'SIP BESUKI', 'COUNTER BESUKI': 'SIP BESUKI'}
for _df_s, _dlr_c, _kr_c in [
    (df_database, 'Nama_Dealer_Clean', 'Koor'),
    (df_faktur, 'Nama Dealer', 'Koor'),
    (df_nota, 'Nama Dealer' if (df_nota is not None and 'Nama Dealer' in df_nota.columns) else 'Dealer', 'Koor'),
    (df_spk, 'Nama_Dealer_SPK', 'Koor_SPK')
]:
    if _df_s is not None and not _df_s.empty and _dlr_c in _df_s.columns:
        if 'Salesman_Clean' in _df_s.columns:
            _sub_sm = _df_s[_df_s['Salesman_Clean'].notna() & _df_s[_dlr_c].isin(daftar_dealer)][['Salesman_Clean', _dlr_c]].drop_duplicates()
            for _, _r in _sub_sm.iterrows():
                _sm_n, _dl_n = clean_str(_r['Salesman_Clean']), clean_str(_r[_dlr_c])
                if _sm_n and _dl_n in daftar_dealer and _sm_n not in mapping_salesman_dealer:
                    mapping_salesman_dealer[_sm_n] = _dl_n
        if _kr_c in _df_s.columns:
            _sub_kr = _df_s[_df_s[_kr_c].notna() & (_df_s[_kr_c] != 'LAIN-LAIN') & _df_s[_dlr_c].isin(daftar_dealer)][[_kr_c, _dlr_c]].drop_duplicates()
            for _, _r in _sub_kr.iterrows():
                _kr_n, _dl_n = clean_str(_r[_kr_c]), clean_str(_r[_dlr_c])
                if _kr_n and _dl_n in daftar_dealer and _kr_n not in mapping_koor_dealer:
                    mapping_koor_dealer[_kr_n] = _dl_n

for _sm_k, _kr_v in mapping_salesman_koor.items():
    _kr_c = clean_str(_kr_v)
    if _sm_k not in mapping_salesman_dealer:
        if _kr_c in mapping_koor_dealer:
            mapping_salesman_dealer[_sm_k] = mapping_koor_dealer[_kr_c]
        else:
            _norm_k = normalize_dealer_name(_kr_c)
            if _norm_k in daftar_dealer:
                mapping_salesman_dealer[_sm_k] = _norm_k

df_rating = None
if paths_rating:
    l_rt = [assign_type_from_lookup(assign_rating_dealer_and_koor(read_single_rating_file(p), mapping_dealer_spk), mapping_type_lookup, mapping_type_lookup_nospace, unmapped_types_all) for p in paths_rating]
    l_rt = [d for d in l_rt if not d.empty]
    if l_rt: df_rating = pd.concat(l_rt, ignore_index=True)

def detect_customer_col(df, is_rating=False):
    if df is None or df.empty: return None
    cu = [str(c).strip().upper() for c in df.columns]
    exact_cands = [
        'NAMA KONSUMEN', 'NAMA CUSTOMER', 'CUSTOMER NAME', 'NAMA PELANGGAN',
        'NAMA PEMILIK', 'NAMA STNK', 'NAMA BPKB', 'NAMA PEMBELI', 'KONSUMEN',
        'CUSTOMER', 'PEMBELI', 'PEMILIK', 'NAMA USER', 'USER NAME'
    ]
    for cand in exact_cands:
        if cand in cu:
            return df.columns[cu.index(cand)]
    ign_kw = {'DEALER', 'CABANG', 'OUTLET', 'SALES', 'PEGAWAI', 'PRAMUNIAGA', 'TEKNISI', 'TYPE', 'TIPE', 'BARANG', 'UNIT', 'FINCOY', 'LEASING', 'KOOR', 'KATEGORI', 'FILE', 'POINT', 'STATUS'}
    for i, c_str in enumerate(cu):
        if not any(kw in c_str for kw in ign_kw) and any(k in c_str for k in ['KONSUMEN', 'CUSTOMER', 'PELANGGAN', 'PEMBELI', 'PEMILIK', 'STNK', 'NAMA']):
            return df.columns[i]
    if is_rating and df.shape[1] > 4:
        return df.columns[4]
    return None

def detect_phone_col(df):
    if df is None or df.empty: return None
    cu = [str(c).strip().upper() for c in df.columns]
    for cand in ['NO HP', 'NO. HP', 'NO TELP', 'NO. TELP', 'TELEPON', 'TELP', 'HP', 'HANDPHONE', 'NO HANDPHONE', 'PHONE', 'MOBILE', 'MOBILE PHONE', 'PHONE NO', 'CONTACT', 'WA', 'NO WA']:
        if cand in cu:
            return df.columns[cu.index(cand)]
    for i, c_str in enumerate(cu):
        if any(k in c_str for k in ['HP', 'TELP', 'TELEPON', 'PHONE', 'MOBILE', 'WA', 'KONTAK']) and 'KODE' not in c_str:
            return df.columns[i]
    return None

def detect_raw_type_col(df):
    if df is None or df.empty: return None
    tc = detect_type_col(df, mapping_type_lookup, mapping_type_lookup_nospace)
    if tc is not None: return tc
    cu = [str(c).strip().upper() for c in df.columns]
    for cand in ['NAMA BARANG', 'DESKRIPSI UNIT', 'TIPE MOTOR', 'TYPE MOTOR', 'NAMA TYPE', 'NAMA TIPE', 'TYPE', 'TIPE', 'MODEL', 'UNIT']:
        if cand in cu: return df.columns[cu.index(cand)]
    return None

def assign_faktur_rating_status(df_f, df_rt):
    if df_f is None or df_f.empty:
        if df_f is not None:
            df_f['Nama_Konsumen_Clean'] = ''
            df_f['No_HP_Clean'] = '-'
            df_f['Tipe_Unit_Display'] = '-'
            df_f['Status_Registrasi_Rating'] = 'BELUM REGISTRASI'
        return df_f

    cust_col_f = detect_customer_col(df_f, is_rating=False)
    if cust_col_f is not None:
        s_cf = df_f[cust_col_f].iloc[:, 0] if isinstance(df_f[cust_col_f], pd.DataFrame) else df_f[cust_col_f]
        df_f['Nama_Konsumen_Clean'] = s_cf.apply(clean_str)
    else:
        df_f['Nama_Konsumen_Clean'] = ''

    hp_col_f = detect_phone_col(df_f)
    if hp_col_f is not None:
        s_hp = df_f[hp_col_f].iloc[:, 0] if isinstance(df_f[hp_col_f], pd.DataFrame) else df_f[hp_col_f]
        df_f['No_HP_Clean'] = s_hp.apply(lambda x: clean_str(x)[:-2] if clean_str(x).endswith('.0') else (clean_str(x) or '-'))
    else:
        df_f['No_HP_Clean'] = '-'

    raw_tc = detect_raw_type_col(df_f)
    if raw_tc is not None:
        s_rt = df_f[raw_tc].iloc[:, 0] if isinstance(df_f[raw_tc], pd.DataFrame) else df_f[raw_tc]
        df_f['Tipe_Unit_Display'] = s_rt.apply(lambda x: clean_str(x) or '-')
    else:
        df_f['Tipe_Unit_Display'] = df_f['Type_Clean'] if 'Type_Clean' in df_f.columns else '-'

    rt_names_exact = set()
    rt_names_alnum = set()
    if df_rt is not None and not df_rt.empty:
        cust_col_rt = detect_customer_col(df_rt, is_rating=True)
        cols_to_scan = [cust_col_rt] if cust_col_rt is not None else []
        # Tambahkan juga pengecekan pada seluruh kolom teks di file rating jika nama konsumen berada di kolom lain
        for cn in df_rt.columns:
            if cn not in cols_to_scan and str(cn).upper() not in {'NAMA_DEALER_CLEAN', 'SALESMAN_CLEAN', 'KOOR', 'KODE_DEALER_CLEAN', 'TANGGAL_PARSED', 'BULAN', 'HARI', 'TAHUN', 'TYPE_CLEAN'}:
                cols_to_scan.append(cn)
        if cust_col_rt is not None:
            # Utamakan kolom konsumen utama terlebih dahulu
            s_cr = df_rt[cust_col_rt].iloc[:, 0] if isinstance(df_rt[cust_col_rt], pd.DataFrame) else df_rt[cust_col_rt]
            for val in s_cr.dropna():
                c_v = clean_str(val)
                if c_v and c_v not in {'NAN', 'NONE', '-', 'CUSTOMER NAME', 'NAMA KONSUMEN', 'NAMA CUSTOMER'}:
                    rt_names_exact.add(c_v)
                    a_v = alnum_str(c_v)
                    if len(a_v) >= 3: rt_names_alnum.add(a_v)
        # Jika hasil kecocokan dengan kolom utama masih 0, scan kolom potensial lainnya di df_rt
        f_names_sample = {x for x in df_f['Nama_Konsumen_Clean'].unique() if x and len(x) >= 3}
        if f_names_sample and not f_names_sample.intersection(rt_names_exact):
            for cn in cols_to_scan:
                s_c = df_rt[cn].iloc[:, 0] if isinstance(df_rt[cn], pd.DataFrame) else df_rt[cn]
                cand_set = {clean_str(v) for v in s_c.dropna() if clean_str(v)}
                if f_names_sample.intersection(cand_set):
                    for c_v in cand_set:
                        rt_names_exact.add(c_v)
                        a_v = alnum_str(c_v)
                        if len(a_v) >= 3: rt_names_alnum.add(a_v)

    def check_reg_status(nm):
        c_nm = clean_str(nm)
        if not c_nm or c_nm in {'NAN', 'NONE', '-', ''}:
            return 'BELUM REGISTRASI'
        if c_nm in rt_names_exact:
            return 'SUDAH REGISTRASI'
        a_nm = alnum_str(c_nm)
        if a_nm and len(a_nm) >= 3 and a_nm in rt_names_alnum:
            return 'SUDAH REGISTRASI'
        return 'BELUM REGISTRASI'

    df_f['Status_Registrasi_Rating'] = df_f['Nama_Konsumen_Clean'].apply(check_reg_status)
    return df_f

if df_faktur is not None:
    df_faktur = assign_faktur_rating_status(df_faktur, df_rating)
if df_faktur_all is not None:
    df_faktur_all = assign_faktur_rating_status(df_faktur_all, df_rating)


def get_unmapped_salesman_details():
    details = {}
    def collect_from_df(df_src, koor_col, dlr_col, src_label):
        if df_src is None or df_src.empty or 'Salesman_Clean' not in df_src.columns: return
        sub = df_src[df_src['Salesman_Clean'].notna() & (df_src[koor_col] == 'LAIN-LAIN')] if koor_col in df_src.columns else df_src[df_src['Salesman_Clean'].notna()]
        for _, r in sub.iterrows():
            sm = clean_str(r.get('Salesman_Clean', ''))
            if not sm or sm in ['NAN', 'NONE', 'TOTAL', 'JUMLAH', '-']: continue
            dlr = clean_str(r.get(dlr_col, '')) if dlr_col in df_src.columns else ''
            if sm not in details: details[sm] = {'dealers': set(), 'sources': set()}
            if dlr and dlr not in ['NAN', 'NONE']: details[sm]['dealers'].add(dlr)
            details[sm]['sources'].add(src_label)
    collect_from_df(df_database, 'Koor', 'Nama_Dealer_Clean', 'Database')
    collect_from_df(df_faktur, 'Koor', 'Nama Dealer', 'Faktur')
    cd_nt = 'Nama Dealer' if (df_nota is not None and 'Nama Dealer' in df_nota.columns) else 'Dealer'
    collect_from_df(df_nota, 'Koor', cd_nt, 'Nota')
    collect_from_df(df_spk, 'Koor_SPK', 'Nama_Dealer_SPK', 'SPK')
    collect_from_df(df_rating, 'Koor', 'Nama_Dealer_Clean', 'Rating')
    return details

def render_unmapped_salesman_alert(key_prefix='sales'):
    unmapped_info = get_unmapped_salesman_details()
    if not unmapped_info:
        st.markdown('<div class="unmapped-sales-box" style="border-left-color:#00FF66; background:linear-gradient(90deg, rgba(0,255,102,0.10) 0%, rgba(14,17,23,0.96) 100%);">✅ <b>Status Data Lookup Koordinator:</b> Seluruh nama salesman pada Database, Faktur, Nota, dan SPK sudah memiliki Koordinator.</div>', unsafe_allow_html=True)
        return
    sorted_names = sorted(unmapped_info.keys())
    db_only_names = [nm for nm in sorted_names if 'Database' in unmapped_info[nm]['sources']]
    badges_html = []
    rows_detail = []
    for nm in sorted_names:
        dlrs = ', '.join(sorted(unmapped_info[nm]['dealers'])) or '-'
        srcs = ', '.join(sorted(unmapped_info[nm]['sources']))
        badges_html.append(f'<span class="unmapped-badge">{nm} <span style="color:#94A3B8;font-weight:400;">({dlrs} | {srcs})</span></span>')
        rows_detail.append({'NAMA SALESMAN (BELUM ADA KOORDINATOR)': nm, 'DEALER': dlrs, 'SUMBER DATA': srcs})
    st.markdown(f"""<div class="unmapped-sales-box">
        <div>⚠️ <b>Ditemukan {len(sorted_names)} Nama Salesman Belum Memiliki Koordinator di Data Lookup ({len(db_only_names)} dari Database):</b></div>
        <div style="margin-top:6px;">{''.join(badges_html)}</div>
    </div>""", unsafe_allow_html=True)
    with st.expander(f"📋 Klik untuk Salin / Lihat Tabel {len(sorted_names)} Nama Salesman Tanpa Koordinator (Untuk Update Data Lookup)"):
        c_u1, c_u2 = st.columns([2, 1])
        with c_u1:
            st.dataframe(pd.DataFrame(rows_detail), hide_index=True, use_container_width=True)
        with c_u2:
            st.caption("Salin daftar nama di bawah ini langsung ke kolom Salesman di Excel **Data Lookup**:")
            st.code('\n'.join(sorted_names), language='text')

today_wib = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)).date()
current_month, current_year = today_wib.month, today_wib.year
for dc in [df_faktur_all, df_faktur, df_nota, df_spk, df_database]:
    if dc is not None and not dc.empty and 'bulan' in dc.columns and dc['bulan'].notna().any():
        current_year = int(dc['tahun'].dropna().max())
        current_month = int(dc[dc['tahun'] == current_year]['bulan'].dropna().max())
        break
last_month, last_month_year = (current_month - 1, current_year) if current_month > 1 else (12, current_year - 1)
NAMA_BULAN_ID = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
nama_bulan_curr = NAMA_BULAN_ID.get(current_month, 'Oktober')
periode_bulan_tahun = f'{nama_bulan_curr} {current_year}'

max_day_in_month = pycal.monthrange(current_year, current_month)[1]
default_day_today = min(today_wib.day, max_day_in_month)
st.sidebar.markdown('### 📅 Periode Analisa')
tgl_kal_pilihan = st.sidebar.date_input('Pilih Tanggal Akhir Periode (Kalender):', value=datetime.date(current_year, current_month, default_day_today), min_value=datetime.date(current_year, current_month, 1), max_value=datetime.date(current_year, current_month, max_day_in_month), format='DD/MM/YYYY')
tanggal_akhir = int(tgl_kal_pilihan[-1].day) if isinstance(tgl_kal_pilihan, (tuple, list)) and len(tgl_kal_pilihan) > 0 else (int(tgl_kal_pilihan.day) if hasattr(tgl_kal_pilihan, 'day') else default_day_today)

target_persen_harian = tabel_target_harian.get(tanggal_akhir, 0.0)
persen_desimal = target_persen_harian / 100.0
col_name_pct = f'{target_persen_harian:.0f}%' if target_persen_harian.is_integer() else f'{target_persen_harian}%'
LIBUR_FILE = 'libur_nasional.json'
DEFAULT_LIBUR_NASIONAL = ['2026-01-01', '2026-01-16', '2026-02-17', '2026-03-19', '2026-03-21', '2026-03-22', '2026-04-03', '2026-04-05', '2026-05-01', '2026-05-14', '2026-05-27', '2026-05-31', '2026-06-01', '2026-06-16', '2026-08-17', '2026-08-25', '2026-12-25']
def _parse_libur(lst):
    out = set()
    for x in lst:
        try: out.add(datetime.date.fromisoformat(str(x).strip()))
        except Exception: pass
    return out
_libur_saved = load_json(LIBUR_FILE)
LIBUR_SET = _parse_libur(_libur_saved['dates'] if isinstance(_libur_saved, dict) and 'dates' in _libur_saved else DEFAULT_LIBUR_NASIONAL)
def is_workday_date(dt): return dt.weekday() != 6 and dt not in LIBUR_SET   # Minggu & libur nasional bukan hari aktif
def is_workday_day(d_n): return is_workday_date(datetime.date(current_year, current_month, d_n))
WORKDAYS_UPTO = [d_n for d_n in range(1, tanggal_akhir + 1) if is_workday_day(d_n)]
SISA_HARI_KERJA = sum(1 for d_n in range(tanggal_akhir + 1, max_day_in_month + 1) if is_workday_day(d_n))
hari_aktif = max(1, len(WORKDAYS_UPTO))
st.sidebar.markdown(f'<div class="target-ideal-caption">🎯 Target Ideal Tgl {tanggal_akhir}: {col_name_pct}</div>', unsafe_allow_html=True)

# ===================== ALARM HARIAN — hanya notifikasi popup tepat di jam alarm (tanpa checklist / rekap / alarm susulan) =====================
DEFAULT_REMINDERS = [('briefing', 'Sudah Kirim Laporan Briefing Pagi ?', '08:30'), ('rekrutmen', 'Sudah Kirim Laporan Rekrutmen ?', '11:00'),
                     ('visit', 'Sudah Kirim Laporan Visit Market ?', '13:00'), ('daily', 'Sudah Kirim Laporan Daily Report ?', '16:00')]
_now_wib = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
_today_s = _now_wib.date().isoformat()
_rm_pending = [{'key': k_r, 'label': lbl_r, 'time': t_r, 'minutes': int(t_r[:2]) * 60 + int(t_r[3:5])} for k_r, lbl_r, t_r in DEFAULT_REMINDERS] if is_workday_date(_now_wib.date()) else []

# popup realtime di browser (hanya saat aplikasi terbuka): muncul sekali tepat di menit jam alarm; jika dibuka setelah jam alarm, tidak ada yang dimunculkan
_rm_js = """<script>
(function(){ try {
  const P = window.parent, D = P.document, items = __ITEMS__, today = '__TODAY__';
  if (P.__bushidoAlarmTimer) P.clearInterval(P.__bushidoAlarmTimer);
  P.__bushidoFired = P.__bushidoFired || {};
  function holder(){ let b = D.getElementById('bushido-alarm-box'); if (!b) { b = D.createElement('div'); b.id = 'bushido-alarm-box'; b.style.cssText = 'position:fixed;top:70px;right:18px;z-index:99999;display:flex;flex-direction:column;gap:10px;max-width:340px;'; D.body.appendChild(b); } return b; }
  function beep(){ try { const A = new (P.AudioContext || P.webkitAudioContext)(), o = A.createOscillator(), g = A.createGain(); o.connect(g); g.connect(A.destination); o.frequency.value = 880; g.gain.value = 0.08; o.start(); setTimeout(() => { o.stop(); A.close(); }, 450); } catch(e) {} }
  function show(it){
    const d = D.createElement('div'); d.className = 'bushido-alarm-pop'; d.dataset.key = it.key;
    d.style.cssText = 'background:#1E1B4B;color:#fff;border:2px solid #FFEA00;border-left:6px solid #FF007F;border-radius:10px;padding:12px 14px;font-family:sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.5);';
    d.innerHTML = '<div style=\"font-weight:800;font-size:15px;\">🔔 ' + it.label + '</div><div style=\"font-size:12px;margin-top:4px;color:#CBD5E1;\">Jadwal ' + it.time + ' WIB</div><div style=\"margin-top:8px;display:flex;gap:8px;\"><button class=\"x\" style=\"cursor:pointer;\">Tutup</button></div>';
    d.querySelector('.x').onclick = () => d.remove();
    holder().appendChild(d); beep();
    try { if (P.Notification && P.Notification.permission === 'granted') new P.Notification(it.label, { body: 'Jadwal ' + it.time + ' WIB' }); } catch(e) {}
  }
  function check(){
    const n = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Jakarta' })), mins = n.getHours() * 60 + n.getMinutes();
    items.forEach(it => { const k = today + it.key; if (mins === it.minutes && !P.__bushidoFired[k]) { P.__bushidoFired[k] = true; show(it); } });
  }
  check(); P.__bushidoAlarmTimer = P.setInterval(check, 10000);
} catch(e) {} })();
</script>"""
with st.sidebar: components.html(_rm_js.replace('__ITEMS__', json.dumps(_rm_pending)).replace('__TODAY__', _today_s), height=0)

with st.sidebar.expander('📆 Hari Libur Nasional', expanded=False):
    st.caption('Hari Minggu & tanggal libur di bawah ini tidak dihitung sebagai hari aktif (AVG, AVG 3/7, Forecast).')
    _lib_txt = st.text_area('Tanggal libur (YYYY-MM-DD, satu per baris)', value='\n'.join(sorted(d_l.isoformat() for d_l in LIBUR_SET)), height=200, key='libur_txt')
    if st.button('💾 Simpan Hari Libur', key='libur_save', use_container_width=True):
        save_json({'dates': sorted(d_l.isoformat() for d_l in _parse_libur(re.split(r'[\s,;]+', _lib_txt)))}, LIBUR_FILE); st.rerun()

def nota_metrics(df_n):
    """AVG NOTA, AVG 7, AVG 3 (rata-rata per HARI KERJA: Minggu & libur nasional tidak dihitung) + forecast s.d akhir bulan."""
    last7, last3 = set(WORKDAYS_UPTO[-7:]), set(WORKDAYS_UPTO[-3:])
    n_all = len(df_n) if df_n is not None else 0
    ok = df_n is not None and not df_n.empty and 'hari' in df_n.columns
    n7 = int(df_n['hari'].isin(last7).sum()) if ok else 0
    n3 = int(df_n['hari'].isin(last3).sum()) if ok else 0
    d7, d3 = max(1, len(last7)), max(1, len(last3))
    avg, avg7, avg3 = n_all / hari_aktif, n7 / d7, n3 / d3
    return {'n': n_all, 'n7': n7, 'n3': n3, 'd7': d7, 'd3': d3, 'avg': avg, 'avg7': avg7, 'avg3': avg3,
            'f_nota': int(round(n_all + avg * SISA_HARI_KERJA)), 'f7': int(round(n_all + avg7 * SISA_HARI_KERJA)), 'f3': int(round(n_all + avg3 * SISA_HARI_KERJA))}

def calc_sales_row(name_label, name_col, targ, df_f_c, df_f_l, df_n_c, df_n_t):
    ideal, stu, stulm, nota, today = round(targ * persen_desimal), len(df_f_c), len(df_f_l), len(df_n_c), len(df_n_t)
    forc, pct = (round(nota / persen_desimal) if persen_desimal > 0 else 0), ((stu / targ * 100.0) if targ > 0 else 0.0)
    _nm = nota_metrics(df_n_c)
    return {name_col: name_label, 'TARGET': targ, 'IDEAL': ideal, 'STU': stu, 'NOTA': nota, 'TODAY': today, col_name_pct: f'{pct:.2f}%', 'GAP TG': stu - targ, 'STU LM': stulm, '% LM': f'{(stu / stulm * 100.0):.2f}%' if stulm > 0 else '0.00%', 'GAP LM': stu - stulm, 'FORC': forc, 'F. NOTA': _nm['f_nota'], 'FORC 7': _nm['f7'], 'FORC 3': _nm['f3'], '_nota': nota, '_ideal': ideal, '_pct': pct}

def calc_proses_row(name_label, name_col, df_db_sub, stu_cnt, df_n_sub=None):
    db_c = len(df_db_sub)
    hot_c = len(df_db_sub[df_db_sub['Data_Type_Clean'] == 'DEAL PROSPECT']) if (not df_db_sub.empty and 'Data_Type_Clean' in df_db_sub.columns) else 0
    mp_c = int(df_db_sub['Salesman_Clean'].dropna().nunique()) if (not df_db_sub.empty and 'Salesman_Clean' in df_db_sub.columns) else 0
    avg_db, db_q, stu_p = ((db_c / mp_c / hari_aktif) if mp_c > 0 else 0.0), ((hot_c / db_c * 100.0) if db_c > 0 else 0.0), ((stu_cnt / db_c * 100.0) if db_c > 0 else 0.0)
    _nm = nota_metrics(df_n_sub)
    return {name_col: name_label, 'JML MP': mp_c, 'AVG DB': f'{avg_db:.2f}', 'DB': db_c, 'HOT': hot_c, 'DB Q': f'{db_q:.2f}%', 'STU': stu_cnt, 'STU%': f'{stu_p:.2f}%', 'AVG NOTA': f"{_nm['avg']:.2f}", 'AVG 7': f"{_nm['avg7']:.2f}", 'AVG 3': f"{_nm['avg3']:.2f}", '_stu_pct': stu_p}

def calc_leasing_row(label_nama, df_c, df_l, name_col):
    spk_c, spk_l = len(df_c), len(df_l)
    acc = len(df_c[df_c['Status_SPK_Clean'] == 'DISETUJUI']) if (not df_c.empty and 'Status_SPK_Clean' in df_c.columns) else 0
    rej = len(df_c[df_c['Status_SPK_Clean'] == 'DITOLAK']) if (not df_c.empty and 'Status_SPK_Clean' in df_c.columns) else 0
    opn = len(df_c[df_c['Status_SPK_Clean'] == 'TERBUKA']) if (not df_c.empty and 'Status_SPK_Clean' in df_c.columns) else 0
    grw, acc_p = ((spk_c / spk_l * 100.0) if spk_l > 0 else 0.0), ((acc / (acc + rej) * 100.0) if (acc + rej) > 0 else 0.0)
    r = {name_col: label_nama, 'SPK': spk_c, 'SPK LM': spk_l, 'GROWTH': f'{grw:.2f}%', 'ACC%': f'{acc_p:.2f}%', 'TERBUKA': opn, '_acc_val': acc_p, '_spk_val': spk_c, '_spk_lm_val': spk_l}
    for lsg in ['BAF', 'ADIRA', 'SOF', 'IMFI']:
        sub_l = df_c[df_c['Leasing_SPK_Clean'] == lsg] if (not df_c.empty and 'Leasing_SPK_Clean' in df_c.columns) else pd.DataFrame()
        la, lr = (len(sub_l[sub_l['Status_SPK_Clean'] == 'DISETUJUI']) if not sub_l.empty else 0), (len(sub_l[sub_l['Status_SPK_Clean'] == 'DITOLAK']) if not sub_l.empty else 0)
        r[lsg], r[f'%{lsg}'] = len(sub_l), f'{(la / (la + lr) * 100.0):.2f}%' if (la + lr) > 0 else '0.00%'
    return r

def build_type_table(df_fc, df_fl, df_dbc, df_spkc, filter_col_vals, col_headers_name, tot_label='TOTAL', sort_by_growth=True):
    lsg_list, rows, t_acc, t_rej = ['BAF', 'ADIRA', 'SOF'], [], 0, 0
    t_lf, t_la, t_lr = {l: 0 for l in lsg_list}, {l: 0 for l in lsg_list}, {l: 0 for l in lsg_list}
    for item_val, f_col_f, f_col_db, f_col_spk in filter_col_vals:
        sf_c = df_fc[df_fc[f_col_f] == item_val] if (not df_fc.empty and f_col_f in df_fc.columns) else pd.DataFrame()
        sf_l = df_fl[df_fl[f_col_f] == item_val] if (not df_fl.empty and f_col_f in df_fl.columns) else pd.DataFrame()
        sdb = df_dbc[df_dbc[f_col_db] == item_val] if (not df_dbc.empty and f_col_db in df_dbc.columns) else pd.DataFrame()
        sspk = df_spkc[df_spkc[f_col_spk] == item_val] if (not df_spkc.empty and f_col_spk in df_spkc.columns) else pd.DataFrame()
        stu, stulm, db_v, spk_v = len(sf_c), len(sf_l), len(sdb), len(sspk)
        hot_v = len(sdb[sdb['Data_Type_Clean'] == 'DEAL PROSPECT']) if (not sdb.empty and 'Data_Type_Clean' in sdb.columns) else 0
        acc_v = len(sspk[sspk['Status_SPK_Clean'] == 'DISETUJUI']) if (not sspk.empty and 'Status_SPK_Clean' in sspk.columns) else 0
        rej_v = len(sspk[sspk['Status_SPK_Clean'] == 'DITOLAK']) if (not sspk.empty and 'Status_SPK_Clean' in sspk.columns) else 0
        t_acc += acc_v; t_rej += rej_v
        grw, dbq, accp, stup = ((stu / stulm * 100.0) if stulm > 0 else 0.0), ((hot_v / db_v * 100.0) if db_v > 0 else 0.0), ((acc_v / (acc_v + rej_v) * 100.0) if (acc_v + rej_v) > 0 else 0.0), ((stu / db_v * 100.0) if db_v > 0 else 0.0)
        r = {col_headers_name: item_val, 'STU': stu, 'STU LM': stulm, 'GROWTH': f'{grw:.2f}%', 'DB': db_v, 'HOT': hot_v, 'DB Q': f'{dbq:.2f}%', 'SPK': spk_v, 'ACC%': f'{accp:.2f}%', 'STU%': f'{stup:.2f}%', '_stu_val': stu, '_growth_val': grw}
        for l in lsg_list:
            fcnt = len(sf_c[sf_c['Leasing_Faktur_Clean'] == l]) if (not sf_c.empty and 'Leasing_Faktur_Clean' in sf_c.columns) else 0
            t_lf[l] += fcnt
            sl = sspk[sspk['Leasing_SPK_Clean'] == l] if (not sspk.empty and 'Leasing_SPK_Clean' in sspk.columns) else pd.DataFrame()
            la, lr = (len(sl[sl['Status_SPK_Clean'] == 'DISETUJUI']) if not sl.empty else 0), (len(sl[sl['Status_SPK_Clean'] == 'DITOLAK']) if not sl.empty else 0)
            t_la[l] += la; t_lr[l] += lr
            r[l], r[f'%{l}'] = fcnt, f'{(la / (la + lr) * 100.0):.2f}%' if (la + lr) > 0 else '0.00%'
            r[f'STU {l}'] = fcnt
        r['STU CASH'] = len(sf_c[sf_c['Leasing_Faktur_Clean'] == 'CASH']) if (not sf_c.empty and 'Leasing_Faktur_Clean' in sf_c.columns) else 0
        rows.append(r)
    if not rows: return pd.DataFrame(), pd.DataFrame(), {}
    df_it = pd.DataFrame(rows).sort_values(by=(['_growth_val', '_stu_val'] if sort_by_growth else ['_stu_val', 'DB']), ascending=([True, True] if sort_by_growth else [False, False])).reset_index(drop=True)
    ts, tsl, tdb, thot, tspk = int(df_it['STU'].sum()), int(df_it['STU LM'].sum()), int(df_it['DB'].sum()), int(df_it['HOT'].sum()), int(df_it['SPK'].sum())
    tgrw, tdbq, taccp, tstup = ((ts / tsl * 100.0) if tsl > 0 else 0.0), ((thot / tdb * 100.0) if tdb > 0 else 0.0), ((t_acc / (t_acc + t_rej) * 100.0) if (t_acc + t_rej) > 0 else 0.0), ((ts / tdb * 100.0) if tdb > 0 else 0.0)
    tot_r = {col_headers_name: tot_label, 'STU': ts, 'STU LM': tsl, 'GROWTH': f'{tgrw:.2f}%', 'DB': tdb, 'HOT': thot, 'DB Q': f'{tdbq:.2f}%', 'SPK': tspk, 'ACC%': f'{taccp:.2f}%', 'STU%': f'{tstup:.2f}%', '_stu_val': ts, '_growth_val': tgrw}
    for l in lsg_list: tot_r[l], tot_r[f'%{l}'] = t_lf[l], f'{(t_la[l] / (t_la[l] + t_lr[l]) * 100.0):.2f}%' if (t_la[l] + t_lr[l]) > 0 else '0.00%'
    for l in lsg_list: tot_r[f'STU {l}'] = t_lf[l]
    tot_r['STU CASH'] = int(df_it['STU CASH'].sum())
    return df_it, pd.concat([df_it, pd.DataFrame([tot_r])], ignore_index=True), tot_r

df_fak_curr_g = df_faktur[(df_faktur['bulan'] == current_month) & (df_faktur['tahun'] == current_year) & (df_faktur['hari'] <= tanggal_akhir)] if (df_faktur is not None and 'bulan' in df_faktur.columns) else pd.DataFrame()
df_fak_lm_g = df_faktur[(df_faktur['bulan'] == last_month) & (df_faktur['tahun'] == last_month_year) & (df_faktur['hari'] <= tanggal_akhir)] if (df_faktur is not None and 'bulan' in df_faktur.columns) else pd.DataFrame()
df_nota_curr_g = df_nota[(df_nota['bulan'] == current_month) & (df_nota['tahun'] == current_year) & (df_nota['hari'] <= tanggal_akhir)] if (df_nota is not None and 'bulan' in df_nota.columns) else pd.DataFrame()
df_nota_tod_g = df_nota[(df_nota['bulan'] == current_month) & (df_nota['tahun'] == current_year) & (df_nota['hari'] == tanggal_akhir)] if (df_nota is not None and 'bulan' in df_nota.columns) else pd.DataFrame()
if df_database is not None and not df_database.empty and 'hari' in df_database.columns and df_database['hari'].notna().any():
    if 'bulan' in df_database.columns and 'tahun' in df_database.columns and ((df_database['bulan'] == current_month) & (df_database['tahun'] == current_year)).any():
        df_db_curr_g = df_database[(df_database['bulan'] == current_month) & (df_database['tahun'] == current_year) & (df_database['hari'] >= 1) & (df_database['hari'] <= tanggal_akhir)]
    else:
        df_db_curr_g = df_database[(df_database['hari'] >= 1) & (df_database['hari'] <= tanggal_akhir)]
else:
    df_db_curr_g = df_database.copy() if df_database is not None else pd.DataFrame()
if df_rating is not None and not df_rating.empty and 'hari' in df_rating.columns and df_rating['hari'].notna().any():
    if 'bulan' in df_rating.columns and 'tahun' in df_rating.columns and ((df_rating['bulan'] == current_month) & (df_rating['tahun'] == current_year)).any():
        df_rating_curr_g = df_rating[(df_rating['bulan'] == current_month) & (df_rating['tahun'] == current_year) & (df_rating['hari'] >= 1) & (df_rating['hari'] <= tanggal_akhir)]
    else:
        df_rating_curr_g = df_rating[(df_rating['hari'] >= 1) & (df_rating['hari'] <= tanggal_akhir)]
else:
    df_rating_curr_g = df_rating.copy() if df_rating is not None else pd.DataFrame()
df_spk_curr_g = df_spk[(df_spk['bulan'] == current_month) & (df_spk['tahun'] == current_year) & (df_spk['hari'] <= tanggal_akhir)] if (df_spk is not None and 'bulan' in df_spk.columns) else pd.DataFrame()
df_spk_lm_g = df_spk[(df_spk['bulan'] == last_month) & (df_spk['tahun'] == last_month_year) & (df_spk['hari'] <= tanggal_akhir)] if (df_spk is not None and 'bulan' in df_spk.columns) else pd.DataFrame()

import math
saved_kpi = load_json(KPI_SAVED_FILE)
saved_td = load_json(TARGET_DEALER_FILE)
saved_tk = load_json(TARGET_KOOR_FILE)
KPI_MANUAL_FILE = 'kpi_dashboard_manual.json'
DEFAULT_T_DB = {'koor': 200, 'counter': 100}   # default T. DB (masih bisa diedit & disimpan di MASTER KPI)
DEFAULT_T_WALKIN = 25                           # default T. Walk In counter (masih bisa diedit & disimpan)

def detect_prospect_type_cols(df):
    """Kolom Prospect Type di file database: cari via nama header (huruf besar/kecil bebas), fallback kolom G (indeks 6)."""
    if df is None or df.empty: return []
    cols = [c for c in df.columns if alnum_str(c).startswith(('PROSPECTTYPE', 'TIPEPROSPECT', 'JENISPROSPECT'))]
    if cols: return cols
    return [df.columns[6]] if df.shape[1] > 6 else []

def count_walkin(df_db_sub):
    """Jumlah baris database dengan Prospect Type (kolom G) = Walk In."""
    cols = detect_prospect_type_cols(df_db_sub)
    if not cols: return 0
    is_walk = pd.Series(False, index=df_db_sub.index)
    for c in cols:
        ser = df_db_sub[c]
        ser = ser.iloc[:, 0] if isinstance(ser, pd.DataFrame) else ser
        is_walk = is_walk | (ser.apply(alnum_str) == 'WALKIN')
    return int(is_walk.sum())

def kpi_entity_dealer(ent):
    """Dealer (dari 7 dealer fokus) tempat koordinator/counter bertugas; None jika di luar 7 dealer fokus."""
    e = clean_str(ent)
    d = mapping_koor_dealer.get(e)
    if d in daftar_dealer: return d
    n = normalize_dealer_name(e)
    return n if n in daftar_dealer else None

_ACTIVE_DB_SM = None
def get_active_db_salesmen():
    """Nama salesman yang masih ada di file Database (acuan MP aktif). Salesman yang sudah tidak ada di Database (resign) tidak dihitung."""
    global _ACTIVE_DB_SM
    if _ACTIVE_DB_SM is None:
        _ACTIVE_DB_SM = set()
        if df_database is not None and not df_database.empty and 'Salesman_Clean' in df_database.columns:
            _ACTIVE_DB_SM = set(clean_str(x) for x in df_database['Salesman_Clean'].dropna().unique() if clean_str(x))
    return _ACTIVE_DB_SM

def is_counter_row_name(nm, *dfs):
    """Counter: lolos is_counter_personnel ATAU di data baris salesman tsb terpetakan ke Koordinator berawalan COUNTER."""
    if is_counter_personnel(nm): return True
    for d_x in dfs:
        for kc in ('Koor', 'Koor_SPK'):
            if d_x is not None and not d_x.empty and kc in d_x.columns and 'Salesman_Clean' in d_x.columns:
                kk = d_x.loc[d_x['Salesman_Clean'] == nm, kc].dropna()
                if not kk.empty and kk.astype(str).str.upper().str.startswith('COUNTER').any(): return True
    return False

def compute_auto_kpi_results(df_f_sub, df_db_sub, df_spk_sub):
    r_stu = len(df_f_sub) if df_f_sub is not None else 0
    if df_f_sub is not None and not df_f_sub.empty and 'Type_Clean' in df_f_sub.columns:
        r_maxi = int(df_f_sub['Type_Clean'].isin(['AT PREMIUM', 'MAXI', 'AT MAXI']).sum())
        r_classy = int((df_f_sub['Type_Clean'] == 'AT CLASSY').sum())
    else:
        r_maxi, r_classy = 0, 0

    mp_set = set()
    for ds in [df_db_sub, df_f_sub, df_spk_sub]:
        if ds is not None and not ds.empty and 'Salesman_Clean' in ds.columns:
            mp_set.update(clean_str(x) for x in ds['Salesman_Clean'].dropna().unique() if clean_str(x) and clean_str(x) not in ['NAN', 'NONE', 'TOTAL'])
    _act = get_active_db_salesmen()
    if _act: mp_set = {m for m in mp_set if m in _act}   # acuan file Database: yang tidak ada di Database (resign) diabaikan
    mp_set = {m for m in mp_set if not is_counter_row_name(m, df_db_sub, df_f_sub, df_spk_sub)}   # counter tidak dihitung sbg QTY Salesman
    r_mp = len(mp_set)

    r_inc = len(df_spk_sub) if df_spk_sub is not None else 0
    acc_c = len(df_spk_sub[df_spk_sub['Status_SPK_Clean'] == 'DISETUJUI']) if (df_spk_sub is not None and not df_spk_sub.empty and 'Status_SPK_Clean' in df_spk_sub.columns) else 0
    rej_c = len(df_spk_sub[df_spk_sub['Status_SPK_Clean'] == 'DITOLAK']) if (df_spk_sub is not None and not df_spk_sub.empty and 'Status_SPK_Clean' in df_spk_sub.columns) else 0
    r_acc_pct = round((acc_c / (acc_c + rej_c) * 100.0), 1) if (acc_c + rej_c) > 0 else 0.0
    return r_stu, r_maxi, r_classy, r_mp, r_inc, r_acc_pct, acc_c, rej_c

_DLR_ROW_CACHE = {}
def get_dealer_master_row(dealer):
    """T./R. MYDR & T./R. G REV dari baris dealer induk di tabel MASTER KPI Dealer (dipakai Koordinator & Counter)."""
    zero = {'T. MYDR': 0, 'R. MYDR': 0, 'T. G REV': 0, 'R. G REV': 0}
    if not dealer or dealer not in daftar_dealer: return zero
    ck = (dealer, json.dumps(saved_kpi.get('dealer', {}).get(dealer, {}), sort_keys=True), tanggal_akhir)
    if ck not in _DLR_ROW_CACHE:
        df_d, _ = build_kpi_section_df([dealer], 'NAMA DEALER', 'dealer', 'dealer')
        _DLR_ROW_CACHE[ck] = zero if (df_d is None or df_d.empty) else {k: safe_int(df_d.iloc[0][k]) for k in zero}
    return _DLR_ROW_CACHE[ck]

def build_kpi_section_df(entity_list, name_col, section_key, filter_mode):
    sec_saved = saved_kpi.get(section_key, {})
    rows = []
    tot_acc_c, tot_rej_c = 0, 0
    for ent in entity_list:
        ent_saved = sec_saved.get(ent, {})
        if filter_mode == 'dealer':
            f_sub = df_fak_curr_g[df_fak_curr_g['Nama Dealer'] == ent] if not df_fak_curr_g.empty else pd.DataFrame()
            db_sub = df_db_curr_g[df_db_curr_g['Nama_Dealer_Clean'] == ent] if not df_db_curr_g.empty else pd.DataFrame()
            spk_sub = df_spk_curr_g[df_spk_curr_g['Nama_Dealer_SPK'] == ent] if not df_spk_curr_g.empty else pd.DataFrame()
            rt_sub = df_rating_curr_g[df_rating_curr_g['Nama_Dealer_Clean'] == ent] if not df_rating_curr_g.empty else pd.DataFrame()
            def_vals = DEFAULT_KPI_DEALER.get(ent, {})
            def_t_stu = safe_int(saved_td.get(ent, def_vals.get('T. STU', 0)))
            def_t_maxi = def_vals.get('T. MAXI', 0)
            def_t_classy = def_vals.get('T. CLASSY', 0)
            def_t_mp = def_vals.get('T. MP', 0)
            def_t_inc = def_vals.get('T. INC', 0)
            def_t_acc = def_vals.get('T. ACC%', 50.0)
        else:
            f_sub = df_fak_curr_g[df_fak_curr_g['Koor'] == ent] if not df_fak_curr_g.empty else pd.DataFrame()
            db_sub = df_db_curr_g[df_db_curr_g['Koor'] == ent] if not df_db_curr_g.empty else pd.DataFrame()
            spk_sub = df_spk_curr_g[df_spk_curr_g['Koor_SPK'] == ent] if not df_spk_curr_g.empty else pd.DataFrame()
            rt_sub = df_rating_curr_g[df_rating_curr_g['Koor'] == ent] if not df_rating_curr_g.empty else pd.DataFrame()
            def_t_stu = get_koor_or_counter_target(ent, saved_tk) or (20 if filter_mode == 'counter' else 25)
            def_t_maxi = 8 if filter_mode == 'counter' else 10
            def_t_classy = 3 if filter_mode == 'counter' else 5
            def_t_mp = 1 if filter_mode == 'counter' else 6
            def_t_inc = 15 if filter_mode == 'counter' else 18
            def_t_acc = 50.0

        r_stu, r_maxi, r_classy, r_mp, r_inc, r_acc_pct, acc_c, rej_c = compute_auto_kpi_results(f_sub, db_sub, spk_sub)
        tot_acc_c += acc_c; tot_rej_c += rej_c

        t_stu = safe_int(ent_saved.get('T. STU', def_t_stu))
        t_maxi = safe_int(ent_saved.get('T. MAXI', def_t_maxi))
        t_classy = safe_int(ent_saved.get('T. CLASSY', def_t_classy))
        t_mp = safe_int(ent_saved.get('T. MP', def_t_mp))
        t_inc = safe_int(ent_saved.get('T. INC', def_t_inc))
        t_acc = safe_float(ent_saved.get('T. ACC%', def_t_acc))
        t_mydr = int(round(r_stu * 0.30))
        r_mydr = len(rt_sub) if (df_rating is not None and not df_rating.empty) else safe_int(ent_saved.get('R. MYDR', 0))
        if filter_mode == 'dealer':
            t_grev = safe_int(ent_saved.get('T. G REV', 0))
            r_grev = safe_int(ent_saved.get('R. G REV', 0))
            extra_cols = {}
        else:
            # MYDR & Google Review koordinator / counter: target & result mengikuti dealer induk (baris dealer di MASTER KPI)
            _dm = get_dealer_master_row(kpi_entity_dealer(ent))
            t_mydr, r_mydr = _dm['T. MYDR'], _dm['R. MYDR']
            t_grev, r_grev = _dm['T. G REV'], _dm['R. G REV']
            # KPI Database (koordinator & counter) dan Walk In (counter) — result dari file database
            extra_cols = {'T. DB': safe_int(ent_saved.get('T. DB', DEFAULT_T_DB[filter_mode])), 'R. DB': len(db_sub), '_dealer': kpi_entity_dealer(ent)}
            if filter_mode == 'counter':
                extra_cols['T. Walk In'] = safe_int(ent_saved.get('T. Walk In', DEFAULT_T_WALKIN))
                extra_cols['R. Walk In'] = count_walkin(db_sub)

        pct_stu = (r_stu / t_stu * 100.0) if t_stu > 0 else 0.0
        rows.append({
            name_col: ent,
            'T. STU': t_stu, 'R. STU': r_stu,
            'T. MAXI': t_maxi, 'R. MAXI': r_maxi,
            'T. CLASSY': t_classy, 'R. CLASSY': r_classy,
            'T. MP': t_mp, 'R. MP': r_mp,
            'T. INC': t_inc, 'R. INC': r_inc,
            'T. ACC%': round(t_acc, 1), 'R. ACC%': round(r_acc_pct, 1),
            'T. MYDR': t_mydr, 'R. MYDR': r_mydr,
            'T. G REV': t_grev, 'R. G REV': r_grev,
            **extra_cols,
            '_pct_stu': pct_stu
        })
    if not rows:
        return pd.DataFrame(), pd.DataFrame()
    df_items = pd.DataFrame(rows).reset_index(drop=True)
    tot_t_acc = round(float(df_items['T. ACC%'].mean()), 1) if not df_items.empty else 50.0
    tot_r_acc = round((tot_acc_c / (tot_acc_c + tot_rej_c) * 100.0), 1) if (tot_acc_c + tot_rej_c) > 0 else 0.0
    tot_t_stu = int(df_items['T. STU'].sum())
    tot_r_stu = int(df_items['R. STU'].sum())
    tot_row = {
        name_col: 'TOTAL',
        'T. STU': tot_t_stu, 'R. STU': tot_r_stu,
        'T. MAXI': int(df_items['T. MAXI'].sum()), 'R. MAXI': int(df_items['R. MAXI'].sum()),
        'T. CLASSY': int(df_items['T. CLASSY'].sum()), 'R. CLASSY': int(df_items['R. CLASSY'].sum()),
        'T. MP': int(df_items['T. MP'].sum()), 'R. MP': int(df_items['R. MP'].sum()),
        'T. INC': int(df_items['T. INC'].sum()), 'R. INC': int(df_items['R. INC'].sum()),
        'T. ACC%': tot_t_acc, 'R. ACC%': tot_r_acc,
        'T. MYDR': int(df_items['T. MYDR'].sum()), 'R. MYDR': int(df_items['R. MYDR'].sum()),
        'T. G REV': int(df_items['T. G REV'].sum()), 'R. G REV': int(df_items['R. G REV'].sum()),
        '_pct_stu': (tot_r_stu / tot_t_stu * 100.0) if tot_t_stu > 0 else 0.0
    }
    if filter_mode != 'dealer' and '_dealer' in df_items.columns:
        _ud = df_items.drop_duplicates('_dealer')
        for _c in ['T. MYDR', 'R. MYDR', 'T. G REV', 'R. G REV']: tot_row[_c] = int(_ud[_c].sum())
    for _tc, _rc in [('T. DB', 'R. DB'), ('T. Walk In', 'R. Walk In')]:
        if _tc in df_items.columns:
            tot_row[_tc], tot_row[_rc] = int(df_items[_tc].sum()), int(df_items[_rc].sum())
    return df_items, pd.concat([df_items, pd.DataFrame([tot_row])], ignore_index=True)

# ===================== DASHBOARD KPI: skema poin (sesuai Excel KPI Report) =====================
KPI_CODES = ['STU','MAX','CLS','OPR','SAL','APV','INC','MYM','MYD','GRT','GRV','OPS']
KPI_NAMES = {'STU':'STU Total','MAX':'STU MAXI','CLS':'STU AT Classy','OPR':'Operational Dealer','SAL':'QTY Salesman','APV':'Approval Ratio Total','INC':'Incoming Total','MYM':'My Yamaha Member Point','MYD':'My Yamaha Dealer Rating','GRT':'Google Rating','GRV':'Google Review','OPS':'Operational Supervisor'}
KPI_MIN_ACV = {'STU':0.95,'MAX':0.95,'CLS':0.95,'OPR':0.90,'SAL':0.75,'APV':0.75,'INC':0.75,'MYM':0.75,'MYD':0.75,'GRT':1.0,'GRV':0.75,'OPS':0.90}
KPI_WEIGHT_MDS = {'STU':20,'MAX':10,'CLS':10,'OPR':5,'SAL':10,'APV':5,'INC':9,'MYM':3,'MYD':8,'GRT':5,'GRV':5,'OPS':10}
KPI_WEIGHT_DEALER = {'STU':20,'MAX':10,'CLS':10,'OPR':15,'SAL':10,'APV':5,'INC':9,'MYM':3,'MYD':8,'GRT':5,'GRV':5,'OPS':0}
KPI_SALES_CODES, KPI_PROCESS_CODES = ['STU','MAX','CLS'], ['OPR','SAL','APV','INC','MYM','MYD','GRT','GRV','OPS']
KPI_DEALER_CODES = {'SIP SOBO':'ED05002','SIP PANJI':'EB05002','SIP SRONO':'ED05005','SIP BESUKI':'EB05002-01','SIP SIAGA':'ED05003','SIP GIRI':'ED05006','SIP A. YANI':'ED05001'}
KPI_MANUAL_COLS = ['T. OPR','R. OPR','T. MYM','R. MYM','T. GRT','R. GRT']
DEFAULT_KPI_OPS = {'T. OPS': 44, 'R. OPS': 48}
DEFAULT_KPI_MANUAL = {
    'SIP PANJI':   {'T. OPR':156,'R. OPR':149,'T. MYM':70.0,'R. MYM':97.14,'T. GRT':4.9,'R. GRT':4.9},
    'SIP BESUKI':  {'T. OPR':156,'R. OPR':153,'T. MYM':70.0,'R. MYM':93.75,'T. GRT':5.0,'R. GRT':5.0},
    'SIP A. YANI': {'T. OPR':0,'R. OPR':0,'T. MYM':70.0,'R. MYM':100.0,'T. GRT':4.8,'R. GRT':4.8},
    'SIP SRONO':   {'T. OPR':156,'R. OPR':156,'T. MYM':70.0,'R. MYM':94.74,'T. GRT':4.9,'R. GRT':4.9},
    'SIP SIAGA':   {'T. OPR':156,'R. OPR':156,'T. MYM':70.0,'R. MYM':100.0,'T. GRT':4.9,'R. GRT':4.9},
    'SIP SOBO':    {'T. OPR':156,'R. OPR':156,'T. MYM':70.0,'R. MYM':100.0,'T. GRT':5.0,'R. GRT':5.0},
    'SIP GIRI':    {'T. OPR':156,'R. OPR':156,'T. MYM':70.0,'R. MYM':100.0,'T. GRT':5.0,'R. GRT':5.0},
}

def kpi_point_generic(achv, min_acv, weight, split=0.5):
    try:
        if achv >= 1: return int(weight)
        if min_acv == 0: return int(math.floor(achv * weight + 1e-9))
        if achv >= min_acv:
            base = math.ceil(split * weight - 1e-9)
            extra = math.floor((achv - min_acv) / (1 - min_acv) * math.floor((1 - split) * weight + 1e-9) + 1e-9)
            return int(base + extra)
        return 0
    except Exception:
        return 0

def kpi_point_grt(target, result, weight, scheme):
    if scheme == 'DEALER':
        if target >= 4.8 and result >= 4.8: return weight
        if target >= 4.8 and result < target and result > 0: return int(math.ceil(weight * 0.5 - 1e-9))
        if target < 4.8 and target > 0 and result >= target: return weight
        return 0
    if target >= 4.8 and result < target: return int(math.ceil(weight * 0.5 - 1e-9))
    if result >= 4.8 and target >= 4.8: return weight
    if result < 4.8 and result >= target: return weight
    return 0

def kpi_score_entity(tr, scheme='MDS'):
    weights = KPI_WEIGHT_MDS if scheme == 'MDS' else KPI_WEIGHT_DEALER
    rows = {}
    for c in KPI_CODES:
        t, r = tr.get(c, (0, 0))
        t, r = float(t or 0), float(r or 0)
        achv = (r / t) if t > 0 else 0.0
        w = weights[c]
        if c == 'GRT': pt = kpi_point_grt(t, r, w, scheme)
        else: pt = kpi_point_generic(achv, KPI_MIN_ACV[c], w, 0.75 if (scheme == 'DEALER' and c in KPI_SALES_CODES) else 0.5)
        rows[c] = dict(code=c, name=KPI_NAMES[c], weight=w, min_acv=KPI_MIN_ACV[c], target=t, result=r, achv=achv, point=pt)
    sales = sum(rows[c]['point'] for c in KPI_SALES_CODES)
    process = sum(rows[c]['point'] for c in KPI_PROCESS_CODES)
    return rows, sales, process, sales + process

def kpi_grade(p): return 'D' if p < 60 else ('C' if p < 70 else ('B' if p < 95 else 'A'))
def kpi_note(process): return '' if process >= 45 else ('CUT 30%' if process >= 30 else 'CUT 50%')

def get_dashboard_kpi_inputs():
    """Target & Result per KPI. STU/MAX/CLS/SAL/APV/INC/MYD/GRV dari MASTER KPI; OPR/MYM/GRT/OPS dari input manual."""
    df_it, df_fl = build_kpi_section_df(daftar_dealer, 'NAMA DEALER', 'dealer', 'dealer')
    man = load_json(KPI_MANUAL_FILE)
    man_d, man_ops = man.get('dealers', {}), {**DEFAULT_KPI_OPS, **man.get('ops', {})}
    ops_pair = (safe_float(man_ops.get('T. OPS')), safe_float(man_ops.get('R. OPS')))
    inputs = {}
    def _g(r_x, k_x): return safe_float(r_x[k_x]) if r_x is not None else 0.0
    for d in daftar_dealer:
        mv = {**DEFAULT_KPI_MANUAL.get(d, {}), **man_d.get(d, {})}
        r = df_it[df_it['NAMA DEALER'] == d].iloc[0] if (df_it is not None and not df_it.empty and d in df_it['NAMA DEALER'].values) else None
        inputs[d] = {'STU': (_g(r, 'T. STU'), _g(r, 'R. STU')), 'MAX': (_g(r, 'T. MAXI'), _g(r, 'R. MAXI')), 'CLS': (_g(r, 'T. CLASSY'), _g(r, 'R. CLASSY')),
                     'OPR': (safe_float(mv.get('T. OPR')), safe_float(mv.get('R. OPR'))), 'SAL': (_g(r, 'T. MP'), _g(r, 'R. MP')),
                     'APV': (_g(r, 'T. ACC%') / 100.0, _g(r, 'R. ACC%') / 100.0), 'INC': (_g(r, 'T. INC'), _g(r, 'R. INC')),
                     'MYM': (safe_float(mv.get('T. MYM')) / 100.0, safe_float(mv.get('R. MYM')) / 100.0), 'MYD': (_g(r, 'T. MYDR'), _g(r, 'R. MYDR')),
                     'GRT': (safe_float(mv.get('T. GRT')), safe_float(mv.get('R. GRT'))), 'GRV': (_g(r, 'T. G REV'), _g(r, 'R. G REV')), 'OPS': ops_pair}
    rt = df_fl[df_fl['NAMA DEALER'] == 'TOTAL'].iloc[0] if (df_fl is not None and not df_fl.empty and 'TOTAL' in df_fl['NAMA DEALER'].values) else None
    ds = list(daftar_dealer)
    stu_w = [max(inputs[d]['STU'][1], 0.0) for d in ds]
    def _mean(idx, pos): return sum(inputs[d][idx][pos] for d in ds) / len(ds)
    mym_r = (sum(inputs[d]['MYM'][1] * w for d, w in zip(ds, stu_w)) / sum(stu_w)) if sum(stu_w) > 0 else _mean('MYM', 1)
    inputs['TOTAL BUSHIDO'] = {'STU': (_g(rt, 'T. STU'), _g(rt, 'R. STU')), 'MAX': (_g(rt, 'T. MAXI'), _g(rt, 'R. MAXI')), 'CLS': (_g(rt, 'T. CLASSY'), _g(rt, 'R. CLASSY')),
                     'OPR': (sum(inputs[d]['OPR'][0] for d in ds), sum(inputs[d]['OPR'][1] for d in ds)), 'SAL': (_g(rt, 'T. MP'), _g(rt, 'R. MP')),
                     'APV': (_g(rt, 'T. ACC%') / 100.0, _g(rt, 'R. ACC%') / 100.0), 'INC': (_g(rt, 'T. INC'), _g(rt, 'R. INC')),
                     'MYM': (_mean('MYM', 0), mym_r), 'MYD': (_g(rt, 'T. MYDR'), _g(rt, 'R. MYDR')),
                     'GRT': (_mean('GRT', 0), _mean('GRT', 1)), 'GRV': (_g(rt, 'T. G REV'), _g(rt, 'R. G REV')), 'OPS': ops_pair}
    return inputs

# ===================== DASHBOARD KPI: tampilan HTML =====================
DASH_NAVY, DASH_TEAL = '#0B2A5B', '#1B5E75'
DASH_ABBR = {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MEI',6:'JUN',7:'JUL',8:'AGU',9:'SEP',10:'OKT',11:'NOV',12:'DES'}
DASH_GRADE_COL = {'A':'#00FF66','B':'#00E5FF','C':'#FFEA00','D':'#FF4D8D'}

def _dash_fmt(code, v):
    if code in ('APV', 'MYM', 'YCN'): return f'{v * 100:.1f}%'
    if code == 'GRT': return f'{v:.1f}'
    if code == 'PRD': return f'{v:.2f}'
    return f'{v:,.0f}'

def _dash_box(label, inner, grow=1, minw=70):
    return (f'<div style="flex:{grow} 1 {minw}px;border:1px solid #1E3A8A;border-radius:8px;overflow:hidden;background:#111827;display:flex;flex-direction:column;">'
            f'<div style="background:{DASH_NAVY};color:#fff;font-size:11px;font-weight:800;text-align:center;padding:5px 4px;letter-spacing:.6px;white-space:nowrap;">{label}</div>{inner}</div>')

def _dash_single(value, color, fs=40):
    return f'<div style="color:{color};font-size:{fs}px;font-weight:900;text-align:center;line-height:1.2;padding:4px;display:flex;align-items:center;justify-content:center;min-height:42px;flex:1;">{value}</div>'

def _dash_split(items, fs=26):
    cells = ''.join(f'<div style="flex:1;text-align:center;padding:4px 3px;border-left:1px solid #1E293B;display:flex;flex-direction:column;justify-content:center;align-items:center;"><div style="font-size:10px;font-weight:800;color:#94A3B8;letter-spacing:.5px;">{l}</div><div style="font-size:{fs}px;font-weight:900;color:{c};line-height:1.25;white-space:nowrap;">{v}</div></div>' for l, v, c in items)
    return f'<div style="display:flex;flex:1;">{cells}</div>'

def build_dashboard_kpi_html(sel_name, date_lbl, date_short, rows, s_pt, p_pt, tot_pt, dealer_tbl, hl_dealer, show_concl, scheme_note, codes=None, rank_kind=None):
    codes_l = list(codes) if codes else list(KPI_CODES)
    grade = kpi_grade(tot_pt); gcol = DASH_GRADE_COL.get(grade, '#FFFFFF')
    def _cc(txt): return {'VERY GOOD': '#00FF66', 'GOOD': '#FFEA00', 'NOT GOOD': '#FF4D8D'}.get(txt, '#64748B')
    res_c = ('VERY GOOD' if s_pt >= 38 else ('GOOD' if s_pt >= 20 else 'NOT GOOD')) if show_concl else '—'
    prc_c = ('VERY GOOD' if p_pt >= 57 else ('GOOD' if p_pt >= 45 else 'NOT GOOD')) if show_concl else '—'
    # --- baris atas ---
    banner = (f'<div style="background:linear-gradient(90deg,{DASH_NAVY},#1E3A8A);color:#fff;text-align:center;font-weight:800;font-size:13px;letter-spacing:.5px;padding:8px 10px;border-radius:10px 10px 0 0;">KEY PERFORMANCE INDICATOR REPORT - {date_lbl}</div>'
              f'<div style="background:#0A1F44;color:#fff;text-align:center;font-weight:800;font-size:13px;letter-spacing:.5px;padding:8px 10px;border-radius:0 0 10px 10px;border:1px solid #1E3A8A;">{sel_name}</div>')
    boxes = (_dash_box('GRADE', _dash_single(grade, gcol, 24), 0.6, 70) + _dash_box('POINT', _dash_single(f'{tot_pt}', '#FFFFFF', 24), 0.7, 80)
             + _dash_box('POINT BY CATEGORY', _dash_split([('RESULT', f'{s_pt}', '#FFFFFF'), ('PROCESS', f'{p_pt}', '#FFFFFF')], 18), 1.4, 140)
             + _dash_box('CONCLUTION', _dash_split([('RESULT', res_c, _cc(res_c)), ('PROCESS', prc_c, _cc(prc_c))], 12), 1.8, 170))
    top = (f'<div style="display:flex;gap:14px;flex-wrap:wrap;align-items:stretch;margin-bottom:14px;"><div style="flex:1.5 1 420px;display:flex;flex-direction:column;">{banner}</div>'
           f'<div style="flex:1.25 1 440px;display:flex;gap:8px;flex-wrap:wrap;align-items:stretch;justify-content:center;text-align:center;">{boxes}</div></div>')
    # --- tabel pencapaian (compact: kolom CODE sempit, nama kategori boleh wrap, tanpa scroll horizontal) ---
    th = f'background:{DASH_NAVY};color:#fff;font-size:10.5px;font-weight:800;letter-spacing:.2px;padding:7px 5px;border-bottom:2px solid #1E3A8A;'
    heads = ['CODE', 'PERFORMANCE CATEGORY', 'WEIGHT', 'MIN ACV', 'TARGET', 'RESULT', 'ACHV', 'POINT']
    trs = []
    for c in codes_l:
        r = rows[c]
        if r['weight'] == 0: bg = 'rgba(148,163,184,0.08)'
        elif r['point'] >= r['weight']: bg = 'rgba(0,255,102,0.13)'
        elif r['point'] > 0: bg = 'rgba(255,234,0,0.11)'
        else: bg = 'rgba(255,0,127,0.15)'
        pb = max(0.0, min(r['achv'], 1.0)) * 100
        td = 'padding:6px 5px;border-bottom:1px solid #1E293B;font-size:12.5px;color:#E2E8F0;'
        tgt_txt = '—' if r.get('fixed') else _dash_fmt(c, r['target'])
        res_txt = '—' if r.get('fixed') else _dash_fmt(c, r['result'])
        min_txt = '—' if (r['weight'] == 0 or r.get('no_min')) else f'{r["min_acv"] * 100:.0f}%'
        trs.append(f'<tr style="background:{bg};"><td style="{td}width:34px;max-width:34px;padding:6px 3px;font-weight:800;color:#FFFFFF;">{c}</td><td style="{td}line-height:1.25;">{r["name"]}</td>'
                   f'<td style="{td}text-align:right;">{r["weight"]}</td><td style="{td}text-align:right;">{min_txt}</td>'
                   f'<td style="{td}text-align:right;">{tgt_txt}</td><td style="{td}text-align:right;">{res_txt}</td>'
                   f'<td style="{td}text-align:right;font-weight:800;background:linear-gradient(90deg,rgba(34,197,94,0.55) {pb:.1f}%,transparent {pb:.1f}%);">{r["achv"] * 100:.1f}%</td>'
                   f'<td style="{td}text-align:right;font-weight:900;color:#FFFFFF;">{r["point"]}</td></tr>')
    table_html = (f'<div style="background:{DASH_TEAL};color:#fff;font-size:12px;font-weight:800;letter-spacing:.6px;text-align:center;padding:7px 8px;border-radius:8px 8px 0 0;">ACHIEVEMENT BY PERFORMANCE CATEGORY</div>'
                  f'<div style="overflow-x:auto;border:1px solid #232B3E;border-radius:0 0 8px 8px;background:#0E1117;"><table style="width:100%;border-collapse:collapse;"><thead><tr>'
                  + ''.join(f'<th style="{th}text-align:{"left" if i < 2 else "right"};{"width:34px;padding:7px 3px;" if i == 0 else ""}">{h}</th>' for i, h in enumerate(heads)) + '</tr></thead><tbody>' + ''.join(trs) + '</tbody></table></div>')
    # --- grafik ---
    max_a = max([rows[c]['achv'] for c in codes_l] + [1.0])
    axis = max(1.2, max_a * 1.18)
    mark = 100.0 / axis
    bars = []
    for c in reversed(codes_l):
        r = rows[c]; w = max(0.0, min(r['achv'] / axis, 1.0)) * 100
        bars.append(f'<div style="display:flex;align-items:center;margin:5px 0;"><div style="width:40%;text-align:right;padding-right:10px;font-size:11.5px;color:#CBD5E1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{r["name"]}</div>'
                    f'<div style="flex:1;position:relative;height:20px;"><div style="position:absolute;left:0;top:0;height:20px;width:{w:.1f}%;background:#1F7A9E;border-radius:0 4px 4px 0;"></div>'
                    f'<div style="position:absolute;left:{mark:.1f}%;top:-3px;height:26px;border-left:1px dashed rgba(255,255,255,0.45);"></div>'
                    f'<div style="position:absolute;left:calc({w:.1f}% + 6px);top:2px;font-size:11px;font-style:italic;font-weight:700;color:#E2E8F0;white-space:nowrap;">{r["achv"] * 100:.1f}%</div></div></div>')
    chart_html = (f'<div style="background:{DASH_TEAL};color:#fff;font-size:12px;font-weight:800;letter-spacing:.6px;padding:7px 12px;border-radius:8px 8px 0 0;display:flex;justify-content:space-between;gap:8px;"><span>HISTORICAL PERFORMANCE KPI PER SUB PERFORMANCE</span><span>{date_short}</span></div>'
                  f'<div style="background:#0F1623;border:1px solid #232B3E;border-radius:0 0 8px 8px;padding:10px 14px 8px 8px;">{"".join(bars)}<div style="text-align:right;font-size:10.5px;color:#94A3B8;margin-top:4px;">┆ garis putus-putus = 100% target</div></div>')
    mid = (f'<div style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start;margin-bottom:14px;"><div style="flex:1.5 1 420px;min-width:0;">{table_html}</div>'
           f'<div style="flex:1 1 360px;min-width:0;">{chart_html}</div></div>')
    if not dealer_tbl:   # dashboard koordinator / counter: tanpa tabel ranking dealer
        return f'<div style="font-family:Source Sans Pro,sans-serif;color:#E2E8F0;">{top}{mid}<div style="font-size:11px;color:#94A3B8;margin-top:2px;">{scheme_note}</div></div>'
    # --- tabel ranking (dealer / koordinator / counter) ---
    rk_codes = list(KPI_ENT_CODES[rank_kind]) if rank_kind else ['STU', 'MAX', 'CLS', 'OPR', 'SAL', 'APV', 'INC', 'MYM', 'MYD', 'GRT', 'GRV']
    rk_min = (lambda c: KPI_ENT_MIN_ACV[rank_kind].get(c, 0.0)) if rank_kind else (lambda c: KPI_MIN_ACV[c])
    rk_title = {'koor': 'RANKING KOORDINATOR', 'counter': 'RANKING COUNTER'}.get(rank_kind, 'RANKING DEALER')
    rk_name_hdr = {'koor': 'KOORDINATOR NAME', 'counter': 'COUNTER NAME'}.get(rank_kind, 'DEALER NAME')
    dh = ['NO', 'CODE', rk_name_hdr, 'POINT', 'GRADE', 'SALES', 'PROCESS'] + rk_codes + ['NOTE']
    dth = f'background:{DASH_NAVY};color:#fff;font-size:11px;font-weight:800;padding:7px 6px;border-bottom:2px solid #1E3A8A;text-align:center;white-space:nowrap;'
    drows = []
    for i, dr in enumerate(dealer_tbl, 1):
        gc = DASH_GRADE_COL.get(dr['grade'], '#FFFFFF')
        bgr = {'D': 'rgba(255,0,127,0.13)', 'C': 'rgba(255,234,0,0.10)', 'B': 'rgba(0,229,255,0.08)', 'A': 'rgba(0,255,102,0.12)'}.get(dr['grade'], 'transparent')
        outl = 'outline:2px solid #00E5FF;outline-offset:-2px;' if dr['name'] == hl_dealer else ''
        dtd = 'padding:6px 6px;border-bottom:1px solid #1E293B;font-size:12.5px;text-align:center;white-space:nowrap;color:#E2E8F0;'
        cells = (f'<td style="{dtd}">{i}</td><td style="{dtd}color:#94A3B8;">{dr["code"]}</td><td style="{dtd}text-align:left;font-weight:800;color:#FFFFFF;">{dr["name"]}</td>'
                 f'<td style="{dtd}font-weight:900;color:#FFFFFF;">{dr["point"]}</td><td style="{dtd}font-weight:900;color:{gc};">{dr["grade"]}</td>'
                 f'<td style="{dtd}">{dr["sales"]}</td><td style="{dtd}">{dr["process"]}</td>')
        for c in rk_codes:
            av = dr['achv'][c]
            col = '#00FF66' if av >= 1 else ('#FFEA00' if av >= rk_min(c) else '#FF80AB')
            cells += f'<td style="{dtd}font-weight:700;color:{col};">{av * 100:.0f}%</td>'
        cells += f'<td style="{dtd}font-weight:800;color:#FF80AB;">{dr["note"]}</td>'
        drows.append(f'<tr style="background:{bgr};{outl}">{cells}</tr>')
    dealer_html = (f'<div style="background:{DASH_TEAL};color:#fff;font-size:12px;font-weight:800;letter-spacing:.6px;text-align:center;padding:7px 8px;border-radius:8px 8px 0 0;">{rk_title} — POINT, GRADE & ACHIEVEMENT PER KPI</div>'
                   f'<div style="overflow-x:auto;border:1px solid #232B3E;border-radius:0 0 8px 8px;background:#0E1117;"><table style="width:100%;border-collapse:collapse;"><thead><tr>'
                   + ''.join(f'<th style="{dth}">{h}</th>' for h in dh) + '</tr></thead><tbody>' + ''.join(drows) + '</tbody></table></div>'
                   f'<div style="font-size:11px;color:#94A3B8;margin-top:6px;">{scheme_note}</div>')
    return f'<div style="font-family:Source Sans Pro,sans-serif;color:#E2E8F0;">{top}{mid}{dealer_html}</div>'


# ===================== DASHBOARD KPI KOORDINATOR & COUNTER (rumus & bobot = sheet Dashboard MASTER_KPI_KOOR / MASTER_KPI_COUNTER) =====================
KPI_ENT_CODES = {'koor':    ['STU', 'CLS', 'MAX', 'PRM', 'SAL', 'PRD', 'DBS', 'INC', 'MYD', 'GRV'],
                 'counter': ['STU', 'CLS', 'MAX', 'PRM', 'WLK', 'MYM', 'DBS', 'INC', 'MYD', 'GRV']}
KPI_ENT_RESULT_CODES = ['STU', 'CLS', 'MAX']
KPI_ENT_NAMES = {'STU': 'STU Total', 'CLS': 'STU AT Classy', 'MAX': 'STU AT PRM (Maxi)', 'PRM': 'Promosi', 'SAL': 'QTY Salesman', 'PRD': 'Productivity Salesman',
                 'WLK': 'Walk In', 'MYM': 'Member Point', 'DBS': 'Database', 'INC': 'Incoming', 'MYD': 'My Yamaha Dealer Rating (MYDR)', 'GRV': 'Google Review'}
KPI_ENT_NAMES_KIND = {'koor': {'PRM': 'Promosi - Aktifitas Online 2X & Offline 2X'}, 'counter': {'PRM': 'Promosi - Live TikTok/IG'}}
KPI_ENT_WEIGHT = {'koor':    {'STU': 20, 'CLS': 10, 'MAX': 10, 'PRM': 15, 'SAL': 10, 'PRD': 5, 'DBS': 10, 'INC': 10, 'MYD': 5, 'GRV': 5},
                  'counter': {'STU': 20, 'CLS': 10, 'MAX': 10, 'PRM': 15, 'WLK': 10, 'MYM': 5, 'DBS': 10, 'INC': 10, 'MYD': 5, 'GRV': 5}}
KPI_ENT_MIN_ACV = {'koor':    {'STU': .70, 'CLS': .70, 'MAX': .70, 'PRM': .85, 'SAL': .85, 'PRD': .85, 'DBS': .85, 'INC': .85, 'MYD': .85, 'GRV': .85},
                   'counter': {'PRM': .85, 'WLK': .60, 'MYM': .85, 'DBS': .85, 'INC': .75, 'MYD': .85, 'GRV': .85}}   # counter STU/CLS/MAX: poin dari tabel lookup (tanpa min ACV)
KPI_ENT_FIXED_ACHV = {'koor': {'PRM'}, 'counter': {'PRM', 'MYM'}}   # Achiev dikunci 100% (permintaan: Promosi semua & Member Point counter = poin penuh)
KPI_ENT_PROD_TARGET = 2.5                                           # target Productivity Salesman koordinator (sheet Dashboard koor, sel F16)
# Tabel poin counter (sheet Sheet5 MASTER_KPI_COUNTER): index = jumlah result unit (0..30) -> (poin COUNTER ADMIN, poin COUNTER MURNI/SALES)
KPI_COUNTER_TABLE = {
    'STU': [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(10,0),(11,0),(13,0),(15,10),(17,11),(18,12),(20,14),(20,15),(20,16),(20,18),(20,19),(20,20)] + [(20,20)] * 10,
    'MAX': [(0,0),(0,0),(0,0),(0,0),(6,0),(8,5),(10,7),(10,8),(10,10)] + [(10,10)] * 22,
    'CLS': [(0,0),(5,0),(10,5),(10,10)] + [(10,10)] * 27,
}
KPI_COUNTER_MURNI = ['NUR AFIFAH APRILIANA', 'EMILIA DIANA', 'SITI NURJANAH', 'KOESMIATI', 'ALBERTINE CHRISANTINA PUTRI', 'IIN BARIROH', 'TRIA DAMAYANTI']
KPI_COUNTER_ADMIN = ['NURUL FADILAH', 'PUTRI ZAIN MAZDA', 'RIKA DWI ASTUTI', 'RISKA MELIYANA', 'MUHAMMAD HAMDAN WAHDI', 'NICKY LINTANG PERTIWI', 'DESVIN NURUL PRISTANTINI',
                     'DIAJENG AYUDHIA UTAMI PUTRI', 'NOVIN MARIA PURWANITA', 'INDAH RETUWATI R.', 'DINI KOYIMATUL HIKMAH', 'HERDIK RIZAL UTAMANDA', 'ANNISA ROISNAINI', 'LAILI NISFIATURROHMA']

def _kpi_num(x): return int(round(x)) if abs(x - round(x)) < 1e-9 else x

def detect_counter_type(ent):
    """'MURNI' / 'ADMIN' dari daftar nama di file MASTER_KPI_COUNTER; tidak dikenali -> ADMIN (bisa diganti manual di dashboard)."""
    e = alnum_str(ent).replace('COUNTER', '')
    def hit(names): return any(alnum_str(n) and (alnum_str(n) in e or (len(e) >= 5 and e in alnum_str(n))) for n in names)
    if hit(KPI_COUNTER_MURNI): return 'MURNI'
    return 'ADMIN'

def kpi_point_ent(kind, code, target, result, weight, ctype='ADMIN'):
    """Poin per item persis rumus kolom Point sheet Dashboard (koor: MASTER_KPI_KOOR, counter: MASTER_KPI_COUNTER). Dibatasi maksimal bobot."""
    t, r = float(target or 0), float(result or 0)
    achv = (r / t) if t > 0 else 0.0
    w = weight
    half_up = int(math.ceil(0.5 * w - 1e-9))
    def mid(mn, mult): return min(w, half_up + int(math.floor((achv - mn) / 0.15 * mult + 1e-9)))
    def near_miss(): return _kpi_num(0.5 * w) if (t <= 8 and r == t - 1 and r > 0) else 0
    if kind == 'counter' and code in ('STU', 'CLS', 'MAX'):
        return KPI_COUNTER_TABLE[code][max(0, min(int(round(r)), 30))][0 if ctype == 'ADMIN' else 1]
    if achv >= 1 - 1e-9: return w
    if code in ('STU', 'CLS', 'MAX'): return mid(0.70, 4) if achv >= 0.70 else near_miss()
    if code in ('PRM', 'DBS'):        return mid(0.85, 4) if achv >= 0.85 else near_miss()
    if code == 'SAL':                 return mid(0.85, 4) if achv >= 0.85 else (_kpi_num(0.5 * w) if (t == 6 and r == 5) else 0)
    if code == 'PRD':                 return mid(0.85, 4) if achv >= 0.85 else 0
    if code == 'WLK':                 return mid(0.60, 2) if achv >= 0.60 else (_kpi_num(0.6 * w) if (t == 6 and r == 5) else 0)
    if code == 'INC':                 return mid(0.75 if kind == 'counter' else 0.85, 2) if achv >= (0.75 if kind == 'counter' else 0.85) else 0
    return mid(0.85, 2) if achv >= 0.85 else 0   # MYD, GRV, MYM

def kpi_score_entity_sim(tr, kind, ctype='ADMIN'):
    rows = {}
    for c in KPI_ENT_CODES[kind]:
        t, r = tr.get(c, (0, 0))
        fixed = c in KPI_ENT_FIXED_ACHV[kind]
        if fixed: t, r = 1.0, 1.0
        t, r = float(t or 0), float(r or 0)
        achv = (r / t) if t > 0 else 0.0
        w = KPI_ENT_WEIGHT[kind][c]
        pt = kpi_point_ent(kind, c, t, r, w, ctype)
        no_min = kind == 'counter' and c in ('STU', 'CLS', 'MAX')
        rows[c] = dict(code=c, name=KPI_ENT_NAMES_KIND[kind].get(c, KPI_ENT_NAMES[c]), weight=w, min_acv=KPI_ENT_MIN_ACV[kind].get(c, KPI_ENT_MIN_ACV[kind].get('STU', 0.0)) if not no_min else 0.0,
                       target=t, result=r, achv=achv, point=pt, fixed=fixed, no_min=no_min)
    sales = sum(rows[c]['point'] for c in KPI_ENT_RESULT_CODES)
    process = sum(rows[c]['point'] for c in KPI_ENT_CODES[kind] if c not in KPI_ENT_RESULT_CODES)
    return rows, _kpi_num(sales), _kpi_num(process), _kpi_num(sales + process)

def get_entity_kpi_inputs(kind, ent):
    """Target & Result per item. Semua angka dari tabel MASTER KPI (koordinator / counter); MYDR & Google Review = dealer induk."""
    df_it, _ = build_kpi_section_df([ent], 'NAMA KOORDINATOR' if kind == 'koor' else 'NAMA COUNTER', kind, kind)
    r = df_it.iloc[0] if (df_it is not None and not df_it.empty) else None
    def g(k): return safe_float(r[k]) if (r is not None and k in r.index) else 0.0
    t_stu, r_stu, t_mp, r_mp = g('T. STU'), g('R. STU'), g('T. MP'), g('R. MP')
    inp = {'STU': (t_stu, r_stu), 'CLS': (g('T. CLASSY'), g('R. CLASSY')), 'MAX': (g('T. MAXI'), g('R. MAXI')), 'PRM': (1.0, 1.0),
           'INC': (g('T. INC'), g('R. INC')), 'DBS': (g('T. DB'), g('R. DB')), 'MYD': (g('T. MYDR'), g('R. MYDR')), 'GRV': (g('T. G REV'), g('R. G REV'))}
    if kind == 'koor':
        inp['SAL'] = (t_mp, r_mp)
        inp['PRD'] = (KPI_ENT_PROD_TARGET, (r_stu / r_mp) if r_mp > 0 else 0.0)
    else:
        inp['WLK'] = (g('T. Walk In'), g('R. Walk In'))
        inp['MYM'] = (1.0, 1.0)
    return inp

def get_focus_entities():
    """Daftar koordinator & counter yang bertugas di 7 dealer fokus (urut sesuai daftar_dealer)."""
    ent_all = set(clean_str(v) for v in mapping_salesman_koor.values() if clean_str(v)) | set(k for k in saved_tk.keys() if k != 'TOTAL')
    for d_s, ck in [(df_faktur, 'Koor'), (df_nota, 'Koor'), (df_database, 'Koor'), (df_spk, 'Koor_SPK'), (df_rating, 'Koor')]:
        if d_s is not None and ck in d_s.columns:
            ent_all.update(clean_str(k) for k in d_s[ck].dropna().unique() if clean_str(k) and clean_str(k) not in ['LAIN-LAIN', 'NAN', 'NONE'])
    focus = [e for e in ent_all if kpi_entity_dealer(e)]
    key_fn = lambda e: (daftar_dealer.index(kpi_entity_dealer(e)), e)
    return sorted([e for e in focus if not e.upper().startswith('COUNTER')], key=key_fn), sorted([e for e in focus if e.upper().startswith('COUNTER')], key=key_fn)

def render_entity_kpi_dashboard(kind, entities, title_txt, sel_key, date_lbl, date_short):
    st.markdown(f'<div class="section-title">{title_txt}</div>', unsafe_allow_html=True)
    lbl = 'Koordinator' if kind == 'koor' else 'Counter'
    if not entities:
        st.info(f'ℹ️ Belum ada {lbl} dari 7 dealer fokus. Pastikan file Data Lookup & Database sudah diupload.')
        return
    sel = st.selectbox(f'👤 Pilih {lbl}:', entities, index=0, key=sel_key, format_func=lambda e: f'{e}  —  {kpi_entity_dealer(e)}')
    ctype = 'ADMIN'
    if kind == 'counter':
        auto_t = detect_counter_type(sel)
        ctype = st.radio('Tipe Counter (menentukan tabel poin STU / Classy / PRM):', ['ADMIN', 'MURNI'], index=['ADMIN', 'MURNI'].index(auto_t), horizontal=True, key=f'ctype_{sel}')
    rows_e, s_e, p_e, t_e = kpi_score_entity_sim(get_entity_kpi_inputs(kind, sel), kind, ctype)
    if kind == 'koor':
        note_e = (f'Dealer: {kpi_entity_dealer(sel)}. Bobot & rumus poin sesuai file MASTER_KPI_KOOR (Result 40 + Process 60 = 100). Target & Result dari tabel MASTER KPI Koordinator; MYDR & Google Review mengikuti dealer induk. '
                  f'Promosi Achiev dikunci 100%. Productivity = STU ÷ QTY Salesman, target {KPI_ENT_PROD_TARGET}.')
    else:
        note_e = (f'Dealer: {kpi_entity_dealer(sel)} | Tipe: COUNTER {ctype}. Bobot & rumus poin sesuai file MASTER_KPI_COUNTER (Result 40 + Process 60 = 100); poin STU / Classy / PRM dari tabel lookup Sheet5. '
                  'Target & Result dari tabel MASTER KPI Counter; MYDR & Google Review mengikuti dealer induk; Walk In dari kolom Prospect Type (Walk In). Promosi & Member Point Achiev dikunci 100%.')
    rank_tbl = []
    for e_k in entities:
        ct_k = detect_counter_type(e_k) if kind == 'counter' else 'ADMIN'
        if e_k == sel: ct_k = ctype
        r_k, s_k, p_k, t_k = kpi_score_entity_sim(get_entity_kpi_inputs(kind, e_k), kind, ct_k)
        rank_tbl.append({'name': e_k, 'code': (kpi_entity_dealer(e_k) or '-').replace('SIP ', ''), 'point': t_k, 'grade': kpi_grade(t_k), 'sales': s_k, 'process': p_k,
                         'achv': {c: r_k[c]['achv'] for c in KPI_ENT_CODES[kind]}, 'note': kpi_note(p_k)})
    rank_tbl.sort(key=lambda x_d: (-x_d['point'], -x_d['process'], x_d['name']))
    html_e = build_dashboard_kpi_html(sel, date_lbl, date_short, rows_e, s_e, p_e, t_e, rank_tbl, sel, False, note_e, codes=KPI_ENT_CODES[kind], rank_kind=kind)
    st.markdown(html_e, unsafe_allow_html=True)
    cap_e = f'<div style="width:1320px;background-color:#0E1117;padding:18px 20px;box-sizing:border-box;">{html_e}</div>'
    render_table_image_buttons(f'cap_dashboard_kpi_{kind}', f'Dashboard_KPI_{lbl}_{sel}_Tgl_{tanggal_akhir}', standalone_html=cap_e)


if menu_pilihan == '🎯 MASTER KPI':
    st.markdown(f'<div class="main-title">DASHBOARD KPI (1 s.d {tanggal_akhir} {periode_bulan_tahun})</div><div class="sub-title">Monitoring Target (T.) vs Result (R.) — KPI Dealer, KPI Koordinator & KPI Counter</div>', unsafe_allow_html=True)

    saved_kpi = load_json(KPI_SAVED_FILE)
    saved_td = load_json(TARGET_DEALER_FILE)
    saved_tk = load_json(TARGET_KOOR_FILE)

    KPI_METRIC_COLS = ['T. STU', 'R. STU', 'T. MAXI', 'R. MAXI', 'T. CLASSY', 'R. CLASSY', 'T. MP', 'R. MP', 'T. INC', 'R. INC', 'T. ACC%', 'R. ACC%', 'T. MYDR', 'R. MYDR', 'T. G REV', 'R. G REV']
    KPI_EDITABLE_COLS = ['T. STU', 'T. MAXI', 'T. CLASSY', 'T. MP', 'T. INC', 'T. ACC%', 'T. G REV', 'R. G REV']
    KPI_PAIRS_ALL = [('T. STU', 'R. STU'), ('T. MAXI', 'R. MAXI'), ('T. CLASSY', 'R. CLASSY'), ('T. MP', 'R. MP'), ('T. INC', 'R. INC'), ('T. ACC%', 'R. ACC%'), ('T. MYDR', 'R. MYDR'), ('T. G REV', 'R. G REV'), ('T. DB', 'R. DB'), ('T. Walk In', 'R. Walk In')]

    def kpi_metric_cols(section_key):
        # Koordinator: + DB | Counter: + DB & Walk In | Dealer: kolom dasar
        return KPI_METRIC_COLS + {'koor': ['T. DB', 'R. DB'], 'counter': ['T. DB', 'R. DB', 'T. Walk In', 'R. Walk In']}.get(section_key, [])

    def kpi_editable_cols(section_key):
        if section_key == 'dealer': return list(KPI_EDITABLE_COLS)
        # G REV koordinator/counter mengikuti dealer -> tidak diedit di sini
        return [c for c in KPI_EDITABLE_COLS if c not in ('T. G REV', 'R. G REV')] + ['T. DB'] + (['T. Walk In'] if section_key == 'counter' else [])

    def build_kpi_capture_html(df_full, name_col, title_txt, dom_id, metric_cols=None):
        cols_all = [name_col] + (metric_cols or KPI_METRIC_COLS)
        pairs = [p for p in KPI_PAIRS_ALL if p[0] in cols_all]
        r_to_t = {r_c: t_c for t_c, r_c in pairs}
        html = [f'<div id="{dom_id}" class="compact-table-wrap"><div class="cap-title-banner">🐺 {title_txt}</div><table class="compact-tbl"><thead><tr>']
        for c in cols_all:
            bg_th = 'background-color:#1E3A8A;color:#FFFFFF;' if c == name_col else ('background-color:#0F172A;color:#F8FAFC;' if c.startswith('T.') else 'background-color:#1E40AF;color:#FFFFFF;')
            html.append(f'<th style="{bg_th}">{c}</th>')
        html.append('</tr></thead><tbody>')
        for _, row in df_full.iterrows():
            nm = str(row[name_col])
            is_tot = nm == 'TOTAL'
            tr_style = 'background-color:#4318FF;color:#FFFFFF;font-weight:800;' if is_tot else ''
            html.append(f'<tr style="{tr_style}">')
            for c in cols_all:
                val = row[c]
                disp_v = f"{val:.1f}%" if c in ['T. ACC%', 'R. ACC%'] else str(val)
                cell_st = ''
                if not is_tot:
                    if c == name_col:
                        cell_st = 'color:#FFFFFF;font-weight:700;'
                    elif c.startswith('T.'):
                        cell_st = 'color:#CBD5E1;background-color:#111827;'
                    elif c in r_to_t:
                        t_col = r_to_t[c]
                        tv, rv = safe_float(row[t_col]), safe_float(row[c])
                        ideal_cmp = tv if c in ['R. MP', 'R. ACC%', 'R. MYDR'] else (tv * persen_desimal)
                        if tv > 0 and rv >= ideal_cmp:
                            cell_st = 'background-color:rgba(0,255,102,0.16);color:#00FF66;font-weight:800;'
                        elif tv > 0:
                            cell_st = 'background-color:rgba(255,0,127,0.22);color:#FF80AB;font-weight:800;'
                        else:
                            cell_st = 'color:#E2E8F0;'
                html.append(f'<td style="{cell_st}">{disp_v}</td>')
            html.append('</tr>')
        html.append('</tbody></table></div>')
        return ''.join(html)

    def render_kpi_section(df_items, df_full, name_col, section_key, title_txt, btn_label):
        if df_full is None or df_full.empty:
            st.info(f"ℹ️ Belum ada data untuk {title_txt}.")
            return
        metric_cols_sec, edit_cols_sec = kpi_metric_cols(section_key), kpi_editable_cols(section_key)
        cols_show = [name_col] + metric_cols_sec
        pairs = [p for p in KPI_PAIRS_ALL if p[0] in cols_show]
        r_to_t = {r_c: t_c for t_c, r_c in pairs}

        def sty_kpi(row):
            if str(row[name_col]) == 'TOTAL':
                return ['background-color: #4318FF; color: #FFFFFF; font-weight: 800'] * len(row)
            styles = []
            for c in cols_show:
                if c == name_col:
                    styles.append('font-weight: 700; color: #FFFFFF')
                elif c.startswith('T.'):
                    styles.append('color: #CBD5E1; background-color: #141A26')
                elif c in r_to_t:
                    t_c = r_to_t[c]
                    tv, rv = safe_float(row[t_c]), safe_float(row[c])
                    ideal_cmp = tv if c in ['R. MP', 'R. ACC%', 'R. MYDR'] else (tv * persen_desimal)
                    if tv > 0 and rv >= ideal_cmp:
                        styles.append('background-color: rgba(0, 255, 102, 0.16); color: #00FF66; font-weight: 800')
                    elif tv > 0:
                        styles.append('background-color: rgba(255, 0, 127, 0.22); color: #FF4081; font-weight: 800')
                    else:
                        styles.append('color: #E2E8F0')
                else:
                    styles.append('')
            return styles

        col_cfg = {name_col: st.column_config.TextColumn(name_col, width="medium")}
        for c in metric_cols_sec:
            if c in ['T. ACC%', 'R. ACC%']:
                col_cfg[c] = st.column_config.NumberColumn(c, width="small", format="%.1f%%")
            else:
                col_cfg[c] = st.column_config.NumberColumn(c, width="small", format="%d")

        disabled_cols = [c for c in cols_show if c not in edit_cols_sec]
        ed_df = st.data_editor(
            df_full[cols_show].style.apply(sty_kpi, axis=1),
            hide_index=True,
            use_container_width=True,
            height=calc_table_height(df_full),
            column_config=col_cfg,
            disabled=disabled_cols,
            key=f'editor_kpi_{section_key}'
        )
        c_b1, c_b2 = st.columns([1, 3])
        with c_b1:
            if st.button(btn_label, type='primary', key=f'btn_save_kpi_{section_key}'):
                cur_all = load_json(KPI_SAVED_FILE)
                sec_dict = cur_all.get(section_key, {})
                td_sync = load_json(TARGET_DEALER_FILE) if section_key == 'dealer' else load_json(TARGET_KOOR_FILE)
                for _, r in ed_df.iterrows():
                    enm = str(r[name_col])
                    if enm == 'TOTAL': continue
                    sec_dict[enm] = {k_ed: (safe_float(r[k_ed]) if 'ACC%' in k_ed else safe_int(r[k_ed])) for k_ed in edit_cols_sec}
                    td_sync[enm] = safe_int(r['T. STU'])
                cur_all[section_key] = sec_dict
                save_json(cur_all, KPI_SAVED_FILE)
                save_json(td_sync, TARGET_DEALER_FILE if section_key == 'dealer' else TARGET_KOOR_FILE)
                st.success(f'✅ Target & Data {title_txt} berhasil disimpan!')
                st.rerun()
        with c_b2:
            cap_id = f'cap_kpi_{section_key}'
            cap_html = build_kpi_capture_html(df_full, name_col, title_txt, cap_id, metric_cols_sec)
            render_table_image_buttons(cap_id, f'{title_txt}_Tgl_{tanggal_akhir}', standalone_html=cap_html)

    df_kpi_dlr_items, df_kpi_dlr_full = build_kpi_section_df(daftar_dealer, 'NAMA DEALER', 'dealer', 'dealer')
    if not df_kpi_dlr_full.empty:
        tot_d = df_kpi_dlr_full.iloc[-1]
        tot_d = df_kpi_dlr_full.iloc[-1]
        bsg_safe(bsg_render_master_kpi_cards, tot_d, target_persen_harian, label="Kartu KPI")

    st.divider()
    jdl_kpi_1 = f'1. TABEL KPI DEALER (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
    st.markdown(f'<div class="section-title">{jdl_kpi_1}</div>', unsafe_allow_html=True)
    render_kpi_section(df_kpi_dlr_items, df_kpi_dlr_full, 'NAMA DEALER', 'dealer', jdl_kpi_1, '💾 Simpan KPI Dealer')

    ent_all_kpi = set(clean_str(v) for v in mapping_salesman_koor.values() if clean_str(v)) | set(k for k in saved_tk.keys() if k != 'TOTAL')
    for d_s, ck in [(df_faktur, 'Koor'), (df_nota, 'Koor'), (df_database, 'Koor'), (df_spk, 'Koor_SPK'), (df_rating, 'Koor')]:
        if d_s is not None and ck in d_s.columns:
            ent_all_kpi.update(clean_str(k) for k in d_s[ck].dropna().unique() if clean_str(k) and clean_str(k) not in ['LAIN-LAIN', 'NAN', 'NONE'])

    koor_entities = sorted([e for e in ent_all_kpi if not e.upper().startswith('COUNTER')])
    cnt_entities = sorted([e for e in ent_all_kpi if e.upper().startswith('COUNTER')])

    st.divider()
    jdl_kpi_2 = f'2. TABEL KPI KOORDINATOR (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
    st.markdown(f'<div class="section-title">{jdl_kpi_2}</div>', unsafe_allow_html=True)
    render_unmapped_salesman_alert('kpi_koor')
    df_kpi_kr_items, df_kpi_kr_full = build_kpi_section_df(koor_entities, 'NAMA KOORDINATOR', 'koor', 'koor')
    render_kpi_section(df_kpi_kr_items, df_kpi_kr_full, 'NAMA KOORDINATOR', 'koor', jdl_kpi_2, '💾 Simpan KPI Koordinator')

    st.divider()
    jdl_kpi_3 = f'3. TABEL KPI COUNTER (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
    st.markdown(f'<div class="section-title">{jdl_kpi_3}</div>', unsafe_allow_html=True)
    df_kpi_cnt_items, df_kpi_cnt_full = build_kpi_section_df(cnt_entities, 'NAMA COUNTER', 'counter', 'counter')
    render_kpi_section(df_kpi_cnt_items, df_kpi_cnt_full, 'NAMA COUNTER', 'counter', jdl_kpi_3, '💾 Simpan KPI Counter')

elif menu_pilihan == '🏦 SPK ONLINE':
    st.markdown(f'<div class="main-title">DASHBOARD LEASING (1 s.d {tanggal_akhir} {periode_bulan_tahun})</div><div class="sub-title">Monitoring SPK, Growth, Approval Rate (Acuan Ideal ACC% = 50%), SPK Terbuka & Rincian Leasing</div>', unsafe_allow_html=True)
    kol_lsg = ['SPK', 'SPK LM', 'GROWTH', 'ACC%', 'TERBUKA', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF', 'IMFI', '%IMFI']
    def get_dlr_lsg(dlrs, lbl, nc='NAMA DEALER'):
        return calc_leasing_row(lbl, df_spk_curr_g[df_spk_curr_g['Nama_Dealer_SPK'].isin(dlrs)] if not df_spk_curr_g.empty else pd.DataFrame(), df_spk_lm_g[df_spk_lm_g['Nama_Dealer_SPK'].isin(dlrs)] if not df_spk_lm_g.empty else pd.DataFrame(), nc)

    d_sit, d_bwi = ['SIP PANJI', 'SIP BESUKI'], ['SIP SRONO', 'SIP SIAGA', 'SIP SOBO', 'SIP GIRI', 'SIP A. YANI']
    df_sit = pd.DataFrame([get_dlr_lsg([d], d) for d in d_sit]).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True)
    df_bwi = pd.DataFrame([get_dlr_lsg([d], d) for d in d_bwi]).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True)
    df_lsg_full = pd.concat([df_sit, pd.DataFrame([get_dlr_lsg(d_sit, 'SUB SITUBONDO')]), df_bwi, pd.DataFrame([get_dlr_lsg(d_bwi, 'SUB BANYUWANGI')]), pd.DataFrame([get_dlr_lsg(daftar_dealer, 'TOTAL')])], ignore_index=True)
    jdl_lsg_dlr = f'DASHBOARD LEASING DEALER (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
    st.markdown(f'<div class="section-title">{jdl_lsg_dlr}</div>', unsafe_allow_html=True)
    render_compact_html_table(pd.concat([df_sit, df_bwi], ignore_index=True), df_lsg_full, ['NAMA DEALER'] + kol_lsg, 'NAMA DEALER', '_acc_val', key_suffix='Leasing_Dealer', title_text=jdl_lsg_dlr)
    bsg_safe(bsg_render_spk_online_charts, df_sit, df_bwi, df_lsg_full, label="Grafik SPK Online")

    saved_tk = load_json(TARGET_KOOR_FILE)
    ent_s = sorted(list(set(clean_str(v) for v in mapping_salesman_koor.values() if clean_str(v)) | set(k for k in saved_tk.keys() if k != 'TOTAL') | (set(str(k) for k in df_spk['Koor_SPK'].dropna().unique() if str(k) != 'LAIN-LAIN') if (df_spk is not None and 'Koor_SPK' in df_spk.columns) else set())))
    for elist, nc, sec_t in [([e for e in ent_s if not e.upper().startswith('COUNTER')], 'NAMA KOORDINATOR', 'DASHBOARD LEASING KOORDINATOR'), ([e for e in ent_s if e.upper().startswith('COUNTER')], 'NAMA COUNTER', 'DASHBOARD LEASING COUNTER')]:
        st.divider()
        full_sec_lsg = f'{sec_t} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{full_sec_lsg}</div>', unsafe_allow_html=True)
        r_l, v_e = [], []
        for e in elist:
            rd = calc_leasing_row(e, df_spk_curr_g[df_spk_curr_g['Koor_SPK'] == e] if not df_spk_curr_g.empty else pd.DataFrame(), df_spk_lm_g[df_spk_lm_g['Koor_SPK'] == e] if not df_spk_lm_g.empty else pd.DataFrame(), nc)
            if get_koor_or_counter_target(e, saved_tk) == 0 and rd['_spk_val'] == 0 and rd['_spk_lm_val'] == 0: continue
            r_l.append(rd); v_e.append(e)
        if r_l:
            df_i = pd.DataFrame(r_l).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True)
            tot_l = calc_leasing_row('TOTAL', df_spk_curr_g[df_spk_curr_g['Koor_SPK'].isin(v_e)] if not df_spk_curr_g.empty else pd.DataFrame(), df_spk_lm_g[df_spk_lm_g['Koor_SPK'].isin(v_e)] if not df_spk_lm_g.empty else pd.DataFrame(), nc)
            render_compact_html_table(df_i, pd.concat([df_i, pd.DataFrame([tot_l])], ignore_index=True), [nc] + kol_lsg, nc, '_acc_val', key_suffix=sec_t, title_text=full_sec_lsg)

    st.divider()
    jdl_stu_lsg_fak = f'STU PER LEASING — FAKTUR (1 s.d {tanggal_akhir} {periode_bulan_tahun} vs Bulan Lalu)'
    st.markdown(f'<div class="section-title">{jdl_stu_lsg_fak}</div>', unsafe_allow_html=True)

    AREA_DEALERS_STU_LEASING = [
        ('JEMBER', ['SENTRAL YAMAHA JEMBER', 'SIP AMBULU', 'SIP BALUNG', 'SIP GAJAH MADA', 'SIP KEBONSARI', 'SIP RAMBIPUJI', 'SIP SUMBERSARI', 'SIP TRUNOJOYO', 'INDO PERKASA JEMBER', 'INDO PERKASA KENCONG', 'SUMBER MAS MOTOR']),
        ('BONDOWOSO', ['SIP BONDOWOSO', 'SIP NANGKAAN']),
        ('SITUBONDO', ['SIP BESUKI', 'SIP PANJI', 'KARUNIA PUTRA MOTOR / SIT']),
        ('BANYUWANGI', ['SIP A. YANI', 'SIP GIRI', 'SIP SIAGA', 'SIP SOBO', 'SIP SRONO', 'AMIN MOTOR BANYUWANGI', 'AMIN MOTOR GENTENG', 'BUDI JAYA MOTOR (BWI)', 'BUDI JAYA MOTOR/ PHJ', 'INDO PERKASA', 'INDO PERKASA CLURING', 'KARUNIA MOTOR (JJG)', 'KARUNIA MOTOR (RGJ)'])
    ]
    ALL_28_DEALERS = [d for _, d_list in AREA_DEALERS_STU_LEASING for d in d_list]

    def match_dealer_stu_leasing(val):
        s = clean_str(val)
        if not s or s in ['NAN', 'NONE']: return ''
        if s in ALL_28_DEALERS: return s
        s_ns = alnum_str(s)
        for d in ALL_28_DEALERS:
            if alnum_str(d) == s_ns: return d
        for k1, k2, res in [('KARUNIA PUTRA', '', 'KARUNIA PUTRA MOTOR / SIT'), ('BUDI JAYA', 'PHJ', 'BUDI JAYA MOTOR/ PHJ'), ('BUDI JAYA', '', 'BUDI JAYA MOTOR (BWI)'), ('KARUNIA MOTOR', 'JJG', 'KARUNIA MOTOR (JJG)'), ('KARUNIA MOTOR', 'RGJ', 'KARUNIA MOTOR (RGJ)'), ('INDO PERKASA', 'KENCONG', 'INDO PERKASA KENCONG'), ('INDO PERKASA', 'CLURING', 'INDO PERKASA CLURING'), ('INDO PERKASA', 'JEMBER', 'INDO PERKASA JEMBER'), ('AMIN MOTOR', 'GENTENG', 'AMIN MOTOR GENTENG'), ('AMIN MOTOR', '', 'AMIN MOTOR BANYUWANGI'), ('SENTRAL YAMAHA', '', 'SENTRAL YAMAHA JEMBER'), ('SUMBER MAS', '', 'SUMBER MAS MOTOR')]:
            if k1 in s and (not k2 or k2 in s): return res
        return normalize_dealer_name(s)

    df_source_faktur_lsg = df_faktur_all if (df_faktur_all is not None and not df_faktur_all.empty) else df_faktur
    if df_source_faktur_lsg is not None and not df_source_faktur_lsg.empty:
        df_fa = df_source_faktur_lsg.copy()
        dlr_col_fa = 'Nama Dealer' if 'Nama Dealer' in df_fa.columns else next((c for c in df_fa.columns if 'DEALER' in str(c).upper()), df_fa.columns[1] if df_fa.shape[1] > 1 else df_fa.columns[0])
        df_fa['Dealer_Map_Leasing'] = df_fa[dlr_col_fa].apply(match_dealer_stu_leasing)
        fa_curr = df_fa[(df_fa['bulan'] == current_month) & (df_fa['tahun'] == current_year) & (df_fa['hari'] >= 1) & (df_fa['hari'] <= tanggal_akhir)] if 'bulan' in df_fa.columns else pd.DataFrame()
        fa_lm = df_fa[(df_fa['bulan'] == last_month) & (df_fa['tahun'] == last_month_year) & (df_fa['hari'] >= 1) & (df_fa['hari'] <= tanggal_akhir)] if 'bulan' in df_fa.columns else pd.DataFrame()
        KREDIT_CATS = ['BAF', 'ADIRA', 'SOF', 'IMFI', 'OTHERS']

        def calc_stu_per_leasing_row(label_row, dealer_subset):
            sub_c = fa_curr[fa_curr['Dealer_Map_Leasing'].isin(dealer_subset)] if not fa_curr.empty else pd.DataFrame()
            sub_l = fa_lm[fa_lm['Dealer_Map_Leasing'].isin(dealer_subset)] if not fa_lm.empty else pd.DataFrame()
            row_d, kredit_c, kredit_l = {'NAMA DEALER': label_row}, 0, 0
            for lsg in KREDIT_CATS:
                c_val = int((sub_c['Leasing_Faktur_Clean'] == lsg).sum()) if not sub_c.empty else 0
                l_val = int((sub_l['Leasing_Faktur_Clean'] == lsg).sum()) if not sub_l.empty else 0
                row_d[lsg], row_d[f'{lsg} LM'] = c_val, l_val
                kredit_c += c_val; kredit_l += l_val
                if lsg == 'BAF': row_d['_baf_grw'], row_d['_baf_val'] = ((c_val / l_val * 100.0) if l_val > 0 else 0.0), c_val
            row_d['BCS'] = f'{(row_d["BAF"] / kredit_c * 100.0 if kredit_c > 0 else 0.0):.1f}%'
            row_d['KREDIT'], row_d['KREDIT LM'] = kredit_c, kredit_l
            cash_c = int((sub_c['Leasing_Faktur_Clean'] == 'CASH').sum()) if not sub_c.empty else 0
            cash_l = int((sub_l['Leasing_Faktur_Clean'] == 'CASH').sum()) if not sub_l.empty else 0
            row_d['CASH'], row_d['CASH LM'], row_d['TOTAL'], row_d['TOTAL LM'] = cash_c, cash_l, kredit_c + cash_c, kredit_l + cash_l
            return row_d

        full_rows_stu_lsg, item_rows_stu_lsg = [], []
        for area_name, d_list in AREA_DEALERS_STU_LEASING:
            area_dealer_rows = sorted([calc_stu_per_leasing_row(d_nm, [d_nm]) for d_nm in d_list], key=lambda r: (r['_baf_grw'], r['_baf_val']))
            full_rows_stu_lsg.extend(area_dealer_rows); item_rows_stu_lsg.extend(area_dealer_rows)
            full_rows_stu_lsg.append(calc_stu_per_leasing_row(area_name, d_list))

        full_rows_stu_lsg.append(calc_stu_per_leasing_row('TOTAL JEMBER', ALL_28_DEALERS))
        row_tot_bushido = calc_stu_per_leasing_row('TOTAL BUSHIDO', daftar_dealer)
        full_rows_stu_lsg.append(row_tot_bushido)

        kredit_bushido_c, kredit_bushido_l = safe_int(row_tot_bushido.get('KREDIT', 0)), safe_int(row_tot_bushido.get('KREDIT LM', 0))
        tot_bushido_c, tot_bushido_l = safe_int(row_tot_bushido.get('TOTAL', 0)), safe_int(row_tot_bushido.get('TOTAL LM', 0))
        cash_bushido_c, cash_bushido_l = safe_int(row_tot_bushido.get('CASH', 0)), safe_int(row_tot_bushido.get('CASH LM', 0))

        row_cs_bushido = {'NAMA DEALER': 'CREDIT SHARE BUSHIDO', 'BCS': row_tot_bushido.get('BCS', '0.0%'), '_baf_grw': 0.0, '_baf_val': 0}
        for lsg in KREDIT_CATS:
            val_c, val_l = safe_int(row_tot_bushido.get(lsg, 0)), safe_int(row_tot_bushido.get(f'{lsg} LM', 0))
            row_cs_bushido[lsg] = f'{(val_c / kredit_bushido_c * 100.0):.1f}%' if kredit_bushido_c > 0 else '0.0%'
            row_cs_bushido[f'{lsg} LM'] = f'{(val_l / kredit_bushido_l * 100.0):.1f}%' if kredit_bushido_l > 0 else '0.0%'
        row_cs_bushido['KREDIT'] = f'{(kredit_bushido_c / tot_bushido_c * 100.0):.1f}%' if tot_bushido_c > 0 else '0.0%'
        row_cs_bushido['KREDIT LM'] = f'{(kredit_bushido_l / tot_bushido_l * 100.0):.1f}%' if tot_bushido_l > 0 else '0.0%'
        row_cs_bushido['CASH'] = f'{(cash_bushido_c / tot_bushido_c * 100.0):.1f}%' if tot_bushido_c > 0 else '0.0%'
        row_cs_bushido['CASH LM'] = f'{(cash_bushido_l / tot_bushido_l * 100.0):.1f}%' if tot_bushido_l > 0 else '0.0%'
        row_cs_bushido['TOTAL'], row_cs_bushido['TOTAL LM'] = ('100.0%' if tot_bushido_c > 0 else '0.0%'), ('100.0%' if tot_bushido_l > 0 else '0.0%')
        full_rows_stu_lsg.append(row_cs_bushido)

        kol_stu_per_lsg = ['NAMA DEALER', 'BCS', 'BAF', 'BAF LM', 'ADIRA', 'ADIRA LM', 'SOF', 'SOF LM', 'IMFI', 'IMFI LM', 'OTHERS', 'OTHERS LM', 'KREDIT', 'KREDIT LM', 'CASH', 'CASH LM', 'TOTAL', 'TOTAL LM']
        render_compact_html_table(pd.DataFrame(item_rows_stu_lsg), pd.DataFrame(full_rows_stu_lsg), kol_stu_per_lsg, 'NAMA DEALER', '_baf_grw', key_suffix=f'STU_Per_Leasing_Tgl_{tanggal_akhir}', header_labels=kol_stu_per_lsg, ultra_compact=True, title_text=jdl_stu_lsg_fak)
    else: st.warning('⚠️ File Faktur belum tersedia. Silakan unggah file Faktur di menu **📁 UPLOAD FILE**.')

    st.divider()
    col_drop_rej, _ = st.columns([1, 3])
    with col_drop_rej: pil_lsg_reject = st.selectbox('🏦 Pilih Leasing (Rejection Analysis):', ['BAF', 'ADIRA', 'SOF'], index=0, key='sel_lsg_rej_analysis')
    jdl_rej_analysis = f'REJECTION ANALYSIS — LEASING {pil_lsg_reject} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
    st.markdown(f'<div class="section-title">{jdl_rej_analysis}</div>', unsafe_allow_html=True)

    if not df_spk_curr_g.empty and 'Leasing_SPK_Clean' in df_spk_curr_g.columns:
        df_spk_lsg_sub = df_spk_curr_g[(df_spk_curr_g['Nama_Dealer_SPK'].isin(daftar_dealer)) & (df_spk_curr_g['Leasing_SPK_Clean'] == pil_lsg_reject)].copy()
        df_rej_only = df_spk_lsg_sub[df_spk_lsg_sub['Status_SPK_Clean'] == 'DITOLAK'].copy()
        reason_cols = [str(r) for r in df_rej_only['Alasan_Reject_Clean'].value_counts().index if str(r).strip()] if (not df_rej_only.empty and 'Alasan_Reject_Clean' in df_rej_only.columns) else []
        rej_rows = []
        for d_fokus in daftar_dealer:
            sub_d_lsg = df_spk_lsg_sub[df_spk_lsg_sub['Nama_Dealer_SPK'] == d_fokus]
            open_cnt = int((sub_d_lsg['Status_SPK_Clean'] == 'TERBUKA').sum()) if not sub_d_lsg.empty else 0
            sub_d_rej = df_rej_only[df_rej_only['Nama_Dealer_SPK'] == d_fokus] if not df_rej_only.empty else pd.DataFrame()
            tot_rej_d = len(sub_d_rej)
            r_dict = {'NAMA DEALER': d_fokus, 'OPEN': open_cnt, 'TOTAL REJECT': tot_rej_d, '_sort_rej': -(tot_rej_d * 100 + open_cnt)}
            for rc in reason_cols: r_dict[rc] = int((sub_d_rej['Alasan_Reject_Clean'] == rc).sum()) if not sub_d_rej.empty else 0
            rej_rows.append(r_dict)
        df_rej_items = pd.DataFrame(rej_rows).sort_values(by=['_sort_rej', 'NAMA DEALER'], ascending=[True, True]).reset_index(drop=True)
        tot_rej_row = {'NAMA DEALER': 'TOTAL', 'OPEN': int(df_rej_items['OPEN'].sum()), 'TOTAL REJECT': int(df_rej_items['TOTAL REJECT'].sum()), '_sort_rej': 0}
        for rc in reason_cols: tot_rej_row[rc] = int(df_rej_items[rc].sum())
        render_compact_html_table(df_rej_items, pd.concat([df_rej_items, pd.DataFrame([tot_rej_row])], ignore_index=True), ['NAMA DEALER', 'OPEN'] + reason_cols + ['TOTAL REJECT'], 'NAMA DEALER', '_sort_rej', key_suffix=f'Rejection_Analysis_{pil_lsg_reject}_Tgl_{tanggal_akhir}', title_text=jdl_rej_analysis)
    else: st.warning('⚠️ Data SPK belum tersedia untuk periode ini.')

elif menu_pilihan == '📊 DASHBOARD KPI':
    st.markdown(f'<div class="main-title">DASHBOARD KPI (1 s.d {tanggal_akhir} {periode_bulan_tahun})</div><div class="sub-title">Laporan Key Performance Indicator — poin, grade & capaian tiap KPI (Target & Result dari MASTER KPI)</div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns([1, 2])
    with col_d1: sel_dash = st.selectbox('🏢 Pilih Dealer:', ['TOTAL BUSHIDO'] + daftar_dealer, index=0, key='sel_dash_kpi')
    # Bobot otomatis: TOTAL BUSHIDO -> bobot MDS (sesuai gambar) | pilih dealer -> bobot Dealer (sesuai Excel R-MDS)
    scheme_dash = 'MDS' if sel_dash == 'TOTAL BUSHIDO' else 'DEALER'
    with col_d2:
        st.write('')
        st.caption('⚖️ Bobot poin otomatis: **' + ('MDS (sesuai gambar)' if scheme_dash == 'MDS' else 'Dealer (sesuai Excel R-MDS)') + '**')

    man_cur = load_json(KPI_MANUAL_FILE)
    man_d_cur = man_cur.get('dealers', {})
    man_ops_cur = {**DEFAULT_KPI_OPS, **man_cur.get('ops', {})}
    with st.expander('✏️ Input KPI Manual — OPR, MYM, GRT & OPS (belum ada di MASTER KPI)'):
        st.caption('Nilai awal diambil dari file KPI Report (15 Okt 2026). Update sesuai data terbaru lalu klik Simpan. MYM dalam persen (contoh 97.5). OPS bersifat level supervisor dan dipakai untuk semua pilihan.')
        df_man = pd.DataFrame([{'DEALER': d, **{k: safe_float(({**DEFAULT_KPI_MANUAL.get(d, {}), **man_d_cur.get(d, {})}).get(k, 0)) for k in KPI_MANUAL_COLS}} for d in daftar_dealer])
        cfg_man = {'DEALER': st.column_config.TextColumn('DEALER', width='medium')}
        for k in KPI_MANUAL_COLS: cfg_man[k] = st.column_config.NumberColumn(k, format='%.2f' if ('MYM' in k or 'GRT' in k) else '%d')
        ed_man = st.data_editor(df_man, hide_index=True, use_container_width=True, disabled=['DEALER'], column_config=cfg_man, key='editor_kpi_manual')
        c_o1, c_o2, c_o3 = st.columns([1, 1, 2])
        with c_o1: ops_t_in = st.number_input('T. OPS (Operational Supervisor)', value=float(safe_float(man_ops_cur.get('T. OPS'))), step=1.0, key='inp_t_ops')
        with c_o2: ops_r_in = st.number_input('R. OPS (Operational Supervisor)', value=float(safe_float(man_ops_cur.get('R. OPS'))), step=1.0, key='inp_r_ops')
        with c_o3:
            st.write('')
            if st.button('💾 Simpan Input Manual', type='primary', key='btn_save_kpi_manual'):
                cur_m = load_json(KPI_MANUAL_FILE)
                cur_m['dealers'] = {str(r_m['DEALER']): {k: safe_float(r_m[k]) for k in KPI_MANUAL_COLS} for _, r_m in ed_man.iterrows()}
                cur_m['ops'] = {'T. OPS': float(ops_t_in), 'R. OPS': float(ops_r_in)}
                save_json(cur_m, KPI_MANUAL_FILE)
                st.success('✅ Input manual KPI berhasil disimpan!')
                st.rerun()

    inputs_dash = get_dashboard_kpi_inputs()
    rows_sel, s_sel, p_sel, t_sel = kpi_score_entity(inputs_dash[sel_dash], scheme_dash)
    dealer_tbl = []
    for d_k in daftar_dealer:
        r_k, s_k, p_k, t_k = kpi_score_entity(inputs_dash[d_k], scheme_dash)
        dealer_tbl.append({'name': d_k, 'code': KPI_DEALER_CODES.get(d_k, '-'), 'point': t_k, 'grade': kpi_grade(t_k), 'sales': s_k, 'process': p_k, 'achv': {c: r_k[c]['achv'] for c in KPI_CODES}, 'note': kpi_note(p_k)})
    dealer_tbl.sort(key=lambda x_d: (-x_d['point'], -x_d['process']))
    date_lbl_dash = f'{tanggal_akhir} {DASH_ABBR.get(current_month, "")} {current_year}'
    date_short_dash = f'{tanggal_akhir:02d}/{current_month:02d}/{current_year}'
    note_dash = ('Bobot skema MDS (sesuai gambar): OPS level supervisor, nilainya sama untuk semua dealer.' if scheme_dash == 'MDS' else 'Bobot skema Dealer (Excel R-MDS): OPR 15 & OPS 0; STU/MAX/CLS memakai 75% poin dasar.') + ' Kolom NOTE: PROCESS ≥45 tanpa potongan, 30–44 = CUT 30%, <30 = CUT 50%. CONCLUTION tampil mulai tgl 27.'
    dash_html = build_dashboard_kpi_html(sel_dash, date_lbl_dash, date_short_dash, rows_sel, s_sel, p_sel, t_sel, dealer_tbl, sel_dash, tanggal_akhir >= 27, note_dash)
    st.markdown(dash_html, unsafe_allow_html=True)
    cap_dash = f'<div style="width:1320px;background-color:#0E1117;padding:18px 20px;box-sizing:border-box;">{dash_html}</div>'
    render_table_image_buttons('cap_dashboard_kpi', f'Dashboard_KPI_{sel_dash}_Tgl_{tanggal_akhir}', standalone_html=cap_dash)

    koor_focus, cnt_focus = get_focus_entities()
    st.divider()
    render_entity_kpi_dashboard('koor', koor_focus, f'DASHBOARD KPI KOORDINATOR (1 s.d {tanggal_akhir} {periode_bulan_tahun})', 'sel_dash_kpi_koor', date_lbl_dash, date_short_dash)
    st.divider()
    render_entity_kpi_dashboard('counter', cnt_focus, f'DASHBOARD KPI COUNTER (1 s.d {tanggal_akhir} {periode_bulan_tahun})', 'sel_dash_kpi_counter', date_lbl_dash, date_short_dash)

elif menu_pilihan == '🏢 STU':
    col_sel_d, col_sel_k = st.columns(2)
    with col_sel_d: dlr_pil = st.selectbox('🏢 Pilih Dealer untuk Review:', ['TOTAL BUSHIDO'] + daftar_dealer, index=0)
    is_total = (dlr_pil == 'TOTAL BUSHIDO')
    dlr_list = daftar_dealer if is_total else [dlr_pil]

    # --- Dropdown ke-2: filter Koordinator / Counter (default ALL = seluruh tim dealer) ---
    _opt_ent = set()
    if not is_total:
        for _ds, _dc, _kc in [(df_faktur, 'Nama Dealer', 'Koor'), (df_nota, ('Nama Dealer' if (df_nota is not None and 'Nama Dealer' in df_nota.columns) else 'Dealer'), 'Koor'),
                              (df_database, 'Nama_Dealer_Clean', 'Koor'), (df_spk, 'Nama_Dealer_SPK', 'Koor_SPK')]:
            if _ds is not None and not _ds.empty and _dc in _ds.columns and _kc in _ds.columns:
                _opt_ent.update(clean_str(v) for v in _ds.loc[_ds[_dc].isin(dlr_list), _kc].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'LAIN-LAIN'])
    _opt_ent = sorted([e for e in _opt_ent if not e.startswith('COUNTER')]) + sorted([e for e in _opt_ent if e.startswith('COUNTER')])
    _lbl_all = 'ALL (SELURUH DEALER)' if is_total else f'ALL (TIM {dlr_pil})'
    with col_sel_k:
        _sel_ent = st.selectbox('👤 Pilih Koordinator / Counter:', [_lbl_all] + _opt_ent, index=0, key=f'sel_koor_stu_{dlr_pil}', disabled=is_total)
    koor_pil = None if (is_total or _sel_ent == _lbl_all) else _sel_ent

    scope_txt = 'Seluruh Dealer BUSHIDO' if is_total else (f'Khusus Dealer {dlr_pil}' if not koor_pil else f'Khusus {koor_pil} (Dealer {dlr_pil})')
    if koor_pil: dlr_pil = f'{dlr_pil} — {koor_pil}'   # label judul tabel, key widget & cache AI ikut berubah per koordinator/counter
    main_hdr_text = f'DETAIL DEALER — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
    sub_hdr_text = f'Rekapitulasi Terpadu Penjualan, Proses Kerja, SPK Leasing, Penjualan Per Type & Detail Salesman {scope_txt} (Acuan Ideal: DB Quality 30% | STU% 10% | ACC% 50%)'
    st.markdown(f'<div class="main-title">{main_hdr_text}</div><div class="sub-title">{sub_hdr_text}</div>', unsafe_allow_html=True)

    saved_td, saved_tk = load_json(TARGET_DEALER_FILE), load_json(TARGET_KOOR_FILE)
    cd_nota = 'Nama Dealer' if (df_nota is not None and 'Nama Dealer' in df_nota.columns) else 'Dealer'

    f_all = df_faktur[df_faktur['Nama Dealer'].isin(dlr_list)] if (df_faktur is not None and 'Nama Dealer' in df_faktur.columns) else pd.DataFrame()
    f_c = df_fak_curr_g[df_fak_curr_g['Nama Dealer'].isin(dlr_list)] if not df_fak_curr_g.empty else pd.DataFrame()
    f_l = df_fak_lm_g[df_fak_lm_g['Nama Dealer'].isin(dlr_list)] if not df_fak_lm_g.empty else pd.DataFrame()
    n_all = df_nota[df_nota[cd_nota].isin(dlr_list)] if (df_nota is not None and cd_nota in df_nota.columns) else pd.DataFrame()
    n_c = df_nota_curr_g[df_nota_curr_g[cd_nota].isin(dlr_list)] if not df_nota_curr_g.empty else pd.DataFrame()
    n_t = df_nota_tod_g[df_nota_tod_g[cd_nota].isin(dlr_list)] if not df_nota_tod_g.empty else pd.DataFrame()
    db_all = df_database[df_database['Nama_Dealer_Clean'].isin(dlr_list)] if (df_database is not None and 'Nama_Dealer_Clean' in df_database.columns) else pd.DataFrame()
    db_c = df_db_curr_g[df_db_curr_g['Nama_Dealer_Clean'].isin(dlr_list)] if not df_db_curr_g.empty else pd.DataFrame()
    s_all = df_spk[df_spk['Nama_Dealer_SPK'].isin(dlr_list)] if (df_spk is not None and 'Nama_Dealer_SPK' in df_spk.columns) else pd.DataFrame()
    s_c = df_spk_curr_g[df_spk_curr_g['Nama_Dealer_SPK'].isin(dlr_list)] if not df_spk_curr_g.empty else pd.DataFrame()
    s_l = df_spk_lm_g[df_spk_lm_g['Nama_Dealer_SPK'].isin(dlr_list)] if not df_spk_lm_g.empty else pd.DataFrame()

    if koor_pil:   # filter seluruh data tab STU hanya untuk Koordinator / Counter terpilih
        def _kfilt(df_x, col_x): return df_x[df_x[col_x] == koor_pil] if (df_x is not None and not df_x.empty and col_x in df_x.columns) else (df_x if df_x is None else df_x.iloc[0:0])
        f_all, f_c, f_l = _kfilt(f_all, 'Koor'), _kfilt(f_c, 'Koor'), _kfilt(f_l, 'Koor')
        n_all, n_c, n_t = _kfilt(n_all, 'Koor'), _kfilt(n_c, 'Koor'), _kfilt(n_t, 'Koor')
        db_all, db_c = _kfilt(db_all, 'Koor'), _kfilt(db_c, 'Koor')
        s_all, s_c, s_l = _kfilt(s_all, 'Koor_SPK'), _kfilt(s_c, 'Koor_SPK'), _kfilt(s_l, 'Koor_SPK')

    ent_dlr = set()
    for ds, ck in [(f_all, 'Koor'), (n_all, 'Koor'), (db_all, 'Koor'), (s_all, 'Koor_SPK')]:
        if not ds.empty and ck in ds.columns: ent_dlr.update(clean_str(v) for v in ds[ck].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'LAIN-LAIN'])
    gab_ent, lbl_tot, kol_nm = sorted(list(ent_dlr)), ('TOTAL BUSHIDO' if is_total else f'TOTAL ({dlr_pil})'), 'KOOR / COUNTER / DEALER'

    r_tot_p = calc_sales_row(lbl_tot, kol_nm, (get_koor_or_counter_target(koor_pil, saved_tk) if koor_pil else sum(safe_int(saved_td.get(d_t, 0)) for d_t in dlr_list)), f_c, f_l, n_c, n_t)
    r_tot_pr = calc_proses_row(lbl_tot, kol_nm, db_c, len(f_c), n_c)
    r_tot_s = calc_leasing_row(lbl_tot, s_c, s_l, kol_nm)

    rp_all = [calc_sales_row(e, kol_nm, get_koor_or_counter_target(e, saved_tk), f_c[f_c['Koor'] == e] if not f_c.empty else pd.DataFrame(), f_l[f_l['Koor'] == e] if not f_l.empty else pd.DataFrame(), n_c[n_c['Koor'] == e] if not n_c.empty else pd.DataFrame(), n_t[n_t['Koor'] == e] if not n_t.empty else pd.DataFrame()) for e in gab_ent]
    df_p_it = pd.DataFrame(rp_all).sort_values(by=['_pct', 'STU'], ascending=[True, True]).reset_index(drop=True) if rp_all else pd.DataFrame()

    rpr_all = [calc_proses_row(e, kol_nm, db_c[db_c['Koor'] == e] if not db_c.empty else pd.DataFrame(), len(f_c[f_c['Koor'] == e]) if not f_c.empty else 0, (n_c[n_c['Koor'] == e] if not n_c.empty else pd.DataFrame())) for e in gab_ent]
    df_pr_it = pd.DataFrame(rpr_all).sort_values(by=['_stu_pct', 'STU'], ascending=[True, True]).reset_index(drop=True) if rpr_all else pd.DataFrame()

    rs_all = [calc_leasing_row(e, s_c[s_c['Koor_SPK'] == e] if not s_c.empty else pd.DataFrame(), s_l[s_l['Koor_SPK'] == e] if not s_l.empty else pd.DataFrame(), kol_nm) for e in gab_ent]
    df_s_it = pd.DataFrame(rs_all).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True) if rs_all else pd.DataFrame()
    # Frame tampilan Tabel 1-3: jika TOTAL BUSHIDO, baris = per Dealer (kolom sama dengan tabel Koordinator)
    if is_total:
        def _dsub(df_x, col_x, d_x): return df_x[df_x[col_x] == d_x] if (df_x is not None and not df_x.empty and col_x in df_x.columns) else pd.DataFrame()
        rp_d = [calc_sales_row(d, kol_nm, safe_int(saved_td.get(d, 0)), _dsub(f_c, 'Nama Dealer', d), _dsub(f_l, 'Nama Dealer', d), _dsub(n_c, cd_nota, d), _dsub(n_t, cd_nota, d)) for d in daftar_dealer]
        df_p_disp = pd.DataFrame(rp_d).sort_values(by=['_pct', 'STU'], ascending=[True, True]).reset_index(drop=True)
        rpr_d = [calc_proses_row(d, kol_nm, _dsub(db_c, 'Nama_Dealer_Clean', d), len(_dsub(f_c, 'Nama Dealer', d)), _dsub(n_c, cd_nota, d)) for d in daftar_dealer]
        df_pr_disp = pd.DataFrame(rpr_d).sort_values(by=['_stu_pct', 'STU'], ascending=[True, True]).reset_index(drop=True)
        rs_d = [calc_leasing_row(d, _dsub(s_c, 'Nama_Dealer_SPK', d), _dsub(s_l, 'Nama_Dealer_SPK', d), kol_nm) for d in daftar_dealer]
        df_s_disp = pd.DataFrame(rs_d).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True)
    else:
        df_p_disp, df_pr_disp, df_s_disp = df_p_it, df_pr_it, df_s_it

    # Tabel 2 (TOTAL BUSHIDO): tambah kolom SPK & ACC% setelah DB Q
    def _spk_acc_vals(df_x):
        n_spk = len(df_x) if df_x is not None else 0
        ok_x = (df_x is not None and not df_x.empty and 'Status_SPK_Clean' in df_x.columns)
        a_x = int((df_x['Status_SPK_Clean'] == 'DISETUJUI').sum()) if ok_x else 0
        r_x = int((df_x['Status_SPK_Clean'] == 'DITOLAK').sum()) if ok_x else 0
        acc_x = (a_x / (a_x + r_x) * 100.0) if (a_x + r_x) > 0 else 0.0
        return n_spk, f'{acc_x:.2f}%'
    r_tot_pr_disp = dict(r_tot_pr)
    if is_total:
        _pr_spk = {d_x: _spk_acc_vals(_dsub(s_c, 'Nama_Dealer_SPK', d_x)) for d_x in daftar_dealer}
        df_pr_disp = df_pr_disp.copy()
        df_pr_disp['SPK'] = df_pr_disp[kol_nm].map(lambda x_n: _pr_spk.get(x_n, (0, '0.00%'))[0])
        df_pr_disp['ACC%'] = df_pr_disp[kol_nm].map(lambda x_n: _pr_spk.get(x_n, (0, '0.00%'))[1])
        r_tot_pr_disp['SPK'], r_tot_pr_disp['ACC%'] = _spk_acc_vals(s_c)
        _lm_d = {d_x: len(_dsub(s_l, 'Nama_Dealer_SPK', d_x)) for d_x in daftar_dealer}
        _grw = lambda a_c, a_l: f'{(a_c / a_l * 100.0):.2f}%' if a_l > 0 else '0.00%'
        df_pr_disp['SPK LM'] = df_pr_disp[kol_nm].map(lambda x_n: _lm_d.get(x_n, 0))
        df_pr_disp['GROWTH'] = df_pr_disp[kol_nm].map(lambda x_n: _grw(_pr_spk.get(x_n, (0, ''))[0], _lm_d.get(x_n, 0)))
        r_tot_pr_disp['SPK LM'], r_tot_pr_disp['GROWTH'] = len(s_l), _grw(len(s_c), len(s_l))

    sm_set = set()
    for ds in [f_c, n_c, db_c, s_c]:
        if not ds.empty and 'Salesman_Clean' in ds.columns: sm_set.update(clean_str(v) for v in ds['Salesman_Clean'].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'TOTAL'])
    if not sm_set:
        for ds in [f_all, n_all, db_all, s_all]:
            if not ds.empty and 'Salesman_Clean' in ds.columns: sm_set.update(clean_str(v) for v in ds['Salesman_Clean'].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'TOTAL'])

    _act_sm = set()   # acuan file Database: salesman yang sudah tidak ada di Database (resign) tidak ditampilkan walau masih ada di Master Employee / Faktur / SPK
    if df_database is not None and not df_database.empty and 'Salesman_Clean' in df_database.columns:
        _act_sm = set(clean_str(v) for v in df_database['Salesman_Clean'].dropna().unique() if clean_str(v))
    if _act_sm: sm_set = {m for m in sm_set if m in _act_sm}

    r_sm, t_sa, t_sr = [], 0, 0
    for sm in sorted(list(sm_set)):
        targ, stu = get_auto_sales_target(sm), (len(f_c[f_c['Salesman_Clean'] == sm]) if (not f_c.empty and 'Salesman_Clean' in f_c.columns) else 0)
        pct_sm = (stu / targ * 100.0) if targ > 0 else 0.0
        sdb = db_c[db_c['Salesman_Clean'] == sm] if (not db_c.empty and 'Salesman_Clean' in db_c.columns) else pd.DataFrame()
        db_v, hot_v = len(sdb), (len(sdb[sdb['Data_Type_Clean'] == 'DEAL PROSPECT']) if (not sdb.empty and 'Data_Type_Clean' in sdb.columns) else 0)
        sspk = s_c[s_c['Salesman_Clean'] == sm] if (not s_c.empty and 'Salesman_Clean' in s_c.columns) else pd.DataFrame()
        spk_v, acc_v, rej_v = len(sspk), (len(sspk[sspk['Status_SPK_Clean'] == 'DISETUJUI']) if (not sspk.empty and 'Status_SPK_Clean' in sspk.columns) else 0), (len(sspk[sspk['Status_SPK_Clean'] == 'DITOLAK']) if (not sspk.empty and 'Status_SPK_Clean' in sspk.columns) else 0)
        t_sa += acc_v; t_sr += rej_v
        dbq_v, stup_v, acc_p_v = (hot_v / db_v * 100.0 if db_v > 0 else 0.0), (stu / db_v * 100.0 if db_v > 0 else 0.0), (acc_v / (acc_v + rej_v) * 100.0 if (acc_v + rej_v) > 0 else 0.0)
        lm_v = len(f_l[f_l['Salesman_Clean'] == sm]) if (not f_l.empty and 'Salesman_Clean' in f_l.columns) else 0
        r_sm.append({'NAMA SALESMAN': sm, 'TARGET': targ, 'STU': stu, col_name_pct: f'{pct_sm:.2f}%', 'AVG DB': f'{(db_v/hari_aktif):.2f}', 'DB': db_v, 'HOT': hot_v, 'DB Q': f'{dbq_v:.2f}%', 'SPK': spk_v, 'ACC%': f'{acc_p_v:.2f}%', 'STU%': f'{stup_v:.2f}%', 'LM': lm_v, '_lm_val': lm_v, '_gap_lm': stu - lm_v, '_stu_val': stu, '_db_val': db_v, '_pct_val': pct_sm, '_dbq_val': dbq_v, '_stup_val': stup_v, '_acc_val': acc_p_v})

    forc_pct_dlr = (r_tot_p['FORC'] / r_tot_p['TARGET'] * 100.0) if r_tot_p['TARGET'] > 0 else 0.0
    nota_tot_now = safe_int(r_tot_p['NOTA'])
    _nm_tot = nota_metrics(n_c)
    div_7, div_3, n7_cnt, n3_cnt = _nm_tot['d7'], _nm_tot['d3'], _nm_tot['n7'], _nm_tot['n3']
    avg_nota_v, avg7_v, avg3_v = _nm_tot['avg'], _nm_tot['avg7'], _nm_tot['avg3']
    sisa_hari_bln = SISA_HARI_KERJA
    forc_nota_v, forc7_v, forc3_v = _nm_tot['f_nota'], _nm_tot['f7'], _nm_tot['f3']

    C_GRN, C_YEL, C_RED, C_CYN = '#00FF66', '#FFEA00', '#FF4D8D', '#00E5FF'
    def _stat_col(v, good, warn): return C_GRN if v >= good else (C_YEL if v >= warn else C_RED)
    def _kpi_card(icon, label, value, sub, color):
        _pg = _KPI_PROG.get(label, (None, None))
        return bsg_card(icon, label, value, sub, color, _pg[0], _pg[1])
    def _kpi_grid(cards): return '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:12px;">' + ''.join(cards) + '</div>'
    def _unit(txt): return f'<span style="font-size:13px;font-weight:600;color:#94A3B8;"> {txt}</span>'
    def _trend(v, ref):
        if v > ref: return f'<span style="color:{C_GRN};font-weight:800;">▲ naik</span> vs AVG NOTA'
        if v < ref: return f'<span style="color:{C_RED};font-weight:800;">▼ turun</span> vs AVG NOTA'
        return '▬ sama dengan AVG NOTA'
    def _forc_card(icon, label, forc_v, avg_v):
        tg = safe_int(r_tot_p['TARGET'])
        pct_f = (forc_v / tg * 100.0) if tg > 0 else None
        col_f = _stat_col(pct_f, 100.0, 85.0) if pct_f is not None else C_CYN
        sub_f = f'{nota_tot_now:,} + {avg_v:.2f} × {sisa_hari_bln} hari kerja' + (f'<br><b style="color:{col_f};">{pct_f:.1f}%</b> dari target {tg:,}' if pct_f is not None else '')
        return _kpi_card(icon, label, f'{forc_v:,}' + _unit('nota'), sub_f, col_f)

    _dbq_n, _stup_n, _acc_n = safe_float(r_tot_pr['DB Q']), safe_float(r_tot_pr['STU%']), safe_float(r_tot_s['ACC%'])
    _grw_n = safe_float(r_tot_s['GROWTH'])
    _KPI_PROG = {'Target vs Result': (min(r_tot_p['_pct'], 100.0), target_persen_harian), 'DB Quality': bsg_ach_bar(_dbq_n, 30.0), 'STU Ratio': bsg_ach_bar(_stup_n, 10.0),
                 'SPK Growth': bsg_ach_bar(_grw_n, 100.0), 'Approval': bsg_ach_bar(_acc_n, 50.0), 'Forecast Closing': (min(forc_pct_dlr, 100.0), None)}
    kpi_cards_row1 = [
        _kpi_card('🎯', 'Target vs Result', f"{r_tot_p['TARGET']:,} / {r_tot_p['STU']:,}", f"<b>{r_tot_p['_pct']:.1f}%</b> tercapai · Ideal {r_tot_p['IDEAL']:,}<br>Nota {r_tot_p['NOTA']:,} · Tgl {tanggal_akhir} ({col_name_pct})", C_GRN if r_tot_p['STU'] >= r_tot_p['IDEAL'] else (C_YEL if r_tot_p['STU'] >= 0.85 * r_tot_p['IDEAL'] else C_RED)),
        _kpi_card('✨', 'DB Quality', r_tot_pr['DB Q'], f"HOT {r_tot_pr['HOT']:,} / {r_tot_pr['DB']:,} DB<br>Ideal 30%", _stat_col(_dbq_n, 30.0, 20.0)),
        _kpi_card('📈', 'STU Ratio', r_tot_pr['STU%'], f"STU {r_tot_pr['STU']:,} / {r_tot_pr['DB']:,} DB<br>Ideal 10%", _stat_col(_stup_n, 10.0, 7.0)),
        _kpi_card('🚀', 'SPK Growth', r_tot_s['GROWTH'], f"SPK {r_tot_s['SPK']:,} vs LM {r_tot_s['SPK LM']:,}", _stat_col(_grw_n, 100.0, 80.0)),
        _kpi_card('✅', 'Approval', r_tot_s['ACC%'], f"Open SPK {r_tot_s['TERBUKA']:,}<br>Ideal 50%", _stat_col(_acc_n, 50.0, 40.0)),
        _kpi_card('🏁', 'Forecast Closing', f"{r_tot_p['FORC']:,}" + _unit('unit'), f"<b>{forc_pct_dlr:.1f}%</b> dari target", _stat_col(forc_pct_dlr, 100.0, 85.0)),
    ]
    kpi_cards_row2 = [
        _kpi_card('📊', 'AVG NOTA', f'{avg_nota_v:.2f}' + _unit('/ hari'), f'{nota_tot_now:,} nota ÷ {hari_aktif} hari kerja<br>tgl 1–{tanggal_akhir} (tanpa Minggu & libur)', C_CYN),
        _kpi_card('⚡', 'AVG 7', f'{avg7_v:.2f}' + _unit('/ hari'), f'{n7_cnt:,} nota ÷ {div_7} hari kerja<br>{_trend(avg7_v, avg_nota_v)}', C_GRN if avg7_v >= avg_nota_v else C_RED),
        _kpi_card('🔥', 'AVG 3', f'{avg3_v:.2f}' + _unit('/ hari'), f'{n3_cnt:,} nota ÷ {div_3} hari kerja<br>{_trend(avg3_v, avg_nota_v)}', C_GRN if avg3_v >= avg_nota_v else C_RED),
        _forc_card('🧮', 'Forc Nota', forc_nota_v, avg_nota_v),
        _forc_card('⚡', 'Forc 7', forc7_v, avg7_v),
        _forc_card('🔥', 'Forc 3', forc3_v, avg3_v),
    ]
    kpi_cards_html = _kpi_grid(kpi_cards_row1) + _kpi_grid(kpi_cards_row2)
    st.markdown(kpi_cards_html, unsafe_allow_html=True)

    df_koor_only, df_cnt_only = pd.DataFrame(), pd.DataFrame()
    if not df_p_it.empty:
        df_koor_only = df_p_it[~df_p_it[kol_nm].str.upper().str.startswith('COUNTER')].copy()
        df_cnt_only = df_p_it[df_p_it[kol_nm].str.upper().str.startswith('COUNTER')].sort_values(by=['_pct', 'STU'], ascending=[True, True])

    def _focus_ent_html(df_ent, empty_msg):
        if df_ent is None or df_ent.empty: return empty_msg
        ev_list = []
        for _, rk in df_ent.iterrows():
            knm = str(rk[kol_nm])
            k_pr = df_pr_it[df_pr_it[kol_nm] == knm].iloc[0] if (not df_pr_it.empty and knm in df_pr_it[kol_nm].values) else {}
            k_sp = df_s_it[df_s_it[kol_nm] == knm].iloc[0] if (not df_s_it.empty and knm in df_s_it[kol_nm].values) else {}
            ev_list.append({'nama': knm, 'target': safe_int(rk['TARGET']), 'ideal': safe_int(rk['IDEAL']), 'stu': safe_int(rk['STU']), 'pct': safe_float(rk['_pct']), 'db': safe_int(k_pr.get('DB', 0)), 'dbq_str': k_pr.get('DB Q', '0.00%'), 'stup_str': k_pr.get('STU%', '0.00%'), 'spk_grw_str': k_sp.get('GROWTH', '0.00%'), 'acc_str': k_sp.get('ACC%', '0.00%'), 'dbq_val': safe_float(k_pr.get('DB Q', 0.0)), 'stup_val': safe_float(k_pr.get('STU%', 0.0)), 'acc_val': safe_float(k_sp.get('_acc_val', 0.0))})
        ev_list.sort(key=lambda x: (0 if x['target'] > 0 else 1, x['pct'], x['stu'], x['stup_val'], x['dbq_val'], x['acc_val']))
        fk = ev_list[0]
        return f"<span style='color:#FFEA00;font-weight:800;'>{fk['nama']}</span> — Target vs Result: <b>{fk['target']}/{fk['stu']} ({fk['pct']:.2f}% | Ideal: {fk['ideal']})</b> | DB Quality: <b>{fk['dbq_str']}</b> | STU Ratio: <b>{fk['stup_str']}</b> | SPK Growth: <b>{fk['spk_grw_str']}</b> | Approval: <b>{fk['acc_str']}</b>"
    focus_koor_html = _focus_ent_html(df_koor_only, "Tidak ada data Koordinator")
    focus_cnt_html = _focus_ent_html(df_cnt_only, "Tidak ada data Counter")

    focus_sm_html = "Tidak ada Salesman aktif (Non-Counter dengan DB >= 2)"
    if r_sm:
        df_sm_all = pd.DataFrame(r_sm)
        df_sm_valid = df_sm_all[(~df_sm_all['NAMA SALESMAN'].apply(is_counter_personnel)) & (df_sm_all['_db_val'] >= 2)].copy()
        if not df_sm_valid.empty:
            df_sm_valid['has_t'] = df_sm_valid['TARGET'].apply(lambda x: 0 if x > 0 else 1)
            df_sm_valid = df_sm_valid.sort_values(by=['has_t', '_pct_val', '_stu_val', '_stup_val', '_dbq_val', '_acc_val', '_db_val'], ascending=[True]*7).reset_index(drop=True)
            fs = df_sm_valid.iloc[0]
            fs_idl = round(safe_int(fs['TARGET']) * persen_desimal)
            focus_sm_html = f"<span style='color:#FFEA00;font-weight:800;'>{fs['NAMA SALESMAN']}</span> — Target vs Result: <b>{fs['TARGET']}/{fs['STU']} ({fs[col_name_pct]} | Ideal: {fs_idl})</b> | DB: <b>{fs['DB']}</b> (DB Quality: <b>{fs['DB Q']}</b>) | STU Ratio: <b>{fs['STU%']}</b> | SPK: <b>{fs['SPK']}</b> (Approval: <b>{fs['ACC%']}</b>)"

    focus_walk_html = 'Tidak ada data Walk In pada periode ini'
    if db_c is not None and not db_c.empty and db_c.shape[1] > 6 and 'Koor' in db_c.columns:
        _wi_all = db_c[db_c.iloc[:, 6].apply(alnum_str) == 'WALKIN']
        if not _wi_all.empty:
            _wi_rows = []
            for e_w, g_w in _wi_all.groupby('Koor'):
                if clean_str(e_w) in ['', 'LAIN-LAIN', 'NAN', 'NONE']: continue
                n_w = len(g_w); s_w = int((g_w['STU'] == 'STU').sum()) if 'STU' in g_w.columns else 0
                _wi_rows.append((clean_str(e_w), n_w, s_w, n_w - s_w))
            _wi_rows.sort(key=lambda x: (-x[3], x[2]))
            _t_n, _t_s = len(_wi_all), (int((_wi_all['STU'] == 'STU').sum()) if 'STU' in _wi_all.columns else 0)
            if _wi_rows:
                f_w = _wi_rows[0]
                focus_walk_html = (f"<span style='color:#FFEA00;font-weight:800;'>{f_w[0]}</span> — DB Walk In: <b>{f_w[1]}</b> | STU: <b>{f_w[2]}</b> | Selisih: <b>{f_w[3]}</b> (STU% Walk In: <b>{(f_w[2] / f_w[1] * 100.0 if f_w[1] else 0.0):.2f}%</b>)"
                                   f" | Total {scope_txt}: DB Walk In <b>{_t_n}</b>, STU <b>{_t_s}</b>, Selisih <b>{_t_n - _t_s}</b>")

    st.markdown(f"""<div class="focus-alert-box"><div>🎯 <b>Focus Koordinator :</b> {focus_koor_html}</div><div style="margin-top:4px;">🏪 <b>Focus Counter :</b> {focus_cnt_html}</div><div style="margin-top:4px;">🚶 <b>Focus Walk In :</b> {focus_walk_html}</div><div style="margin-top:4px;">👤 <b>Focus Salesman :</b> {focus_sm_html}</div></div>""", unsafe_allow_html=True)

    _tbl_counter = [0]
    def nxt_no():
        _tbl_counter[0] += 1
        return _tbl_counter[0]

    tab_rk, tab_pp, tab_sl, tab_sm, tab_an = st.tabs(['📌 Ringkasan Visual', '💼 Penjualan & Proses', '🏦 SPK, Leasing & Type', '👤 Salesman & Konsumen', '🧠 Analisa & Action Plan'])
    with tab_rk:
        bsg_safe(bsg_render_ringkasan, dict(kol_nm=kol_nm, ideal_pct=target_persen_harian, tanggal_akhir=tanggal_akhir, max_day=max_day_in_month, df_p_disp=df_p_disp, df_pr_disp=df_pr_disp,
                 df_s_disp=df_s_disp, r_tot_p=r_tot_p, r_tot_pr=r_tot_pr, r_tot_s=r_tot_s, f_c=f_c, s_c=s_c, is_total=is_total, scope_key=dlr_pil,
                 period_key=f'{current_year}-{current_month}', dlr_label=dlr_pil, sisa_hari=SISA_HARI_KERJA, hari_aktif=hari_aktif), label='Ringkasan visual')
    with tab_pp:
        jdl_rev_1 = f'{nxt_no()}. TABEL PENJUALAN — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_1}</div>', unsafe_allow_html=True)
        kol_pj = [kol_nm, 'TARGET', 'IDEAL', 'STU', 'NOTA', 'TODAY', col_name_pct, 'GAP TG', 'STU LM', '% LM', 'GAP LM', 'FORC', 'F. NOTA', 'FORC 7', 'FORC 3']
        df_p_full = pd.concat([df_p_disp, pd.DataFrame([r_tot_p])], ignore_index=True)

        tbl1_only_html = build_compact_html_string(df_p_disp, df_p_full, kol_pj, kol_nm, '_pct', f'cap_tbl1_inner_{dlr_pil}', title_text=None)
        custom_cap_tbl1 = f"""<div style="width:1320px;background-color:#0E1117;padding:20px 24px;font-family:'Source Sans Pro',sans-serif;color:#FFFFFF;box-sizing:border-box;">
        <div style="font-size:38px;font-weight:800;color:#4318FF;margin-bottom:4px;line-height:1.1;">{main_hdr_text}</div>
        <div style="font-size:14px;font-weight:600;color:#64748B;margin-bottom:18px;">{sub_hdr_text}</div>
        {kpi_cards_html}
        <div style="margin-top:12px;margin-bottom:18px;padding:11px 16px;background:linear-gradient(90deg,rgba(255,0,127,0.14) 0%,rgba(14,17,23,0.95) 100%);border-left:4px solid #FF007F;border-top:1px solid #2D3748;border-right:1px solid #2D3748;border-bottom:1px solid #2D3748;border-radius:6px;font-size:13.5px;line-height:1.65;color:#E2E8F0;">
            <div>🎯 <b>Focus Koordinator :</b> {focus_koor_html}</div>
            <div style="margin-top:4px;">🏪 <b>Focus Counter :</b> {focus_cnt_html}</div>
            <div style="margin-top:4px;">🚶 <b>Focus Walk In :</b> {focus_walk_html}</div>
            <div style="margin-top:4px;">👤 <b>Focus Salesman :</b> {focus_sm_html}</div>
        </div>
        <hr style="border:none;border-top:1px solid #2D3748;margin:16px 0;">
        <div style="font-size:21px;font-weight:700;color:#4318FF;margin-bottom:10px;">{jdl_rev_1}</div>
        {tbl1_only_html}
    </div>"""
        render_compact_html_table(df_p_disp, df_p_full, kol_pj, kol_nm, '_pct', key_suffix=f'Review_1_Penjualan_{dlr_pil}', title_text=jdl_rev_1, custom_capture_html=custom_cap_tbl1)

        if is_total:
            st.divider()
            jdl_rev_1b = f'{nxt_no()}. TABEL PENJUALAN KOORDINATOR & COUNTER PER DEALER — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
            st.markdown(f'<div class="section-title">{jdl_rev_1b}</div>', unsafe_allow_html=True)
            rows_1b_items, rows_1b_full = [], []
            for d_g in list(df_p_disp[kol_nm]):
                f_c_d, f_l_d = _dsub(f_c, 'Nama Dealer', d_g), _dsub(f_l, 'Nama Dealer', d_g)
                n_c_d, n_t_d = _dsub(n_c, cd_nota, d_g), _dsub(n_t, cd_nota, d_g)
                ents_d = set()
                for ds_g, ck_g, dc_g in [(f_all, 'Koor', 'Nama Dealer'), (n_all, 'Koor', cd_nota), (db_all, 'Koor', 'Nama_Dealer_Clean'), (s_all, 'Koor_SPK', 'Nama_Dealer_SPK')]:
                    sub_g = _dsub(ds_g, dc_g, d_g)
                    if not sub_g.empty and ck_g in sub_g.columns: ents_d.update(clean_str(v) for v in sub_g[ck_g].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE'])
                rows_e = []
                for e_g in sorted(ents_d):
                    r_e = calc_sales_row(e_g, kol_nm, get_koor_or_counter_target(e_g, saved_tk), _dsub(f_c_d, 'Koor', e_g), _dsub(f_l_d, 'Koor', e_g), _dsub(n_c_d, 'Koor', e_g), _dsub(n_t_d, 'Koor', e_g))
                    if r_e['TARGET'] == 0 and r_e['STU'] == 0 and r_e['NOTA'] == 0 and r_e['STU LM'] == 0: continue
                    rows_e.append(r_e)
                rows_e.sort(key=lambda r_z: (0 if r_z['TARGET'] > 0 else 1, r_z['_pct'], r_z['STU']))
                rows_1b_items.extend(rows_e)
                rows_1b_full.extend(rows_e)
                rows_1b_full.append(calc_sales_row(f'SUB TOTAL {d_g}', kol_nm, safe_int(saved_td.get(d_g, 0)), f_c_d, f_l_d, n_c_d, n_t_d))
            if rows_1b_items:
                df_1b_items = pd.DataFrame(rows_1b_items)
                df_1b_full = pd.concat([pd.DataFrame(rows_1b_full), pd.DataFrame([r_tot_p])], ignore_index=True)
                render_compact_html_table(df_1b_items, df_1b_full, kol_pj, kol_nm, '_pct', key_suffix=f'Review_1B_Koor_Counter_Per_Dealer_{dlr_pil}', title_text=jdl_rev_1b)
            else:
                st.info('ℹ️ Belum ada data Koordinator / Counter pada periode ini.')

        st.divider()
        jdl_rev_2 = f'{nxt_no()}. TABEL PROSES KERJA — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_2}</div>', unsafe_allow_html=True)
        kol_pr = [kol_nm, 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'SPK LM', 'GROWTH', 'STU', 'STU%', 'AVG NOTA', 'AVG 7', 'AVG 3'] if is_total else [kol_nm, 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'STU', 'STU%', 'AVG NOTA', 'AVG 7', 'AVG 3']
        render_compact_html_table(df_pr_disp, pd.concat([df_pr_disp, pd.DataFrame([r_tot_pr_disp])], ignore_index=True), kol_pr, kol_nm, '_stu_pct', key_suffix=f'Review_2_Proses_{dlr_pil}', title_text=jdl_rev_2)

        with st.expander('🔍 Rekonsiliasi Jumlah Database (cek selisih KPI vs Tabel Proses vs file asli)', expanded=False):
            _rc_rows = []
            _raw_by_dlr = {}
            for p_db in (paths_database or []):
                d_n = normalize_dealer_name(os.path.splitext(os.path.basename(p_db))[0]) or 'TIDAK DIKETAHUI'
                _raw_by_dlr[d_n] = _raw_by_dlr.get(d_n, 0) + db_file_rawcount(p_db, get_file_mtime(p_db))
            _da = df_database_alldlr if (df_database_alldlr is not None and not df_database_alldlr.empty) else pd.DataFrame()
            for d_n in sorted(set(list(_raw_by_dlr.keys()) + (list(_da['Nama_Dealer_Clean'].unique()) if not _da.empty else []))):
                g_d = _da[_da['Nama_Dealer_Clean'] == d_n] if not _da.empty else pd.DataFrame()
                in_m = g_d[(g_d['bulan'] == current_month) & (g_d['tahun'] == current_year)] if (not g_d.empty and 'bulan' in g_d.columns) else g_d
                in_p = in_m[in_m['hari'] <= tanggal_akhir] if (not in_m.empty and 'hari' in in_m.columns) else in_m
                _rc_rows.append({'DEALER': d_n + ('' if d_n in daftar_dealer else '  (di luar daftar dealer → tidak dihitung)'), 'BARIS FILE (MENTAH)': _raw_by_dlr.get(d_n, 0), 'TERBACA': len(g_d),
                                 'TANGGAL TAK TERBACA': int(g_d['Tanggal_Parsed'].isna().sum()) if (not g_d.empty and 'Tanggal_Parsed' in g_d.columns) else 0,
                                 'BULAN INI (SEMUA TGL)': len(in_m), f'S.D TGL {tanggal_akhir}': len(in_p),
                                 'KOOR TAK TERPETAKAN (LAIN-LAIN)': int((in_p['Koor'] == 'LAIN-LAIN').sum()) if (not in_p.empty and 'Koor' in in_p.columns) else 0})
            if _rc_rows:
                _rc_df = pd.DataFrame(_rc_rows)
                _rc_tot = {c: (_rc_df[c].sum() if c != 'DEALER' else 'TOTAL') for c in _rc_df.columns}
                st.dataframe(pd.concat([_rc_df, pd.DataFrame([_rc_tot])], ignore_index=True), hide_index=True, use_container_width=True)
            _kpi_sum_koor = sum(len(df_db_curr_g[df_db_curr_g['Koor'] == e_k]) for e_k in gab_ent) if not df_db_curr_g.empty else 0
            st.caption(f'Tabel Proses (TOTAL) = {len(db_c):,} baris | jumlah per koordinator/counter (dipakai KPI) = {_kpi_sum_koor:,} baris. Selisih keduanya = baris yang koordinatornya tidak terpetakan (LAIN-LAIN) — salesman perlu dilengkapi di Lookup. '
                       'Baris tanpa Customer Name tetap dihitung bila tanggal prospeknya valid; baris dengan tanggal tak terbaca tidak masuk periode.')

        st.divider()
        jdl_rev_pt = f'{nxt_no()}. TABEL REVIEW AKTIFITAS (PROSPECT TYPE) — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_pt}</div>', unsafe_allow_html=True)
        def _act_vals(d_x):
            n_db = len(d_x)
            n_hot = int(d_x['Data_Type_Clean'].isin(['DEAL PROSPECT', 'SEAL PROSPECT']).sum()) if (n_db and 'Data_Type_Clean' in d_x.columns) else 0
            n_stu = int((d_x['STU'] == 'STU').sum()) if (n_db and 'STU' in d_x.columns) else 0
            return n_db, n_hot, (n_hot / n_db * 100.0 if n_db else 0.0), n_stu, (n_stu / n_db * 100.0 if n_db else 0.0)
        _ACT_TGT_PCT = {'EVENT': 30, 'WALKIN': 20, 'MEDIASOSIAL': 25, 'EVENTNONNACS': 10, 'KUNJUNGANRUMAH': 10, 'SERVICE': 5}   # % dari target total
        def _act_pct(nm):
            a_n = alnum_str(nm)
            if a_n in _ACT_TGT_PCT: return _ACT_TGT_PCT[a_n]
            if 'SOSMED' in a_n or 'MEDIASOSIAL' in a_n: return 25
            if 'NONNACS' in a_n: return 10
            return None
        _act_tgt_total = safe_int(r_tot_p['TARGET'])
        def _act_table(db_df, grp, name_col, tot_label, with_target=False):
            rows = []
            for g_v in grp.unique():
                v_a = _act_vals(db_df[grp == g_v])
                r_a = {name_col: g_v, 'DB': v_a[0], 'HOT': v_a[1], 'DB Q': f'{v_a[2]:.2f}%', 'STU': v_a[3], 'STU%': f'{v_a[4]:.2f}%', '_stu_pct': v_a[4]}
                if with_target:
                    pc = _act_pct(g_v); tg = int(round(_act_tgt_total * pc / 100.0)) if pc is not None else 0
                    r_a['TARGET'] = tg if pc is not None else '-'
                    r_a['ACHIEV'] = (f'{(v_a[3] / tg * 100.0):.2f}%' if tg > 0 else '0.00%') if pc is not None else '-'
                rows.append(r_a)
            df_i = pd.DataFrame(rows).sort_values(by=['DB'], ascending=[False]).reset_index(drop=True)
            v_t = _act_vals(db_df)
            tot = {name_col: tot_label, 'DB': v_t[0], 'HOT': v_t[1], 'DB Q': f'{v_t[2]:.2f}%', 'STU': v_t[3], 'STU%': f'{v_t[4]:.2f}%', '_stu_pct': v_t[4]}
            if with_target: tot['TARGET'], tot['ACHIEV'] = _act_tgt_total, (f'{(v_t[3] / _act_tgt_total * 100.0):.2f}%' if _act_tgt_total > 0 else '0.00%')
            return df_i, pd.concat([df_i, pd.DataFrame([tot])], ignore_index=True)
        _kol_act = ['DB', 'HOT', 'DB Q', 'STU', 'STU%']
        _kol_act_pt = ['TARGET', 'STU', 'ACHIEV', 'DB', 'HOT', 'DB Q', 'STU%']
        _jdl_sub_base = f'{nxt_no()}. TABEL SUB PROSPECT TYPE — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        if db_c is None or db_c.empty or db_c.shape[1] < 8:
            st.info('ℹ️ Belum ada data Database pada periode ini.')
            st.divider()
            st.markdown(f'<div class="section-title">{_jdl_sub_base}</div>', unsafe_allow_html=True)
            st.info('ℹ️ Belum ada data Database pada periode ini.')
        else:
            _pt_g = db_c.iloc[:, 6].apply(lambda v: clean_str(v) or '(KOSONG)')   # kolom G = Prospect Type
            _st_g = db_c.iloc[:, 7].apply(lambda v: strip_sub_code(v) or '(KOSONG)')   # kolom H = Sub Prospect Type (tanpa kode di depan)
            _df_pt_i, _df_pt_f = _act_table(db_c, _pt_g, 'PROSPECT TYPE', lbl_tot, with_target=True)
            render_compact_html_table(_df_pt_i, _df_pt_f, ['PROSPECT TYPE'] + _kol_act_pt, 'PROSPECT TYPE', '_stu_pct', key_suffix=f'Review_Aktifitas_PT_{dlr_pil}', title_text=jdl_rev_pt)

            st.divider()
            st.markdown(f'<div class="section-title">{_jdl_sub_base}</div>', unsafe_allow_html=True)
            _opt_pt = list(_df_pt_i['PROSPECT TYPE'])
            _sel_pt = st.selectbox('📂 Pilih Prospect Type:', _opt_pt, index=0, key=f'sel_sub_pt_{dlr_pil}')
            _db_sel = db_c[_pt_g == _sel_pt]
            _df_sub_i, _df_sub_f = _act_table(_db_sel, _st_g[_pt_g == _sel_pt], 'SUB PROSPECT TYPE', f'TOTAL {_sel_pt}')
            render_compact_html_table(_df_sub_i, _df_sub_f, ['SUB PROSPECT TYPE'] + _kol_act, 'SUB PROSPECT TYPE', '_stu_pct', key_suffix=f'Review_Aktifitas_Sub_{dlr_pil}_{_sel_pt}', title_text=f'{_jdl_sub_base} — {_sel_pt}', wrap_first=True)

    with tab_sl:
        jdl_rev_3 = f'{nxt_no()}. TABEL SPK & LEASING — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_3}</div>', unsafe_allow_html=True)
        kol_sp = [kol_nm, 'SPK', 'SPK LM', 'GROWTH', 'ACC%', 'TERBUKA', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF', 'IMFI', '%IMFI']
        render_compact_html_table(df_s_disp, pd.concat([df_s_disp, pd.DataFrame([r_tot_s])], ignore_index=True), kol_sp, kol_nm, '_acc_val', key_suffix=f'Review_3_Leasing_{dlr_pil}', title_text=jdl_rev_3)
        bsg_safe(bsg_render_leasing_charts, df_s_disp, r_tot_s, kol_nm, label="Grafik leasing")

        st.divider()
        sfx4 = ' & PER DEALER' if is_total else ''
        jdl_rev_4 = f'{nxt_no()}. TABEL PENJUALAN PER TYPE{sfx4} — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_4}</div>', unsafe_allow_html=True)
        TYPE_TGT_PCT = {'AT PREMIUM': 60, 'AT CLASSY': 25, 'AT LPM': 10, 'MOPED': 3, 'OTHERS': 2}   # % dari target total (dealer / total sesuai dropbox)
        TYPE_ORDER = list(TYPE_TGT_PCT.keys())
        kol_t_d = ['TYPE', 'TARGET', 'STU', 'ACHIEV', 'LM', 'GROWTH', 'DB', 'HOT', 'DB Q', 'STU CASH', 'STU BAF', 'STU ADIRA', 'STU SOF']
        _tgt_total = safe_int(r_tot_p['TARGET'])
        def _grp_type(d_x):
            if d_x is None or d_x.empty or 'Type_Clean' not in d_x.columns: return d_x
            d_x = d_x.copy(); d_x['Type_Grp'] = d_x['Type_Clean'].where(d_x['Type_Clean'].isin(['AT PREMIUM', 'AT CLASSY', 'AT LPM', 'MOPED']), 'OTHERS')
            return d_x
        def _add_tgt(df_x, tgt_fn):
            if df_x is None or df_x.empty: return df_x
            df_x = df_x.copy()
            df_x['TARGET'] = [tgt_fn(str(v)) for v in df_x['TYPE']]
            df_x['ACHIEV'] = [f'{(safe_int(a) / t * 100.0):.2f}%' if t > 0 else '0.00%' for a, t in zip(df_x['STU'], df_x['TARGET'])]
            df_x['LM'] = df_x['STU LM']   # 'STU LM' tetap dipertahankan (dipakai tabel Analisa)
            return df_x
        f_cg, f_lg, db_cg, s_cg = _grp_type(f_c), _grp_type(f_l), _grp_type(db_c), _grp_type(s_c)
        df_td_i, df_td_f, _ = build_type_table(f_cg, f_lg, db_cg, s_cg, [(k, 'Type_Grp', 'Type_Grp', 'Type_Grp') for k in TYPE_ORDER], 'TYPE', tot_label=lbl_tot, sort_by_growth=True)
        _tfn = lambda nm: _tgt_total if nm == lbl_tot else int(round(_tgt_total * TYPE_TGT_PCT.get(nm, 0) / 100.0))
        df_td_i, df_td_f = _add_tgt(df_td_i, _tfn), _add_tgt(df_td_f, _tfn)
        if not df_td_f.empty and is_total:
            rows_t_full = []
            for _, tr_row in df_td_i.iterrows():
                kt_n = str(tr_row['TYPE'])
                r_type = tr_row.to_dict(); r_type['_row_ratio'] = float('nan')
                rows_t_full.append(r_type)
                di_t, _, _ = build_type_table(f_cg[f_cg['Type_Grp'] == kt_n] if not f_cg.empty else pd.DataFrame(), f_lg[f_lg['Type_Grp'] == kt_n] if not f_lg.empty else pd.DataFrame(), db_cg[db_cg['Type_Grp'] == kt_n] if not db_cg.empty else pd.DataFrame(), s_cg[s_cg['Type_Grp'] == kt_n] if not s_cg.empty else pd.DataFrame(), [(d_x, 'Nama Dealer', 'Nama_Dealer_Clean', 'Nama_Dealer_SPK') for d_x in daftar_dealer], 'TYPE', sort_by_growth=True)
                if di_t.empty: continue
                di_t = _add_tgt(di_t, lambda nm, _k=kt_n: int(round(safe_int(saved_td.get(nm, 0)) * TYPE_TGT_PCT.get(_k, 0) / 100.0)))
                g_min, g_max = float(di_t['_growth_val'].min()), float(di_t['_growth_val'].max())
                for j_t, r_dt in di_t.iterrows():
                    rd_t = r_dt.to_dict()
                    rd_t['_row_ratio'] = ((float(r_dt['_growth_val']) - g_min) / (g_max - g_min)) if g_max > g_min else (j_t / max(1, len(di_t) - 1))
                    rows_t_full.append(rd_t)
            r_tot_type = df_td_f.iloc[-1].to_dict(); r_tot_type['_row_ratio'] = float('nan')
            rows_t_full.append(r_tot_type)
            render_compact_html_table(df_td_i, pd.DataFrame(rows_t_full), kol_t_d, 'TYPE', '_growth_val', key_suffix=f'Review_4_Type_{dlr_pil}', title_text=jdl_rev_4, highlight_names=set(TYPE_ORDER))
        elif not df_td_f.empty: render_compact_html_table(df_td_i, df_td_f, kol_t_d, 'TYPE', '_growth_val', key_suffix=f'Review_4_Type_{dlr_pil}', title_text=jdl_rev_4)
        bsg_safe(bsg_render_type_charts, df_td_i, target_persen_harian, label="Grafik type")

    with tab_sm:
        jdl_rev_5 = f'{nxt_no()}. TABEL DETAIL SALESMAN — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_5}</div>', unsafe_allow_html=True)
        if len(mapping_emp_target) <= len(FIXED_COUNTER_TARGETS): st.warning('⚠️ File Master Employee belum diunggah. Silakan unggah di menu **📁 UPLOAD FILE** agar kolom TARGET otomatis terisi.')
        kol_sm = ['NAMA SALESMAN', 'TARGET', 'STU'] + (['LM'] if is_total else []) + [col_name_pct, 'AVG DB', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%']
        if r_sm:
            df_smi = pd.DataFrame(r_sm)
            if is_total:
                df_smi['_no_target'] = (df_smi['TARGET'] <= 0).astype(int)
                df_smi = df_smi.sort_values(by=['_no_target', '_pct_val', '_gap_lm', '_stu_val', '_db_val'], ascending=[True, True, True, True, True]).reset_index(drop=True)
            else:
                df_smi = df_smi.sort_values(by=['TARGET', '_pct_val', '_stu_val', '_db_val'], ascending=[False, True, True, True]).reset_index(drop=True)
            tt, ts, tdb, thot, tspk, n_sm = int(df_smi['TARGET'].sum()), int(df_smi['STU'].sum()), int(df_smi['DB'].sum()), int(df_smi['HOT'].sum()), int(df_smi['SPK'].sum()), len(df_smi)
            tpct_sm = (ts / tt * 100.0) if tt > 0 else 0.0
            tot_sm = {'NAMA SALESMAN': lbl_tot, 'TARGET': tt, 'STU': ts, col_name_pct: f'{tpct_sm:.2f}%', 'AVG DB': f'{(tdb/n_sm/hari_aktif if n_sm>0 else 0):.2f}', 'DB': tdb, 'HOT': thot, 'DB Q': f'{(thot/tdb*100 if tdb>0 else 0):.2f}%', 'SPK': tspk, 'ACC%': f'{(t_sa/(t_sa+t_sr)*100 if (t_sa+t_sr)>0 else 0):.2f}%', 'STU%': f'{(ts/tdb*100 if tdb>0 else 0):.2f}%', '_stu_val': ts, '_pct_val': tpct_sm}
            tot_sm['LM'] = int(df_smi['LM'].sum())
            render_compact_html_table(df_smi, pd.concat([df_smi, pd.DataFrame([tot_sm])], ignore_index=True), kol_sm, 'NAMA SALESMAN', '_pct_val', key_suffix=f'Review_5_Salesman_{dlr_pil}', title_text=jdl_rev_5)
            bsg_safe(bsg_render_salesman_charts, df_smi, target_persen_harian, label="Grafik salesman")
        else: st.info(f'ℹ️ Belum ada data Salesman untuk dealer {dlr_pil}.')

        st.divider()
        jdl_rev_unreg = f'{nxt_no()}. TABEL KONSUMEN BELUM REGISTRASI RATING (MYDR) — {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})'
        st.markdown(f'<div class="section-title">{jdl_rev_unreg}</div>', unsafe_allow_html=True)
        if not f_c.empty and 'Status_Registrasi_Rating' in f_c.columns:
            tot_stu_dlr = len(f_c)
            df_sudah_reg = f_c[f_c['Status_Registrasi_Rating'] == 'SUDAH REGISTRASI'].copy()
            df_belum_reg = f_c[f_c['Status_Registrasi_Rating'] == 'BELUM REGISTRASI'].copy()
            jml_sudah, jml_belum = len(df_sudah_reg), len(df_belum_reg)
            pct_reg_dlr = (jml_sudah / tot_stu_dlr * 100.0) if tot_stu_dlr > 0 else 0.0
            st.markdown(f'''<div class="unmapped-sales-box" style="border-left-color:#00E5FF; background:linear-gradient(90deg, rgba(0,229,255,0.10) 0%, rgba(14,17,23,0.96) 100%); margin-bottom:10px;">
            📊 <b>Rekapitulasi Status Registrasi Rating (MYDR) — {dlr_pil}:</b> Total Faktur (STU): <b>{tot_stu_dlr} Konsumen</b> &nbsp;|&nbsp;
            <span style="color:#00FF66;font-weight:800;">✅ Sudah Registrasi: {jml_sudah} Konsumen ({pct_reg_dlr:.1f}%)</span> &nbsp;|&nbsp;
            <span style="color:#FF007F;font-weight:800;">⚠️ Belum Registrasi: {jml_belum} Konsumen ({100.0 - pct_reg_dlr:.1f}%)</span>
        </div>''', unsafe_allow_html=True)
            bsg_safe(bsg_render_reg_donut, jml_sudah, jml_belum, label="Donut registrasi")

            if not df_belum_reg.empty:
                df_belum_reg = df_belum_reg.sort_values(by=['Tanggal_Parsed', 'Salesman_Clean', 'Nama_Konsumen_Clean'], ascending=[True, True, True]).reset_index(drop=True)
                rows_unreg = []
                for idx_u, r_u in df_belum_reg.iterrows():
                    tgl_str = r_u['Tanggal_Parsed'].strftime('%d/%m/%Y') if (pd.notna(r_u.get('Tanggal_Parsed')) and hasattr(r_u.get('Tanggal_Parsed'), 'strftime')) else '-'
                    nm_kons = clean_str(r_u.get('Nama_Konsumen_Clean', '')) or '-'
                    no_hp = clean_str(r_u.get('No_HP_Clean', '')) or '-'
                    tp_unit = clean_str(r_u.get('Tipe_Unit_Display', '')) or clean_str(r_u.get('Type_Clean', '')) or '-'
                    lsg_u = clean_str(r_u.get('Leasing_Faktur_Clean', '')) or '-'
                    sm_u = clean_str(r_u.get('Salesman_Clean', '')) or '-'
                    kr_u = clean_str(r_u.get('Koor', '')) or '-'
                    st_u = clean_str(r_u.get('Status_Registrasi_Rating', 'BELUM REGISTRASI'))
                    rows_unreg.append({
                        'NO': idx_u + 1,
                        'TGL FAKTUR': tgl_str,
                        'NAMA KONSUMEN': nm_kons,
                        'NO. HP': no_hp,
                        'TIPE UNIT': tp_unit,
                        'PEMBAYARAN': lsg_u,
                        'NAMA SALESMAN': sm_u,
                        'KOORDINATOR': kr_u,
                        'STATUS REGISTRASI': st_u,
                        '_sort_val': 0.0
                    })
                df_unreg_items = pd.DataFrame(rows_unreg)
                tot_unreg_row = {
                    'NO': 'TOTAL',
                    '_summary': f'TOTAL STU: {tot_stu_dlr} KONSUMEN &nbsp;|&nbsp; SUDAH REGISTRASI: {jml_sudah} &nbsp;|&nbsp; BELUM REGISTRASI: {jml_belum} &nbsp;|&nbsp; CAPAIAN: {pct_reg_dlr:.1f}%',
                    '_sort_val': 0.0
                }
                kol_unreg = ['NO', 'TGL FAKTUR', 'NAMA KONSUMEN', 'NO. HP', 'TIPE UNIT', 'PEMBAYARAN', 'NAMA SALESMAN', 'KOORDINATOR', 'STATUS REGISTRASI']
                df_unreg_full = pd.concat([df_unreg_items, pd.DataFrame([tot_unreg_row])], ignore_index=True)
                render_compact_html_table(df_unreg_items, df_unreg_full, kol_unreg, 'NO', '_sort_val', key_suffix=f'Review_6_Belum_Registrasi_{dlr_pil}', title_text=jdl_rev_unreg, wrap_first='all')

                with st.expander(f"📋 Lihat Seluruh Data Faktur ({tot_stu_dlr} Konsumen: Sudah & Belum Registrasi) — {dlr_pil}"):
                    all_f_rows = []
                    for idx_a, r_a in f_c.sort_values(by=['Status_Registrasi_Rating', 'Tanggal_Parsed', 'Nama_Konsumen_Clean']).reset_index(drop=True).iterrows():
                        tgl_a = r_a['Tanggal_Parsed'].strftime('%d/%m/%Y') if (pd.notna(r_a.get('Tanggal_Parsed')) and hasattr(r_a.get('Tanggal_Parsed'), 'strftime')) else '-'
                        all_f_rows.append({
                            'NO': idx_a + 1,
                            'TGL FAKTUR': tgl_a,
                            'NAMA KONSUMEN': clean_str(r_a.get('Nama_Konsumen_Clean', '')) or '-',
                            'NO. HP': clean_str(r_a.get('No_HP_Clean', '')) or '-',
                            'TIPE UNIT': clean_str(r_a.get('Tipe_Unit_Display', '')) or '-',
                            'PEMBAYARAN': clean_str(r_a.get('Leasing_Faktur_Clean', '')) or '-',
                            'NAMA SALESMAN': clean_str(r_a.get('Salesman_Clean', '')) or '-',
                            'KOORDINATOR': clean_str(r_a.get('Koor', '')) or '-',
                            'STATUS REGISTRASI': clean_str(r_a.get('Status_Registrasi_Rating', ''))
                        })
                    st.dataframe(pd.DataFrame(all_f_rows), hide_index=True, use_container_width=True)
            else:
                st.success(f'🎉 Luar Biasa! Seluruh konsumen faktur ({tot_stu_dlr} konsumen) di {dlr_pil} SUDAH melakukan registrasi rating (MYDR).')
        else:
            st.info(f'ℹ️ Belum ada data Faktur untuk dealer {dlr_pil} pada periode ini.')

    with tab_an:
        tgl_sasaran = 30 if tanggal_akhir > 21 else min(30, tanggal_akhir + 7)
        sisa_hari = max(1, sum(1 for d_n in range(tanggal_akhir + 1, min(tgl_sasaran, max_day_in_month) + 1) if is_workday_day(d_n)))
        horizon_lbl = f"Optimalisasi Closing s.d Tgl 30 {periode_bulan_tahun} ({sisa_hari} Hari Kerja)" if tanggal_akhir > 21 else f"Akselerasi 7 Hari ke Depan s.d Tgl {tgl_sasaran} {periode_bulan_tahun} ({sisa_hari} Hari Kerja)"

        jdl_rev_6 = f'{nxt_no()}. TABEL ANALISA & ACTION PLAN — {dlr_pil} ({horizon_lbl})'
        st.markdown(f'<div class="section-title">{jdl_rev_6}</div>', unsafe_allow_html=True)

        dlr_targ, dlr_ideal, dlr_stu, dlr_nota, dlr_stulm = safe_int(r_tot_p.get('TARGET', 0)), safe_int(r_tot_p.get('IDEAL', 0)), safe_int(r_tot_p.get('STU', 0)), safe_int(r_tot_p.get('NOTA', 0)), safe_int(r_tot_p.get('STU LM', 0))
        dlr_pct, dlr_gap_ideal, dlr_gap_lm = safe_float(r_tot_p.get('_pct', 0.0)), dlr_stu - dlr_ideal, dlr_stu - dlr_stulm
        cur_mp, cur_db, cur_hot = (safe_int(r_tot_pr.get('JML MP', 0)) or max(1, len(r_sm))), safe_int(r_tot_pr.get('DB', 0)), safe_int(r_tot_pr.get('HOT', 0))
        cur_avg_db, cur_dbq, cur_stup = ((cur_db / cur_mp / hari_aktif) if cur_mp > 0 else 0.0), ((cur_hot / cur_db * 100.0) if cur_db > 0 else 0.0), ((dlr_stu / cur_db * 100.0) if cur_db > 0 else 0.0)
        cur_spk, cur_spk_lm, cur_open_spk, cur_acc_pct = safe_int(r_tot_s.get('SPK', 0)), safe_int(r_tot_s.get('SPK LM', 0)), safe_int(r_tot_s.get('TERBUKA', 0)), safe_float(r_tot_s.get('_acc_val', 0.0))

        pct_sasaran = tabel_target_harian.get(tgl_sasaran, 100.0) / 100.0
        tambahan_stu_wajib, stu_sasaran_rasional = calc_rational_7d_addition(dlr_stu, dlr_targ, tanggal_akhir, tgl_sasaran, persen_desimal, pct_sasaran, active_mp=cur_mp)
        target_stu_per_hari = tambahan_stu_wajib / sisa_hari

        fak_kredit_curr = {l_k: (len(f_c[f_c['Leasing_Faktur_Clean'] == l_k]) if (not f_c.empty and 'Leasing_Faktur_Clean' in f_c.columns) else 0) for l_k in ['BAF', 'ADIRA', 'SOF']}
        tot_fak_kredit_curr = sum(fak_kredit_curr.values())
        lsg_stats = [(l_nm, safe_int(r_tot_s.get(l_nm, 0)), safe_float(r_tot_s.get(f'%{l_nm}', 0.0))) for l_nm in ['BAF', 'ADIRA', 'SOF', 'IMFI']]
        lsg_active = [x for x in lsg_stats if x[1] > 0]
        best_lsg, best_fak_lsg = (max(lsg_active, key=lambda x: (x[2], x[1])) if lsg_active else ('BAF', 0, 0.0)), max(['BAF', 'ADIRA', 'SOF'], key=lambda k: fak_kredit_curr[k])

        df_rej_dlr = s_c[s_c['Status_SPK_Clean'] == 'DITOLAK'] if (not s_c.empty and 'Status_SPK_Clean' in s_c.columns) else pd.DataFrame()
        top_rej_reasons_str, top_1_reason = "Belum ada SPK ditolak", "Kapasitas/SLIK"
        if not df_rej_dlr.empty and 'Alasan_Reject_Clean' in df_rej_dlr.columns:
            vc_rej = df_rej_dlr['Alasan_Reject_Clean'].value_counts()
            if not vc_rej.empty: top_1_reason, top_rej_reasons_str = str(vc_rej.index[0]), ", ".join([f"{k} ({v} SPK)" for k, v in vc_rej.head(4).items()])

        eff_acc_rate = 0.50 if cur_acc_pct >= 99.9 else (max(IDEAL_ACC_PCT, cur_acc_pct) / 100.0)
        potensi_stu_open = min(tambahan_stu_wajib, round(cur_open_spk * eff_acc_rate))
        kebutuhan_spk_baru = max(2, round(max(1, tambahan_stu_wajib - round(potensi_stu_open * 0.5)) / eff_acc_rate))
        target_db_baru_total = max(round(tambahan_stu_wajib / (IDEAL_STU_PCT / 100.0)), int(cur_mp * 3 * sisa_hari))
        target_db_per_mp_hari = min(5.0, max(3.0, round((target_db_baru_total / sisa_hari) / cur_mp, 1))) if cur_mp > 0 else 3.5
        tot_db_plan_dlr = round(target_db_per_mp_hari * cur_mp * sisa_hari)

        default_cond_dealer = limit_words(f"STU {dlr_stu} unit ({dlr_pct:.1f}% dari target {dlr_targ}), gap ideal {dlr_gap_ideal:+d} unit, vs LM {dlr_gap_lm:+d} unit. Input {cur_avg_db:.1f} DB/MP/hari ({cur_db} DB), DB Q {cur_dbq:.1f}% (ideal 30%), STU% {cur_stup:.1f}% (ideal 10%).")
        default_plan_dealer = limit_words(f"Target rasional s.d tgl {tgl_sasaran}: kejar +{tambahan_stu_wajib} STU (menjadi {stu_sasaran_rasional} unit / {target_stu_per_hari:.1f} STU/hari). Input {target_db_per_mp_hari:.1f} DB/MP/hari (+{tot_db_plan_dlr} DB) TANPA MENURUNKAN KUALITAS DATABASE.")

        default_cond_type, default_plan_type, wt_rational_str = "Data type belum tersedia.", "Belum ada rencana aksi per type.", ""
        wt_name, wt_stu, wt_lm, wt_db, wt_hot, wt_spk, wt_stu_add, wt_spk_add, wt_db_add = "AT PREMIUM", 0, 0, 0, 0, 0, 2, 4, 20
        _df_td_focus = df_td_i[df_td_i['TYPE'].isin(FOKUS_KATEGORI_TYPE)] if not df_td_i.empty else df_td_i   # analisa tetap fokus AT Premium/Classy/LPM
        if not _df_td_focus.empty:
            wt_row = _df_td_focus.iloc[0]
            wt_name, wt_stu, wt_lm, wt_db, wt_hot, wt_spk = str(wt_row['TYPE']), safe_int(wt_row['STU']), safe_int(wt_row['STU LM']), safe_int(wt_row['DB']), safe_int(wt_row['HOT']), safe_int(wt_row['SPK'])
            default_cond_type = limit_words(f"Segmen terendah {wt_name}: STU {wt_stu} vs LM {wt_lm} ({wt_stu - wt_lm:+d} unit, Growth {wt_row['GROWTH']}). Input {wt_db} DB, {wt_hot} HOT (DB Q {wt_row['DB Q']} vs 30%), {wt_spk} SPK (ACC% {wt_row['ACC%']}), STU% {wt_row['STU%']}.")
            wt_stu_add = max(2, min(round(tambahan_stu_wajib * 0.45), max(3, round((wt_stu / hari_aktif) * sisa_hari * 1.8) + 2)))
            wt_spk_add, wt_db_add = max(wt_stu_add + 1, round(wt_stu_add / 0.5)), max(round(wt_stu_add / 0.10), sisa_hari * cur_mp)
            wt_rational_str = f"Segmen terburuk {wt_name}: target rasional +{wt_stu_add} STU (menjadi {wt_stu + wt_stu_add} unit), +{wt_spk_add} SPK, +{wt_db_add} DB."
            default_plan_type = limit_words(f"Fokus {wt_name}: kejar +{wt_stu_add} STU (menjadi {wt_stu + wt_stu_add} unit) dan +{wt_spk_add} SPK (ACC% >=50%). Tambah +{wt_db_add} DB {wt_name} TANPA MENURUNKAN KUALITAS DATABASE (DB Q >=30%, STU% >=10%).")

        default_cond_leasing = limit_words(f"Total {cur_spk} SPK (vs LM {cur_spk_lm}), ACC% 100% belum valid karena {cur_open_spk} SPK masih Terbuka. Faktur kredit cair {tot_fak_kredit_curr} unit (BAF {fak_kredit_curr['BAF']}, ADIRA {fak_kredit_curr['ADIRA']}, SOF {fak_kredit_curr['SOF']}).") if cur_acc_pct >= 99.9 else limit_words(f"Total {cur_spk} SPK (vs LM {cur_spk_lm}), ACC% {cur_acc_pct:.1f}% (ideal 50%), {cur_open_spk} SPK Terbuka, reject tertinggi: {top_1_reason}. Faktur kredit {tot_fak_kredit_curr} unit (terkuat {best_lsg[0]}).")
        default_plan_leasing = limit_words(f"Eksekusi {cur_open_spk} SPK Terbuka dalam 1x24 jam (target cair +{potensi_stu_open} STU) dan tambah +{kebutuhan_spk_baru} SPK baru. Prioritaskan 60% aplikasi ke {best_fak_lsg} serta perketat screening {top_1_reason} agar ACC% >=50%.")

        default_cond_koor, default_plan_koor, wk_rational_str = "Belum ada data Koordinator.", "Belum ada rencana aksi Koordinator.", ""
        wk_nm, wk_t, wk_s, wk_add, wk_goal_rasional, wk_spk_need, wk_db_per_sm, wk_mp = "-", 0, 0, 2, 2, 4, 4, 1
        if not df_koor_only.empty:
            wk = df_koor_only.sort_values(by=['_pct', 'STU'], ascending=[True, True]).iloc[0]
            wk_nm, wk_t, wk_i, wk_s, wk_pct = str(wk[kol_nm]), safe_int(wk['TARGET']), safe_int(wk['IDEAL']), safe_int(wk['STU']), safe_float(wk['_pct'])
            wk_pr = df_pr_it[df_pr_it[kol_nm] == wk_nm].iloc[0] if (not df_pr_it.empty and wk_nm in df_pr_it[kol_nm].values) else {}
            wk_sp = df_s_it[df_s_it[kol_nm] == wk_nm].iloc[0] if (not df_s_it.empty and wk_nm in df_s_it[kol_nm].values) else {}
            wk_mp = max(1, safe_int(wk_pr.get('JML MP', 1)))
            default_cond_koor = limit_words(f"Koordinator terendah {wk_nm}: STU {wk_s}/{wk_t} unit ({wk_pct:.1f}%, gap ideal {wk_s - wk_i:+d}). Input {wk_pr.get('AVG DB', '0')} DB/MP/hari, DB Q {wk_pr.get('DB Q', '0%')} (ideal 30%), STU% {wk_pr.get('STU%', '0%')}, ACC% {wk_sp.get('ACC%', '0%')} .")
            wk_add, wk_goal_rasional = calc_rational_7d_addition(wk_s, wk_t, tanggal_akhir, tgl_sasaran, persen_desimal, pct_sasaran, active_mp=wk_mp)
            wk_spk_need, wk_db_per_sm = max(wk_add + 1, round(wk_add / 0.5)), min(5, max(3, round((wk_add / 0.10) / max(1, wk_mp * sisa_hari))))
            wk_rational_str = f"Koordinator terburuk {wk_nm} (STU saat ini {wk_s} dari target {wk_t}): target rasional 7 hari adalah +{wk_add} STU (menjadi {wk_goal_rasional} unit), +{wk_spk_need} SPK, {wk_db_per_sm} DB/MP/hari."
            default_plan_koor = limit_words(f"Tim {wk_nm} kejar target rasional +{wk_add} STU (menjadi {wk_goal_rasional} unit) dan +{wk_spk_need} SPK baru. Disiplinkan {wk_mp} MP input {wk_db_per_sm} DB/hari TANPA MENURUNKAN KUALITAS DATABASE (DB Q >=30%, STU% >=10%).")

        default_cond_counter, default_plan_counter, wc_rational_str = "Belum ada data Counter.", "Belum ada rencana aksi Counter.", ""
        wc_nm, wc_t, wc_s, wc_add, wc_goal_rasional, wc_spk_need, wc_db_hari = "-", 0, 0, 2, 2, 4, 4
        if not df_cnt_only.empty:
            wc = df_cnt_only.iloc[0]
            wc_nm, wc_t, wc_i, wc_s, wc_pct = str(wc[kol_nm]), safe_int(wc['TARGET']), safe_int(wc['IDEAL']), safe_int(wc['STU']), safe_float(wc['_pct'])
            wc_pr = df_pr_it[df_pr_it[kol_nm] == wc_nm].iloc[0] if (not df_pr_it.empty and wc_nm in df_pr_it[kol_nm].values) else {}
            wc_sp = df_s_it[df_s_it[kol_nm] == wc_nm].iloc[0] if (not df_s_it.empty and wc_nm in df_s_it[kol_nm].values) else {}
            default_cond_counter = limit_words(f"Counter terendah {wc_nm}: STU {wc_s}/{wc_t} unit ({wc_pct:.1f}%, gap ideal {wc_s - wc_i:+d}). Prospek {wc_pr.get('DB', 0)} DB, DB Q {wc_pr.get('DB Q', '0%')} (ideal 30%), STU% {wc_pr.get('STU%', '0%')}, ACC% {wc_sp.get('ACC%', '0%')} .")
            wc_add, wc_goal_rasional = calc_rational_7d_addition(wc_s, wc_t, tanggal_akhir, tgl_sasaran, persen_desimal, pct_sasaran, active_mp=1)
            wc_spk_need, wc_db_hari = max(wc_add + 1, round(wc_add / 0.5)), min(6, max(4, round((wc_add / 0.10) / sisa_hari)))
            wc_rational_str = f"Counter terburuk {wc_nm} (STU saat ini {wc_s} dari target {wc_t}): target rasional 7 hari adalah +{wc_add} STU (menjadi {wc_goal_rasional} unit), +{wc_spk_need} SPK, {wc_db_hari} DB/hari."
            default_plan_counter = limit_words(f"{wc_nm} kejar target rasional +{wc_add} STU (menjadi {wc_goal_rasional} unit), cairkan {safe_int(wc_sp.get('TERBUKA', 0))} SPK Terbuka, cetak +{wc_spk_need} SPK. Input {wc_db_hari} DB/hari TANPA MENURUNKAN KUALITAS DATABASE (DB Q >=30%).")

        default_cond_mp = "Seluruh Salesman lapangan aktif sudah di zona aman."
        default_plan_mp = "Pertahankan input database harian TANPA MENURUNKAN KUALITAS DATABASE sesuai standar DB Q 30%, STU% 10%, ACC% 50%."
        top_bad_raw_str, names_kritis, cnt_kritis = "Tidak ada salesman aktif di zona kritis.", "-", 0
        if r_sm:
            df_sm_eval = pd.DataFrame(r_sm)
            min_p_tbl, max_p_tbl = float(df_sm_eval['_pct_val'].min()), float(df_sm_eval['_pct_val'].max())
            def is_zona_kritis(row_s):
                v_p, t_g, s_u = safe_float(row_s['_pct_val']), safe_int(row_s['TARGET']), safe_int(row_s['STU'])
                idl = round(t_g * persen_desimal)
                if (s_u >= idl and idl > 0) or (v_p >= target_persen_harian and target_persen_harian > 0): return False
                ratio_c = ((v_p - min_p_tbl) / (max_p_tbl - min_p_tbl)) if max_p_tbl > min_p_tbl else 0.0
                return (ratio_c <= 0.15) or (v_p < target_persen_harian)
            df_sm_non_cnt = df_sm_eval[(~df_sm_eval['NAMA SALESMAN'].apply(is_counter_personnel)) & (df_sm_eval['_db_val'] >= 2)].copy()
            df_kritis_with_target = df_sm_non_cnt[(df_sm_non_cnt['TARGET'] > 0) & (df_sm_non_cnt.apply(is_zona_kritis, axis=1))].sort_values(by=['TARGET', '_pct_val', '_stu_val', '_db_val'], ascending=[False, True, True, True])
            if not df_kritis_with_target.empty:
                max_kritis_target = int(df_kritis_with_target['TARGET'].max())
                top_bad = df_kritis_with_target[df_kritis_with_target['TARGET'] == max_kritis_target].head(4)
                if len(top_bad) < 3: top_bad = df_kritis_with_target.head(4)
            else: top_bad = df_sm_non_cnt[df_sm_non_cnt.apply(is_zona_kritis, axis=1)].sort_values(by=['TARGET', '_pct_val', '_stu_val', '_db_val'], ascending=[False, True, True, True]).head(4)
            if not top_bad.empty:
                cnt_kritis = len(top_bad)
                names_kritis = ", ".join([f"{rb['NAMA SALESMAN']} (STU {safe_int(rb['STU'])}/{safe_int(rb['TARGET'])}, DB {safe_int(rb['DB'])}, SPK {safe_int(rb['SPK'])})" for _, rb in top_bad.iterrows()])
                top_bad_raw_str = "; ".join([f"{rb['NAMA SALESMAN']}: Target {rb['TARGET']}, STU {rb['STU']} ({rb[col_name_pct]}), DB {rb['DB']} (AVG {rb['AVG DB']}), HOT {rb['HOT']} (DB Q {rb['DB Q']}), SPK {rb['SPK']} (ACC% {rb['ACC%']}), STU% {rb['STU%']} -> Target Rasional 7 Hari: +1 s.d +2 STU" for _, rb in top_bad.iterrows()])
                default_cond_mp = limit_words(f"{cnt_kritis} Salesman aktif zona kritis: {names_kritis}. Rata-rata DB Quality dan konversi STU% masih di bawah standar ideal 30% dan 10%.")
                default_plan_mp = limit_words(f"Kawal joint canvassing {cnt_kritis} MP kritis untuk kejar target rasional +1 s.d +2 STU dan +3 SPK/orang. Wajib input 4 DB/hari/MP TANPA MENURUNKAN KUALITAS DATABASE (DB Q >=30%).")

        def _prospect_stats(db_df, kws, exact=False):
            if db_df is None or db_df.empty or db_df.shape[1] < 8: return None
            m_p = db_df.iloc[:, 6].apply(alnum_str).apply(lambda v: (v in kws) if exact else any(k_w in v for k_w in kws))
            d_p = db_df[m_p]
            if d_p.empty: return None
            n_p, h_p, q_p, s_p, sp_p = _act_vals(d_p)
            sub_nm = d_p.iloc[:, 7].apply(lambda v: strip_sub_code(v) or '(KOSONG)')
            subs = []
            for g_v in sub_nm.unique():
                v_s = _act_vals(d_p[sub_nm == g_v]); subs.append((g_v, v_s[0], v_s[1], v_s[2], v_s[3], v_s[4]))
            subs.sort(key=lambda x: -x[1])
            weak = sorted([x for x in subs if x[1] >= 3] or subs, key=lambda x: (x[5], x[3], -x[1]))
            return {'n': n_p, 'hot': h_p, 'dbq': q_p, 'stu': s_p, 'stup': sp_p, 'share': (n_p / len(db_df) * 100.0 if len(db_df) else 0.0), 'subs': subs, 'weak': weak[0] if weak else None}
        def _md_texts(label, st_p, with_sub):
            if not st_p:
                return (f'Belum ada database {label} pada periode ini (1 s.d {tanggal_akhir}).', f'Aktifkan kegiatan {label} dan wajib input database tiap kegiatan TANPA MENURUNKAN KUALITAS DATABASE.')
            top = st_p['subs'][0]
            if with_sub and st_p['weak']:   # Aktifitas MD: khusus prospect EVENT -> sub terlemah
                w = st_p['weak']
                cond = f"Event total {st_p['n']} DB (STU {st_p['stu']}, STU% {st_p['stup']:.1f}%). Sub terlemah {w[0]}: {w[1]} DB, HOT {w[2]} (DB Q {w[3]:.1f}% vs 30%), STU {w[4]} (STU% {w[5]:.1f}% vs 10%)."
                need_w = max(0, math.ceil(w[1] * IDEAL_STU_PCT / 100.0) - w[4])
                plan = (f"Evaluasi event {w[0]}: follow-up {w[2]} HOT 1x24 jam, kejar +{need_w} STU (STU% 10%), perketat penjaringan agar DB Q >=30% TANPA MENURUNKAN KUALITAS DATABASE." if need_w > 0
                        else f"Pertahankan konversi {w[0]} di atas 10% dan replikasi pola terbaiknya ke sub Event lain TANPA MENURUNKAN KUALITAS DATABASE.")
                return cond, plan
            cond = f"{label} {st_p['n']} DB ({st_p['share']:.1f}% dari total DB), HOT {st_p['hot']} (DB Q {st_p['dbq']:.1f}% vs 30%), STU {st_p['stu']} (STU% {st_p['stup']:.1f}% vs 10%). Sub terbesar {top[0]} ({top[1]} DB, STU% {top[5]:.1f}%)."
            need = max(0, math.ceil(st_p['n'] * IDEAL_STU_PCT / 100.0) - st_p['stu'])
            plan = (f"Fokus {top[0]}: follow-up {st_p['hot']} HOT 1x24 jam, kejar +{need} STU agar STU% mencapai 10%" if need > 0 else f"Pertahankan STU% {label} di atas 10%, perluas {top[0]}") + ", saring data agar DB Q >=30% TANPA MENURUNKAN KUALITAS DATABASE."
            return cond, plan
        _st_event, _st_sosmed = _prospect_stats(db_c, ['EVENT'], exact=True), _prospect_stats(db_c, ['MEDIASOSIAL', 'SOSMED'])
        default_cond_md, default_plan_md = _md_texts('Event', _st_event, True)
        default_cond_sosmed, default_plan_sosmed = _md_texts('Media Sosial', _st_sosmed, False)

        def build_smart_dynamic_narrative():
            v_idx = random.randint(0, 2)
            b_dlr = "kualitas prospek DB Q rendah" if cur_dbq < 25 else "konversi closing HOT ke STU macet"
            c_dlr = [
                f"Bottleneck {dlr_pil} pada {b_dlr} (DB Q {cur_dbq:.1f}% vs 30%, STU% {cur_stup:.1f}% vs 10%), memicu defisit ideal {dlr_gap_ideal:+d} unit (STU {dlr_stu}/{dlr_targ}, vs LM {dlr_gap_lm:+d}).",
                f"Capaian {dlr_pil} baru {dlr_stu} unit ({dlr_pct:.1f}%), tertahan {b_dlr}: dari {cur_db} DB hanya jadi {cur_hot} HOT ({cur_dbq:.1f}%) dan {dlr_stu} STU ({cur_stup:.1f}%).",
                f"Realisasi {dlr_stu}/{dlr_targ} unit (gap ideal {dlr_gap_ideal:+d}) akibat lemahnya filter prospek ({cur_avg_db:.1f} DB/MP/hr, DB Q {cur_dbq:.1f}%, STU% {cur_stup:.1f}%)."
            ][v_idx]
            p_dlr = [
                f"Akselerasi s.d tgl {tgl_sasaran}: kunci +{tambahan_stu_wajib} STU (total {stu_sasaran_rasional} unit / {target_stu_per_hari:.1f} STU/hr) dan {target_db_per_mp_hari:.1f} DB/MP/hr (+{tot_db_plan_dlr} DB) TANPA MENURUNKAN KUALITAS DATABASE.",
                f"Kejar kuota rasional +{tambahan_stu_wajib} STU ({target_stu_per_hari:.1f} unit/hr) lewat bedah {cur_hot} HOT prospek serta disiplin {target_db_per_mp_hari:.1f} DB/MP/hr TANPA MENURUNKAN KUALITAS DATABASE.",
                f"Wajib tambah +{tambahan_stu_wajib} STU (menjadi {stu_sasaran_rasional} unit) dan +{tot_db_plan_dlr} DB baru (DB Q >=30%, STU% >=10%) TANPA MENURUNKAN KUALITAS DATABASE."
            ][v_idx]
            c_tp = f"Kontraksi terdalam di {wt_name} (STU {wt_stu} vs LM {wt_lm}); dari {wt_db} DB hanya menghasilkan {wt_hot} HOT dan {wt_spk} SPK sehingga konversi terhambat." if not df_td_i.empty else default_cond_type
            p_tp = f"Genjot segmen {wt_name}: sasar +{wt_stu_add} STU (menjadi {wt_stu + wt_stu_add} unit), +{wt_spk_add} SPK, dan +{wt_db_add} DB tertarget TANPA MENURUNKAN KUALITAS DATABASE." if not df_td_i.empty else default_plan_type
            c_lsg = f"Dari {cur_spk} SPK (LM {cur_spk_lm}), faktur kredit cair {tot_fak_kredit_curr} unit; tertahan {cur_open_spk} SPK Terbuka dan reject dominan karena {top_1_reason} (ACC% {cur_acc_pct:.1f}%)."
            p_lsg = f"Selesaikan {cur_open_spk} SPK Terbuka dalam 1x24 jam (cair +{potensi_stu_open} STU), cetak +{kebutuhan_spk_baru} SPK baru, alihkan aplikasi ke {best_fak_lsg} & perketat pra-screening {top_1_reason}."
            c_kr = f"Tim {wk_nm} di zona kritis (STU {wk_s}/{wk_t}); produktivitas DB lapangan dan rasio konversi HOT ke STU masih di bawah standar 30% & 10%." if not df_koor_only.empty else default_cond_koor
            p_kr = f"Tim {wk_nm} wajib amankan +{wk_add} STU (menjadi {wk_goal_rasional} unit), +{wk_spk_need} SPK, dan {wk_db_per_sm} DB/MP/hr TANPA MENURUNKAN KUALITAS DATABASE." if not df_koor_only.empty else default_plan_koor
            c_cn = f"Konversi walk-in/leads digital {wc_nm} belum optimal (STU {wc_s}/{wc_t}), dipicu rendahnya follow-up HOT prospek ke pengajuan SPK." if not df_cnt_only.empty else default_cond_counter
            p_cn = f"Fokus {wc_nm} kejar +{wc_add} STU (total {wc_goal_rasional} unit), cetak +{wc_spk_need} SPK, serta input {wc_db_hari} DB/hr TANPA MENURUNKAN KUALITAS DATABASE." if not df_cnt_only.empty else default_plan_counter
            c_mp = f"Terdeteksi {cnt_kritis} salesman zona kritis ({names_kritis}) dengan target besar namun minim konversi SPK dan rendah DB Quality." if cnt_kritis > 0 else default_cond_mp
            p_mp = f"Supervisi harian {cnt_kritis} MP kritis untuk mengunci +1 s.d +2 STU, +3 SPK, dan 4-5 DB/hr/orang TANPA MENURUNKAN KUALITAS DATABASE." if cnt_kritis > 0 else default_plan_mp
            return {k: limit_words(v, MAX_NARRATIVE_WORDS) for k, v in {'cond_dealer': c_dlr, 'plan_dealer': p_dlr, 'cond_type': c_tp, 'plan_type': p_tp, 'cond_leasing': c_lsg, 'plan_leasing': p_lsg, 'cond_koor': c_kr, 'plan_koor': p_kr, 'cond_counter': c_cn, 'plan_counter': p_cn, 'cond_mp': c_mp, 'plan_mp': p_mp, 'cond_md': default_cond_md, 'plan_md': default_plan_md, 'cond_sosmed': default_cond_sosmed, 'plan_sosmed': default_plan_sosmed}.items()}

        active_api_key = resolve_gemini_api_key()
        cache_key = f"ai_tbl6_v10_35w_{dlr_pil}_{tanggal_akhir}_{dlr_stu}_{cur_db}_{cur_spk}"

        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1: gen_ai_clicked = st.button('✨ Generate Narasi Dinamis dengan AI (Gemini)', type='primary', use_container_width=True)
        with col_btn2:
            with st.expander('🤖 Pengaturan / Generate API Key Share GitHub (Klik untuk buka)'):
                st.caption('💡 Untuk memanggil server Gemini secara langsung, gunakan API Key gratis dari Google AI Studio (diawali **`AIzaSy...`**). Jika menggunakan token lain, sistem otomatis memakai *Smart Dynamic Analyzer*:')
                inp_api_key = st.text_input('Masukkan / Ganti Gemini API Key (Format AIzaSy...):', value=active_api_key, type='password')
                c_k1, c_k2 = st.columns(2)
                with c_k1:
                    if st.button('💾 Terapkan & Simpan API Key', use_container_width=True):
                        clean_inp = inp_api_key.strip() or DEFAULT_SHARED_API_KEY
                        st.session_state['shared_gemini_api_key'] = clean_inp
                        save_json({'gemini_api_key': clean_inp}, AI_CONFIG_FILE)
                        active_api_key = clean_inp
                        st.success('✅ API Key disimpan & aktif!')
                with c_k2:
                    st.markdown('<a href="https://aistudio.google.com/app/apikey" target="_blank" style="display:inline-block;text-align:center;width:100%;padding:6px 10px;background:#1E293B;color:#00E5FF;border:1px solid #334155;border-radius:6px;text-decoration:none;font-size:12.5px;font-weight:700;">🔑 Ambil Key AIzaSy Gratis (Google AI Studio)</a>', unsafe_allow_html=True)
                st.code('GEMINI_API_KEY = "AIzaSy...isi-key-Anda..."', language='toml'); st.caption('🔒 Simpan key di .streamlit/secrets.toml (atau env GEMINI_API_KEY), jangan ditulis di kode.')

        if gen_ai_clicked:
            with st.spinner(f'🤖 Sedang membedah data mentah & menyusun Target Rasional 7 Hari ke depan untuk {dlr_pil} (Maks 35 kata/sel)...'):
                raw_t1 = df_p_it[[kol_nm, 'TARGET', 'IDEAL', 'STU', 'NOTA', col_name_pct, 'STU LM', '% LM']].to_string(index=False) if not df_p_it.empty else "Kosong"
                raw_t2 = df_pr_it[[kol_nm, 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'STU', 'STU%']].to_string(index=False) if not df_pr_it.empty else "Kosong"
                raw_t3 = df_s_it[[kol_nm, 'SPK', 'SPK LM', 'GROWTH', 'ACC%', 'TERBUKA', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF', 'IMFI', '%IMFI']].to_string(index=False) if not df_s_it.empty else "Kosong"
                raw_t4 = df_td_i[['TYPE', 'STU', 'STU LM', 'GROWTH', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%']].to_string(index=False) if not df_td_i.empty else "Kosong"
                raw_context_for_ai = (
                    f"Dealer: {dlr_pil} | Periode: 1 s.d {tanggal_akhir} {periode_bulan_tahun} | Horizon Action Plan: {horizon_lbl}.\n"
                    f"ACUAN TARGET RASIONAL 7 HARI KE DEPAN (WAJIB DIPAKAI AI AGAR TARGET MASUK AKAL & MENANTANG):\n"
                    f"- Dealer {dlr_pil} (STU saat ini {dlr_stu} dari target bulanan {dlr_targ}, Ideal tgl {tanggal_akhir}={dlr_ideal}): Target Rasional s.d tgl {tgl_sasaran} adalah tambahan +{tambahan_stu_wajib} STU (sehingga total mencapai {stu_sasaran_rasional} unit, atau {target_stu_per_hari:.1f} STU/hari), input {target_db_per_mp_hari:.1f} DB/MP/hari.\n"
                    f"- {wt_rational_str}\n- {wk_rational_str}\n- {wc_rational_str}\n"
                    f"TOTAL LEASING & FAKTUR KREDIT: Total SPK={cur_spk} (LM={cur_spk_lm}), ACC%={cur_acc_pct:.1f}%, SPK Terbuka={cur_open_spk} (target cair rasional +{potensi_stu_open} STU, tambah +{kebutuhan_spk_baru} SPK baru). Faktur Kredit Cair={tot_fak_kredit_curr} unit (BAF={fak_kredit_curr['BAF']}, ADIRA={fak_kredit_curr['ADIRA']}, SOF={fak_kredit_curr['SOF']}). Alasan Reject SPK Tertinggi: {top_rej_reasons_str}.\n"
                    f"--- DATA TABEL 1 (PENJUALAN KOOR/COUNTER) ---\n{raw_t1}\n--- DATA TABEL 2 (PROSES KERJA KOOR/COUNTER) ---\n{raw_t2}\n--- DATA TABEL 3 (LEASING KOOR/COUNTER) ---\n{raw_t3}\n--- DATA TABEL 4 (PER TYPE) ---\n{raw_t4}\n--- DATA SALESMAN AKTIF ZONA KRITIS (NON-COUNTER, DB>=2) ---\n{top_bad_raw_str}"
                )
                raw_context_for_ai += f"\n--- AKTIFITAS MD: SUB PROSPECT TYPE EVENT ---\n{default_cond_md}\n--- PROSPECT MEDIA SOSIAL ---\n{default_cond_sosmed}"
                try:
                    st.session_state[cache_key] = call_gemini_ai_table(active_api_key, raw_context_for_ai)
                    st.success('✅ Narasi Dinamis AI Gemini dengan Target Rasional (Maks 35 kata per kotak) berhasil dibuat!')
                except Exception:
                    st.session_state[cache_key] = build_smart_dynamic_narrative()
                    st.success('✅ Narasi Dinamis berbasis Analisa Silang Tabel 1–5 berhasil diperbarui! (Tips: Gunakan key berawalan `AIzaSy...` dari Google AI Studio pada menu pengaturan di kanan atas jika ingin terhubung ke Cloud LLM).')

        ai_res = st.session_state.get(cache_key, {})
        analisa_rows_data = [
            ('🏢 STU Dealer', limit_words(ai_res.get('cond_dealer', default_cond_dealer)), limit_words(ai_res.get('plan_dealer', default_plan_dealer))),
            ('🏍️ STU Per Type', limit_words(ai_res.get('cond_type', default_cond_type)), limit_words(ai_res.get('plan_type', default_plan_type))),
            ('💼 Leasing', limit_words(ai_res.get('cond_leasing', default_cond_leasing)), limit_words(ai_res.get('plan_leasing', default_plan_leasing))),
            ('👔 STU Koordinator', limit_words(ai_res.get('cond_koor', default_cond_koor)), limit_words(ai_res.get('plan_koor', default_plan_koor))),
            ('🏪 STU Counter', limit_words(ai_res.get('cond_counter', default_cond_counter)), limit_words(ai_res.get('plan_counter', default_plan_counter))),
            ('👥 STU Man Power', limit_words(ai_res.get('cond_mp', default_cond_mp)), limit_words(ai_res.get('plan_mp', default_plan_mp))),
            ('📣 Aktifitas MD (Event)', limit_words(ai_res.get('cond_md', default_cond_md)), limit_words(ai_res.get('plan_md', default_plan_md))),
            ('📱 Media Sosial', limit_words(ai_res.get('cond_sosmed', default_cond_sosmed)), limit_words(ai_res.get('plan_sosmed', default_plan_sosmed))),
        ]

        rows_html_list, copy_texts_dict = [], {}
        for idx_r, (item_lbl, c_txt, p_txt) in enumerate(analisa_rows_data):
            cid, pid = f"cond_txt_{idx_r}", f"plan_txt_{idx_r}"
            copy_texts_dict[cid], copy_texts_dict[pid] = c_txt, p_txt
            rows_html_list.append(f'<tr><td class="item-col">{item_lbl}</td><td class="cond-col">{format_paragraphs_html(c_txt)}<div class="cell-btn-wrap no-capture"><button class="cell-copy-btn" onclick="copyCellText(\'{cid}\', this)">📋 Copy Condition</button></div></td><td class="plan-col">{format_paragraphs_html(p_txt)}<div class="cell-btn-wrap no-capture"><button class="cell-copy-btn" onclick="copyCellText(\'{pid}\', this)">📋 Copy Action Plan</button></div></td></tr>')

        tabel_analisa_dom_id = f"Capture_Analisa_{re.sub(r'[^a-zA-Z0-9]', '_', dlr_pil)}"
        copy_payload_json, safe_dlr_fname = json.dumps(copy_texts_dict), re.sub(r'[^a-zA-Z0-9_-]', '_', f"Analisa_ActionPlan_{dlr_pil}_Tgl_{tanggal_akhir}")

        components.html(f"""<html><head><script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script><style>
        body {{ margin: 0; padding: 0; background: transparent; font-family: 'Source Sans Pro', sans-serif; color: #E2E8F0; }}
        .compact-table-wrap {{ width: 100%; overflow-x: auto; border-radius: 8px; border: 1px solid #2D3748; background-color: #0E1117; }}
        .cap-title-banner {{ background: linear-gradient(90deg, #4318FF 0%, #1E293B 100%); color: #FFFFFF !important; font-family: 'Source Sans Pro', sans-serif; font-size: 15px; font-weight: 800; padding: 9px 14px; border-bottom: 2px solid #3B18FF; letter-spacing: 0.4px; text-align: left; }}
        table.narrative-tbl {{ width: 100%; border-collapse: collapse; font-family: 'Source Sans Pro', sans-serif; font-size: 13.5px; background-color: #0E1117; }}
        table.narrative-tbl th {{ background-color: #4318FF; color: #FFFFFF; font-weight: 700; padding: 10px 14px; border: 1px solid #2D3748; text-align: left; font-size: 13.5px; }}
        table.narrative-tbl td {{ padding: 10px 14px; border: 1px solid #2D3748; text-align: left; vertical-align: top; color: #E2E8F0; line-height: 1.55; font-weight: 400; }}
        table.narrative-tbl td.item-col {{ width: 15%; color: #E2E8F0; text-align: left; background-color: #161B26; white-space: nowrap; font-weight: 600; }}
        table.narrative-tbl td.cond-col {{ width: 42.5%; background-color: #0E1117; }}
        table.narrative-tbl td.plan-col {{ width: 42.5%; background-color: #111622; }}
        p.nar-p {{ margin: 0 0 6px 0; padding: 0; color: #E2E8F0; font-weight: 400; line-height: 1.55; text-align: left; }}
        p.nar-p:last-of-type {{ margin-bottom: 4px; }}
        .cell-btn-wrap {{ display: flex; justify-content: flex-end; margin-top: 4px; }}
        .cell-copy-btn {{ background-color: #1E293B; color: #CBD5E1; border: 1px solid #334155; border-radius: 5px; padding: 3px 9px; font-size: 11.5px; font-weight: 600; cursor: pointer; transition: all 0.15s; }}
        .cell-copy-btn:hover {{ background-color: #4318FF; color: #FFFFFF; border-color: #4318FF; }}
        .bottom-toolbar {{ display: flex; align-items: center; gap: 10px; margin-top: 10px; padding-bottom: 6px; flex-wrap: wrap; }}
        .act-btn {{ background-color: #1E293B; color: #E2E8F0; border: 1px solid #334155; border-radius: 6px; padding: 6px 13px; font-size: 12.5px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.15s; }}
        .act-btn:hover {{ background-color: #4318FF; color: #FFFFFF; border-color: #4318FF; }}
        .print-btn {{ background-color: #4318FF; color: #FFFFFF; border: 1px solid #4318FF; }}
        .print-btn:hover {{ background-color: #3311CC; }}
        #status_analisa {{ font-size: 12.5px; color: #00FF66; font-weight: 600; }}
    </style></head><body>
    <div id="{tabel_analisa_dom_id}" class="compact-table-wrap">
        <div class="cap-title-banner capture-only-banner" style="display:none;">🐺 {jdl_rev_6}</div>
        <table class="narrative-tbl">
            <thead><tr><th style="width:15%;">ITEM</th><th style="width:42.5%;">CONDITION (ANALISA SINGKAT MAKS 35 KATA — IDEAL: DB Q 30% | STU% 10% | ACC% 50%)</th><th style="width:42.5%;">ACTION PLAN (TARGET RASIONAL MAKS 35 KATA — {horizon_lbl.upper()})</th></tr></thead>
            <tbody>{''.join(rows_html_list)}</tbody>
        </table>
    </div>
    <div class="bottom-toolbar">
        <button class="act-btn" onclick="captureAnalisaTbl('copy')">📸 Copy Tabel (Gambar)</button>
        <button class="act-btn" onclick="captureAnalisaTbl('jpg')">📥 Download JPG</button>
        <button class="act-btn print-btn" onclick="printAnalisaTbl()">🖨️ Print / Print Preview Tabel Analisa</button>
        <span id="status_analisa"></span>
    </div>
    <script>
    const cellTexts = {copy_payload_json};
    function fallbackCopyText(text) {{
        const ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.left = '-9999px';
        document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
    }}
    async function copyCellText(keyId, btnEl) {{
        const txt = cellTexts[keyId] || ''; const origLabel = btnEl.innerText;
        try {{ await navigator.clipboard.writeText(txt); }} catch (e) {{ fallbackCopyText(txt); }}
        btnEl.innerText = '✅ Tersalin!'; btnEl.style.backgroundColor = '#00C853'; btnEl.style.color = '#FFFFFF';
        setTimeout(() => {{ btnEl.innerText = origLabel; btnEl.style.backgroundColor = ''; btnEl.style.color = ''; }}, 2000);
    }}
    async function captureAnalisaTbl(mode) {{
        const msg = document.getElementById('status_analisa'); msg.style.color = '#FFEA00'; msg.innerText = 'Memproses gambar tabel analisa...';
        const tblEl = document.getElementById('{tabel_analisa_dom_id}');
        const btns = tblEl.querySelectorAll('.no-capture');
        const bannerEl = tblEl.querySelector('.capture-only-banner');
        btns.forEach(b => b.style.display = 'none');
        if (bannerEl) bannerEl.style.display = 'block';
        try {{
            const canvas = await html2canvas(tblEl, {{ backgroundColor: '#0E1117', scale: 2, useCORS: true, logging: false }});
            btns.forEach(b => b.style.display = 'flex');
            if (bannerEl) bannerEl.style.display = 'none';
            if (mode === 'copy') {{
                canvas.toBlob(async (blob) => {{
                    try {{
                        await navigator.clipboard.write([new ClipboardItem({{ 'image/png': blob }})]);
                        msg.style.color = '#00FF66'; msg.innerText = '✅ Gambar Tabel Analisa + Judul disalin ke Clipboard! (Siap Ctrl+V di WA/Word/Excel)';
                    }} catch (err) {{
                        const a = document.createElement('a'); a.href = canvas.toDataURL('image/jpeg', 0.95); a.download = '{safe_dlr_fname}.jpg'; a.click();
                        msg.style.color = '#00E5FF'; msg.innerText = '📥 Gambar otomatis diunduh sebagai JPG.';
                    }}
                    setTimeout(() => msg.innerText = '', 4500);
                }}, 'image/png');
            }} else {{
                const a = document.createElement('a'); a.href = canvas.toDataURL('image/jpeg', 0.95); a.download = '{safe_dlr_fname}.jpg'; a.click();
                msg.style.color = '#00FF66'; msg.innerText = '✅ File {safe_dlr_fname}.jpg berhasil diunduh!';
                setTimeout(() => msg.innerText = '', 4000);
            }}
        }} catch (e) {{
            btns.forEach(b => b.style.display = 'flex');
            if (bannerEl) bannerEl.style.display = 'none';
            msg.style.color = '#FF007F'; msg.innerText = 'Gagal: ' + e.message;
        }}
    }}
    function printAnalisaTbl() {{
        const tblClone = document.getElementById('{tabel_analisa_dom_id}').cloneNode(true);
        tblClone.querySelectorAll('.no-capture').forEach(el => el.remove());
        tblClone.querySelectorAll('.capture-only-banner').forEach(el => el.remove());
        const w = window.open('', '_blank', 'width=1100,height=800');
        w.document.write(`
            <html><head><title>Print Review Analisa — DEALER {dlr_pil} (1 s.d {tanggal_akhir} {periode_bulan_tahun})</title>
            <style>
                @page {{ size: A4 landscape; margin: 12mm; }}
                body {{ font-family: Arial, sans-serif; color: #111827; background: #FFFFFF; margin: 0; padding: 10px; }}
                h2 {{ color: #1E3A8A; margin: 0 0 4px 0; font-size: 18px; }}
                .sub {{ color: #4B5563; font-size: 12.5px; margin-bottom: 12px; font-weight: 600; }}
                table.narrative-tbl {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
                table.narrative-tbl th {{ background-color: #1E3A8A !important; color: #FFFFFF !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; padding: 8px 10px; border: 1px solid #1F2937; text-align: left; }}
                table.narrative-tbl td {{ padding: 8px 10px; border: 1px solid #374151; vertical-align: top; text-align: left; line-height: 1.5; color: #111827; }}
                table.narrative-tbl td.item-col {{ font-weight: bold; width: 14%; background-color: #F3F4F6 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; text-align: left; white-space: nowrap; }}
                p.nar-p {{ margin: 0; }}
                .no-print-bar {{ margin-bottom: 12px; padding: 8px 12px; background: #EEF2FF; border: 1px solid #4318FF; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }}
                .no-print-bar button {{ background: #4318FF; color: #fff; border: none; padding: 6px 14px; border-radius: 5px; font-weight: bold; cursor: pointer; }}
                @media print {{ .no-print-bar {{ display: none !important; }} }}
            </style></head><body>
            <div class="no-print-bar">
                <span><strong>🖨️ Print Preview:</strong> Gunakan pengaturan <em>Landscape</em> pada dialog printer untuk hasil cetak terbaik.</span>
                <button onclick="window.print()">🖨️ Cetak Sekarang / Simpan PDF</button>
            </div>
            <h2>TABEL ANALISA & ACTION PLAN — DEALER {dlr_pil}</h2>
            <div class="sub">Periode Analisa: 1 s.d {tanggal_akhir} {periode_bulan_tahun} | Fokus Horizon: {horizon_lbl} | Acuan Ideal: DB Quality 30%, STU% 10%, ACC% 50%</div>
            ` + tblClone.innerHTML + `
            <script>setTimeout(() => window.print(), 400);<\\/script></body></html>
        `);
        w.document.close();
    }}
    </script></body></html>""", height=620, scrolling=True)

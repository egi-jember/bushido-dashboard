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
</style>""", unsafe_allow_html=True)

DEFAULT_SHARED_API_KEY = "AQ.Ab8RN6LAV5JudlB8Ht6CnFRdJWnvX-be0Jn8zb4NHQ8CNjyHUg"
IDEAL_DBQ_PCT, IDEAL_STU_PCT, IDEAL_ACC_PCT, MAX_NARRATIVE_WORDS = 30.0, 10.0, 50.0, 35
SUBTOTAL_ROW_LABELS = {'SUB SITUBONDO', 'SUB BANYUWANGI', 'JEMBER', 'BONDOWOSO', 'SITUBONDO', 'BANYUWANGI'}
tabel_target_harian = {1:0.0, 2:1.0, 3:2.0, 4:5.0, 5:8.0, 6:12.0, 7:18.0, 8:21.0, 9:24.0, 10:29.0, 11:34.0, 12:36.0, 13:40.0, 14:44.0, 15:48.0, 16:51.0, 17:54.0, 18:57.0, 19:60.0, 20:63.0, 21:67.0, 22:70.0, 23:73.0, 24:77.0, 25:79.0, 26:82.0, 27:84.0, 28:88.0, 29:92.0, 30:100.0, 31:100.0}
FIXED_COUNTER_TARGETS = {'IIN BARIROH': 25, 'SITI NURJANAH': 25, 'TRIA DAMAYANTI': 25, 'MUHAMMAD HAMDAN WAHDI': 15, 'DESVIN NURUL PRISTANTINI': 15, 'RIKA DWI ASTUTI': 15, 'NURUL FADILAH': 15}
FOKUS_KATEGORI_TYPE = ['AT PREMIUM', 'AT CLASSY', 'AT LPM']
daftar_dealer = ['SIP PANJI', 'SIP BESUKI', 'SIP A. YANI', 'SIP SRONO', 'SIP SIAGA', 'SIP SOBO', 'SIP GIRI']
TARGET_DEALER_FILE, TARGET_KOOR_FILE, AI_CONFIG_FILE, UPLOAD_DIR = 'dealer_targets_saved.json', 'koor_targets_saved.json', 'ai_config.json', 'saved_raw_files'
DB_Multi_DIR, RAW_META_FILE = os.path.join(UPLOAD_DIR, 'database_files'), os.path.join(UPLOAD_DIR, 'metadata.json')
os.makedirs(DB_Multi_DIR, exist_ok=True)

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

def build_compact_html_string(df_items, df_full, columns, name_col, metric_col, table_dom_id, header_labels=None, ultra_compact=False, title_text=None):
    if df_full is None or df_full.empty: return ''
    hdrs = header_labels if (header_labels is not None and len(header_labels) == len(columns)) else columns
    min_v = float(df_items[metric_col].min()) if (df_items is not None and not df_items.empty and metric_col in df_items.columns) else 0.0
    max_v = float(df_items[metric_col].max()) if (df_items is not None and not df_items.empty and metric_col in df_items.columns) else 0.0
    n_items = len(df_items) if df_items is not None else 0
    wrap_cls, tbl_cls = ('ultra-compact-wrap', 'ultra-compact-tbl') if ultra_compact else ('compact-table-wrap', 'compact-tbl')
    banner_html = f'<div class="cap-title-banner">🐺 {title_text}</div>' if title_text else ''
    html = [f'<div id="{table_dom_id}" class="{wrap_cls}">{banner_html}<table class="{tbl_cls}"><thead><tr>'] + [f'<th>{h}</th>' for h in hdrs] + ['</tr></thead><tbody>']
    for _, row in df_full.iterrows():
        nm = str(row[name_col])
        style = 'background-color: #4318FF; color: #FFFFFF; font-weight: 800;' if (nm.startswith('TOTAL') or nm.startswith('CREDIT SHARE')) else ('background-color: #1E293B; color: #FFFFFF; font-weight: 800;' if nm in SUBTOTAL_ROW_LABELS else '')
        if not style and df_items is not None and not df_items.empty and metric_col in df_items.columns:
            m_idx = df_items.index[df_items[name_col] == nm].tolist()
            if m_idx:
                v = float(df_items.loc[m_idx[0], metric_col])
                style = f'color: {get_neon_gradient_hex(((v - min_v) / (max_v - min_v)) if max_v > min_v else (m_idx[0] / max(1, n_items - 1)))};'
        html.append(f'<tr style="{style}">' + ''.join(f'<td>{row[c]}</td>' for c in columns) + '</tr>')
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

def render_compact_html_table(df_items, df_full, columns, name_col, metric_col, key_suffix='tbl', header_labels=None, ultra_compact=False, title_text=None, custom_capture_html=None):
    if df_full is None or df_full.empty: return
    dom_id = f"Capture_{re.sub(r'[^a-zA-Z0-9]', '_', key_suffix)}"
    html_display_str = build_compact_html_string(df_items, df_full, columns, name_col, metric_col, dom_id, header_labels=header_labels, ultra_compact=ultra_compact, title_text=None)
    cap_title = title_text if title_text else key_suffix.replace('_', ' ')
    html_capture_str = custom_capture_html if custom_capture_html is not None else build_compact_html_string(df_items, df_full, columns, name_col, metric_col, f"{dom_id}_cap", header_labels=header_labels, ultra_compact=ultra_compact, title_text=cap_title)
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
    for old in glob.glob(os.path.join(DB_Multi_DIR, "*")):
        try: os.remove(old)
        except Exception: pass
    names, paths = [], []
    for uf in up_files:
        p = os.path.join(DB_Multi_DIR, uf.name)
        with open(p, 'wb') as f: f.write(uf.getbuffer())
        names.append(uf.name); paths.append(p)
    meta = load_json(RAW_META_FILE)
    meta['database_multi'] = {'file_names': names, 'saved_paths': paths, 'count': len(names), 'updated_at': datetime.datetime.now().strftime('%d %b %Y, %H:%M WIB')}
    save_json(meta, RAW_META_FILE)

def get_saved_file_path(prefix):
    meta = load_json(RAW_META_FILE)
    if prefix in meta and os.path.exists(meta[prefix].get('saved_path', '')): return meta[prefix]['saved_path']
    m = glob.glob(os.path.join(UPLOAD_DIR, f"{prefix}_latest.*"))
    return m[0] if m else None

def get_saved_database_paths():
    meta = load_json(RAW_META_FILE)
    if 'database_multi' in meta:
        v = [p for p in meta['database_multi'].get('saved_paths', []) if os.path.exists(p)]
        if v: return v
    return sorted(glob.glob(os.path.join(DB_Multi_DIR, "*.*")))

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
Lakukan analisa silang yang tajam (temukan akar masalah/bottleneck tersembunyi dari data di atas) dan susun Action Plan taktis terukur dalam format JSON murni dengan 12 key berikut.

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
  "plan_mp": "Maks 35 kata: kuota rasional +1 s.d +2 STU, SPK, & 4-5 DB/hari per salesman kritis TANPA MENURUNKAN KUALITAS DATABASE."
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
MAIN_TABS, UPLOAD_TAB = ['📈 SALES', '🏍️ BY TYPE', '⚙️ PROCESS', '🏦 LEASING', '🏢 DETAIL DEALER'], '📁 UPLOAD FILE'
if 'active_menu_tab' not in st.session_state: st.session_state['active_menu_tab'] = '📈 SALES'

def on_main_nav_change():
    if st.session_state.get('nav_main_radio') is not None: st.session_state['active_menu_tab'], st.session_state['nav_upload_radio'] = st.session_state['nav_main_radio'], None
def on_upload_nav_change():
    if st.session_state.get('nav_upload_radio') is not None: st.session_state['active_menu_tab'], st.session_state['nav_main_radio'] = st.session_state['nav_upload_radio'], None

st.sidebar.radio('Menu Bushido Analysis:', MAIN_TABS, index=MAIN_TABS.index(st.session_state['active_menu_tab']) if st.session_state['active_menu_tab'] in MAIN_TABS else None, key='nav_main_radio', on_change=on_main_nav_change, label_visibility='collapsed')
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
st.sidebar.radio('Menu Upload File:', [UPLOAD_TAB], index=0 if st.session_state['active_menu_tab'] == UPLOAD_TAB else None, key='nav_upload_radio', on_change=on_upload_nav_change, label_visibility='collapsed')
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
menu_pilihan = st.session_state['active_menu_tab']

def clean_str(val): return '' if pd.isna(val) else ' '.join(str(val).split()).upper()
def nospace_str(val): return '' if pd.isna(val) else ''.join(str(val).split()).upper()
def alnum_str(val): return '' if pd.isna(val) else ''.join(c for c in str(val).upper() if c.isalnum())
FIXED_COUNTER_TARGETS_NS = {alnum_str(k): v for k, v in FIXED_COUNTER_TARGETS.items()}

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

def normalize_dealer_name(val):
    s = clean_str(val)
    if not s or s in ['NAN', 'NONE'] or s in daftar_dealer: return s
    if any(k in s for k in ['A YANI', 'A. YANI', 'AYANI', 'A.YANI']): return 'SIP A. YANI'
    for k, v in [('BESUKI', 'SIP BESUKI'), ('PANJI', 'SIP PANJI'), ('SRONO', 'SIP SRONO'), ('SIAGA', 'SIP SIAGA'), ('SOBO', 'SIP SOBO'), ('GIRI', 'SIP GIRI')]:
        if k in s: return v
    return s

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

def read_single_db_file(fpath):
    df_raw = pd.read_csv(fpath, header=None) if fpath.lower().endswith('.csv') else pd.read_excel(fpath, header=None)
    if df_raw is None or df_raw.empty: return pd.DataFrame()
    h_idx = next((r for r in range(min(25, len(df_raw))) if any(m in [clean_str(v) for v in df_raw.iloc[r].values if pd.notna(v)] for m in ['CUSTOMER NAME', 'POINT NAME', 'PROSPECT DATE', 'DATA TYPE', 'KTP NO.', 'POINT CODE'])), 0)
    df = df_raw.iloc[h_idx + 1:].copy()
    df.columns = make_unique_columns([str(c).strip() for c in df_raw.iloc[h_idx].values])
    df = df.dropna(how='all').reset_index(drop=True)
    cu = [c.upper() for c in df.columns]
    s_chk = df.iloc[:, cu.index('CUSTOMER NAME')] if 'CUSTOMER NAME' in cu else df.iloc[:, 0]
    df = df[s_chk.notna() & ~s_chk.astype(str).str.strip().str.upper().isin(['CUSTOMER NAME', 'NO', 'NO.', 'TOTAL', 'JUMLAH', 'NAN', 'NONE', ''])].reset_index(drop=True)
    df['Nama_Dealer_Clean'] = normalize_dealer_name(os.path.splitext(os.path.basename(fpath))[0]) or 'TIDAK DIKETAHUI'
    col_k = df.iloc[:, cu.index('POINT NAME')].astype(str).str.strip().str.upper() if 'POINT NAME' in cu else (df.iloc[:, 10].astype(str).str.strip().str.upper() if df.shape[1] > 10 else None)
    if col_k is not None: df.loc[col_k == 'SIP PANJI BESUKI', 'Nama_Dealer_Clean'] = 'SIP BESUKI'
    df['Data_Type_Clean'] = df.iloc[:, cu.index('DATA TYPE')].astype(str).str.strip().str.upper() if 'DATA TYPE' in cu else (df.iloc[:, 5].astype(str).str.strip().str.upper() if df.shape[1] > 5 else '')
    return parse_date_cols(df)

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

path_faktur, path_nota, path_lookup = get_saved_file_path('faktur'), get_saved_file_path('nota'), get_saved_file_path('lookup')
paths_database, path_spk = get_saved_database_paths(), get_saved_file_path('spk')
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

mapping_salesman_koor, mapping_dealer_spk, mapping_type_lookup, mapping_type_lookup_nospace, daftar_kategori_type = {}, {}, {}, {}, []
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
        sc, kc, hr = None, None, None
        for r in range(min(50, len(df_lk))):
            for c, val in enumerate(df_lk.iloc[r]):
                vs = clean_str(val)
                if any(k in vs for k in ['NAMA SALES', 'SALESMAN', 'PRAMUNIAGA', 'PEGAWAI']): sc = c
                elif 'KOOR' in vs: kc = c
            if sc is not None and kc is not None: hr = r; break
        if sc is not None and kc is not None:
            for i in range(hr + 1, len(df_lk)):
                sm, kr = clean_str(df_lk.iloc[i, sc]), clean_str(df_lk.iloc[i, kc])
                if sm and sm not in ['NAN', 'NONE']: mapping_salesman_koor[sm] = kr
        if df_lk.shape[1] > 9:
            for i in range(len(df_lk)):
                ri, rj = clean_str(df_lk.iloc[i, 8]), clean_str(df_lk.iloc[i, 9])
                if ri and rj and ri not in ['NAN', 'NONE'] and rj not in ['NAN', 'NONE']:
                    ni, nj = normalize_dealer_name(ri), normalize_dealer_name(rj)
                    if nj in daftar_dealer: mapping_dealer_spk[ri] = nj
                    elif ni in daftar_dealer: mapping_dealer_spk[rj] = ni
                    else: mapping_dealer_spk[ri] = nj
    except Exception as e: st.error(f'Error Lookup: {e}')

unmapped_types_all, sales_tanpa_koor, sales_tanpa_koor_db, sales_tanpa_koor_spk = set(), set(), set(), set()

def assign_koor_and_sales(df, col_idx_override=None, tracker=None, koor_col_name='Koor'):
    if df is None or df.empty: return df
    cu = [str(c).strip().upper() for c in df.columns]
    sc_name = df.columns[col_idx_override] if (col_idx_override is not None and df.shape[1] > col_idx_override) else None
    if sc_name is None: sc_name = next((df.columns[cu.index(x)] for x in ['NAMA PEGAWAI', 'NAMA SALES', 'NAMA PRAMUNIAGA', 'SALESMAN', 'PRAMUNIAGA', 'SALES', 'SALES NAME', 'NAMA SALESMAN', 'SALES PERSON', 'SALESPERSON', 'PIC', 'EMPLOYEE NAME', 'SALESMAN NAME', 'CREATED BY', 'USER INPUT'] if x in cu), None)
    if sc_name is None and len(df.columns) > 7 and not str(df.iloc[0, 7]).strip().isdigit(): sc_name = df.columns[7]
    if sc_name is not None:
        s_s = df[sc_name].iloc[:, 0] if isinstance(df[sc_name], pd.DataFrame) else df[sc_name]
        s_cl = s_s.astype(str).str.split().str.join(' ').str.upper()
        df['Salesman_Clean'] = s_cl.where(~s_cl.isin(['NAN', 'NONE', '', 'NA', '-']), None)
        def map_kr(s):
            if s and pd.notna(s) and mapping_salesman_koor:
                if s not in mapping_salesman_koor and tracker is not None: tracker.add(s)
                return mapping_salesman_koor.get(s, 'LAIN-LAIN')
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

current_month, current_year = 10, 2026
for dc in [df_faktur_all, df_faktur, df_nota, df_spk, df_database]:
    if dc is not None and not dc.empty and 'bulan' in dc.columns and dc['bulan'].notna().any():
        current_year = int(dc['tahun'].dropna().max())
        current_month = int(dc[dc['tahun'] == current_year]['bulan'].dropna().max())
        break
last_month, last_month_year = (current_month - 1, current_year) if current_month > 1 else (12, current_year - 1)

max_day_in_month = pycal.monthrange(current_year, current_month)[1]
st.sidebar.markdown('### 📅 Periode Analisa')
tgl_kal_pilihan = st.sidebar.date_input('Pilih Tanggal Akhir Periode (Kalender):', value=datetime.date(current_year, current_month, min(14, max_day_in_month)), min_value=datetime.date(current_year, current_month, 1), max_value=datetime.date(current_year, current_month, max_day_in_month), format='DD/MM/YYYY')
tanggal_akhir = int(tgl_kal_pilihan[-1].day) if isinstance(tgl_kal_pilihan, (tuple, list)) and len(tgl_kal_pilihan) > 0 else (int(tgl_kal_pilihan.day) if hasattr(tgl_kal_pilihan, 'day') else 14)

target_persen_harian = tabel_target_harian.get(tanggal_akhir, 0.0)
persen_desimal = target_persen_harian / 100.0
col_name_pct = f'{target_persen_harian:.0f}%' if target_persen_harian.is_integer() else f'{target_persen_harian}%'
hari_aktif = max(1, int(tanggal_akhir))
st.sidebar.markdown(f'<div class="target-ideal-caption">🎯 Target Ideal Tgl {tanggal_akhir}: {col_name_pct}</div>', unsafe_allow_html=True)

if menu_pilihan == '📁 UPLOAD FILE':
    st.markdown('<div class="main-title">UPLOAD FILE MENTAH</div><div class="sub-title">Silakan unggah ke-6 kategori sumber data serta logo di bawah ini (tersimpan otomatis & permanen)</div>', unsafe_allow_html=True)
    meta_info = load_json(RAW_META_FILE)
    logo_uf = st.file_uploader('🐺 Upload Logo AZURA Pojok Kiri Atas (.jpg / .png)', type=['jpg', 'jpeg', 'png'], key='azura_logo_up')
    if logo_uf: save_raw_file(logo_uf, 'azura_logo'); st.success(f"✅ Logo AZURA berhasil diperbarui: **{logo_uf.name}**"); st.rerun()
    st.divider()
    for lbl_up, lbl, kp, exts in [('1. Upload Faktur (.xls / .xlsx)', 'Faktur', 'faktur', ['xls', 'xlsx']), ('2. Upload Nota (.xls / .xlsx)', 'Nota', 'nota', ['xls', 'xlsx']), ('3. Upload Data Lookup (.xls / .xlsx)', 'Data Lookup', 'lookup', ['xls', 'xlsx'])]:
        uf = st.file_uploader(lbl_up, type=exts, key=f'{kp}_up')
        if uf: save_raw_file(uf, kp); st.success(f"✅ {lbl} diperbarui: **{uf.name}**")
        elif kp in meta_info and os.path.exists(meta_info[kp].get('saved_path', '')): st.info(f"📌 **{lbl} Aktif:** `{meta_info[kp]['original_name']}` ({meta_info[kp]['updated_at']})")
        else: st.warning(f"⚠️ Belum ada file {lbl}.")
    db_ups = st.file_uploader('4. Upload File Database — Bisa Pilih 6 File Sekaligus (.xls / .xlsx / .csv)', type=['xls', 'xlsx', 'csv'], accept_multiple_files=True, key='db_up')
    if db_ups: save_database_files(db_ups); st.success(f"✅ **{len(db_ups)} File Database** disimpan.")
    elif 'database_multi' in meta_info and get_saved_database_paths(): st.info(f"📌 **Database Aktif ({meta_info['database_multi'].get('count',0)} File):** `{', '.join(meta_info['database_multi'].get('file_names',[]))}`")
    else: st.warning("⚠️ Belum ada file Database.")
    for lbl_up, lbl, kp in [('5. Upload File SPK (.xls / .xlsx / .csv)', 'SPK', 'spk'), ('6. Upload File Master Employee (.xls / .xlsx / .csv) — Target Otomatis Salesman (Kolom C: Nama, Kolom F: Posisi)', 'Master Employee', 'employee')]:
        uf = st.file_uploader(lbl_up, type=['xls', 'xlsx', 'csv'], key=f'{kp}_up')
        if uf: save_raw_file(uf, kp); st.success(f"✅ {lbl} diperbarui: **{uf.name}**")
        elif kp in meta_info and os.path.exists(meta_info[kp].get('saved_path', '')): st.info(f"📌 **{lbl} Aktif:** `{meta_info[kp]['original_name']}` ({meta_info[kp]['updated_at']})")
        else: st.warning(f"⚠️ Belum ada file {lbl}.")

def calc_sales_row(name_label, name_col, targ, df_f_c, df_f_l, df_n_c, df_n_t):
    ideal, stu, stulm, nota, today = round(targ * persen_desimal), len(df_f_c), len(df_f_l), len(df_n_c), len(df_n_t)
    forc, pct = (round(nota / persen_desimal) if persen_desimal > 0 else 0), ((stu / targ * 100.0) if targ > 0 else 0.0)
    return {name_col: name_label, 'TARGET': targ, 'IDEAL': ideal, 'STU': stu, 'NOTA': nota, 'TODAY': today, col_name_pct: f'{pct:.2f}%', 'GAP TG': stu - targ, 'STU LM': stulm, '% LM': f'{(stu / stulm * 100.0):.2f}%' if stulm > 0 else '0.00%', 'GAP LM': stu - stulm, 'FORC': forc, '_nota': nota, '_ideal': ideal, '_pct': pct}

def calc_proses_row(name_label, name_col, df_db_sub, stu_cnt):
    db_c = len(df_db_sub)
    hot_c = len(df_db_sub[df_db_sub['Data_Type_Clean'] == 'DEAL PROSPECT']) if (not df_db_sub.empty and 'Data_Type_Clean' in df_db_sub.columns) else 0
    mp_c = int(df_db_sub['Salesman_Clean'].dropna().nunique()) if (not df_db_sub.empty and 'Salesman_Clean' in df_db_sub.columns) else 0
    avg_db, db_q, stu_p = ((db_c / mp_c / hari_aktif) if mp_c > 0 else 0.0), ((hot_c / db_c * 100.0) if db_c > 0 else 0.0), ((stu_cnt / db_c * 100.0) if db_c > 0 else 0.0)
    return {name_col: name_label, 'JML MP': mp_c, 'AVG DB': f'{avg_db:.2f}', 'DB': db_c, 'HOT': hot_c, 'DB Q': f'{db_q:.2f}%', 'STU': stu_cnt, 'STU%': f'{stu_p:.2f}%', '_stu_pct': stu_p}

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
        rows.append(r)
    if not rows: return pd.DataFrame(), pd.DataFrame(), {}
    df_it = pd.DataFrame(rows).sort_values(by=(['_growth_val', '_stu_val'] if sort_by_growth else ['_stu_val', 'DB']), ascending=([True, True] if sort_by_growth else [False, False])).reset_index(drop=True)
    ts, tsl, tdb, thot, tspk = int(df_it['STU'].sum()), int(df_it['STU LM'].sum()), int(df_it['DB'].sum()), int(df_it['HOT'].sum()), int(df_it['SPK'].sum())
    tgrw, tdbq, taccp, tstup = ((ts / tsl * 100.0) if tsl > 0 else 0.0), ((thot / tdb * 100.0) if tdb > 0 else 0.0), ((t_acc / (t_acc + t_rej) * 100.0) if (t_acc + t_rej) > 0 else 0.0), ((ts / tdb * 100.0) if tdb > 0 else 0.0)
    tot_r = {col_headers_name: tot_label, 'STU': ts, 'STU LM': tsl, 'GROWTH': f'{tgrw:.2f}%', 'DB': tdb, 'HOT': thot, 'DB Q': f'{tdbq:.2f}%', 'SPK': tspk, 'ACC%': f'{taccp:.2f}%', 'STU%': f'{tstup:.2f}%', '_stu_val': ts, '_growth_val': tgrw}
    for l in lsg_list: tot_r[l], tot_r[f'%{l}'] = t_lf[l], f'{(t_la[l] / (t_la[l] + t_lr[l]) * 100.0):.2f}%' if (t_la[l] + t_lr[l]) > 0 else '0.00%'
    return df_it, pd.concat([df_it, pd.DataFrame([tot_r])], ignore_index=True), tot_r

df_fak_curr_g = df_faktur[(df_faktur['bulan'] == current_month) & (df_faktur['tahun'] == current_year) & (df_faktur['hari'] <= tanggal_akhir)] if (df_faktur is not None and 'bulan' in df_faktur.columns) else pd.DataFrame()
df_fak_lm_g = df_faktur[(df_faktur['bulan'] == last_month) & (df_faktur['tahun'] == last_month_year) & (df_faktur['hari'] <= tanggal_akhir)] if (df_faktur is not None and 'bulan' in df_faktur.columns) else pd.DataFrame()
df_nota_curr_g = df_nota[(df_nota['bulan'] == current_month) & (df_nota['tahun'] == current_year) & (df_nota['hari'] <= tanggal_akhir)] if (df_nota is not None and 'bulan' in df_nota.columns) else pd.DataFrame()
df_nota_tod_g = df_nota[(df_nota['bulan'] == current_month) & (df_nota['tahun'] == current_year) & (df_nota['hari'] == tanggal_akhir)] if (df_nota is not None and 'bulan' in df_nota.columns) else pd.DataFrame()
df_db_curr_g = df_database[(df_database['hari'] >= 1) & (df_database['hari'] <= tanggal_akhir)] if (df_database is not None and 'hari' in df_database.columns and df_database['hari'].notna().any()) else (df_database.copy() if df_database is not None else pd.DataFrame())
df_spk_curr_g = df_spk[(df_spk['bulan'] == current_month) & (df_spk['tahun'] == current_year) & (df_spk['hari'] <= tanggal_akhir)] if (df_spk is not None and 'bulan' in df_spk.columns) else pd.DataFrame()
df_spk_lm_g = df_spk[(df_spk['bulan'] == last_month) & (df_spk['tahun'] == last_month_year) & (df_spk['hari'] <= tanggal_akhir)] if (df_spk is not None and 'bulan' in df_spk.columns) else pd.DataFrame()

if menu_pilihan == '📈 SALES':
    st.markdown(f'<div class="main-title">DASHBOARD PENJUALAN (s.d Tgl {tanggal_akhir} Oktober 2026)</div><div class="sub-title">Sistem Monitoring Kinerja Dealer Terpadu</div>', unsafe_allow_html=True)
    kolom_dlr = ['NAMA DEALER', 'TARGET', 'IDEAL', 'STU', 'NOTA', 'TODAY', col_name_pct, 'GAP TG', 'STU LM', '% LM', 'GAP LM', 'FORC']
    saved_td, saved_tk = load_json(TARGET_DEALER_FILE), load_json(TARGET_KOOR_FILE)
    cd_nota = 'Nama Dealer' if (df_nota is not None and 'Nama Dealer' in df_nota.columns) else 'Dealer'

    d_rows = [calc_sales_row(d, 'NAMA DEALER', safe_int(saved_td.get(d, 0)), df_fak_curr_g[df_fak_curr_g['Nama Dealer'] == d] if not df_fak_curr_g.empty else pd.DataFrame(), df_fak_lm_g[df_fak_lm_g['Nama Dealer'] == d] if not df_fak_lm_g.empty else pd.DataFrame(), df_nota_curr_g[df_nota_curr_g[cd_nota] == d] if not df_nota_curr_g.empty else pd.DataFrame(), df_nota_tod_g[df_nota_tod_g[cd_nota] == d] if not df_nota_tod_g.empty else pd.DataFrame()) for d in daftar_dealer]
    df_dealers = pd.DataFrame(d_rows).sort_values(by=['_pct', 'STU'], ascending=[True, True]).reset_index(drop=True)
    tot_r = calc_sales_row('TOTAL', 'NAMA DEALER', int(df_dealers['TARGET'].sum()), df_fak_curr_g, df_fak_lm_g, df_nota_curr_g, df_nota_tod_g)
    tot_r['IDEAL'], tot_r['FORC'] = int(df_dealers['IDEAL'].sum()), int(df_dealers['FORC'].sum())
    df_full = pd.concat([df_dealers, pd.DataFrame([tot_r])], ignore_index=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"**🎯 Target vs Result**<br><span style='font-size:24px;font-weight:bold;'>{tot_r['TARGET']:,} / {tot_r['NOTA']:,}</span><br><b>{tot_r['_pct']:.2f}% tercapai</b>", unsafe_allow_html=True)
    k2.markdown(f"**📅 Nota Hari Ini**<br><span style='font-size:24px;font-weight:bold;'>{tot_r['TODAY']:,} Unit</span><br><b>Tgl {tanggal_akhir} Oktober</b>", unsafe_allow_html=True)
    k3.markdown(f"**📊 AVG Nota (s.d Tgl {tanggal_akhir})**<br><span style='font-size:24px;font-weight:bold;'>{(tot_r['NOTA']/hari_aktif):.2f} / hari</span><br><b>Total {tot_r['NOTA']} nota</b>", unsafe_allow_html=True)
    k4.markdown(f"**📈 Forecast Total**<br><span style='font-size:24px;font-weight:bold;'>{tot_r['FORC']:,} Unit</span><br><b>Forecast vs Target: {(tot_r['FORC']/tot_r['TARGET']*100 if tot_r['TARGET']>0 else 0):.2f}%</b>", unsafe_allow_html=True)

    def render_editable_sales(df_src, cols, name_col, avg_pct, key_s, save_file, btn_lbl, title_txt):
        def sty(row):
            v = row[name_col]
            if v == 'TOTAL': return ['background-color: #4318FF; color: #FFFFFF'] * len(row)
            m = df_src[df_src[name_col] == v]
            if not m.empty:
                stu, idl, pc = m.iloc[0]['STU'], m.iloc[0]['_ideal'], m.iloc[0]['_pct']
                return ['color: #00FF66' if stu >= idl else ('color: #FFEA00' if pc > avg_pct else 'color: #FF007F')] * len(row)
            return [''] * len(row)
        ed = st.data_editor(df_src[cols].style.apply(sty, axis=1), hide_index=True, use_container_width=False, height=calc_table_height(df_src), column_config=get_compact_col_config(cols, name_col, 'TARGET'), disabled=[c for c in cols if c != 'TARGET'], key=key_s)
        c_b1, c_b2 = st.columns([1, 3])
        with c_b1:
            if st.button(btn_lbl, type='primary', key=f'btn_{key_s}'):
                cur = load_json(save_file)
                for _, r in ed.iterrows():
                    if r[name_col] != 'TOTAL': cur[r[name_col]] = safe_int(r['TARGET'])
                save_json(cur, save_file); st.success('Target disimpan!'); st.rerun()
        with c_b2:
            df_items_only = df_src[df_src[name_col] != 'TOTAL'].reset_index(drop=True)
            render_table_image_buttons(f'cap_{key_s}', f'Penjualan_{key_s}_Tgl_{tanggal_akhir}', standalone_html=build_compact_html_string(df_items_only, df_src, cols, name_col, '_pct', f'cap_{key_s}', title_text=title_txt))

    st.divider()
    st.markdown('<div class="section-title">DASHBOARD PENJUALAN DEALER</div>', unsafe_allow_html=True)
    render_editable_sales(df_full, kolom_dlr, 'NAMA DEALER', tot_r['_pct'], 'tbl_dlr', TARGET_DEALER_FILE, '💾 Simpan Target Manual Dealer', f'DASHBOARD PENJUALAN DEALER (1 s.d {tanggal_akhir} Oktober 2026)')

    ent_all = set(clean_str(v) for v in mapping_salesman_koor.values() if clean_str(v)) | set(k for k in saved_tk.keys() if k != 'TOTAL')
    for d_s in [df_faktur, df_nota]:
        if d_s is not None and 'Koor' in d_s.columns: ent_all.update(str(k) for k in d_s['Koor'].dropna().unique() if str(k) != 'LAIN-LAIN')
    k_list, c_list = [], []
    for ent in sorted(list(ent_all)):
        r_e = calc_sales_row(ent, 'NAMA', get_koor_or_counter_target(ent, saved_tk), df_fak_curr_g[df_fak_curr_g['Koor'] == ent] if not df_fak_curr_g.empty else pd.DataFrame(), df_fak_lm_g[df_fak_lm_g['Koor'] == ent] if not df_fak_lm_g.empty else pd.DataFrame(), df_nota_curr_g[df_nota_curr_g['Koor'] == ent] if not df_nota_curr_g.empty else pd.DataFrame(), df_nota_tod_g[df_nota_tod_g['Koor'] == ent] if not df_nota_tod_g.empty else pd.DataFrame())
        if r_e['TARGET'] == 0 and r_e['STU'] == 0 and r_e['NOTA'] == 0 and r_e['STU LM'] == 0: continue
        (c_list if ent.upper().startswith('COUNTER') else k_list).append(r_e)

    for sub_l, nc, sec_t, k_ed, btn_l in [(k_list, 'NAMA KOORDINATOR', 'DASHBOARD PENJUALAN KOORDINATOR', 'tbl_koor', '💾 Simpan Target Koordinator'), (c_list, 'NAMA COUNTER', 'DASHBOARD PENJUALAN COUNTER', 'tbl_cnt', '💾 Simpan Target Counter')]:
        st.divider()
        st.markdown(f'<div class="section-title">{sec_t}</div>', unsafe_allow_html=True)
        if sub_l:
            df_s = pd.DataFrame(sub_l).sort_values(by=['_pct', 'STU'], ascending=[True, True]).reset_index(drop=True).rename(columns={'NAMA': nc})
            tt, ts, tsl = int(df_s['TARGET'].sum()), int(df_s['STU'].sum()), int(df_s['STU LM'].sum())
            tp = (ts / tt * 100.0) if tt > 0 else 0.0
            tr = {nc: 'TOTAL', 'TARGET': tt, 'IDEAL': int(df_s['IDEAL'].sum()), 'STU': ts, 'NOTA': int(df_s['NOTA'].sum()), 'TODAY': int(df_s['TODAY'].sum()), col_name_pct: f'{tp:.2f}%', 'GAP TG': ts - tt, 'STU LM': tsl, '% LM': f'{(ts/tsl*100 if tsl>0 else 0):.2f}%', 'GAP LM': ts - tsl, 'FORC': int(df_s['FORC'].sum()), '_ideal': int(df_s['IDEAL'].sum()), '_pct': tp}
            cols_s = [nc, 'TARGET', 'IDEAL', 'STU', 'NOTA', 'TODAY', col_name_pct, 'GAP TG', 'STU LM', '% LM', 'GAP LM', 'FORC']
            render_editable_sales(pd.concat([df_s, pd.DataFrame([tr])], ignore_index=True), cols_s, nc, tp, k_ed, TARGET_KOOR_FILE, btn_l, f'{sec_t} (1 s.d {tanggal_akhir} Oktober 2026)')

elif menu_pilihan == '🏍️ BY TYPE':
    st.markdown(f'<div class="main-title">DASHBOARD PENJUALAN PER TYPE (1 s.d {tanggal_akhir} Oktober 2026)</div><div class="sub-title">Analisa Performa Unit Berdasarkan Kategori Type (Fokus: AT PREMIUM, AT CLASSY, AT LPM)</div>', unsafe_allow_html=True)
    pil_dlr = st.selectbox('🏢 Filter Dealer (Tabel Rekap Per Type):', ['SEMUA DEALER'] + daftar_dealer, index=0)
    fc = df_fak_curr_g if pil_dlr == 'SEMUA DEALER' else (df_fak_curr_g[df_fak_curr_g['Nama Dealer'] == pil_dlr] if not df_fak_curr_g.empty else pd.DataFrame())
    fl = df_fak_lm_g if pil_dlr == 'SEMUA DEALER' else (df_fak_lm_g[df_fak_lm_g['Nama Dealer'] == pil_dlr] if not df_fak_lm_g.empty else pd.DataFrame())
    dbc = df_db_curr_g if pil_dlr == 'SEMUA DEALER' else (df_db_curr_g[df_db_curr_g['Nama_Dealer_Clean'] == pil_dlr] if not df_db_curr_g.empty else pd.DataFrame())
    spkc = df_spk_curr_g if pil_dlr == 'SEMUA DEALER' else (df_spk_curr_g[df_spk_curr_g['Nama_Dealer_SPK'] == pil_dlr] if not df_spk_curr_g.empty else pd.DataFrame())

    kol_tp = ['TYPE', 'STU', 'STU LM', 'GROWTH', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF']
    df_ti, df_tf, tr_t = build_type_table(fc, fl, dbc, spkc, [(k, 'Type_Clean', 'Type_Clean', 'Type_Clean') for k in FOKUS_KATEGORI_TYPE], 'TYPE', sort_by_growth=True)
    if not df_tf.empty:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"**🏍️ Total STU**<br><span style='font-size:24px;font-weight:bold;color:#00FF66;'>{tr_t['STU']:,} Unit</span><br><b>LM: {tr_t['STU LM']:,} ({tr_t['GROWTH']})</b>", unsafe_allow_html=True)
        c2.markdown(f"**🗂️ Total DB**<br><span style='font-size:24px;font-weight:bold;'>{tr_t['DB']:,}</span><br><b>Hot Prospect: {tr_t['HOT']:,}</b>", unsafe_allow_html=True)
        c3.markdown(f"**✨ DB Quality (Ideal 30%)**<br><span style='font-size:24px;font-weight:bold;color:#00E5FF;'>{tr_t['DB Q']}</span><br><b>HOT / DB</b>", unsafe_allow_html=True)
        c4.markdown(f"**📝 Total SPK (Ideal ACC 50%)**<br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{tr_t['SPK']:,} ({tr_t['ACC%']})</span><br><b>SPK Quality</b>", unsafe_allow_html=True)
        c5.markdown(f"**📈 Konversi STU% (Ideal 10%)**<br><span style='font-size:24px;font-weight:bold;color:#FF007F;'>{tr_t['STU%']}</span><br><b>STU / DB</b>", unsafe_allow_html=True)
        st.divider()
        jdl_rekap_tp = f'TABEL PENJUALAN PER TYPE — {pil_dlr} (1 s.d {tanggal_akhir} Oktober 2026)'
        st.markdown(f'<div class="section-title">{jdl_rekap_tp}</div>', unsafe_allow_html=True)
        render_compact_html_table(df_ti, df_tf, kol_tp, 'TYPE', '_growth_val', key_suffix=f'Rekap_Type_{pil_dlr}', title_text=jdl_rekap_tp)

    kol_dt = ['NAMA DEALER', 'STU', 'STU LM', 'GROWTH', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF']
    for kt, jdl in [('AT PREMIUM', 'TABEL PENJUALAN AT PREMIUM PER DEALER'), ('AT CLASSY', 'TABEL PENJUALAN AT CLASSY PER DEALER'), ('AT LPM', 'TABEL PENJUALAN AT LPM PER DEALER')]:
        st.divider()
        full_jdl_tp = f'{jdl} (1 s.d {tanggal_akhir} Oktober 2026)'
        st.markdown(f'<div class="section-title">{full_jdl_tp}</div>', unsafe_allow_html=True)
        di, df_d, _ = build_type_table(df_fak_curr_g[df_fak_curr_g['Type_Clean'] == kt] if not df_fak_curr_g.empty else pd.DataFrame(), df_fak_lm_g[df_fak_lm_g['Type_Clean'] == kt] if not df_fak_lm_g.empty else pd.DataFrame(), df_db_curr_g[df_db_curr_g['Type_Clean'] == kt] if not df_db_curr_g.empty else pd.DataFrame(), df_spk_curr_g[df_spk_curr_g['Type_Clean'] == kt] if not df_spk_curr_g.empty else pd.DataFrame(), [(d, 'Nama Dealer', 'Nama_Dealer_Clean', 'Nama_Dealer_SPK') for d in daftar_dealer], 'NAMA DEALER', sort_by_growth=True)
        render_compact_html_table(di, df_d, kol_dt, 'NAMA DEALER', '_growth_val', key_suffix=jdl, title_text=full_jdl_tp)

elif menu_pilihan == '⚙️ PROCESS':
    st.markdown(f'<div class="main-title">PROSES KERJA (1 s.d {tanggal_akhir} Oktober 2026)</div><div class="sub-title">Monitoring Database, Hot Prospect, Produktivitas MP, DB Quality (Ideal 30%) & Konversi STU (Ideal 10%)</div>', unsafe_allow_html=True)
    db_rows = [calc_proses_row(d, 'NAMA DEALER', df_db_curr_g[df_db_curr_g['Nama_Dealer_Clean'] == d] if not df_db_curr_g.empty else pd.DataFrame(), len(df_fak_curr_g[df_fak_curr_g['Nama Dealer'] == d]) if not df_fak_curr_g.empty else 0) for d in daftar_dealer]
    df_dbd = pd.DataFrame(db_rows).sort_values(by='_stu_pct', ascending=True).reset_index(drop=True)
    t_db, t_hot, t_mp, t_stu = int(df_dbd['DB'].sum()), int(df_dbd['HOT'].sum()), int(df_dbd['JML MP'].sum()), int(df_dbd['STU'].sum())
    t_avg, t_q, t_sp = (t_db / t_mp / hari_aktif if t_mp > 0 else 0.0), (t_hot / t_db * 100.0 if t_db > 0 else 0.0), (t_stu / t_db * 100.0 if t_db > 0 else 0.0)
    tot_dbr = pd.DataFrame([{'NAMA DEALER': 'TOTAL', 'JML MP': t_mp, 'AVG DB': f'{t_avg:.2f}', 'DB': t_db, 'HOT': t_hot, 'DB Q': f'{t_q:.2f}%', 'STU': t_stu, 'STU%': f'{t_sp:.2f}%', '_stu_pct': t_sp}])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f"**🗂️ Total Database**<br><span style='font-size:24px;font-weight:bold;color:#00FF66;'>{t_db:,}</span>", unsafe_allow_html=True)
    c2.markdown(f"**🔥 Hot Prospect**<br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{t_hot:,}</span>", unsafe_allow_html=True)
    c3.markdown(f"**👥 Total MP Input**<br><span style='font-size:24px;font-weight:bold;'>{t_mp:,} MP ({t_avg:.2f}/hr)</span>", unsafe_allow_html=True)
    c4.markdown(f"**✨ DB Quality (Ideal 30%)**<br><span style='font-size:24px;font-weight:bold;color:#00E5FF;'>{t_q:.2f}%</span>", unsafe_allow_html=True)
    c5.markdown(f"**📈 Total STU (Ideal STU% 10%)**<br><span style='font-size:24px;font-weight:bold;color:#FF007F;'>{t_stu:,} ({t_sp:.2f}%)</span>", unsafe_allow_html=True)

    st.divider()
    jdl_pr_dlr = f'PROSES KERJA DEALER (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_pr_dlr}</div>', unsafe_allow_html=True)
    render_compact_html_table(df_dbd, pd.concat([df_dbd, tot_dbr], ignore_index=True), ['NAMA DEALER', 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'STU', 'STU%'], 'NAMA DEALER', '_stu_pct', key_suffix='Proses_Kerja_Dealer', title_text=jdl_pr_dlr)

    saved_tk = load_json(TARGET_KOOR_FILE)
    ent_p = set(clean_str(v) for v in mapping_salesman_koor.values() if clean_str(v)) | set(k for k in saved_tk.keys() if k != 'TOTAL')
    for ds in [df_fak_curr_g, df_db_curr_g]:
        if not ds.empty and 'Koor' in ds.columns: ent_p.update(str(k) for k in ds['Koor'].dropna().unique() if str(k) != 'LAIN-LAIN')
    pk_list, pc_list = [], []
    for ent in sorted(list(ent_p)):
        rp = calc_proses_row(ent, 'NAMA', df_db_curr_g[df_db_curr_g['Koor'] == ent] if not df_db_curr_g.empty else pd.DataFrame(), len(df_fak_curr_g[df_fak_curr_g['Koor'] == ent]) if not df_fak_curr_g.empty else 0)
        if get_koor_or_counter_target(ent, saved_tk) == 0 and rp['DB'] == 0 and rp['STU'] == 0: continue
        (pc_list if ent.upper().startswith('COUNTER') else pk_list).append(rp)

    for sl, nc, st_lbl in [(pk_list, 'NAMA KOORDINATOR', 'PROSES KERJA KOORDINATOR'), (pc_list, 'NAMA COUNTER', 'PROSES KERJA COUNTER')]:
        st.divider()
        full_st_lbl = f'{st_lbl} (1 s.d {tanggal_akhir} Oktober 2026)'
        st.markdown(f'<div class="section-title">{full_st_lbl}</div>', unsafe_allow_html=True)
        if sl:
            dfs = pd.DataFrame(sl).sort_values(by='_stu_pct', ascending=True).reset_index(drop=True).rename(columns={'NAMA': nc})
            sdb, shot, smp, sstu = int(dfs['DB'].sum()), int(dfs['HOT'].sum()), int(dfs['JML MP'].sum()), int(dfs['STU'].sum())
            tr = pd.DataFrame([{nc: 'TOTAL', 'JML MP': smp, 'AVG DB': f'{(sdb/smp/hari_aktif if smp>0 else 0):.2f}', 'DB': sdb, 'HOT': shot, 'DB Q': f'{(shot/sdb*100 if sdb>0 else 0):.2f}%', 'STU': sstu, 'STU%': f'{(sstu/sdb*100 if sdb>0 else 0):.2f}%', '_stu_pct': (sstu/sdb*100 if sdb>0 else 0)}])
            render_compact_html_table(dfs, pd.concat([dfs, tr], ignore_index=True), [nc, 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'STU', 'STU%'], nc, '_stu_pct', key_suffix=st_lbl, title_text=full_st_lbl)

elif menu_pilihan == '🏦 LEASING':
    st.markdown(f'<div class="main-title">DASHBOARD LEASING (1 s.d {tanggal_akhir} Oktober 2026)</div><div class="sub-title">Monitoring SPK, Growth, Approval Rate (Acuan Ideal ACC% = 50%), SPK Terbuka & Rincian Leasing</div>', unsafe_allow_html=True)
    kol_lsg = ['SPK', 'SPK LM', 'GROWTH', 'ACC%', 'TERBUKA', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF', 'IMFI', '%IMFI']
    def get_dlr_lsg(dlrs, lbl, nc='NAMA DEALER'):
        return calc_leasing_row(lbl, df_spk_curr_g[df_spk_curr_g['Nama_Dealer_SPK'].isin(dlrs)] if not df_spk_curr_g.empty else pd.DataFrame(), df_spk_lm_g[df_spk_lm_g['Nama_Dealer_SPK'].isin(dlrs)] if not df_spk_lm_g.empty else pd.DataFrame(), nc)

    d_sit, d_bwi = ['SIP PANJI', 'SIP BESUKI'], ['SIP SRONO', 'SIP SIAGA', 'SIP SOBO', 'SIP GIRI', 'SIP A. YANI']
    df_sit = pd.DataFrame([get_dlr_lsg([d], d) for d in d_sit]).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True)
    df_bwi = pd.DataFrame([get_dlr_lsg([d], d) for d in d_bwi]).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True)
    df_lsg_full = pd.concat([df_sit, pd.DataFrame([get_dlr_lsg(d_sit, 'SUB SITUBONDO')]), df_bwi, pd.DataFrame([get_dlr_lsg(d_bwi, 'SUB BANYUWANGI')]), pd.DataFrame([get_dlr_lsg(daftar_dealer, 'TOTAL')])], ignore_index=True)
    jdl_lsg_dlr = f'DASHBOARD LEASING DEALER (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_lsg_dlr}</div>', unsafe_allow_html=True)
    render_compact_html_table(pd.concat([df_sit, df_bwi], ignore_index=True), df_lsg_full, ['NAMA DEALER'] + kol_lsg, 'NAMA DEALER', '_acc_val', key_suffix='Leasing_Dealer', title_text=jdl_lsg_dlr)

    saved_tk = load_json(TARGET_KOOR_FILE)
    ent_s = sorted(list(set(clean_str(v) for v in mapping_salesman_koor.values() if clean_str(v)) | set(k for k in saved_tk.keys() if k != 'TOTAL') | (set(str(k) for k in df_spk['Koor_SPK'].dropna().unique() if str(k) != 'LAIN-LAIN') if (df_spk is not None and 'Koor_SPK' in df_spk.columns) else set())))
    for elist, nc, sec_t in [([e for e in ent_s if not e.upper().startswith('COUNTER')], 'NAMA KOORDINATOR', 'DASHBOARD LEASING KOORDINATOR'), ([e for e in ent_s if e.upper().startswith('COUNTER')], 'NAMA COUNTER', 'DASHBOARD LEASING COUNTER')]:
        st.divider()
        full_sec_lsg = f'{sec_t} (1 s.d {tanggal_akhir} Oktober 2026)'
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
    jdl_stu_lsg_fak = f'STU PER LEASING — FAKTUR (1 s.d {tanggal_akhir} Oktober 2026 vs Bulan Lalu)'
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
    jdl_rej_analysis = f'REJECTION ANALYSIS — LEASING {pil_lsg_reject} (1 s.d {tanggal_akhir} Oktober 2026)'
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

elif menu_pilihan == '🏢 DETAIL DEALER':
    dlr_pil = st.selectbox('🏢 Pilih Dealer untuk Review:', daftar_dealer, index=0)
    main_hdr_text = f'DETAIL DEALER — {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)'
    sub_hdr_text = f'Rekapitulasi Terpadu Penjualan, Proses Kerja, SPK Leasing, Penjualan Per Type & Detail Salesman Khusus Dealer {dlr_pil} (Acuan Ideal: DB Quality 30% | STU% 10% | ACC% 50%)'
    st.markdown(f'<div class="main-title">{main_hdr_text}</div><div class="sub-title">{sub_hdr_text}</div>', unsafe_allow_html=True)

    saved_td, saved_tk = load_json(TARGET_DEALER_FILE), load_json(TARGET_KOOR_FILE)
    cd_nota = 'Nama Dealer' if (df_nota is not None and 'Nama Dealer' in df_nota.columns) else 'Dealer'

    f_all = df_faktur[df_faktur['Nama Dealer'] == dlr_pil] if (df_faktur is not None and 'Nama Dealer' in df_faktur.columns) else pd.DataFrame()
    f_c = df_fak_curr_g[df_fak_curr_g['Nama Dealer'] == dlr_pil] if not df_fak_curr_g.empty else pd.DataFrame()
    f_l = df_fak_lm_g[df_fak_lm_g['Nama Dealer'] == dlr_pil] if not df_fak_lm_g.empty else pd.DataFrame()
    n_all = df_nota[df_nota[cd_nota] == dlr_pil] if (df_nota is not None and cd_nota in df_nota.columns) else pd.DataFrame()
    n_c = df_nota_curr_g[df_nota_curr_g[cd_nota] == dlr_pil] if not df_nota_curr_g.empty else pd.DataFrame()
    n_t = df_nota_tod_g[df_nota_tod_g[cd_nota] == dlr_pil] if not df_nota_tod_g.empty else pd.DataFrame()
    db_all = df_database[df_database['Nama_Dealer_Clean'] == dlr_pil] if (df_database is not None and 'Nama_Dealer_Clean' in df_database.columns) else pd.DataFrame()
    db_c = df_db_curr_g[df_db_curr_g['Nama_Dealer_Clean'] == dlr_pil] if not df_db_curr_g.empty else pd.DataFrame()
    s_all = df_spk[df_spk['Nama_Dealer_SPK'] == dlr_pil] if (df_spk is not None and 'Nama_Dealer_SPK' in df_spk.columns) else pd.DataFrame()
    s_c = df_spk_curr_g[df_spk_curr_g['Nama_Dealer_SPK'] == dlr_pil] if not df_spk_curr_g.empty else pd.DataFrame()
    s_l = df_spk_lm_g[df_spk_lm_g['Nama_Dealer_SPK'] == dlr_pil] if not df_spk_lm_g.empty else pd.DataFrame()

    ent_dlr = set()
    for ds, ck in [(f_all, 'Koor'), (n_all, 'Koor'), (db_all, 'Koor'), (s_all, 'Koor_SPK')]:
        if not ds.empty and ck in ds.columns: ent_dlr.update(clean_str(v) for v in ds[ck].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'LAIN-LAIN'])
    gab_ent, lbl_tot, kol_nm = sorted(list(ent_dlr)), f'TOTAL ({dlr_pil})', 'KOOR / COUNTER / DEALER'

    r_tot_p = calc_sales_row(lbl_tot, kol_nm, safe_int(saved_td.get(dlr_pil, 0)), f_c, f_l, n_c, n_t)
    r_tot_pr = calc_proses_row(lbl_tot, kol_nm, db_c, len(f_c))
    r_tot_s = calc_leasing_row(lbl_tot, s_c, s_l, kol_nm)

    rp_all = [calc_sales_row(e, kol_nm, get_koor_or_counter_target(e, saved_tk), f_c[f_c['Koor'] == e] if not f_c.empty else pd.DataFrame(), f_l[f_l['Koor'] == e] if not f_l.empty else pd.DataFrame(), n_c[n_c['Koor'] == e] if not n_c.empty else pd.DataFrame(), n_t[n_t['Koor'] == e] if not n_t.empty else pd.DataFrame()) for e in gab_ent]
    df_p_it = pd.DataFrame(rp_all).sort_values(by=['_pct', 'STU'], ascending=[True, True]).reset_index(drop=True) if rp_all else pd.DataFrame()

    rpr_all = [calc_proses_row(e, kol_nm, db_c[db_c['Koor'] == e] if not db_c.empty else pd.DataFrame(), len(f_c[f_c['Koor'] == e]) if not f_c.empty else 0) for e in gab_ent]
    df_pr_it = pd.DataFrame(rpr_all).sort_values(by=['_stu_pct', 'STU'], ascending=[True, True]).reset_index(drop=True) if rpr_all else pd.DataFrame()

    rs_all = [calc_leasing_row(e, s_c[s_c['Koor_SPK'] == e] if not s_c.empty else pd.DataFrame(), s_l[s_l['Koor_SPK'] == e] if not s_l.empty else pd.DataFrame(), kol_nm) for e in gab_ent]
    df_s_it = pd.DataFrame(rs_all).sort_values(by=['_acc_val', '_spk_val'], ascending=[True, True]).reset_index(drop=True) if rs_all else pd.DataFrame()

    sm_set = set()
    for ds in [f_c, n_c, db_c, s_c]:
        if not ds.empty and 'Salesman_Clean' in ds.columns: sm_set.update(clean_str(v) for v in ds['Salesman_Clean'].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'TOTAL'])
    if not sm_set:
        for ds in [f_all, n_all, db_all, s_all]:
            if not ds.empty and 'Salesman_Clean' in ds.columns: sm_set.update(clean_str(v) for v in ds['Salesman_Clean'].dropna().unique() if clean_str(v) and clean_str(v) not in ['NAN', 'NONE', 'TOTAL'])

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
        r_sm.append({'NAMA SALESMAN': sm, 'TARGET': targ, 'STU': stu, col_name_pct: f'{pct_sm:.2f}%', 'AVG DB': f'{(db_v/hari_aktif):.2f}', 'DB': db_v, 'HOT': hot_v, 'DB Q': f'{dbq_v:.2f}%', 'SPK': spk_v, 'ACC%': f'{acc_p_v:.2f}%', 'STU%': f'{stup_v:.2f}%', '_stu_val': stu, '_db_val': db_v, '_pct_val': pct_sm, '_dbq_val': dbq_v, '_stup_val': stup_v, '_acc_val': acc_p_v})

    forc_pct_dlr = (r_tot_p['FORC'] / r_tot_p['TARGET'] * 100.0) if r_tot_p['TARGET'] > 0 else 0.0
    kpi_items_html = [
        f"<b>🎯 Target vs Result</b><br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{r_tot_p['TARGET']:,} / {r_tot_p['STU']:,}</span><br><b>{r_tot_p['_pct']:.2f}% tercapai (Nota: {r_tot_p['NOTA']:,})<br>Ideal Tgl {tanggal_akhir} ({col_name_pct}): {r_tot_p['IDEAL']:,} Unit</b>",
        f"<b>✨ Database Quality</b><br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{r_tot_pr['DB Q']}</span><br><b>Hot: {r_tot_pr['HOT']:,} / {r_tot_pr['DB']:,} DB (Ideal 30%)</b>",
        f"<b>📈 STU Ratio</b><br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{r_tot_pr['STU%']}</span><br><b>STU: {r_tot_pr['STU']:,} / {r_tot_pr['DB']:,} DB (Ideal 10%)</b>",
        f"<b>🚀 SPK Growth</b><br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{r_tot_s['GROWTH']}</span><br><b>SPK: {r_tot_s['SPK']:,} vs LM: {r_tot_s['SPK LM']:,}</b>",
        f"<b>✅ Approval Ratio</b><br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{r_tot_s['ACC%']}</span><br><b>Open SPK: {r_tot_s['TERBUKA']:,} (Ideal 50%)</b>",
        f"<b>🏁 Forecast Closing</b><br><span style='font-size:24px;font-weight:bold;color:#FFEA00;'>{r_tot_p['FORC']:,} Unit</span><br><b>Forecast vs Target: {forc_pct_dlr:.2f}%</b>"
    ]
    for col_st, h_str in zip(st.columns(6), kpi_items_html): col_st.markdown(h_str, unsafe_allow_html=True)

    df_koor_only, df_cnt_only = pd.DataFrame(), pd.DataFrame()
    if not df_p_it.empty:
        df_koor_only = df_p_it[~df_p_it[kol_nm].str.upper().str.startswith('COUNTER')].copy()
        df_cnt_only = df_p_it[df_p_it[kol_nm].str.upper().str.startswith('COUNTER')].sort_values(by=['_pct', 'STU'], ascending=[True, True])

    focus_koor_html = "Tidak ada data Koordinator"
    if not df_koor_only.empty:
        k_eval_list = []
        for _, rk in df_koor_only.iterrows():
            knm = str(rk[kol_nm])
            k_pr = df_pr_it[df_pr_it[kol_nm] == knm].iloc[0] if (not df_pr_it.empty and knm in df_pr_it[kol_nm].values) else {}
            k_sp = df_s_it[df_s_it[kol_nm] == knm].iloc[0] if (not df_s_it.empty and knm in df_s_it[kol_nm].values) else {}
            k_eval_list.append({'nama': knm, 'target': safe_int(rk['TARGET']), 'ideal': safe_int(rk['IDEAL']), 'stu': safe_int(rk['STU']), 'pct': safe_float(rk['_pct']), 'db': safe_int(k_pr.get('DB', 0)), 'dbq_str': k_pr.get('DB Q', '0.00%'), 'stup_str': k_pr.get('STU%', '0.00%'), 'spk_grw_str': k_sp.get('GROWTH', '0.00%'), 'acc_str': k_sp.get('ACC%', '0.00%'), 'dbq_val': safe_float(k_pr.get('DB Q', 0.0)), 'stup_val': safe_float(k_pr.get('STU%', 0.0)), 'acc_val': safe_float(k_sp.get('_acc_val', 0.0))})
        k_eval_list.sort(key=lambda x: (0 if x['target'] > 0 else 1, x['pct'], x['stu'], x['stup_val'], x['dbq_val'], x['acc_val']))
        fk = k_eval_list[0]
        focus_koor_html = f"<span style='color:#FFEA00;font-weight:800;'>{fk['nama']}</span> — Target vs Result: <b>{fk['target']}/{fk['stu']} ({fk['pct']:.2f}% | Ideal: {fk['ideal']})</b> | DB Quality: <b>{fk['dbq_str']}</b> | STU Ratio: <b>{fk['stup_str']}</b> | SPK Growth: <b>{fk['spk_grw_str']}</b> | Approval: <b>{fk['acc_str']}</b>"

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

    st.markdown(f"""<div class="focus-alert-box"><div>🎯 <b>Focus Koordinator :</b> {focus_koor_html}</div><div style="margin-top:4px;">👤 <b>Focus Salesman :</b> {focus_sm_html}</div></div>""", unsafe_allow_html=True)

    st.divider()
    jdl_rev_1 = f'1. TABEL PENJUALAN — {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_rev_1}</div>', unsafe_allow_html=True)
    kol_pj = [kol_nm, 'TARGET', 'IDEAL', 'STU', 'NOTA', 'TODAY', col_name_pct, 'GAP TG', 'STU LM', '% LM', 'GAP LM', 'FORC']
    df_p_full = pd.concat([df_p_it, pd.DataFrame([r_tot_p])], ignore_index=True)

    tbl1_only_html = build_compact_html_string(df_p_it, df_p_full, kol_pj, kol_nm, '_pct', f'cap_tbl1_inner_{dlr_pil}', title_text=None)
    kpi_grid_cells = ''.join(f'<div style="flex:1;min-width:160px;font-size:13.5px;line-height:1.45;color:#FFFFFF;">{item}</div>' for item in kpi_items_html)
    custom_cap_tbl1 = f"""<div style="width:1320px;background-color:#0E1117;padding:20px 24px;font-family:'Source Sans Pro',sans-serif;color:#FFFFFF;box-sizing:border-box;">
        <div style="font-size:38px;font-weight:800;color:#4318FF;margin-bottom:4px;line-height:1.1;">{main_hdr_text}</div>
        <div style="font-size:14px;font-weight:600;color:#64748B;margin-bottom:18px;">{sub_hdr_text}</div>
        <div style="display:flex;justify-content:space-between;gap:14px;margin-bottom:16px;">{kpi_grid_cells}</div>
        <div style="margin-top:12px;margin-bottom:18px;padding:11px 16px;background:linear-gradient(90deg,rgba(255,0,127,0.14) 0%,rgba(14,17,23,0.95) 100%);border-left:4px solid #FF007F;border-top:1px solid #2D3748;border-right:1px solid #2D3748;border-bottom:1px solid #2D3748;border-radius:6px;font-size:13.5px;line-height:1.65;color:#E2E8F0;">
            <div>🎯 <b>Focus Koordinator :</b> {focus_koor_html}</div>
            <div style="margin-top:4px;">👤 <b>Focus Salesman :</b> {focus_sm_html}</div>
        </div>
        <hr style="border:none;border-top:1px solid #2D3748;margin:16px 0;">
        <div style="font-size:21px;font-weight:700;color:#4318FF;margin-bottom:10px;">{jdl_rev_1}</div>
        {tbl1_only_html}
    </div>"""
    render_compact_html_table(df_p_it, df_p_full, kol_pj, kol_nm, '_pct', key_suffix=f'Review_1_Penjualan_{dlr_pil}', title_text=jdl_rev_1, custom_capture_html=custom_cap_tbl1)

    st.divider()
    jdl_rev_2 = f'2. TABEL PROSES KERJA — {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_rev_2}</div>', unsafe_allow_html=True)
    kol_pr = [kol_nm, 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'STU', 'STU%']
    render_compact_html_table(df_pr_it, pd.concat([df_pr_it, pd.DataFrame([r_tot_pr])], ignore_index=True), kol_pr, kol_nm, '_stu_pct', key_suffix=f'Review_2_Proses_{dlr_pil}', title_text=jdl_rev_2)

    st.divider()
    jdl_rev_3 = f'3. TABEL SPK & LEASING — {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_rev_3}</div>', unsafe_allow_html=True)
    kol_sp = [kol_nm, 'SPK', 'SPK LM', 'GROWTH', 'ACC%', 'TERBUKA', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF', 'IMFI', '%IMFI']
    render_compact_html_table(df_s_it, pd.concat([df_s_it, pd.DataFrame([r_tot_s])], ignore_index=True), kol_sp, kol_nm, '_acc_val', key_suffix=f'Review_3_Leasing_{dlr_pil}', title_text=jdl_rev_3)

    st.divider()
    jdl_rev_4 = f'4. TABEL PENJUALAN PER TYPE — {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_rev_4}</div>', unsafe_allow_html=True)
    kol_t_d = ['TYPE', 'STU', 'STU LM', 'GROWTH', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF']
    df_td_i, df_td_f, _ = build_type_table(f_c, f_l, db_c, s_c, [(k, 'Type_Clean', 'Type_Clean', 'Type_Clean') for k in FOKUS_KATEGORI_TYPE], 'TYPE', tot_label=lbl_tot, sort_by_growth=True)
    if not df_td_f.empty: render_compact_html_table(df_td_i, df_td_f, kol_t_d, 'TYPE', '_growth_val', key_suffix=f'Review_4_Type_{dlr_pil}', title_text=jdl_rev_4)

    st.divider()
    jdl_rev_5 = f'5. TABEL DETAIL SALESMAN — {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)'
    st.markdown(f'<div class="section-title">{jdl_rev_5}</div>', unsafe_allow_html=True)
    if len(mapping_emp_target) <= len(FIXED_COUNTER_TARGETS): st.warning('⚠️ File Master Employee belum diunggah. Silakan unggah di menu **📁 UPLOAD FILE** agar kolom TARGET otomatis terisi.')
    kol_sm = ['NAMA SALESMAN', 'TARGET', 'STU', col_name_pct, 'AVG DB', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%']
    if r_sm:
        df_smi = pd.DataFrame(r_sm).sort_values(by=['TARGET', '_pct_val', '_stu_val', '_db_val'], ascending=[False, True, True, True]).reset_index(drop=True)
        tt, ts, tdb, thot, tspk, n_sm = int(df_smi['TARGET'].sum()), int(df_smi['STU'].sum()), int(df_smi['DB'].sum()), int(df_smi['HOT'].sum()), int(df_smi['SPK'].sum()), len(df_smi)
        tpct_sm = (ts / tt * 100.0) if tt > 0 else 0.0
        tot_sm = {'NAMA SALESMAN': lbl_tot, 'TARGET': tt, 'STU': ts, col_name_pct: f'{tpct_sm:.2f}%', 'AVG DB': f'{(tdb/n_sm/hari_aktif if n_sm>0 else 0):.2f}', 'DB': tdb, 'HOT': thot, 'DB Q': f'{(thot/tdb*100 if tdb>0 else 0):.2f}%', 'SPK': tspk, 'ACC%': f'{(t_sa/(t_sa+t_sr)*100 if (t_sa+t_sr)>0 else 0):.2f}%', 'STU%': f'{(ts/tdb*100 if tdb>0 else 0):.2f}%', '_stu_val': ts, '_pct_val': tpct_sm}
        render_compact_html_table(df_smi, pd.concat([df_smi, pd.DataFrame([tot_sm])], ignore_index=True), kol_sm, 'NAMA SALESMAN', '_pct_val', key_suffix=f'Review_5_Salesman_{dlr_pil}', title_text=jdl_rev_5)
    else: st.info(f'ℹ️ Belum ada data Salesman untuk dealer {dlr_pil}.')

    st.divider()
    tgl_sasaran = 30 if tanggal_akhir > 21 else min(30, tanggal_akhir + 7)
    sisa_hari = max(1, tgl_sasaran - tanggal_akhir)
    horizon_lbl = f"Optimalisasi Closing s.d Tgl 30 Oktober 2026 ({sisa_hari} Hari Kerja)" if tanggal_akhir > 21 else f"Akselerasi 7 Hari ke Depan s.d Tgl {tgl_sasaran} Oktober 2026 ({sisa_hari} Hari Kerja)"

    jdl_rev_6 = f'6. TABEL ANALISA & ACTION PLAN — {dlr_pil} ({horizon_lbl})'
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
    if not df_td_i.empty:
        wt_row = df_td_i.iloc[0]
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
        return {k: limit_words(v, MAX_NARRATIVE_WORDS) for k, v in {'cond_dealer': c_dlr, 'plan_dealer': p_dlr, 'cond_type': c_tp, 'plan_type': p_tp, 'cond_leasing': c_lsg, 'plan_leasing': p_lsg, 'cond_koor': c_kr, 'plan_koor': p_kr, 'cond_counter': c_cn, 'plan_counter': p_cn, 'cond_mp': c_mp, 'plan_mp': p_mp}.items()}

    active_api_key = resolve_gemini_api_key()
    cache_key = f"ai_tbl6_v9_35w_{dlr_pil}_{tanggal_akhir}_{dlr_stu}_{cur_db}_{cur_spk}"

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
                st.markdown('<a href="[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)" target="_blank" style="display:inline-block;text-align:center;width:100%;padding:6px 10px;background:#1E293B;color:#00E5FF;border:1px solid #334155;border-radius:6px;text-decoration:none;font-size:12.5px;font-weight:700;">🔑 Ambil Key AIzaSy Gratis (Google AI Studio)</a>', unsafe_allow_html=True)
            st.code(f'GEMINI_API_KEY = "{inp_api_key.strip() or active_api_key}"', language='toml')

    if gen_ai_clicked:
        with st.spinner(f'🤖 Sedang membedah data mentah & menyusun Target Rasional 7 Hari ke depan untuk {dlr_pil} (Maks 35 kata/sel)...'):
            raw_t1 = df_p_it[[kol_nm, 'TARGET', 'IDEAL', 'STU', 'NOTA', col_name_pct, 'STU LM', '% LM']].to_string(index=False) if not df_p_it.empty else "Kosong"
            raw_t2 = df_pr_it[[kol_nm, 'JML MP', 'AVG DB', 'DB', 'HOT', 'DB Q', 'STU', 'STU%']].to_string(index=False) if not df_pr_it.empty else "Kosong"
            raw_t3 = df_s_it[[kol_nm, 'SPK', 'SPK LM', 'GROWTH', 'ACC%', 'TERBUKA', 'BAF', '%BAF', 'ADIRA', '%ADIRA', 'SOF', '%SOF', 'IMFI', '%IMFI']].to_string(index=False) if not df_s_it.empty else "Kosong"
            raw_t4 = df_td_i[['TYPE', 'STU', 'STU LM', 'GROWTH', 'DB', 'HOT', 'DB Q', 'SPK', 'ACC%', 'STU%']].to_string(index=False) if not df_td_i.empty else "Kosong"
            raw_context_for_ai = (
                f"Dealer: {dlr_pil} | Periode: 1 s.d {tanggal_akhir} Oktober 2026 | Horizon Action Plan: {horizon_lbl}.\n"
                f"ACUAN TARGET RASIONAL 7 HARI KE DEPAN (WAJIB DIPAKAI AI AGAR TARGET MASUK AKAL & MENANTANG):\n"
                f"- Dealer {dlr_pil} (STU saat ini {dlr_stu} dari target bulanan {dlr_targ}, Ideal tgl {tanggal_akhir}={dlr_ideal}): Target Rasional s.d tgl {tgl_sasaran} adalah tambahan +{tambahan_stu_wajib} STU (sehingga total mencapai {stu_sasaran_rasional} unit, atau {target_stu_per_hari:.1f} STU/hari), input {target_db_per_mp_hari:.1f} DB/MP/hari.\n"
                f"- {wt_rational_str}\n- {wk_rational_str}\n- {wc_rational_str}\n"
                f"TOTAL LEASING & FAKTUR KREDIT: Total SPK={cur_spk} (LM={cur_spk_lm}), ACC%={cur_acc_pct:.1f}%, SPK Terbuka={cur_open_spk} (target cair rasional +{potensi_stu_open} STU, tambah +{kebutuhan_spk_baru} SPK baru). Faktur Kredit Cair={tot_fak_kredit_curr} unit (BAF={fak_kredit_curr['BAF']}, ADIRA={fak_kredit_curr['ADIRA']}, SOF={fak_kredit_curr['SOF']}). Alasan Reject SPK Tertinggi: {top_rej_reasons_str}.\n"
                f"--- DATA TABEL 1 (PENJUALAN KOOR/COUNTER) ---\n{raw_t1}\n--- DATA TABEL 2 (PROSES KERJA KOOR/COUNTER) ---\n{raw_t2}\n--- DATA TABEL 3 (LEASING KOOR/COUNTER) ---\n{raw_t3}\n--- DATA TABEL 4 (PER TYPE) ---\n{raw_t4}\n--- DATA SALESMAN AKTIF ZONA KRITIS (NON-COUNTER, DB>=2) ---\n{top_bad_raw_str}"
            )
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
    ]

    rows_html_list, copy_texts_dict = [], {}
    for idx_r, (item_lbl, c_txt, p_txt) in enumerate(analisa_rows_data):
        cid, pid = f"cond_txt_{idx_r}", f"plan_txt_{idx_r}"
        copy_texts_dict[cid], copy_texts_dict[pid] = c_txt, p_txt
        rows_html_list.append(f'<tr><td class="item-col">{item_lbl}</td><td class="cond-col">{format_paragraphs_html(c_txt)}<div class="cell-btn-wrap no-capture"><button class="cell-copy-btn" onclick="copyCellText(\'{cid}\', this)">📋 Copy Condition</button></div></td><td class="plan-col">{format_paragraphs_html(p_txt)}<div class="cell-btn-wrap no-capture"><button class="cell-copy-btn" onclick="copyCellText(\'{pid}\', this)">📋 Copy Action Plan</button></div></td></tr>')

    tabel_analisa_dom_id = f"Capture_Analisa_{re.sub(r'[^a-zA-Z0-9]', '_', dlr_pil)}"
    copy_payload_json, safe_dlr_fname = json.dumps(copy_texts_dict), re.sub(r'[^a-zA-Z0-9_-]', '_', f"Analisa_ActionPlan_{dlr_pil}_Tgl_{tanggal_akhir}")

    components.html(f"""<html><head><script src="[https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js)"></script><style>
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
            <html><head><title>Print Review Analisa — DEALER {dlr_pil} (1 s.d {tanggal_akhir} Oktober 2026)</title>
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
            <div class="sub">Periode Analisa: 1 s.d {tanggal_akhir} Oktober 2026 | Fokus Horizon: {horizon_lbl} | Acuan Ideal: DB Quality 30%, STU% 10%, ACC% 50%</div>
            ` + tblClone.innerHTML + `
            <script>setTimeout(() => window.print(), 400);<\\/script></body></html>
        `);
        w.document.close();
    }}
    </script></body></html>""", height=620, scrolling=True)

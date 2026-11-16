"""
rssm_faktur.py — Tarik laporan dari Online Report RSSM / RM lalu export ke Excel (97-2003) Data-Only,
persis seperti langkah manual: Login → Laporan → pilih laporan → Lokasi JEMBER → Periode → Eksport → Lihat → Export.

Laporan yang didukung (lihat LAPORAN di bawah):
  • faktur : http://103.123.97.83/RSSM/ · PENGAJUAN FAKTUR DETAIL          · tgl 1 bulan LALU s/d hari ini
  • nota   : http://103.123.97.83/rm/   · NOTA JUAL SEPEDA MOTOR NETT MDS  · tgl 1 bulan INI  s/d hari ini
  • spk    : http://103.123.97.83/rm/   · SPK LEASING                      · tgl 1 bulan LALU s/d hari ini
  • stok   : http://103.123.97.83/rm/   · STOK DETAIL (Transaksi: SEPEDA MOTOR) · posisi per hari ini (tanpa tgl awal)

Dipakai 2 cara:
  1. Dari aplikasi Streamlit (tombol "⚡ Generate Faktur" / "⚡ Generate Nota" di menu Upload File) — user/password dari Secrets.
  2. Dijalankan langsung di PC untuk uji coba / cadangan:
         python rssm_faktur.py            (menanyakan laporan, user & password; file .xls disimpan di folder ini)

Hanya memakai library standar Python + requests (sudah terpasang bersama Streamlit).
"""
import datetime
import html
import json
import re

import requests

LAPORAN = {
    'faktur': dict(judul='Faktur', base_url='http://103.123.97.83/RSSM/', report='PENGAJUAN FAKTUR DETAIL',
                   area_kode='03', area_nama='JEMBER', periode='bulan_lalu',
                   judul_file='PENGAJUAN FAKTUR DETAIL', min_baris=10),
    'nota': dict(judul='Nota', base_url='http://103.123.97.83/rm/', report='NOTA JUAL SEPEDA MOTOR NETT MDS',
                 area_kode='13', area_nama='JEMBER', periode='bulan_ini',
                 judul_file='NOTA PENJUALAN SEPEDA MOTOR NETT', min_baris=8),
    'spk': dict(judul='SPK', base_url='http://103.123.97.83/rm/', report='SPK LEASING',
                area_kode='13', area_nama='JEMBER', periode='bulan_lalu',
                judul_file='SPK LEASING', min_baris=7),
    'stok': dict(judul='Stok', base_url='http://103.123.97.83/rm/', report='STOK DETAIL',
                 area_kode='13', area_nama='JEMBER', periode='hari_ini', tanpa_tgl_awal=True,
                 transaksi_kode='M', transaksi_nama='SEPEDA MOTOR',
                 judul_file='STOK DETAIL', min_baris=11),
}
EXPORT_FORMAT = 'RecordToMSExcel'          # = "Microsoft Excel (97-2003) Data-Only"
XLS_MAGIC = b'\xd0\xcf\x11\xe0'            # tanda awal file .xls (format Excel 97-2003)
_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'


class RSSMError(Exception):
    """Kesalahan yang pesannya aman ditampilkan ke pengguna."""


def _hidden_fields(page):
    """Semua <input type="hidden"> di halaman → {name: value}."""
    out = {}
    for tag in re.findall(r'<input\b[^>]*>', page, flags=re.I):
        if not re.search(r'type\s*=\s*"hidden"', tag, flags=re.I):
            continue
        n_ = re.search(r'\bname\s*=\s*"([^"]+)"', tag)
        v_ = re.search(r'\bvalue\s*=\s*"([^"]*)"', tag)
        if n_:
            out[html.unescape(n_.group(1))] = html.unescape(v_.group(1)) if v_ else ''
    return out


def _span_text(page, span_id):
    m_ = re.search(r'<span[^>]*id="' + re.escape(span_id) + r'"[^>]*>(.*?)</span>', page, flags=re.S | re.I)
    return re.sub(r'<[^>]+>', ' ', html.unescape(m_.group(1))).strip() if m_ else ''


def _crystal_state_json(raw):
    """State viewer di halaman memakai tanda kutip tunggal (gaya JavaScript); browser mengirimnya kembali sebagai JSON."""
    if not raw:
        return raw
    try:
        return json.dumps(json.loads(raw.replace("'", '"')), separators=(',', ':'))
    except Exception:
        return raw   # bentuk tak terduga → kirim apa adanya


def _log(log, msg):
    if log:
        try:
            log(msg)
        except Exception:
            pass


def periode_default(jenis='faktur', today=None):
    """faktur/spk: tgl 1 bulan lalu s/d hari ini · nota: tgl 1 bulan ini s/d hari ini · stok: hari ini (WIB)."""
    today = today or (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).date()
    awal = today.replace(day=1)
    per = LAPORAN.get(jenis, {}).get('periode')
    if per == 'bulan_lalu':
        awal = (awal - datetime.timedelta(days=1)).replace(day=1)
    elif per == 'hari_ini':
        awal = today
    return awal, today


def tarik_laporan(user, password, report, tgl_awal, tgl_akhir, area_kode, area_nama, base_url, timeout=300, log=None,
                  transaksi_kode='', transaksi_nama='', tanpa_tgl_awal=False):
    """Login, buka laporan `report`, export Excel Data-Only. Return bytes file .xls. Gagal → RSSMError (pesan berbahasa Indonesia)."""
    base_url = base_url.rstrip('/') + '/'
    s_ = requests.Session()
    s_.headers.update({'User-Agent': _UA})
    try:
        # 1) Login (sama dengan tombol "Masuk": POST JSON ke Login.aspx/ValidasiLogin)
        _log(log, 'Login…')
        s_.get(base_url + 'Login.aspx', timeout=30)
        r_ = s_.post(base_url + 'Login.aspx/ValidasiLogin', json={'UserID': user, 'ePassword': password},
                     headers={'X-Requested-With': 'XMLHttpRequest'}, timeout=30)
        try:
            hasil = (r_.json() or {}).get('d')
        except ValueError:
            raise RSSMError(f'Login gagal: balasan server tidak dikenali (HTTP {r_.status_code}).')
        if hasil not in ('SUKSES_1', 'SUKSES_0'):
            raise RSSMError('Login ditolak: ' + re.sub(r'<[^>]+>', ' ', str(hasil or 'tanpa keterangan')).strip())

        # 2) Halaman Laporan (ReportFilter)
        _log(log, 'Membuka menu Laporan…')
        r_ = s_.get(base_url + 'ReportFilter.aspx', timeout=60)
        if 'MainContent_ListReport' not in r_.text:
            raise RSSMError('Menu Laporan tidak terbuka setelah login (akun mungkin tidak punya akses Laporan).')
        if f'value="{report}"' not in r_.text:
            raise RSSMError(f'Laporan "{report}" tidak ada di daftar laporan akun ini.')
        form = _hidden_fields(r_.text)
        try:   # langkah yang sama dengan mengklik nama laporan di daftar (mengaktifkan kolom tanggal)
            s_.post(base_url + 'ReportFilter.aspx/CekParameter', json={'ReportName': report}, timeout=30)
        except requests.RequestException:
            pass

        # 3) Isi filter & klik "Lihat" (mode Eksport)
        _log(log, f'Menyiapkan laporan per {tgl_akhir:%d-%m-%Y}…' if tanpa_tgl_awal else f'Menyiapkan laporan {tgl_awal:%d-%m-%Y} s/d {tgl_akhir:%d-%m-%Y}…')
        form.update({
            '__EVENTTARGET': '', '__EVENTARGUMENT': '',
            'ctl00$MainContent$ListReport': report,
            'ctl00$MainContent$ddlArea': str(area_kode),
            'ctl00$MainContent$ccdArea_ClientState': f'{area_kode}:::{area_nama}:::',
            'ctl00$MainContent$ddlLocation': '',          # [Pilih Lokasi] = semua lokasi
            'ctl00$MainContent$ccdLocation_ClientState': '::::::',
            'ctl00$MainContent$ccdTransaction_ClientState': '::::::',
            'ctl00$MainContent$TBeginDate': tgl_awal.strftime('%d-%m-%Y'),
            'ctl00$MainContent$TEndDate': tgl_akhir.strftime('%d-%m-%Y'),
            'ctl00$MainContent$RMode': 'Eksport',
            'ctl00$MainContent$BPrint': 'Lihat',
        })
        if tanpa_tgl_awal:   # kolom tanggal awal terkunci di web untuk laporan ini → tidak ikut dikirim (sama seperti browser)
            form.pop('ctl00$MainContent$TBeginDate', None)
        if transaksi_kode:   # mis. STOK DETAIL: Transaksi = SEPEDA MOTOR
            form['ctl00$MainContent$ddlTransaction'] = str(transaksi_kode)
            form['ctl00$MainContent$ccdTransaction_ClientState'] = f'{transaksi_kode}:::{transaksi_nama}:::'
        r_ = s_.post(base_url + 'ReportFilter.aspx', data=form, timeout=timeout)
        if '__CRYSTALSTATE' not in r_.text:
            err_ = _span_text(r_.text, 'MainContent_LErr')
            if err_:
                raise RSSMError('Permintaan laporan ditolak: ' + err_)
            r_ = s_.get(base_url + 'ReportViewer.aspx', timeout=timeout)   # bila server hanya membuka jendela baru
        if '__CRYSTALSTATE' not in r_.text:
            raise RSSMError('Laporan tidak terbentuk (halaman ReportViewer tidak berisi laporan). Coba lagi atau cek periode.')

        # 4) Export → Excel (97-2003) Data-Only (sama dengan tombol Export di viewer)
        _log(log, 'Export ke Excel…')
        vw = _hidden_fields(r_.text)
        st_key = next((k_ for k_ in vw if k_.startswith('__CRYSTALSTATE')), '__CRYSTALSTATECRV')
        viewer_id = st_key[len('__CRYSTALSTATE'):] or 'CRV'
        vw[st_key] = _crystal_state_json(vw.get(st_key, ''))
        vw['__EVENTTARGET'] = viewer_id
        vw['__EVENTARGUMENT'] = json.dumps({'text': EXPORT_FORMAT, 'range': 'false', 'tb': 'crexport'})
        r_ = s_.post(base_url + 'ReportViewer.aspx', data=vw, timeout=timeout)
        data = r_.content or b''
        if not data.startswith(XLS_MAGIC):
            snippet = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', r_.text[:3000])).strip()[:160] if data else 'kosong'
            raise RSSMError(f'Export tidak menghasilkan file Excel (HTTP {r_.status_code}, isi: {snippet}).')
        _log(log, f'Selesai — {len(data) / 1024:,.0f} KB')
        return data
    except requests.exceptions.ConnectTimeout:
        raise RSSMError('Server tidak menjawab (timeout). Server mungkin sedang mati, atau tidak bisa dijangkau dari lokasi ini.')
    except requests.exceptions.ConnectionError:
        raise RSSMError('Server tidak bisa dihubungi dari lokasi ini (koneksi ditolak / diblokir).')
    except requests.exceptions.ReadTimeout:
        raise RSSMError('Server terlalu lama menyiapkan laporan (timeout). Coba lagi, atau persempit periode.')
    finally:
        try:
            s_.get(base_url + 'Login.aspx', timeout=10)   # = Sign-Out
        except Exception:
            pass
        s_.close()


def tarik(jenis, user, password, tgl_awal=None, tgl_akhir=None, log=None, **override):
    """Tarik laporan jenis 'faktur' / 'nota' memakai pengaturan LAPORAN (bisa ditimpa: base_url, area_kode, area_nama)."""
    cfg = dict(LAPORAN[jenis]); cfg.update({k_: v_ for k_, v_ in override.items() if v_})
    a0, b0 = periode_default(jenis)
    return tarik_laporan(user, password, cfg['report'], tgl_awal or a0, tgl_akhir or b0,
                         cfg['area_kode'], cfg['area_nama'], cfg['base_url'], log=log,
                         transaksi_kode=cfg.get('transaksi_kode', ''), transaksi_nama=cfg.get('transaksi_nama', ''),
                         tanpa_tgl_awal=bool(cfg.get('tanpa_tgl_awal')))


def tarik_faktur(user, password, tgl_awal, tgl_akhir, area_kode='03', area_nama='JEMBER', base_url=LAPORAN['faktur']['base_url'], timeout=300, log=None):
    """Kompatibel dengan versi sebelumnya."""
    return tarik_laporan(user, password, LAPORAN['faktur']['report'], tgl_awal, tgl_akhir, area_kode, area_nama, base_url, timeout, log)


if __name__ == '__main__':   # uji coba di PC: python rssm_faktur.py
    import getpass
    print('=== Tarik laporan RSSM / RM ===')
    j_ = (input('Laporan [faktur / nota / spk / stok / semua] (Enter = semua): ').strip().lower() or 'semua')
    jenis_list = list(LAPORAN) if j_ == 'semua' else [j_]
    u_ = input('ID User : ').strip()
    p_ = getpass.getpass('Password: ')
    gagal = 0
    for jn in jenis_list:
        a_, b_ = periode_default(jn)
        print(f'\n--- {LAPORAN[jn]["judul"]} · ' + (f'per {b_:%d-%m-%Y}' if LAPORAN[jn].get('tanpa_tgl_awal') else f'{a_:%d-%m-%Y} s/d {b_:%d-%m-%Y}'))
        try:
            isi = tarik(jn, u_, p_, a_, b_, log=print)
        except (RSSMError, KeyError) as e_:
            print('GAGAL:', e_); gagal += 1
            continue
        nama = f'{jn.upper()}_RSSM_{b_:%d%m%Y}.xls'
        with open(nama, 'wb') as f_:
            f_.write(isi)
        print('Tersimpan:', nama)
    raise SystemExit(1 if gagal else 0)

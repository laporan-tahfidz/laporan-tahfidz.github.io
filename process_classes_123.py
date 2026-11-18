import sqlite3
import json
import datetime
from collections import defaultdict, Counter

conn = sqlite3.connect('everynight-in-my-dream.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

days_indo = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
months_indo = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
               'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

def format_indo_date(date_val):
    if not date_val:
        return '-'
    s = str(date_val).strip()[:10]
    try:
        dt = datetime.datetime.strptime(s, '%Y-%m-%d')
        day_name = days_indo[dt.weekday()]
        month_name = months_indo[dt.month]
        return f"{day_name}, {dt.day} {month_name} {dt.year}"
    except Exception:
        return s

juz_surah_names = {
    1: "Al-Fatihah 1 - Al-Baqarah 141",
    2: "Al-Baqarah 142 - Al-Baqarah 252",
    3: "Al-Baqarah 253 - Ali 'Imran 92",
    4: "Ali 'Imran 93 - An-Nisa' 23",
    5: "An-Nisa' 24 - An-Nisa' 147",
    6: "An-Nisa' 148 - Al-Ma'idah 81",
    7: "Al-Ma'idah 82 - Al-An'am 110",
    8: "Al-An'am 111 - Al-A'raf 87",
    9: "Al-A'raf 88 - Al-Anfal 40",
    10: "Al-Anfal 41 - At-Taubah 92",
    11: "At-Taubah 93 - Hud 5",
    12: "Hud 6 - Yusuf 52",
    13: "Yusuf 53 - Ibrahim 52",
    14: "Al-Hijr 1 - An-Nahl 128",
    15: "Al-Isra' 1 - Al-Kahf 74",
    16: "Al-Kahf 75 - Ta-Ha 135",
    17: "Al-Anbiya' 1 - Al-Hajj 78",
    18: "Al-Mu'minun 1 - Al-Furqan 20",
    19: "Al-Furqan 21 - An-Naml 55",
    20: "An-Naml 56 - Al-'Ankabut 45",
    21: "Al-'Ankabut 46 - Al-Ahzab 30",
    22: "Al-Ahzab 31 - Ya-Sin 27",
    23: "Ya-Sin 28 - Az-Zumar 31",
    24: "Az-Zumar 32 - Fussilat 46",
    25: "Fussilat 47 - Al-Jatsiyah 37",
    26: "Al-Ahqaf 1 - Adz-Dzariyat 30",
    27: "Adz-Dzariyat 31 - Al-Hadid 29",
    28: "Al-Mujadilah 1 - At-Tahrim 12",
    29: "Al-Mulk 1 - Al-Mursalat 50",
    30: "An-Naba' 1 - An-Nas 6"
}

sequence = [30, 29] + list(range(1, 29))

# Musyrif mapping
musyrif_map = {}
for r in c.execute("SELECT id, nama FROM musyrif"):
    musyrif_map[r['id']] = r['nama']

# Assignment mapping
santri_musyrif = {}
for r in c.execute("SELECT santri_nik, musyrif_id FROM musyrfst WHERE musyrif_id IS NOT NULL"):
    santri_musyrif[str(r['santri_nik'])] = r['musyrif_id']

# Settings
settings = dict(c.execute("SELECT key, value FROM settings").fetchall())
kelas1_year = int(settings.get('kelas1_year', 2026))
kelas2_year = int(settings.get('kelas2_year', 2025))
kelas3_year = int(settings.get('kelas3_year', 2024))

allowed_years = {kelas1_year, kelas2_year, kelas3_year}

# Query ONLY santri in Kelas 1, 2, 3
santri_rows = c.execute(
    "SELECT * FROM santri WHERE tahun_masuk IN (?, ?, ?) ORDER BY tahun_masuk DESC, nama_sesuai_kk ASC",
    (kelas1_year, kelas2_year, kelas3_year)
).fetchall()

santri_nik_set = set(str(s['nik']) for s in santri_rows if s['nik'])
santri_id_set = set(s['id'] for s in santri_rows)

print(f"Total Santri Kelas 1, 2, 3: {len(santri_rows)}")

# Query Pencapaian for these santri only
pencapaian_rows = c.execute(
    "SELECT * FROM pencapaian WHERE nik IN (" + ",".join("?" for _ in santri_nik_set) + ") OR santri_id IN (" + ",".join("?" for _ in santri_id_set) + ") ORDER BY created_at ASC",
    list(santri_nik_set) + list(santri_id_set)
).fetchall()

pencapaian_by_nik = defaultdict(list)
pencapaian_by_id = defaultdict(list)
all_record_dates = []

for r in pencapaian_rows:
    p = dict(r)
    dt_str = str(p.get('created_at', ''))[:10]
    if dt_str:
        all_record_dates.append(dt_str)
    if p.get('nik'):
        pencapaian_by_nik[str(p['nik'])].append(p)
    if p.get('santri_id'):
        pencapaian_by_id[p['santri_id']].append(p)

# Query Tes for these santri only
tes_rows = c.execute(
    "SELECT * FROM tes WHERE nik IN (" + ",".join("?" for _ in santri_nik_set) + ") OR santri_id IN (" + ",".join("?" for _ in santri_id_set) + ") ORDER BY created_at ASC",
    list(santri_nik_set) + list(santri_id_set)
).fetchall()

tes_by_nik = defaultdict(list)
tes_by_id = defaultdict(list)
for r in tes_rows:
    t = dict(r)
    dt_str = str(t.get('created_at', ''))[:10]
    if dt_str:
        all_record_dates.append(dt_str)
    if t.get('nik'):
        tes_by_nik[str(t['nik'])].append(t)
    if t.get('santri_id'):
        tes_by_id[t['santri_id']].append(t)

# Query Laporansabtu for these santri only
sabtu_rows = c.execute(
    "SELECT * FROM laporansabtu WHERE nik IN (" + ",".join("?" for _ in santri_nik_set) + ") OR santri_id IN (" + ",".join("?" for _ in santri_id_set) + ") ORDER BY created_at DESC",
    list(santri_nik_set) + list(santri_id_set)
).fetchall()

sabtu_by_nik = defaultdict(list)
sabtu_by_id = defaultdict(list)
for r in sabtu_rows:
    ls = dict(r)
    dt_str = str(ls.get('created_at', ''))[:10]
    if dt_str:
        all_record_dates.append(dt_str)
    try:
        ls['murajaah'] = json.loads(ls['murajaahentries']) if ls['murajaahentries'] else []
    except:
        ls['murajaah'] = []
    try:
        ls['hafalan_tidak_lancar'] = json.loads(ls['hafalanentries']) if ls['hafalanentries'] else []
    except:
        ls['hafalan_tidak_lancar'] = []
        
    if ls.get('nik'):
        sabtu_by_nik[str(ls['nik'])].append(ls)
    if ls.get('santri_id'):
        try:
            sabtu_by_id[int(ls['santri_id'])].append(ls)
        except:
            pass

min_date = min(all_record_dates) if all_record_dates else '2026-01-01'
max_date = max(all_record_dates) if all_record_dates else '2026-11-18'

syahadah_groups = {
    'pertama': [30, 29, 1, 2, 3],
    'kedua': [4, 5, 6, 7, 8],
    'ketiga': [9, 10, 11, 12, 13],
    'keempat': [14, 15, 16, 17, 18],
    'kelima': [19, 20, 21, 22, 23],
    'keenam': [24, 25, 26, 27, 28]
}

def get_predikat(tipe, errors):
    if errors is None:
        return 'N/A'
    errors = int(errors)
    if tipe == 'syahadah':
        if errors <= 10: return 'Mumtaz (Istimewa)'
        if errors <= 20: return 'Jayyid Jiddan (Sangat Baik)'
        if errors <= 30: return 'Jayyid (Baik)'
        if errors <= 40: return 'Maqbul (Cukup)'
        return 'Mardud (Mengulang)'
    else:
        if errors <= 5: return 'Mumtaz (Istimewa)'
        if errors <= 10: return 'Jayyid Jiddan (Sangat Baik)'
        if errors <= 15: return 'Jayyid (Baik)'
        if errors <= 20: return 'Maqbul (Cukup)'
        return 'Mardud (Mengulang)'

def syahadah_to_num(sy_text):
    m = {'pertama': 1, 'kedua': 2, 'ketiga': 3, 'keempat': 4, 'kelima': 5, 'keenam': 6}
    return m.get(sy_text.lower(), 1) if sy_text else 0

all_santri = []
juz_stats = {j: {'juz': j, 'name': juz_surah_names[j], 'hafal_count': 0, 'tes_lancar': 0, 'tes_tidak_lancar': 0, 'sabtu_issues': 0} for j in range(1, 31)}

for s in santri_rows:
    s_dict = dict(s)
    sid = s_dict['id']
    nik = str(s_dict['nik']) if s_dict.get('nik') else ''
    tm = int(s_dict.get('tahun_masuk') or 0)
    
    if tm == kelas1_year:
        kelas_id = "kelas_1"
        kelas_name = "Kelas 1 (Ula)"
        tingkat = "Ula"
    elif tm == kelas2_year:
        kelas_id = "kelas_2"
        kelas_name = "Kelas 2 (Wustho)"
        tingkat = "Wustho"
    elif tm == kelas3_year:
        kelas_id = "kelas_3"
        kelas_name = "Kelas 3 (Ulya)"
        tingkat = "Ulya"
    else:
        continue # strictly only kelas 1, 2, 3
        
    m_id = santri_musyrif.get(nik)
    m_nama = musyrif_map.get(m_id, "Belum Ada Halaqah / Mandiri")
    
    achievements = pencapaian_by_nik.get(nik, [])
    if not achievements and sid in pencapaian_by_id:
        achievements = pencapaian_by_id[sid]
        
    tests = tes_by_nik.get(nik, [])
    if not tests and sid in tes_by_id:
        tests = tes_by_id[sid]
        
    sabtu_reps = sabtu_by_nik.get(nik, [])
    if not sabtu_reps and sid in sabtu_by_id:
        sabtu_reps = sabtu_by_id[sid]
        
    achieved_juz_raw = set()
    for a in achievements:
        if a.get('juz') is not None:
            achieved_juz_raw.add(int(a['juz']))
            
    max_pos = 0
    for j in achieved_juz_raw:
        if j in sequence:
            pos = sequence.index(j) + 1
            if pos > max_pos:
                max_pos = pos
                
    achieved_juz_list = sequence[:max_pos]
    for j in achieved_juz_list:
        juz_stats[j]['hafal_count'] += 1
        
    test_status_map = {}
    test_counts = defaultdict(int)
    for t in tests:
        if t.get('juz') is not None:
            jz = int(t['juz'])
            st = t.get('status') or 'lancar'
            test_status_map[jz] = st
            test_counts[jz] += 1
            if st == 'lancar':
                juz_stats[jz]['tes_lancar'] += 1
            else:
                juz_stats[jz]['tes_tidak_lancar'] += 1
                
    lancar_juz_list = [j for j, st in test_status_map.items() if st == 'lancar']
    lancar_juz_list.sort(key=lambda x: sequence.index(x) if x in sequence else 99)
    
    tidak_lancar_tests = [j for j, st in test_status_map.items() if st == 'tidak_lancar']
    tidak_lancar_tests.sort(key=lambda x: sequence.index(x) if x in sequence else 99)
    
    achieved_not_tested = [j for j in achieved_juz_list if j not in test_status_map]
    
    syahadahs = []
    for a in achievements:
        if a.get('type') == 'syahadah':
            syahadah_tingkat = a.get('syahadah', '')
            kes = a.get('kesalahan')
            pred = get_predikat('syahadah', kes)
            syahadahs.append({
                'id': a['id'],
                'tingkat': syahadah_tingkat,
                'tingkat_num': syahadah_to_num(syahadah_tingkat),
                'juz_cakupan': syahadah_groups.get(syahadah_tingkat, []),
                'juz_cakupan_str': ", ".join(f"Juz {x}" for x in syahadah_groups.get(syahadah_tingkat, [])),
                'kesalahan': kes,
                'predikat': pred,
                'penguji': a.get('penguji') or 'Penguji Tahfidz',
                'catatan': a.get('catatan') or 'Tidak ada catatan khusus.',
                'created_at': str(a.get('created_at', ''))[:10],
                'created_at_indo': format_indo_date(a.get('created_at'))
            })
            
    order_sy = ['pertama', 'kedua', 'ketiga', 'keempat', 'kelima', 'keenam']
    syahadahs.sort(key=lambda x: order_sy.index(x['tingkat']) if x['tingkat'] in order_sy else 99)
    
    juziyahs = []
    for a in achievements:
        if a.get('type') == 'juziyah':
            kes = a.get('kesalahan')
            pred = get_predikat('juziyah', kes)
            juziyahs.append({
                'id': a['id'],
                'juz': a.get('juz'),
                'kesalahan': kes,
                'predikat': pred,
                'penguji': a.get('penguji') or 'Musyrif',
                'catatan': a.get('catatan') or '',
                'created_at': str(a.get('created_at', ''))[:10],
                'created_at_indo': format_indo_date(a.get('created_at'))
            })
    juziyahs.sort(key=lambda x: sequence.index(x['juz']) if x['juz'] in sequence else 99)
    
    sabtu_issues = []
    for sr in sabtu_reps:
        for he in sr['hafalan_tidak_lancar']:
            jz = he.get('juz')
            if jz:
                try:
                    jz_int = int(jz)
                    if 1 <= jz_int <= 30:
                        juz_stats[jz_int]['sabtu_issues'] += 1
                except:
                    pass
            sabtu_issues.append({
                'juz': jz,
                'startPage': he.get('startPage', '-'),
                'endPage': he.get('endPage', '-'),
                'tanggal': str(sr.get('created_at', ''))[:10],
                'tanggal_indo': format_indo_date(sr.get('created_at'))
            })
            
    last_ziyadah = None
    for a in reversed(achievements):
        if a.get('type') == 'ziyadah':
            last_ziyadah = {
                'juz': a.get('juz'),
                'halaman': a.get('halaman'),
                'kesalahan': a.get('kesalahan'),
                'created_at': str(a.get('created_at', ''))[:10],
                'created_at_indo': format_indo_date(a.get('created_at'))
            }
            break
            
    last_achievement = None
    if achievements:
        la = achievements[-1]
        last_achievement = {
            'id': la['id'],
            'type': la.get('type'),
            'juz': la.get('juz'),
            'kesalahan': la.get('kesalahan'),
            'halaman': la.get('halaman'),
            'created_at': str(la.get('created_at', ''))[:10],
            'created_at_indo': format_indo_date(la.get('created_at'))
        }

    # Grid mapping
    juz_grid = []
    for j in range(1, 31):
        is_hafal = j in achieved_juz_list
        is_lancar = j in lancar_juz_list
        is_tl = j in tidak_lancar_tests
        
        if is_lancar:
            status = 'lancar'
            label = 'Lancar / Mutqin'
            color = 'bg-emerald-500 text-white border-emerald-600'
        elif is_tl:
            status = 'tidak_lancar'
            label = 'Belum Lancar (Perlu Remidi)'
            color = 'bg-rose-500 text-white border-rose-600'
        elif is_hafal:
            status = 'hafal_belum_tes'
            label = 'Sudah Setor (Belum Ujian Kelancaran)'
            color = 'bg-amber-400 text-slate-900 border-amber-500'
        else:
            status = 'belum_hafal'
            label = 'Belum Dihafal'
            color = 'bg-slate-100 text-slate-400 border-slate-200'
            
        juz_grid.append({
            'juz': j,
            'name': juz_surah_names[j],
            'status': status,
            'label': label,
            'color': color
        })
        
    total_ach = len(achieved_juz_list)
    total_lan = len(lancar_juz_list)
    total_tl = len(tidak_lancar_tests)
    
    if total_lan > 0 and total_lan == total_ach and total_ach >= 5:
        fluency_label = "Sangat Lancar (Semua Teruji Mutqin)"
        fluency_desc = f"Seluruh {total_lan} juz yang dihafal telah teruji mutqin."
    elif total_lan > 0 and total_lan >= (total_ach / 2):
        fluency_label = "Lancar Sebagian Besar"
        fluency_desc = f"{total_lan} dari {total_ach} juz telah teruji lancar."
    elif total_lan > 0:
        fluency_label = "Sebagian Lancar"
        fluency_desc = f"{total_lan} juz mutqin, {len(achieved_not_tested)} juz menanti tes."
    elif total_tl > 0:
        fluency_label = "Perlu Penguatan & Remidi"
        fluency_desc = f"{total_tl} juz belum lulus tes kelancaran dan butuh murajaah intensif."
    elif total_ach == 0:
        fluency_label = "Belum Ada Setoran"
        fluency_desc = "Belum ada riwayat setoran hafalan tercatat."
    else:
        fluency_label = "Proses Penyetoran (Belum Tes)"
        fluency_desc = f"Telah mencapai {total_ach} juz, menunggu jadwal tes kelancaran."

    highest_sy_num = max([s_entry['tingkat_num'] for s_entry in syahadahs]) if syahadahs else 0
    next_sy_num = highest_sy_num + 1
    target_juz_count = next_sy_num * 5
    remaining_juz_for_syahadah = max(0, target_juz_count - total_ach)
    
    if highest_sy_num >= 6:
        syahadah_status_summary = "Khatam 30 Juz Mutqin (Semua Syahadah Tuntas)"
        syahadah_progress_pct = 100
    elif remaining_juz_for_syahadah == 0 and total_ach >= target_juz_count:
        syahadah_status_summary = f"Siap Mengikuti Syahadah {next_sy_num} ({target_juz_count} Juz Lengkap!)"
        syahadah_progress_pct = 100
    else:
        completed_in_tier = 5 - remaining_juz_for_syahadah
        syahadah_status_summary = f"Menuju Syahadah {next_sy_num} (Kurang {remaining_juz_for_syahadah} Juz)"
        syahadah_progress_pct = min(100, int((completed_in_tier / 5) * 100))

    jk = s_dict.get('jenis_kelamin') or ''
    if not jk:
        if 'Akhwat' in m_nama or 'Usth' in m_nama:
            jk = 'Perempuan'
        else:
            jk = 'Laki-laki'

    # Compact raw records for dynamic client-side date filtering
    raw_achievements = [
        {
            'id': a['id'],
            'type': a.get('type') or 'ziyadah',
            'juz': int(a['juz']) if a.get('juz') is not None else None,
            'kesalahan': a.get('kesalahan'),
            'halaman': a.get('halaman'),
            'syahadah': a.get('syahadah'),
            'penguji': a.get('penguji') or 'Penguji',
            'catatan': a.get('catatan') or '',
            'created_at': str(a.get('created_at', ''))[:10],
            'created_at_indo': format_indo_date(a.get('created_at'))
        } for a in achievements
    ]

    raw_tests = [
        {
            'id': t['id'],
            'juz': int(t['juz']) if t.get('juz') is not None else None,
            'status': t.get('status') or 'lancar',
            'created_at': str(t.get('created_at', ''))[:10],
            'created_at_indo': format_indo_date(t.get('created_at'))
        } for t in tests
    ]

    raw_sabtu = [
        {
            'id': sr['id'],
            'created_at': str(sr.get('created_at', ''))[:10],
            'created_at_indo': format_indo_date(sr.get('created_at')),
            'hafalan_tidak_lancar': sr.get('hafalan_tidak_lancar', [])
        } for sr in sabtu_reps
    ]

    all_santri.append({
        'id': sid,
        'nik': nik,
        'nis': s_dict.get('nis') or '-',
        'nama': s_dict.get('nama_sesuai_kk') or s_dict.get('nama_panggilan') or f'Santri {sid}',
        'panggilan': s_dict.get('nama_panggilan') or '',
        'tahun_masuk': tm,
        'kelas_id': kelas_id,
        'kelas_name': kelas_name,
        'tingkat': tingkat,
        'status': s_dict.get('status') or 'Aktif',
        'jenis_kelamin': jk,
        'musyrif_id': m_id,
        'musyrif_nama': m_nama,
        'total_pencapaian_records': len(achievements),
        'total_juz_dicapai': total_ach,
        'achieved_juz_list': achieved_juz_list,
        'achieved_juz_str': ", ".join(f"Juz {x}" for x in achieved_juz_list) if achieved_juz_list else "Belum Ada",
        'total_juz_lancar': total_lan,
        'lancar_juz_list': lancar_juz_list,
        'lancar_juz_str': ", ".join(f"Juz {x}" for x in lancar_juz_list) if lancar_juz_list else "Belum Ada",
        'total_tidak_lancar': total_tl,
        'tidak_lancar_tests': tidak_lancar_tests,
        'tidak_lancar_str': ", ".join(f"Juz {x}" for x in tidak_lancar_tests) if tidak_lancar_tests else "-",
        'achieved_not_tested': achieved_not_tested,
        'sabtu_issues_count': len(sabtu_issues),
        'sabtu_issues': sabtu_issues,
        'has_syahadah': len(syahadahs) > 0,
        'syahadah_count': len(syahadahs),
        'highest_syahadah_num': highest_sy_num,
        'highest_syahadah': syahadahs[-1]['tingkat'] if syahadahs else None,
        'syahadah_status_summary': syahadah_status_summary,
        'syahadah_progress_pct': syahadah_progress_pct,
        'syahadahs': syahadahs,
        'juziyah_count': len(juziyahs),
        'juziyahs': juziyahs,
        'last_ziyadah': last_ziyadah,
        'last_achievement': last_achievement,
        'juz_grid': juz_grid,
        'fluency_label': fluency_label,
        'fluency_desc': fluency_desc,
        'raw_achievements': raw_achievements,
        'raw_tests': raw_tests,
        'raw_sabtu': raw_sabtu
    })

# Summary Stats for Kelas 1, 2, 3 only
total_students = len(all_santri)
active_students = sum(1 for s in all_santri if s['status'] == 'Aktif')
inactive_students = total_students - active_students
syahadah_holders = sum(1 for s in all_santri if s['has_syahadah'])
total_syahadah_certs = sum(s['syahadah_count'] for s in all_santri)
total_juz_memorized = sum(s['total_juz_dicapai'] for s in all_santri)
total_juz_fluent = sum(s['total_juz_lancar'] for s in all_santri)

syahadah_tier_counts = Counter()
for s in all_santri:
    for sy in s['syahadahs']:
        syahadah_tier_counts[sy['tingkat']] += 1

ready_for_syahadah_list = [s for s in all_santri if not s['has_syahadah'] and s['total_juz_dicapai'] >= 5]
in_progress_non_syahadah = [s for s in all_santri if not s['has_syahadah'] and 1 <= s['total_juz_dicapai'] < 5]
unstarted_non_syahadah = [s for s in all_santri if not s['has_syahadah'] and s['total_juz_dicapai'] == 0]

# Class breakdown (strictly kelas 1, 2, 3)
classes_summary = {}
for k_id, k_name in [('kelas_1', 'Kelas 1 (Ula)'), ('kelas_2', 'Kelas 2 (Wustho)'), ('kelas_3', 'Kelas 3 (Ulya)')]:
    c_students = [s for s in all_santri if s['kelas_id'] == k_id]
    tot = len(c_students)
    act = sum(1 for s in c_students if s['status'] == 'Aktif')
    sy = sum(1 for s in c_students if s['has_syahadah'])
    j_ach = sum(s['total_juz_dicapai'] for s in c_students)
    j_lan = sum(s['total_juz_lancar'] for s in c_students)
    
    classes_summary[k_id] = {
        'id': k_id,
        'name': k_name,
        'total_santri': tot,
        'aktif': act,
        'syahadah_holders': sy,
        'syahadah_pct': round((sy / tot * 100), 1) if tot > 0 else 0,
        'avg_juz_dicapai': round(j_ach / tot, 1) if tot > 0 else 0,
        'avg_juz_lancar': round(j_lan / tot, 1) if tot > 0 else 0,
        'total_juz_dicapai': j_ach,
        'total_juz_lancar': j_lan
    }

# Halaqah breakdown (strictly the 6 active halaqah)
halaqah_summary = {}
for m_id, m_name in musyrif_map.items():
    m_students = [s for s in all_santri if s['musyrif_id'] == m_id]
    tot = len(m_students)
    act = sum(1 for s in m_students if s['status'] == 'Aktif')
    sy = sum(1 for s in m_students if s['has_syahadah'])
    j_ach = sum(s['total_juz_dicapai'] for s in m_students)
    j_lan = sum(s['total_juz_lancar'] for s in m_students)
    
    halaqah_summary[m_name] = {
        'musyrif_id': m_id,
        'musyrif_nama': m_name,
        'total_santri': tot,
        'aktif': act,
        'syahadah_holders': sy,
        'syahadah_pct': round((sy / tot * 100), 1) if tot > 0 else 0,
        'avg_juz_dicapai': round(j_ach / tot, 1) if tot > 0 else 0,
        'avg_juz_lancar': round(j_lan / tot, 1) if tot > 0 else 0,
        'total_juz_dicapai': j_ach,
        'total_juz_lancar': j_lan
    }

dataset = {
    'metadata': {
        'generated_at': '2026-11-18 WITA',
        'generated_at_indo': format_indo_date('2026-11-18'),
        'database_source': 'everynight-in-my-dream.db',
        'scope': 'Hanya Santri Kelas 1, 2, dan 3 (Alumni tidak dimasukkan)',
        'institution_name': 'Pesantren Tahfidzul Quran',
        'timezone': 'Asia/Makassar (WITA)',
        'min_date': min_date,
        'max_date': max_date,
        'min_date_indo': format_indo_date(min_date),
        'max_date_indo': format_indo_date(max_date)
    },
    'summary': {
        'total_santri': total_students,
        'santri_aktif': active_students,
        'santri_tidak_aktif': inactive_students,
        'santri_dengan_syahadah': syahadah_holders,
        'santri_belum_syahadah': total_students - syahadah_holders,
        'total_sertifikat_syahadah': total_syahadah_certs,
        'total_juz_dihafal': total_juz_memorized,
        'total_juz_lancar': total_juz_fluent,
        'total_pencapaian_records': len(pencapaian_rows),
        'total_tes_records': len(tes_rows),
        'total_laporansabtu_records': len(sabtu_rows),
        'syahadah_tier_counts': dict(syahadah_tier_counts),
        'ready_for_syahadah_count': len(ready_for_syahadah_list),
        'in_progress_non_syahadah_count': len(in_progress_non_syahadah),
        'unstarted_non_syahadah_count': len(unstarted_non_syahadah)
    },
    'classes_summary': classes_summary,
    'halaqah_summary': halaqah_summary,
    'juz_stats': list(juz_stats.values()),
    'santri_list': all_santri
}

with open('full_report_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created for Classes 1, 2, 3 only: {total_students} santri, {syahadah_holders} lulus syahadah. Date bounds: {min_date} ({format_indo_date(min_date)}) to {max_date} ({format_indo_date(max_date)}).")

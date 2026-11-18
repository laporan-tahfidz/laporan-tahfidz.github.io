const INDO_DAYS = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
    const INDO_MONTHS = [
      'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ];

    function formatIndoDate(dateStr) {
      if (!dateStr || dateStr === '-' || dateStr === 'Belum Ada' || dateStr === 'null' || dateStr === 'undefined') return '-';
      if (typeof dateStr === 'string' && (dateStr.includes('Januari') || dateStr.includes('Februari') || dateStr.includes('Maret') || dateStr.includes('April') || dateStr.includes('Mei') || dateStr.includes('Juni') || dateStr.includes('Juli') || dateStr.includes('Agustus') || dateStr.includes('September') || dateStr.includes('Oktober') || dateStr.includes('November') || dateStr.includes('Desember'))) {
        return dateStr;
      }
      const cleanStr = String(dateStr).trim().split(' ')[0];
      const parts = cleanStr.split('-');
      if (parts.length === 3) {
        const y = parseInt(parts[0], 10);
        const m = parseInt(parts[1], 10) - 1;
        const d = parseInt(parts[2], 10);
        const dateObj = new Date(y, m, d);
        if (!isNaN(dateObj.getTime())) {
          const dayName = INDO_DAYS[dateObj.getDay()];
          const monthName = INDO_MONTHS[m];
          return `${dayName}, ${d} ${monthName} ${y}`;
        }
      }
      return dateStr;
    }

    const rawDataElem = document.getElementById('embedded-data');
    let DB = JSON.parse(rawDataElem.textContent);
    let ALL_SANTRI = DB.santri_list;
    let filteredSantri = [...ALL_SANTRI];
    let currentSort = { column: 'nama', asc: true };
    let currentModalSantri = null;

    let currentDateRange = {
      start: DB.metadata.min_date || '2026-01-16',
      end: DB.metadata.max_date || '2026-11-18',
      isCustom: false
    };
    let currentPeriodData = null;

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-emerald-50', 'text-emerald-800', 'border', 'border-emerald-300');
        btn.classList.add('text-slate-600');
      });
      document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));

      const activeBtn = document.getElementById('tab-' + tabId);
      const activeContent = document.getElementById('content-' + tabId);
      if (activeBtn && activeContent) {
        activeBtn.classList.add('active', 'bg-emerald-50', 'text-emerald-800', 'border', 'border-emerald-300');
        activeBtn.classList.remove('text-slate-600');
        activeContent.classList.remove('hidden');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
      lucide.createIcons();
    }

    // Dynamic Period Computation (Excluding Evaluasi Sabtu)
    function computePeriodData(startDate, endDate) {
      const isAllTime = (startDate <= DB.metadata.min_date && endDate >= DB.metadata.max_date);
      
      let totalPencapaian = 0;
      let totalTes = 0;
      let totalSyahadahCerts = 0;
      let totalJuziyahExams = 0;
      let syahadahTierCounts = { 'pertama': 0, 'kedua': 0, 'ketiga': 0, 'keempat': 0 };
      let syahadahRecords = [];
      let santriActiveCount = 0;
      let totalJuzSetor = 0;
      let totalJuzLancar = 0;

      let juzStats = {};
      for (let j = 1; j <= 30; j++) {
        juzStats[j] = { juz: j, hafal_in_period: 0, tes_lancar_in_period: 0, tes_tl_in_period: 0 };
      }

      const periodSantriList = ALL_SANTRI.map(s => {
        const pInPeriod = (s.raw_achievements || []).filter(a => a.created_at >= startDate && a.created_at <= endDate);
        const tInPeriod = (s.raw_tests || []).filter(t => t.created_at >= startDate && t.created_at <= endDate);
        const syInPeriod = (s.syahadahs || []).filter(sy => sy.created_at >= startDate && sy.created_at <= endDate);
        const jzInPeriod = (s.juziyahs || []).filter(j => j.created_at >= startDate && j.created_at <= endDate);

        totalPencapaian += pInPeriod.length;
        totalTes += tInPeriod.length;
        totalSyahadahCerts += syInPeriod.length;
        totalJuziyahExams += jzInPeriod.length;

        syInPeriod.forEach(sy => {
          syahadahTierCounts[sy.tingkat] = (syahadahTierCounts[sy.tingkat] || 0) + 1;
          syahadahRecords.push({
            santri: s,
            syahadah: sy
          });
        });

        const hasActivity = (pInPeriod.length > 0 || tInPeriod.length > 0);
        if (hasActivity) santriActiveCount++;

        const juzSetorInPeriod = Array.from(new Set(pInPeriod.filter(a => a.juz).map(a => a.juz)));
        const testLancarInPeriod = tInPeriod.filter(t => t.status === 'lancar');
        const testTlInPeriod = tInPeriod.filter(t => t.status === 'tidak_lancar');
        const juzLancarInPeriod = Array.from(new Set(testLancarInPeriod.map(t => t.juz)));
        const juzTlInPeriod = Array.from(new Set(testTlInPeriod.map(t => t.juz)));

        totalJuzSetor += juzSetorInPeriod.length;
        totalJuzLancar += juzLancarInPeriod.length;

        juzSetorInPeriod.forEach(j => { if (juzStats[j]) juzStats[j].hafal_in_period++; });
        juzLancarInPeriod.forEach(j => { if (juzStats[j]) juzStats[j].tes_lancar_in_period++; });
        juzTlInPeriod.forEach(j => { if (juzStats[j]) juzStats[j].tes_tl_in_period++; });

        let lastDateInPeriod = null;
        let lastDateIndo = '-';
        let allDates = [
          ...pInPeriod.map(x => x.created_at),
          ...tInPeriod.map(x => x.created_at)
        ].sort();
        if (allDates.length > 0) {
          lastDateInPeriod = allDates[allDates.length - 1];
          lastDateIndo = formatIndoDate(lastDateInPeriod);
        }

        return {
          ...s,
          pInPeriod,
          tInPeriod,
          period_has_activity: hasActivity,
          period_pencapaian_count: pInPeriod.length,
          period_tests_count: tInPeriod.length,
          period_syahadahs: syInPeriod,
          period_juziyahs: jzInPeriod,
          period_juziyah_count: jzInPeriod.length,
          period_juz_setor: juzSetorInPeriod,
          period_juz_setor_count: juzSetorInPeriod.length,
          period_juz_lancar: juzLancarInPeriod,
          period_juz_lancar_count: juzLancarInPeriod.length,
          period_juz_tidak_lancar: juzTlInPeriod,
          period_juz_tidak_lancar_count: juzTlInPeriod.length,
          period_last_date: lastDateInPeriod,
          period_last_date_indo: lastDateIndo
        };
      });

      return {
        startDate,
        endDate,
        startDateIndo: formatIndoDate(startDate),
        endDateIndo: formatIndoDate(endDate),
        isAllTime,
        periodSantriList,
        totalPencapaian,
        totalTes,
        totalSyahadahCerts,
        totalJuziyahExams,
        syahadahTierCounts,
        syahadahRecords,
        santriActiveCount,
        totalJuzSetor,
        totalJuzLancar,
        juzStats
      };
    }

    function setPresetRange(key) {
      let start, end;
      if (key === 'all') {
        start = DB.metadata.min_date;
        end = DB.metadata.max_date;
      } else if (key === 'user_example') {
        start = '2026-07-01';
        end = '2026-10-03';
      } else if (key === 'sem1_2026') {
        start = '2026-07-01';
        end = DB.metadata.max_date;
      } else if (key === 'sem2_2026') {
        start = '2026-01-01';
        end = '2026-06-30';
      } else if (key === 'last_30d') {
        start = '2026-10-19';
        end = DB.metadata.max_date;
      }

      document.getElementById('filterStartDate').value = start;
      document.getElementById('filterEndDate').value = end;

      document.querySelectorAll('.preset-btn').forEach(b => {
        b.classList.remove('bg-emerald-600', 'text-white', 'shadow-2xs');
        b.classList.add('bg-slate-100', 'text-slate-700');
      });
      const activeBtn = document.getElementById('preset-btn-' + key);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
        activeBtn.classList.add('bg-emerald-600', 'text-white', 'shadow-2xs');
      }

      applyDateRangeFilter();
    }

    function onDateInputChange() {
      document.querySelectorAll('.preset-btn').forEach(b => {
        b.classList.remove('bg-emerald-600', 'text-white', 'shadow-2xs');
        b.classList.add('bg-slate-100', 'text-slate-700');
      });
    }

    function applyDateRangeFilter() {
      let start = document.getElementById('filterStartDate').value;
      let end = document.getElementById('filterEndDate').value;

      if (!start) start = DB.metadata.min_date;
      if (!end) end = DB.metadata.max_date;
      if (start > end) {
        const tmp = start; start = end; end = tmp;
        document.getElementById('filterStartDate').value = start;
        document.getElementById('filterEndDate').value = end;
      }

      currentDateRange = { start, end, isCustom: !(start <= DB.metadata.min_date && end >= DB.metadata.max_date) };
      currentPeriodData = computePeriodData(start, end);

      const startIndo = formatIndoDate(start);
      const endIndo = formatIndoDate(end);

      const badgeText = document.getElementById('badgeActivePeriodText');
      const spanText = document.getElementById('activePeriodSpanText');
      const statsText = document.getElementById('activePeriodStatsText');
      const btnResetInline = document.getElementById('btnResetInline');

      if (currentDateRange.isCustom) {
        badgeText.textContent = `${startIndo} s/d ${endIndo}`;
        spanText.textContent = `${startIndo} s/d ${endIndo}`;
        statsText.textContent = `(${currentPeriodData.totalPencapaian} setoran, ${currentPeriodData.totalSyahadahCerts} kelulusan syahadah, ${currentPeriodData.totalJuzLancar} tes lancar)`;
        btnResetInline.classList.remove('hidden');
      } else {
        badgeText.textContent = 'Semua Waktu';
        spanText.textContent = `${startIndo} s/d ${endIndo}`;
        statsText.textContent = `(Menampilkan seluruh 44 santri & riwayat pencapaian)`;
        btnResetInline.classList.add('hidden');
      }

      updateExecutiveHighlights(currentPeriodData);
      renderAllCharts(currentPeriodData);
      renderSyahadahTable();
      populateKelancaranTables();
      populateGroupingCards();
      applyFilters();
      lucide.createIcons();
    }

    function resetDateRangeFilter() {
      setPresetRange('all');
    }

    function updateExecutiveHighlights(data) {
      if (!data) return;

      if (data.isAllTime) {
        document.getElementById('kpi-total-santri').textContent = DB.summary.total_santri;
        document.getElementById('kpi-sub-santri').innerHTML = `<span class="text-emerald-700 font-semibold">${DB.summary.santri_aktif} Aktif</span> • ${DB.summary.santri_tidak_aktif} Non-aktif`;
        
        document.getElementById('kpi-total-syahadah').textContent = DB.summary.santri_dengan_syahadah;
        document.getElementById('kpi-sub-syahadah').textContent = `${DB.summary.total_sertifikat_syahadah} Sertifikat (5-Juz Mutqin)`;

        document.getElementById('kpi-total-juz').innerHTML = `${DB.summary.total_juz_dihafal} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-juz').textContent = `Rata-rata ${(DB.summary.total_juz_dihafal / DB.summary.total_santri).toFixed(1)} Juz/Santri`;

        document.getElementById('kpi-total-lancar').innerHTML = `${DB.summary.total_juz_lancar} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-lancar').textContent = 'Lolos Ujian Kelancaran';

        document.getElementById('kpi-total-juziyah').textContent = DB.summary.total_juziyah_exams || 150;
        document.getElementById('kpi-sub-juziyah').textContent = 'Ujian 1-Juz Sekali Duduk';

        document.getElementById('kpi-total-pencapaian').textContent = (DB.summary.total_pencapaian_records + DB.summary.total_tes_records).toLocaleString('id-ID');
        document.getElementById('kpi-sub-pencapaian').textContent = `${DB.summary.total_pencapaian_records} Setor • ${DB.summary.total_tes_records} Tes`;
      } else {
        document.getElementById('kpi-total-santri').textContent = data.santriActiveCount;
        document.getElementById('kpi-sub-santri').innerHTML = `<span class="text-emerald-700 font-semibold">${data.santriActiveCount} Menyetor di Periode Ini</span>`;

        document.getElementById('kpi-total-syahadah').textContent = data.totalSyahadahCerts;
        document.getElementById('kpi-sub-syahadah').textContent = `${data.syahadahRecords.length} Ujian di Periode Ini`;

        document.getElementById('kpi-total-juz').innerHTML = `${data.totalJuzSetor} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-juz').textContent = `Disetor di Periode Ini`;

        document.getElementById('kpi-total-lancar').innerHTML = `${data.totalJuzLancar} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-lancar').textContent = `Lolos Tes di Periode Ini`;

        document.getElementById('kpi-total-juziyah').textContent = data.totalJuziyahExams;
        document.getElementById('kpi-sub-juziyah').textContent = `Ujian Juziyah di Periode Ini`;

        document.getElementById('kpi-total-pencapaian').textContent = (data.totalPencapaian + data.totalTes).toLocaleString('id-ID');
        document.getElementById('kpi-sub-pencapaian').textContent = `${data.totalPencapaian} Setor • ${data.totalTes} Tes`;
      }

      // Top Achievers in Period
      const listSantri = data.periodSantriList || ALL_SANTRI;
      const topAchievers = [...listSantri].sort((a,b) => {
        if (!data.isAllTime) {
          return (b.period_juz_setor_count - a.period_juz_setor_count) || (b.total_juz_dicapai - a.total_juz_dicapai);
        }
        return b.total_juz_dicapai - a.total_juz_dicapai;
      }).slice(0, 5);

      document.getElementById('list-top-achievers').innerHTML = topAchievers.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-5 h-5 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center text-[10px] font-bold shrink-0">${idx + 1}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-emerald-700 text-xs">${data.isAllTime ? s.total_juz_dicapai : s.period_juz_setor_count} Juz</div>
            <div class="text-[9px] text-slate-400">${data.isAllTime ? `${s.total_juz_lancar} lancar` : `${s.total_juz_dicapai} total`}</div>
          </div>
        </div>
      `).join('');

      // Top Fluent in Period
      const topFluent = [...listSantri].sort((a,b) => {
        if (!data.isAllTime) {
          return (b.period_juz_lancar_count - a.period_juz_lancar_count) || (b.total_juz_lancar - a.total_juz_lancar);
        }
        return b.total_juz_lancar - a.total_juz_lancar;
      }).slice(0, 5);

      document.getElementById('list-top-fluent').innerHTML = topFluent.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center text-[10px] font-bold shrink-0">${idx + 1}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-teal-700 text-xs">${data.isAllTime ? s.total_juz_lancar : s.period_juz_lancar_count} Juz</div>
            <div class="text-[9px] text-slate-400">${data.isAllTime ? `${s.total_juz_dicapai} dicapai` : `${s.total_juz_lancar} total`}</div>
          </div>
        </div>
      `).join('');

      // Top Challenging Juz (Remidi Tes Kelancaran)
      const juzEntries = Object.values(data.juzStats || {}).map(j => ({
        ...j,
        surah: (DB.juz_stats.find(js => js.juz === j.juz) || {}).name || `Juz ${j.juz}`,
        hafal_count: (DB.juz_stats.find(js => js.juz === j.juz) || {}).hafal_count || 0,
        total_remidi: data.isAllTime ? ((DB.juz_stats.find(js => js.juz === j.juz) || {}).tes_tidak_lancar || 0) : (j.tes_tl_in_period || 0)
      })).sort((a,b) => b.total_remidi - a.total_remidi).slice(0, 5);

      document.getElementById('list-challenging-juz').innerHTML = juzEntries.map(j => `
        <div class="flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-6 h-6 rounded-lg bg-rose-100 text-rose-800 flex items-center justify-center text-[10px] font-bold shrink-0">Juz ${j.juz}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${j.surah}</div>
              <div class="text-[10px] text-slate-400">${j.hafal_count} santri hafal</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-rose-600 text-xs">${j.total_remidi}x Remidi</div>
            <div class="text-[9px] text-slate-400">Ujian Kelancaran</div>
          </div>
        </div>
      `).join('');
    }

    // Chart instances
    let chartInstanceClass = null;
    let chartInstanceSyahadah = null;
    let chartInstanceJuz = null;

    function renderAllCharts(data) {
      if (!data) data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const textColor = '#334155';
      const gridColor = '#f1f5f9';

      // 1. Chart Class Comparison
      const ctxClass = document.getElementById('chartClassComparison')?.getContext('2d');
      if (ctxClass) {
        if (chartInstanceClass) chartInstanceClass.destroy();
        
        const classNames = ['Kelas 1 (Ula)', 'Kelas 2 (Wustho)', 'Kelas 3 (Ulya)'];
        const classKeys = ['kelas_1', 'kelas_2', 'kelas_3'];
        
        let avgAchieved = [];
        let avgLancar = [];

        classKeys.forEach(k => {
          const listInClass = (data.periodSantriList || ALL_SANTRI).filter(s => s.kelas_id === k);
          const totalInClass = listInClass.length || 1;
          if (data.isAllTime) {
            const sumAch = listInClass.reduce((acc, s) => acc + s.total_juz_dicapai, 0);
            const sumLan = listInClass.reduce((acc, s) => acc + s.total_juz_lancar, 0);
            avgAchieved.push(+(sumAch / totalInClass).toFixed(1));
            avgLancar.push(+(sumLan / totalInClass).toFixed(1));
          } else {
            const sumAch = listInClass.reduce((acc, s) => acc + s.period_juz_setor_count, 0);
            const sumLan = listInClass.reduce((acc, s) => acc + s.period_juz_lancar_count, 0);
            avgAchieved.push(+(sumAch / totalInClass).toFixed(1));
            avgLancar.push(+(sumLan / totalInClass).toFixed(1));
          }
        });

        chartInstanceClass = new Chart(ctxClass, {
          type: 'bar',
          data: {
            labels: classNames,
            datasets: [
              {
                label: data.isAllTime ? 'Rata-rata Juz Dicapai' : 'Rata-rata Disetor Periode Ini',
                data: avgAchieved,
                backgroundColor: '#10b981',
                borderRadius: 4
              },
              {
                label: data.isAllTime ? 'Rata-rata Juz Lancar' : 'Rata-rata Lulus Tes Periode Ini',
                data: avgLancar,
                backgroundColor: '#0d9488',
                borderRadius: 4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: textColor, font: { size: 10, family: 'Plus Jakarta Sans' } } }
            },
            scales: {
              x: { ticks: { color: textColor, font: { size: 10 } }, grid: { display: false } },
              y: { ticks: { color: textColor, font: { size: 9 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }

      // 2. Chart Syahadah Status
      const ctxSyahadah = document.getElementById('chartSyahadahStatus')?.getContext('2d');
      if (ctxSyahadah) {
        if (chartInstanceSyahadah) chartInstanceSyahadah.destroy();
        
        let labels, values, bgColors;
        if (data.isAllTime) {
          labels = [
            'Lulus (' + DB.summary.santri_dengan_syahadah + ')',
            'Siap Ujian (' + DB.summary.ready_for_syahadah_count + ')',
            'Berproses (' + DB.summary.in_progress_non_syahadah_count + ')',
            'Awal / Non-aktif (' + DB.summary.unstarted_non_syahadah_count + ')'
          ];
          values = [
            DB.summary.santri_dengan_syahadah,
            DB.summary.ready_for_syahadah_count,
            DB.summary.in_progress_non_syahadah_count,
            DB.summary.unstarted_non_syahadah_count
          ];
          bgColors = ['#f59e0b', '#10b981', '#3b82f6', '#94a3b8'];
        } else {
          labels = [
            'Syahadah 1 (' + (data.syahadahTierCounts['pertama'] || 0) + ')',
            'Syahadah 2 (' + (data.syahadahTierCounts['kedua'] || 0) + ')',
            'Syahadah 3 (' + (data.syahadahTierCounts['ketiga'] || 0) + ')',
            'Syahadah 4 (' + (data.syahadahTierCounts['keempat'] || 0) + ')'
          ];
          values = [
            data.syahadahTierCounts['pertama'] || 0,
            data.syahadahTierCounts['kedua'] || 0,
            data.syahadahTierCounts['ketiga'] || 0,
            data.syahadahTierCounts['keempat'] || 0
          ];
          bgColors = ['#f59e0b', '#10b981', '#3b82f6', '#8b5cf6'];
        }

        chartInstanceSyahadah = new Chart(ctxSyahadah, {
          type: 'doughnut',
          data: {
            labels: labels,
            datasets: [{
              data: values,
              backgroundColor: bgColors,
              borderWidth: 0
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'bottom', labels: { color: textColor, font: { size: 9 } } }
            },
            cutout: '65%'
          }
        });
      }

      // 3. Chart Juz Issues (Purely Tes Remidi - Evaluasi Sabtu Excluded)
      const ctxJuz = document.getElementById('chartJuzIssuesFull')?.getContext('2d');
      if (ctxJuz) {
        if (chartInstanceJuz) chartInstanceJuz.destroy();
        
        let sortedJuz;
        if (data.isAllTime) {
          sortedJuz = [...DB.juz_stats].sort((a,b) => b.tes_tidak_lancar - a.tes_tidak_lancar);
        } else {
          sortedJuz = Object.values(data.juzStats || {}).sort((a,b) => b.tes_tl_in_period - a.tes_tl_in_period);
        }

        chartInstanceJuz = new Chart(ctxJuz, {
          type: 'bar',
          data: {
            labels: sortedJuz.map(j => 'J' + j.juz),
            datasets: [
              {
                label: data.isAllTime ? 'Remidi Tes Kelancaran' : 'Remidi Tes Periode Ini',
                data: sortedJuz.map(j => data.isAllTime ? j.tes_tidak_lancar : j.tes_tl_in_period),
                backgroundColor: '#ef4444',
                borderRadius: 4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: textColor, font: { size: 10 } } }
            },
            scales: {
              x: { ticks: { color: textColor, font: { size: 9 } }, grid: { display: false } },
              y: { ticks: { color: textColor, font: { size: 9 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }
    }

    let currentSyahadahFilter = 'semua';
    function filterSyahadahTab(filterKey) {
      currentSyahadahFilter = filterKey;
      document.querySelectorAll('.subtab-sy-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-emerald-600', 'text-white');
        btn.classList.add('bg-slate-100', 'text-slate-700');
      });
      const activeBtn = document.getElementById('subtab-sy-' + filterKey.replace('_', '-'));
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
        activeBtn.classList.add('active', 'bg-emerald-600', 'text-white');
      }
      renderSyahadahTable();
    }

    function renderSyahadahTable() {
      const tbody = document.getElementById('syahadah-table-body');
      const mobileCards = document.getElementById('syahadah-mobile-cards');
      const titleElem = document.getElementById('syahadah-table-title');
      const countElem = document.getElementById('syahadah-table-count');

      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      let records = [];

      if (currentSyahadahFilter === 'belum_siap') {
        titleElem.textContent = 'Santri Kelas 1-3 Belum Syahadah Namun Sudah Hafal >= 5 Juz (Siap Ujian)';
        const readySantri = listSantri.filter(s => !s.has_syahadah && s.total_juz_dicapai >= 5);
        countElem.textContent = `${readySantri.length} Santri`;

        mobileCards.innerHTML = readySantri.map(s => `
          <div class="p-3 bg-white hover:bg-slate-50 transition space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-slate-900">${s.nama}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Siap Ujian 1</span>
            </div>
            <div class="text-[11px] text-slate-500">${s.kelas_name} • ${s.musyrif_nama}</div>
            <div class="text-xs text-emerald-700 font-semibold">${s.total_juz_dicapai} Juz Dicapai (${s.achieved_juz_str})</div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-emerald-50 text-emerald-700 font-semibold text-xs border border-emerald-200">
              Lihat Rapor 30 Juz
            </button>
          </div>
        `).join('');

        tbody.innerHTML = readySantri.map(s => `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.musyrif_nama}</div></td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">Siap Syahadah 1</span></td>
            <td class="py-3 px-4 text-xs font-bold text-emerald-700">${s.total_juz_dicapai} Juz<div class="text-[10px] text-slate-400 font-normal">${s.achieved_juz_str}</div></td>
            <td class="py-3 px-4 text-xs text-amber-700 font-medium">${s.juziyah_count} Juziyah Tuntas</td>
            <td class="py-3 px-4 text-xs text-slate-500">Belum Ujian</td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs">Sudah menuntaskan batas 5 juz. Direkomendasikan segera diuji Syahadah 1.</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200">Rapor</button></td>
          </tr>
        `).join('');
        return;
      }

      if (currentSyahadahFilter === 'belum_proses') {
        titleElem.textContent = 'Santri Kelas 1-3 yang Sedang Berproses Menuju Syahadah 1 (1 - 4 Juz)';
        const inProgress = listSantri.filter(s => !s.has_syahadah && s.total_juz_dicapai > 0 && s.total_juz_dicapai < 5);
        countElem.textContent = `${inProgress.length} Santri`;

        mobileCards.innerHTML = inProgress.map(s => {
          const needed = 5 - s.total_juz_dicapai;
          return `
          <div class="p-3 bg-white hover:bg-slate-50 transition space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-slate-900">${s.nama}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-blue-50 text-blue-800">Kurang ${needed} Juz</span>
            </div>
            <div class="text-[11px] text-slate-500">${s.kelas_name} • ${s.musyrif_nama}</div>
            <div class="text-xs text-blue-700 font-semibold">${s.total_juz_dicapai} dari 5 Juz (${s.achieved_juz_str})</div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-slate-100 text-slate-700 font-semibold text-xs border border-slate-200">
              Lihat Rapor
            </button>
          </div>
        `;}).join('');

        tbody.innerHTML = inProgress.map(s => `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.musyrif_nama}</div></td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">Menuju Syahadah 1</span></td>
            <td class="py-3 px-4 text-xs font-bold text-blue-700">${s.total_juz_dicapai} / 5 Juz<div class="text-[10px] text-slate-400 font-normal">${s.achieved_juz_str}</div></td>
            <td class="py-3 px-4 text-xs text-emerald-700 font-bold">${s.total_juz_lancar} Juz Lancar</td>
            <td class="py-3 px-4 text-xs text-slate-500">Ziyadah Aktif</td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs">Kurang ${5 - s.total_juz_dicapai} juz untuk mencapai target Syahadah 1.</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200">Rapor</button></td>
          </tr>
        `).join('');
        return;
      }

      listSantri.forEach(s => {
        const syList = data.isAllTime ? s.syahadahs : (s.period_syahadahs || []);
        syList.forEach(sy => {
          if (currentSyahadahFilter === 'semua' || sy.tingkat === currentSyahadahFilter) {
            records.push({ santri: s, syahadah: sy });
          }
        });
      });

      titleElem.textContent = data.isAllTime 
        ? 'Daftar Santri Kelas 1, 2, & 3 Pemegang Sertifikasi Syahadah'
        : `Daftar Ujian Syahadah pada Periode ${data.startDateIndo} s/d ${data.endDateIndo}`;
      countElem.textContent = `${records.length} Catatan`;

      if (records.length === 0) {
        mobileCards.innerHTML = `<div class="p-6 text-center text-xs text-slate-400">Tidak ada catatan syahadah pada rentang waktu atau filter ini.</div>`;
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400">Tidak ada catatan syahadah pada rentang waktu atau filter ini.</td></tr>`;
        return;
      }

      mobileCards.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        const dateFormatted = formatIndoDate(sy.created_at);
        return `
          <div class="p-3 bg-white hover:bg-slate-50 transition space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-slate-900">${s.nama}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300">
                Syahadah ${sy.tingkat.toUpperCase()}
              </span>
            </div>
            <div class="flex items-center justify-between text-[11px]">
              <span class="text-slate-500">${s.kelas_name} • ${s.musyrif_nama}</span>
              <span class="font-bold text-emerald-800">${sy.predikat} (${sy.kesalahan} salah)</span>
            </div>
            <div class="text-[11px] text-slate-600 bg-slate-50 p-2 rounded-lg border border-slate-100">
              <div><strong>Cakupan:</strong> ${sy.juz_cakupan_str}</div>
              <div class="text-[10px] text-slate-500 mt-0.5 font-medium">Penguji: ${sy.penguji} • <strong class="text-emerald-800">${dateFormatted}</strong></div>
              ${sy.catatan ? `<div class="italic text-[10px] text-slate-500 mt-1">"${sy.catatan}"</div>` : ''}
            </div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-emerald-50 text-emerald-800 font-semibold text-xs border border-emerald-200">
              Lihat Rapor 30 Juz
            </button>
          </div>
        `;
      }).join('');

      tbody.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        const dateFormatted = formatIndoDate(sy.created_at);
        let badgeClass = 'badge-mumtaz';
        if (sy.predikat.includes('Jayyid Jiddan')) badgeClass = 'badge-jayyid-jiddan';
        else if (sy.predikat.includes('Jayyid')) badgeClass = 'badge-jayyid';

        return `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.musyrif_nama}</div></td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-50 text-amber-800 border border-amber-300">Syahadah ${sy.tingkat.toUpperCase()}</span></td>
            <td class="py-3 px-4 text-xs font-medium text-slate-700">${sy.juz_cakupan_str}</td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded text-xs font-bold ${badgeClass}">${sy.predikat}</span><div class="text-[10px] text-slate-500 mt-0.5">${sy.kesalahan} kesalahan</div></td>
            <td class="py-3 px-4 text-xs"><div class="font-medium text-slate-800">${sy.penguji}</div><div class="text-[11px] text-emerald-800 font-semibold mt-0.5">${dateFormatted}</div></td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs italic">"${sy.catatan}"</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-emerald-50 hover:bg-emerald-100 text-emerald-800 transition">Rapor</button></td>
          </tr>
        `;
      }).join('');
    }

    function populateKelancaranTables() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      const fluent = [...listSantri].filter(s => {
        return data.isAllTime ? s.total_juz_lancar > 0 : s.period_juz_lancar_count > 0;
      }).sort((a,b) => {
        if (!data.isAllTime) return b.period_juz_lancar_count - a.period_juz_lancar_count;
        return b.total_juz_lancar - a.total_juz_lancar;
      });
      
      document.getElementById('list-fluent-mobile').innerHTML = fluent.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-3 bg-white hover:bg-slate-50 cursor-pointer transition flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${data.isAllTime ? s.lancar_juz_str : (s.period_juz_lancar.map(j => 'Juz ' + j).join(', ') || '-')}</div>
          </div>
          <span class="px-2 py-1 rounded text-xs font-bold bg-emerald-100 text-emerald-800 shrink-0">
            ${data.isAllTime ? s.total_juz_lancar : s.period_juz_lancar_count} Juz Lancar
          </span>
        </div>
      `).join('');

      document.getElementById('table-fluent-students').innerHTML = fluent.map(s => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
          <td class="py-2 px-3 font-bold text-slate-900">${s.nama}</td>
          <td class="py-2 px-3 text-[11px] text-slate-500">${s.kelas_name}</td>
          <td class="py-2 px-3 font-bold text-emerald-700">${data.isAllTime ? s.total_juz_lancar : s.period_juz_lancar_count} Juz</td>
          <td class="py-2 px-3 text-[11px] text-slate-600 truncate max-w-xs">${data.isAllTime ? s.lancar_juz_str : (s.period_juz_lancar.map(j => 'Juz ' + j).join(', ') || '-')}</td>
          <td class="py-2 px-3 text-center"><button class="px-2 py-0.5 text-[11px] font-semibold rounded bg-emerald-50 text-emerald-800">Lihat</button></td>
        </tr>
      `).join('');

      const needAttn = [...listSantri].filter(s => {
        if (!data.isAllTime) {
          return s.period_juz_tidak_lancar_count > 0;
        }
        return s.total_tidak_lancar > 0;
      }).sort((a,b) => {
        if (!data.isAllTime) {
          return b.period_juz_tidak_lancar_count - a.period_juz_tidak_lancar_count;
        }
        return b.total_tidak_lancar - a.total_tidak_lancar;
      });
      
      document.getElementById('list-need-attention-mobile').innerHTML = needAttn.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-3 bg-white hover:bg-slate-50 cursor-pointer transition flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${data.isAllTime ? s.tidak_lancar_str : (s.period_juz_tidak_lancar.map(j=>'Juz '+j).join(', ') || '-')}</div>
          </div>
          <span class="px-2 py-1 rounded text-xs font-bold bg-rose-100 text-rose-800 shrink-0">
            ${data.isAllTime ? `${s.total_tidak_lancar} Juz Remidi` : `${s.period_juz_tidak_lancar_count} Juz Remidi`}
          </span>
        </div>
      `).join('');

      document.getElementById('table-need-attention-students').innerHTML = needAttn.map(s => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
          <td class="py-2 px-3 font-bold text-slate-900">${s.nama}</td>
          <td class="py-2 px-3 text-[11px] text-slate-500">${s.kelas_name}</td>
          <td class="py-2 px-3 font-bold text-rose-700">${data.isAllTime ? s.tidak_lancar_str : (s.period_juz_tidak_lancar.map(j=>'Juz '+j).join(', ') || '-')}</td>
          <td class="py-2 px-3 text-[11px] text-amber-700 font-medium">Perlu Pengulangan Tes</td>
          <td class="py-2 px-3 text-center"><button class="px-2 py-0.5 text-[11px] font-semibold rounded bg-rose-50 text-rose-800">Bimbing</button></td>
        </tr>
      `).join('');
    }

    function populateGroupingCards() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      // Classes (Kelas 1, 2, 3)
      const classContainer = document.getElementById('cards-classes-grid');
      const classMeta = [
        { id: 'kelas_1', name: 'Kelas 1 (Ula)' },
        { id: 'kelas_2', name: 'Kelas 2 (Wustho)' },
        { id: 'kelas_3', name: 'Kelas 3 (Ulya)' }
      ];

      classContainer.innerHTML = classMeta.map(cm => {
        const c_students = listSantri.filter(s => s.kelas_id === cm.id);
        const tot = c_students.length;
        const act = data.isAllTime ? c_students.filter(s => s.status === 'Aktif').length : c_students.filter(s => s.period_has_activity).length;
        const sy = data.isAllTime ? c_students.filter(s => s.has_syahadah).length : c_students.reduce((acc, s) => acc + s.period_syahadahs.length, 0);
        const j_ach = data.isAllTime ? c_students.reduce((acc, s) => acc + s.total_juz_dicapai, 0) : c_students.reduce((acc, s) => acc + s.period_juz_setor_count, 0);
        const j_lan = data.isAllTime ? c_students.reduce((acc, s) => acc + s.total_juz_lancar, 0) : c_students.reduce((acc, s) => acc + s.period_juz_lancar_count, 0);

        return `
          <div onclick="filterByGroup('kelas', '${cm.id}')" class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs hover:border-emerald-500 cursor-pointer transition">
            <div class="flex items-center justify-between mb-2.5">
              <h4 class="font-bold text-slate-900 text-xs sm:text-sm truncate">${cm.name}</h4>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-600 shrink-0">${tot} Santri</span>
            </div>
            <div class="space-y-1.5 text-xs text-slate-500">
              <div class="flex justify-between"><span>${data.isAllTime ? 'Santri Aktif:' : 'Santri Menyetor:'}</span><strong class="text-slate-700">${act}</strong></div>
              <div class="flex justify-between"><span>${data.isAllTime ? 'Total Hafalan:' : 'Total Disetor:'}</span><strong class="text-emerald-700 font-bold">${j_ach} Juz</strong></div>
              <div class="flex justify-between"><span>${data.isAllTime ? 'Total Lancar:' : 'Lulus Tes Lancar:'}</span><strong class="text-teal-700 font-bold">${j_lan} Juz</strong></div>
              <div class="flex justify-between"><span>Lulus Syahadah:</span><strong class="text-amber-700 font-bold">${sy} ${data.isAllTime ? `(${Math.round(sy/tot*100)}%)` : 'Lulus'}</strong></div>
            </div>
          </div>
        `;
      }).join('');

      // Halaqah
      const halaqahContainer = document.getElementById('cards-halaqah-grid');
      const halaqahs = Object.values(DB.halaqah_summary);

      halaqahContainer.innerHTML = halaqahs.map(h => {
        const m_students = listSantri.filter(s => s.musyrif_nama === h.musyrif_nama);
        const tot = m_students.length;
        const act = data.isAllTime ? m_students.filter(s => s.status === 'Aktif').length : m_students.filter(s => s.period_has_activity).length;
        const j_ach = data.isAllTime ? m_students.reduce((acc, s) => acc + s.total_juz_dicapai, 0) : m_students.reduce((acc, s) => acc + s.period_juz_setor_count, 0);
        const sy = data.isAllTime ? m_students.filter(s => s.has_syahadah).length : m_students.reduce((acc, s) => acc + s.period_syahadahs.length, 0);

        return `
          <div onclick="filterByGroup('halaqah', '${h.musyrif_nama}')" class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs hover:border-teal-500 cursor-pointer transition">
            <div class="flex items-center justify-between mb-2.5">
              <h4 class="font-bold text-slate-900 text-xs sm:text-sm truncate mr-2" title="${h.musyrif_nama}">${h.musyrif_nama}</h4>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 text-teal-800 shrink-0">${tot} Santri</span>
            </div>
            <div class="space-y-1.5 text-xs text-slate-500">
              <div class="flex justify-between"><span>${data.isAllTime ? 'Santri Aktif:' : 'Santri Menyetor:'}</span><strong class="text-slate-700">${act}</strong></div>
              <div class="flex justify-between"><span>${data.isAllTime ? 'Total Juz:' : 'Juz Disetor:'}</span><strong class="text-emerald-700 font-bold">${j_ach} Juz</strong></div>
              <div class="flex justify-between"><span>Lulus Syahadah:</span><strong class="text-amber-700 font-bold">${sy} Santri</strong></div>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterByGroup(type, val) {
      switchTab('santri');
      if (type === 'kelas') {
        document.getElementById('filterKelas').value = val;
      } else if (type === 'halaqah') {
        document.getElementById('filterHalaqah').value = val;
      }
      applyFilters();
    }

    function initHalaqahFilterDropdown() {
      const select = document.getElementById('filterHalaqah');
      const halaqahs = Object.keys(DB.halaqah_summary);
      halaqahs.forEach(h => {
        const opt = document.createElement('option');
        opt.value = h;
        opt.textContent = h;
        select.appendChild(opt);
      });
    }

    function applyFilters() {
      const search = document.getElementById('searchInput').value.toLowerCase().trim();
      const kFilter = document.getElementById('filterKelas').value;
      const hFilter = document.getElementById('filterHalaqah').value;
      const sFilter = document.getElementById('filterSyahadah').value;

      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      filteredSantri = listSantri.filter(s => {
        if (search) {
          const matchName = s.nama.toLowerCase().includes(search);
          const matchNis = s.nis.toLowerCase().includes(search);
          if (!matchName && !matchNis) return false;
        }

        if (kFilter !== 'semua' && s.kelas_id !== kFilter) return false;
        if (hFilter !== 'semua' && s.musyrif_nama !== hFilter) return false;

        if (sFilter === 'syahadah') {
          if (data.isAllTime) { if (!s.has_syahadah) return false; }
          else { if (s.period_syahadahs.length === 0) return false; }
        } else if (sFilter === 'siap') {
          if (s.has_syahadah || s.total_juz_dicapai < 5) return false;
        } else if (sFilter === 'belum') {
          if (s.has_syahadah) return false;
        }

        return true;
      });

      sortFilteredSantri();
      renderSantriViews();
    }

    function resetFilters() {
      document.getElementById('searchInput').value = '';
      document.getElementById('filterKelas').value = 'semua';
      document.getElementById('filterHalaqah').value = 'semua';
      document.getElementById('filterSyahadah').value = 'semua';
      applyFilters();
    }

    function sortSantriTable(col) {
      if (currentSort.column === col) {
        currentSort.asc = !currentSort.asc;
      } else {
        currentSort.column = col;
        currentSort.asc = true;
      }
      sortFilteredSantri();
      renderSantriViews();
    }

    function sortFilteredSantri() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      filteredSantri.sort((a,b) => {
        let valA, valB;
        if (currentSort.column === 'nama') {
          valA = a.nama.toLowerCase(); valB = b.nama.toLowerCase();
        } else if (currentSort.column === 'kelas') {
          valA = a.kelas_name; valB = b.kelas_name;
        } else if (currentSort.column === 'halaqah') {
          valA = a.musyrif_nama; valB = b.musyrif_nama;
        } else if (currentSort.column === 'juz_dicapai') {
          valA = data.isAllTime ? a.total_juz_dicapai : a.period_juz_setor_count;
          valB = data.isAllTime ? b.total_juz_dicapai : b.period_juz_setor_count;
        } else if (currentSort.column === 'juz_lancar') {
          valA = data.isAllTime ? a.total_juz_lancar : a.period_juz_lancar_count;
          valB = data.isAllTime ? b.total_juz_lancar : b.period_juz_lancar_count;
        }
        if (valA < valB) return currentSort.asc ? -1 : 1;
        if (valA > valB) return currentSort.asc ? 1 : -1;
        return 0;
      });
    }

    function renderSantriViews() {
      document.getElementById('filterResultCount').textContent = filteredSantri.length;
      const mobileContainer = document.getElementById('santriMobileCards');
      const tableBody = document.getElementById('santriTableBody');

      if (filteredSantri.length === 0) {
        mobileContainer.innerHTML = `<div class="p-8 text-center text-xs text-slate-400 bg-white rounded-2xl border border-slate-200">Tidak ada santri yang sesuai kriteria pencarian.</div>`;
        tableBody.innerHTML = `<tr><td colspan="8" class="text-center py-10 text-slate-400">Tidak ada santri yang sesuai kriteria pencarian.</td></tr>`;
        return;
      }

      const isAllTime = (currentPeriodData && currentPeriodData.isAllTime) || !currentPeriodData;

      // Mobile Cards View
      mobileContainer.innerHTML = filteredSantri.map(s => {
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);
        let badgeSy = '';
        if (s.has_syahadah) {
          badgeSy = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          badgeSy = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">Siap Ujian 1</span>`;
        }

        const periodSetorInfo = isAllTime 
          ? `<strong class="text-emerald-700">${s.total_juz_dicapai} Juz</strong>`
          : `<strong class="text-emerald-700">${s.period_juz_setor_count} Juz di periode ini</strong> (${s.total_juz_dicapai} total)`;

        const periodLancarInfo = isAllTime
          ? `${s.total_juz_lancar} Juz Lancar`
          : `${s.period_juz_lancar_count} Lancar (${s.total_juz_lancar} total)`;

        const lastActivityFormatted = isAllTime 
          ? (s.last_ziyadah ? s.last_ziyadah.created_at_indo : '-')
          : (s.period_last_date_indo || '-');

        return `
          <div onclick="openSantriModal(${s.id})" class="bg-white rounded-2xl p-3.5 border border-slate-200 shadow-xs space-y-2.5 active:scale-[0.99] transition cursor-pointer">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-slate-900">${s.nama}</h4>
                <div class="text-[10px] text-slate-400">NIS: ${s.nis} • ${s.kelas_name}</div>
              </div>
              <div class="text-right">${badgeSy}</div>
            </div>

            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-500">Capaian: ${periodSetorInfo}</span>
                <span class="text-teal-700 font-semibold">${periodLancarInfo}</span>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>

            <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[10px] text-slate-400">
              <span class="truncate max-w-[180px]">Musyrif: ${s.musyrif_nama}</span>
              <span class="font-semibold text-emerald-800">${lastActivityFormatted} &rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      // Desktop Table View
      tableBody.innerHTML = filteredSantri.map(s => {
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);
        let syahadahBadge = '<span class="text-slate-400 text-xs">-</span>';
        if (s.has_syahadah) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-300">Siap Ujian 1</span>`;
        }

        const achDisplay = isAllTime 
          ? `<div class="flex items-center gap-1.5"><span class="font-bold text-emerald-700 text-xs">${s.total_juz_dicapai} Juz</span><span class="text-[10px] text-slate-400">(${pct}%)</span></div>`
          : `<div class="flex items-center gap-1.5"><span class="font-bold text-emerald-700 text-xs">${s.period_juz_setor_count} Juz</span><span class="text-[10px] text-slate-400">(${s.total_juz_dicapai} total)</span></div>`;

        const lanDisplay = isAllTime
          ? `${s.total_juz_lancar} Juz`
          : `${s.period_juz_lancar_count} Juz (${s.total_juz_lancar} total)`;

        return `
          <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.jenis_kelamin}</div></td>
            <td class="py-3 px-4 text-xs font-medium text-slate-700 truncate max-w-[180px]">${s.musyrif_nama}</td>
            <td class="py-3 px-4">
              ${achDisplay}
              <div class="w-16 bg-slate-100 rounded-full h-1 mt-1 overflow-hidden"><div class="bg-emerald-500 h-1 rounded-full" style="width: ${pct}%"></div></div>
            </td>
            <td class="py-3 px-4 font-bold text-teal-700 text-xs">${lanDisplay}</td>
            <td class="py-3 px-4">${syahadahBadge}</td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700">${s.fluency_label}</span></td>
            <td class="py-3 px-4 text-center"><button class="px-3 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs">Rapor</button></td>
          </tr>
        `;
      }).join('');
    }

    function openSantriModal(santriId) {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;
      const s = listSantri.find(item => item.id === santriId);
      if (!s) return;
      currentModalSantri = s;

      document.getElementById('modal-avatar').textContent = s.nama.charAt(0);
      document.getElementById('modal-nama').textContent = s.nama;
      document.getElementById('modal-status').textContent = s.status;
      document.getElementById('modal-nis').textContent = `NIS: ${s.nis}`;
      document.getElementById('modal-kelas').textContent = s.kelas_name;
      document.getElementById('modal-halaqah').textContent = s.musyrif_nama;

      document.getElementById('modal-juz-dicapai').textContent = `${s.total_juz_dicapai} Juz`;
      document.getElementById('modal-juz-lancar').textContent = `${s.total_juz_lancar} Juz`;

      if (s.has_syahadah) {
        document.getElementById('modal-syahadah-highest').textContent = `Syahadah ${s.highest_syahadah.toUpperCase()}`;
        document.getElementById('modal-syahadah-count').textContent = `${s.syahadah_count} Sertifikat Lulus`;
      } else {
        document.getElementById('modal-syahadah-highest').textContent = 'Belum Ada';
        document.getElementById('modal-syahadah-count').textContent = s.total_juz_dicapai >= 5 ? 'Siap Ujian 1' : 'Dalam Proses';
      }

      document.getElementById('modal-juziyah-count').textContent = `${s.juziyah_count} Juziyah`;
      document.getElementById('modal-tidak-lancar-count').textContent = `${s.total_tidak_lancar} Juz Remidi`;

      document.getElementById('modal-target-title').textContent = s.syahadah_status_summary;
      document.getElementById('modal-target-pct').textContent = `${s.syahadah_progress_pct}%`;
      document.getElementById('modal-target-bar').style.width = `${s.syahadah_progress_pct}%`;
      
      const lastAchDate = s.last_achievement ? formatIndoDate(s.last_achievement.created_at) : '-';
      document.getElementById('modal-target-desc').textContent = `Setoran Terakhir: ${s.last_achievement ? `${s.last_achievement.type.toUpperCase()} di Juz ${s.last_achievement.juz || '-'} (${lastAchDate})` : 'Belum ada setoran'}`;

      const grid = document.getElementById('modal-juz-grid');
      grid.innerHTML = s.juz_grid.map(g => {
        let style = 'bg-slate-100 text-slate-400 border-slate-200';
        if (g.status === 'lancar') style = 'bg-emerald-500 text-white font-bold border-emerald-600 shadow-xs';
        else if (g.status === 'hafal_belum_tes') style = 'bg-amber-400 text-slate-900 font-bold border-amber-500';
        else if (g.status === 'tidak_lancar') style = 'bg-rose-500 text-white font-bold border-rose-600';

        const isSetorInPeriod = (s.period_juz_setor || []).includes(g.juz);
        const periodRing = isSetorInPeriod ? 'ring-2 ring-emerald-400 ring-offset-1' : '';

        return `
          <button onclick="selectJuzTile(${g.juz})" type="button" class="p-1.5 sm:p-2 rounded-xl border text-center transition active:scale-95 ${style} ${periodRing}">
            <div class="text-[10px] sm:text-xs font-black">J${g.juz}</div>
            <div class="text-[8px] sm:text-[9px] mt-0.5 truncate">${g.status === 'lancar' ? 'Lancar' : (g.status === 'hafal_belum_tes' ? 'Setor' : (g.status === 'tidak_lancar' ? 'Remidi' : '-'))}</div>
          </button>
        `;
      }).join('');

      selectJuzTile(s.achieved_juz_list.length > 0 ? s.achieved_juz_list[0] : 1);

      const sySection = document.getElementById('modal-syahadah-section');
      const syList = document.getElementById('modal-syahadah-list');
      if (s.syahadahs.length > 0) {
        sySection.classList.remove('hidden');
        syList.innerHTML = s.syahadahs.map(sy => {
          const formattedDate = formatIndoDate(sy.created_at);
          return `
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-xs space-y-1">
              <div class="flex items-center justify-between font-bold text-amber-900">
                <span>Syahadah ${sy.tingkat.toUpperCase()} (${sy.juz_cakupan_str})</span>
                <span class="px-2 py-0.5 rounded bg-amber-200 text-amber-900">${sy.predikat} (${sy.kesalahan} salah)</span>
              </div>
              <div class="text-[11px] text-slate-600">Penguji: ${sy.penguji} • <strong class="text-emerald-800">${formattedDate}</strong></div>
              ${sy.catatan ? `<div class="italic text-[10px] text-slate-500">"${sy.catatan}"</div>` : ''}
            </div>
          `;
        }).join('');
      } else {
        sySection.classList.add('hidden');
      }

      const jzSection = document.getElementById('modal-juziyah-section');
      const jzList = document.getElementById('modal-juziyah-list');
      if (s.juziyahs.length > 0) {
        jzSection.classList.remove('hidden');
        jzList.innerHTML = s.juziyahs.map(j => {
          const formattedDate = formatIndoDate(j.created_at);
          return `
            <div class="p-2.5 rounded-xl bg-indigo-50/70 border border-indigo-200 text-xs flex items-center justify-between">
              <div>
                <strong class="text-indigo-950 font-bold">Juz ${j.juz}</strong>
                <span class="text-slate-500 ml-2 text-[11px]">Predikat: <strong class="text-emerald-800">${j.predikat}</strong> (${j.kesalahan} salah)</span>
              </div>
              <span class="text-[11px] font-semibold text-slate-600">${formattedDate}</span>
            </div>
          `;
        }).join('');
      } else {
        jzSection.classList.add('hidden');
      }

      let rek = `Alhamdulillah, ananda ${s.nama} (${s.kelas_name}) saat ini telah menyelesaikan ${s.total_juz_dicapai} Juz. `;
      if (s.total_tidak_lancar > 0) {
        rek += `Sangat dianjurkan untuk memperkuat murajaah pada ${s.tidak_lancar_str} yang sebelumnya tercatat remidi sebelum menambah ziyadah baru. `;
      }
      if (s.total_juz_dicapai >= 5 && !s.has_syahadah) {
        rek += `Ananda sudah siap secara kapasitas untuk mengambil Ujian Syahadah 1 (5 Juz). Mohon bimbingan orang tua di rumah untuk melatih murajaah sambung ayat. `;
      } else if (s.has_syahadah) {
        rek += `Pertahankan pencapaian mutqin Syahadah ${s.highest_syahadah} dengan konsisten tadarus 1 juz per hari.`;
      } else {
        rek += `Pertahankan kedisiplinan setoran harian bersama musyrif halaqah.`;
      }
      document.getElementById('modal-rekomendasi').textContent = rek;

      document.getElementById('santriModal').classList.remove('hidden');
      lucide.createIcons();
    }

    function selectJuzTile(juzNum) {
      if (!currentModalSantri) return;
      const g = currentModalSantri.juz_grid.find(item => item.juz === juzNum);
      if (!g) return;

      document.getElementById('selected-juz-badge').textContent = g.juz;
      document.getElementById('selected-juz-title').textContent = `Juz ${g.juz}`;
      document.getElementById('selected-juz-surah').textContent = `(${g.name})`;
      document.getElementById('selected-juz-status').textContent = g.label;

      const statusElem = document.getElementById('selected-juz-status');
      if (g.status === 'lancar') {
        statusElem.className = 'text-[11px] font-bold text-emerald-700 shrink-0';
      } else if (g.status === 'tidak_lancar') {
        statusElem.className = 'text-[11px] font-bold text-rose-700 shrink-0';
      } else if (g.status === 'hafal_belum_tes') {
        statusElem.className = 'text-[11px] font-bold text-amber-700 shrink-0';
      } else {
        statusElem.className = 'text-[11px] font-semibold text-slate-400 shrink-0';
      }
    }

    function closeSantriModal() {
      document.getElementById('santriModal').classList.add('hidden');
      currentModalSantri = null;
    }

    function exportToCSV() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = filteredSantri;
      
      let csv = 'NIS,Nama,Kelas,Halaqah,Status,Gender,Total Juz Dicapai,Juz Disetor di Periode,Total Juz Lancar,Syahadah,Aktivitas Terakhir di Periode\n';
      listSantri.forEach(s => {
        csv += `"${s.nis}","${s.nama}","${s.kelas_name}","${s.musyrif_nama}","${s.status}","${s.jenis_kelamin}",${s.total_juz_dicapai},${s.period_juz_setor_count || 0},${s.total_juz_lancar},"${s.highest_syahadah || '-'}","${s.period_last_date_indo || '-'}\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `laporan_tahfidz_kelas_123_${currentDateRange.start}_sd_${currentDateRange.end}.csv`;
      link.click();
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('filterStartDate').value = DB.metadata.min_date;
      document.getElementById('filterEndDate').value = DB.metadata.max_date;
      document.getElementById('topBarUpdateDate').textContent = `Pembaruan: ${formatIndoDate(DB.metadata.max_date)}`;
      document.getElementById('footerMetadata').innerHTML = `Snapshot: <code class="font-mono text-emerald-700">everynight-in-my-dream.db</code> • 44 Santri • Pembaruan: ${formatIndoDate(DB.metadata.max_date)}`;

      initHalaqahFilterDropdown();
      setPresetRange('all');
    });

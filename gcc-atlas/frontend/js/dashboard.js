/**
 * Dashboard Module for GCC Atlas
 * Loads dynamic KPIs, renders Chart.js visualizations, and displays recent records.
 */

const dashboardModule = {
  sectorChartInstance: null,
  cityChartInstance: null,
  isLoaded: false,

  async load() {
    try {
      const res = await fetch('/api/dashboard');
      if (!res.ok) throw new Error('Failed to load dashboard data');
      const data = await res.json();
      this.renderKPIs(data);
      this.renderCharts(data);
      this.renderRecentCompanies(data.recent_companies);
      this.renderRecentExpansions(data.recent_expansions);
      if (data.prototype_disclaimer) {
        const discEl = document.getElementById('dashboard-disclaimer-text');
        if (discEl) discEl.innerText = data.prototype_disclaimer;
      }
      this.isLoaded = true;
    } catch (err) {
      console.error('Error loading dashboard:', err);
      app.showToast('Failed to load dashboard intelligence', 'error');
    }
  },

  renderKPIs(data) {
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.innerText = val !== undefined ? val : '--';
    };

    setVal('kpi-total-companies', data.total_companies);
    setVal('kpi-total-cities', data.total_cities);
    setVal('kpi-total-sectors', data.total_sectors);
    setVal('kpi-total-sources', data.total_sources);
  },

  renderCharts(data) {
    if (typeof Chart === 'undefined') {
      console.warn('Chart.js is not loaded yet');
      return;
    }

    // 1. Sector Doughnut Chart
    const sectorCtx = document.getElementById('sectorChart');
    if (sectorCtx) {
      if (this.sectorChartInstance) {
        this.sectorChartInstance.destroy();
      }

      const sectorLabels = data.sector_distribution.map(s => s.sector);
      const sectorCounts = data.sector_distribution.map(s => s.count);
      const sectorColors = [
        '#2563eb', // Royal Blue
        '#0284c7', // Sky Blue
        '#059669', // Emerald
        '#7c3aed', // Violet
        '#d97706', // Amber
        '#dc2626', // Red
        '#475569'  // Slate
      ];

      this.sectorChartInstance = new Chart(sectorCtx, {
        type: 'doughnut',
        data: {
          labels: sectorLabels,
          datasets: [{
            data: sectorCounts,
            backgroundColor: sectorColors.slice(0, sectorLabels.length),
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                boxWidth: 12,
                font: { size: 11, family: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto' },
                color: '#1e293b'
              }
            },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${ctx.label}: ${ctx.raw} GCCs (${((ctx.raw / data.total_companies) * 100).toFixed(1)}%)`
              }
            }
          },
          cutout: '65%'
        }
      });
    }

    // 2. City Bar Chart
    const cityCtx = document.getElementById('cityChart');
    if (cityCtx) {
      if (this.cityChartInstance) {
        this.cityChartInstance.destroy();
      }

      const cityLabels = data.city_distribution.map(c => c.city_name);
      const cityCounts = data.city_distribution.map(c => c.count);

      this.cityChartInstance = new Chart(cityCtx, {
        type: 'bar',
        data: {
          labels: cityLabels,
          datasets: [{
            label: 'GCC Count',
            data: cityCounts,
            backgroundColor: '#2563eb',
            borderRadius: 6,
            barThickness: 28
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 2, color: '#64748b', font: { size: 11 } },
              grid: { color: '#f1f5f9' }
            },
            x: {
              ticks: { color: '#1e293b', font: { size: 12, weight: '500' } },
              grid: { display: false }
            }
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => ` ${ctx.raw} Verified GCCs`
              }
            }
          }
        }
      });
    }
  },

  renderRecentCompanies(companies) {
    const tbody = document.getElementById('recent-companies-tbody');
    if (!tbody) return;

    if (!companies || companies.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--navy-500);">No company records found.</td></tr>';
      return;
    }

    tbody.innerHTML = companies.map(c => `
      <tr>
        <td>
          <div class="company-name-cell" onclick="companiesModule.openCompanyDetail('${c.id}')">${c.name}</div>
          <div class="company-subtext">${c.hq_country}</div>
        </td>
        <td><strong>${c.city_name}</strong></td>
        <td><span class="badge badge-sector">${c.sector}</span></td>
        <td><span class="badge badge-verified">● Verified</span></td>
      </tr>
    `).join('');
  },

  renderRecentExpansions(expansions) {
    const container = document.getElementById('recent-expansions-list');
    if (!container) return;

    if (!expansions || expansions.length === 0) {
      container.innerHTML = '<div style="text-align: center; color: var(--navy-500);">No expansion milestones recorded.</div>';
      return;
    }

    container.innerHTML = expansions.map(e => `
      <div style="background-color: var(--bg-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
          <div>
            <span style="font-weight: 700; color: var(--navy-900); font-size: 14px;">${e.company_name}</span>
            <span class="badge badge-sector" style="margin-left: 6px;">${e.city_name}</span>
          </div>
          <span style="font-size: 11px; color: var(--navy-500); font-weight: 600;">${e.date}</span>
        </div>
        <div style="font-weight: 600; font-size: 13px; color: var(--primary); margin-bottom: 4px;">${e.announcement_title}</div>
        <p style="font-size: 12px; color: var(--navy-700); line-height: 1.4; margin-bottom: 8px;">${e.details}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
          <span style="color: var(--navy-500);">Source: ${e.source_name}</span>
          <a href="${e.source_url}" target="_blank" class="evidence-link">Source Link ↗</a>
        </div>
      </div>
    `).join('');
  }
};

window.dashboardModule = dashboardModule;

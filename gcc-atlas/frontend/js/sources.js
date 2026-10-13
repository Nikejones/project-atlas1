/**
 * Sources & Data Quality Module for GCC Atlas
 * Handles sources catalogue rendering, data completeness metrics, and governance disclosures.
 */

const sourcesModule = {
  isLoaded: false,

  async load() {
    try {
      const res = await fetch('/api/sources');
      if (!res.ok) throw new Error('Failed to load sources and quality report');
      const data = await res.json();

      this.renderQualityScorecard(data.quality_metrics);
      this.renderSourcesTable(data.sources);

      if (data.methodology_note) {
        const methEl = document.getElementById('sources-methodology-text');
        if (methEl) {
          methEl.innerHTML = `
            ${data.methodology_note}
            <br><br>
            <strong>Zero-Fabrication Commitment:</strong> If specific figures (such as unverified establishment years or confidential lease terms) cannot be corroborated through primary public evidence, they are transparently displayed as <em>"Data unavailable"</em>.
          `;
        }
      }

      this.isLoaded = true;
    } catch (err) {
      console.error('Error loading sources:', err);
      app.showToast('Could not load sources and governance data', 'error');
    }
  },

  renderQualityScorecard(metrics) {
    const setPct = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.innerText = `${val}%`;
    };

    setPct('quality-year-pct', metrics.year_established_completeness_pct);
    setPct('quality-evidence-pct', metrics.evidence_url_completeness_pct);
    setPct('quality-rent-pct', metrics.rent_benchmark_completeness_pct);
    setPct('quality-verification-pct', metrics.verification_rate_pct);
  },

  renderSourcesTable(sources) {
    const tbody = document.getElementById('sources-table-body');
    if (!tbody) return;

    if (!sources || sources.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--navy-500);">No source records found.</td></tr>';
      return;
    }

    tbody.innerHTML = sources.map(s => `
      <tr>
        <td>
          <div style="font-weight: 600; color: var(--navy-900);">${s.name}</div>
          <div style="font-size: 11px; color: var(--navy-500); max-width: 380px;">${s.description || ''}</div>
        </td>
        <td>
          <span class="badge badge-sector">${s.category}</span>
        </td>
        <td>
          <strong style="color: var(--primary);">${s.linked_company_count}</strong> GCCs
        </td>
        <td>
          <span class="badge ${s.reliability_tier.includes('Primary') ? 'badge-verified' : 'badge-under-review'}">
            ${s.reliability_tier}
          </span>
        </td>
        <td style="font-size: 12px; color: var(--navy-600); white-space: nowrap;">
          ${s.last_checked_date}
        </td>
        <td>
          <a href="${s.url}" target="_blank" class="evidence-link">
            <span>Official Portal</span>
            <span>↗</span>
          </a>
        </td>
      </tr>
    `).join('');
  }
};

window.sourcesModule = sourcesModule;

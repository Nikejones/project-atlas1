/**
 * Cities Module for GCC Atlas
 * Handles city multi-select, side-by-side comparison matrix, and rule-based trade-off synthesis.
 */

const citiesModule = {
  selectedCities: ['bengaluru', 'hyderabad'],
  availableCities: [],
  isLoaded: false,

  async load() {
    try {
      if (this.availableCities.length === 0) {
        const res = await fetch('/api/cities');
        if (!res.ok) throw new Error('Failed to load cities');
        const data = await res.json();
        this.availableCities = data.items;
        this.renderCitySelector();
      }
      await this.runComparison();
      this.isLoaded = true;
    } catch (err) {
      console.error('Error in cities module:', err);
      app.showToast('Could not load city benchmarking data', 'error');
    }
  },

  renderCitySelector() {
    const container = document.getElementById('city-pill-selector');
    if (!container) return;

    container.innerHTML = this.availableCities.map(c => {
      const isSelected = this.selectedCities.includes(c.id);
      return `
        <button class="city-pill-btn ${isSelected ? 'selected' : ''}" data-city-id="${c.id}">
          <span>${isSelected ? '✓' : '+'}</span>
          <span>${c.name}</span>
          <span style="font-size: 11px; opacity: 0.8;">(${c.gcc_count} GCCs)</span>
        </button>
      `;
    }).join('');

    container.querySelectorAll('.city-pill-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cityId = btn.getAttribute('data-city-id');
        this.toggleCity(cityId);
      });
    });
  },

  toggleCity(cityId) {
    if (this.selectedCities.includes(cityId)) {
      if (this.selectedCities.length <= 2) {
        app.showToast('Comparison requires at least 2 cities', 'error');
        return;
      }
      this.selectedCities = this.selectedCities.filter(id => id !== cityId);
    } else {
      if (this.selectedCities.length >= 4) {
        app.showToast('You can compare a maximum of 4 cities simultaneously', 'error');
        return;
      }
      this.selectedCities.push(cityId);
    }

    this.renderCitySelector();
    this.runComparison();
  },

  async runComparison() {
    const matrixContainer = document.getElementById('city-matrix-container');
    const tradeoffContainer = document.getElementById('city-tradeoff-summary');
    if (!matrixContainer) return;

    matrixContainer.innerHTML = '<div style="padding: 30px; grid-column: 1 / -1; text-align: center;"><div class="spinner"></div></div>';

    try {
      const query = this.selectedCities.join(',');
      const res = await fetch(`/api/cities/compare?city_ids=${query}`);
      if (!res.ok) throw new Error('Comparison failed');
      const data = await res.json();

      this.renderMatrix(data.compared_cities);
      this.renderTradeoffSummary(data.tradeoff_analysis);
    } catch (err) {
      console.error('Error running comparison:', err);
      matrixContainer.innerHTML = '<div style="padding: 24px; color: var(--navy-500); grid-column: 1 / -1; text-align: center;">Comparison data could not be retrieved.</div>';
    }
  },

  renderTradeoffSummary(tradeoff) {
    const el = document.getElementById('city-tradeoff-summary');
    if (!el) return;

    // Convert markdown bullets and bolds into clean HTML
    let html = tradeoff.summary_text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/• (.*?)(?=\n|$)/g, '<div style="margin: 4px 0 4px 12px;">• $1</div>')
      .replace(/\n\n/g, '<br><br>');

    if (tradeoff.data_limitations_note) {
      html += `<div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed var(--border-strong); font-size: 12px; color: var(--navy-500); font-style: italic;">
        ${tradeoff.data_limitations_note}
      </div>`;
    }

    el.innerHTML = html;
  },

  renderMatrix(cities) {
    const container = document.getElementById('city-matrix-container');
    if (!container) return;

    // Define matrix dimensions
    const colCount = cities.length;
    container.style.gridTemplateColumns = `200px repeat(${colCount}, minmax(220px, 1fr))`;

    let html = '';

    // 1. Header row
    html += '<div class="matrix-header-cell">Metropolitan Corridor</div>';
    cities.forEach(c => {
      html += `
        <div class="matrix-col-header">
          <div style="font-size: 16px; font-weight: 700; color: var(--navy-900);">${c.name}</div>
          <div style="font-size: 12px; color: var(--navy-500); font-weight: 500;">${c.state} • ${c.tier}</div>
          <div style="margin-top: 6px;"><span class="badge badge-verified">${c.gcc_count} GCCs in Dataset</span></div>
        </div>
      `;
    });

    // Metric rows helper
    const addRow = (metricLabel, getValueFn) => {
      html += `<div class="matrix-metric-label">${metricLabel}</div>`;
      cities.forEach(c => {
        html += `<div class="matrix-metric-val">${getValueFn(c)}</div>`;
      });
    };

    // 2. Grade A Office Rent
    addRow('🏢 Grade A Office Rental', c => {
      if (c.indicative_rent_min === null || c.indicative_rent_min === undefined) {
        return '<span style="color: var(--navy-500);">Data unavailable</span>';
      }
      return `
        <strong style="font-size: 15px; color: var(--navy-900);">₹${c.indicative_rent_min} – ₹${c.indicative_rent_max}</strong>
        <div style="font-size: 11px; color: var(--navy-600);">per sq ft / month</div>
        <div style="font-size: 11px; color: var(--navy-500); margin-top: 2px;">${c.indicative_rent_period || 'H1 2024'}</div>
      `;
    });

    // 3. Tech Salary: Entry-Level (0-2 yrs)
    addRow('💻 Tech Salary: Entry (0–2y)', c => {
      if (c.indicative_salary_entry_lakh === null) return '<span style="color: var(--navy-500);">Data unavailable</span>';
      return `<strong>₹${c.indicative_salary_entry_lakh} Lakh</strong> / annum`;
    });

    // 4. Tech Salary: Mid-Level (3-7 yrs)
    addRow('💻 Tech Salary: Mid (3–7y)', c => {
      if (c.indicative_salary_mid_lakh === null) return '<span style="color: var(--navy-500);">Data unavailable</span>';
      return `<strong style="color: var(--primary);">₹${c.indicative_salary_mid_lakh} Lakh</strong> / annum`;
    });

    // 5. Tech Salary: Senior / Lead (8-12+ yrs)
    addRow('💻 Tech Salary: Senior (8–12y+)', c => {
      if (c.indicative_salary_senior_lakh === null) return '<span style="color: var(--navy-500);">Data unavailable</span>';
      return `<strong>₹${c.indicative_salary_senior_lakh} Lakh</strong> / annum`;
    });

    // 6. State Incentive Frameworks
    addRow('🏛️ State IT Policy & Incentives', c => {
      return c.state_incentives || '<span style="color: var(--navy-500);">Data unavailable</span>';
    });

    // 7. Talent Depth & Universities
    addRow('🎓 Talent & University Depth', c => {
      return c.talent_ecosystem || '<span style="color: var(--navy-500);">Data unavailable</span>';
    });

    // 8. Infrastructure & Transit
    addRow('✈️ Airport, Metro & Roads', c => {
      return c.infrastructure_notes || '<span style="color: var(--navy-500);">Data unavailable</span>';
    });

    // 9. Key Strategic Advantage
    addRow('✨ Primary Competitive Edge', c => {
      return `<span style="color: var(--success); font-weight: 500;">${c.tradeoff_pros || 'Data unavailable'}</span>`;
    });

    // 10. Operational Trade-Off / Limitation
    addRow('⚠️ Operational Friction Point', c => {
      return `<span style="color: var(--warning); font-weight: 500;">${c.tradeoff_cons || 'Data unavailable'}</span>`;
    });

    // 11. Benchmark Source
    addRow('🔗 Verified Benchmark Sourcing', c => {
      if (!c.source_url) return '<span style="color: var(--navy-500);">Data unavailable</span>';
      return `<a href="${c.source_url}" target="_blank" class="evidence-link">Official Report ↗</a><div style="font-size: 11px; color: var(--navy-500);">Updated: ${c.last_updated || '2024'}</div>`;
    });

    container.innerHTML = html;
  }
};

window.citiesModule = citiesModule;

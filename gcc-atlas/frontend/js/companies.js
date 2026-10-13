/**
 * Companies Directory Module for GCC Atlas
 * Handles search, filters, pagination, table rendering, and profile modal.
 */

const companiesModule = {
  state: {
    search: '',
    city: '',
    sector: '',
    verificationStatus: '',
    sortBy: 'name',
    sortOrder: 'asc',
    page: 1,
    limit: 10,
    totalPages: 1,
    totalRecords: 0
  },

  init() {
    this.setupListeners();
    this.setupModal();
  },

  setupListeners() {
    // Search input
    const searchInput = document.getElementById('comp-filter-search');
    if (searchInput) {
      let debounceTimer;
      searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          this.state.search = e.target.value.trim();
          this.state.page = 1;
          this.load();
        }, 300);
      });
    }

    // City filter
    const citySelect = document.getElementById('comp-filter-city');
    if (citySelect) {
      citySelect.addEventListener('change', (e) => {
        this.state.city = e.target.value;
        this.state.page = 1;
        this.load();
      });
    }

    // Sector filter
    const sectorSelect = document.getElementById('comp-filter-sector');
    if (sectorSelect) {
      sectorSelect.addEventListener('change', (e) => {
        this.state.sector = e.target.value;
        this.state.page = 1;
        this.load();
      });
    }

    // Status filter
    const statusSelect = document.getElementById('comp-filter-status');
    if (statusSelect) {
      statusSelect.addEventListener('change', (e) => {
        this.state.verificationStatus = e.target.value;
        this.state.page = 1;
        this.load();
      });
    }

    // Sort select
    const sortSelect = document.getElementById('comp-sort-by');
    if (sortSelect) {
      sortSelect.addEventListener('change', (e) => {
        this.state.sortBy = e.target.value;
        this.load();
      });
    }

    // Reset button
    const resetBtn = document.getElementById('comp-clear-filters-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        this.resetFilters();
      });
    }

    // Pagination buttons
    const prevBtn = document.getElementById('btn-prev-page');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (this.state.page > 1) {
          this.state.page--;
          this.load();
        }
      });
    }

    const nextBtn = document.getElementById('btn-next-page');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (this.state.page < this.state.totalPages) {
          this.state.page++;
          this.load();
        }
      });
    }
  },

  setupModal() {
    const modal = document.getElementById('company-detail-modal');
    const closeBtn = document.getElementById('modal-close-x');
    if (!modal) return;

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        modal.classList.remove('open');
      });
    }

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('open');
      }
    });
  },

  setSearchQuery(query) {
    const searchInput = document.getElementById('comp-filter-search');
    if (searchInput) searchInput.value = query;
    this.state.search = query;
    this.state.page = 1;
    this.load();
  },

  resetFilters() {
    this.state = {
      search: '',
      city: '',
      sector: '',
      verificationStatus: '',
      sortBy: 'name',
      sortOrder: 'asc',
      page: 1,
      limit: 10,
      totalPages: 1,
      totalRecords: 0
    };

    const searchInput = document.getElementById('comp-filter-search');
    if (searchInput) searchInput.value = '';

    const citySelect = document.getElementById('comp-filter-city');
    if (citySelect) citySelect.value = '';

    const sectorSelect = document.getElementById('comp-filter-sector');
    if (sectorSelect) sectorSelect.value = '';

    const statusSelect = document.getElementById('comp-filter-status');
    if (statusSelect) statusSelect.value = '';

    const sortSelect = document.getElementById('comp-sort-by');
    if (sortSelect) sortSelect.value = 'name';

    this.load();
  },

  async load() {
    const tbody = document.getElementById('companies-table-body');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 24px;"><div class="spinner"></div></td></tr>';
    }

    try {
      const params = new URLSearchParams();
      if (this.state.search) params.append('search', this.state.search);
      if (this.state.city) params.append('city', this.state.city);
      if (this.state.sector) params.append('sector', this.state.sector);
      if (this.state.verificationStatus) params.append('verification_status', this.state.verificationStatus);
      if (this.state.sortBy) params.append('sort_by', this.state.sortBy);
      if (this.state.sortOrder) params.append('sort_order', this.state.sortOrder);
      params.append('page', this.state.page);
      params.append('limit', this.state.limit);

      const res = await fetch(`/api/companies?${params.toString()}`);
      if (!res.ok) throw new Error('Failed to fetch companies');
      const data = await res.json();

      this.state.totalRecords = data.total;
      this.state.totalPages = data.total_pages;

      this.populateFilterDropdowns(data.available_cities, data.available_sectors);
      this.renderTable(data.items);
      this.renderPagination(data);
    } catch (err) {
      console.error('Error fetching companies:', err);
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--navy-500);">Failed to load company records.</td></tr>';
      }
      app.showToast('Could not load company directory', 'error');
    }
  },

  populateFilterDropdowns(cities, sectors) {
    const citySelect = document.getElementById('comp-filter-city');
    if (citySelect && citySelect.options.length <= 1) {
      cities.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.innerText = c;
        citySelect.appendChild(opt);
      });
    }

    const sectorSelect = document.getElementById('comp-filter-sector');
    if (sectorSelect && sectorSelect.options.length <= 1) {
      sectors.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.innerText = s;
        sectorSelect.appendChild(opt);
      });
    }
  },

  renderTable(companies) {
    const tbody = document.getElementById('companies-table-body');
    const countEl = document.getElementById('comp-results-count');
    if (!tbody) return;

    if (countEl) {
      countEl.innerText = `Showing ${companies.length} of ${this.state.totalRecords} records matching criteria`;
    }

    if (!companies || companies.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" style="text-align: center; padding: 36px;">
            <div class="empty-state">
              <div class="empty-icon">🔍</div>
              <div class="empty-title">No company records found</div>
              <div class="empty-desc">Try clearing or broadening your search keywords or city filters.</div>
            </div>
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = companies.map(c => {
      const year = c.year_established ? c.year_established : '<span style="color: var(--navy-500);">Data unavailable</span>';
      const statusBadge = c.verification_status === 'Verified'
        ? '<span class="badge badge-verified">● Verified</span>'
        : '<span class="badge badge-under-review">● Under Review</span>';

      return `
        <tr>
          <td>
            <div class="company-name-cell" onclick="companiesModule.openCompanyDetail('${c.id}')">${c.name}</div>
            <div class="company-subtext">${c.parent_company || c.name}</div>
          </td>
          <td>${c.hq_country}</td>
          <td><strong>${c.city_name}</strong></td>
          <td><span class="badge badge-sector">${c.sector}</span></td>
          <td>${year}</td>
          <td style="max-width: 220px; font-size: 12px; color: var(--navy-700); line-height: 1.3;">
            ${c.business_functions}
          </td>
          <td>${statusBadge}</td>
          <td>
            <a href="${c.evidence_url}" target="_blank" class="evidence-link" title="${c.source_name}">
              <span>Evidence</span>
              <span>↗</span>
            </a>
          </td>
          <td>
            <button class="quick-action-btn" onclick="companiesModule.openCompanyDetail('${c.id}')" style="padding: 4px 8px; font-size: 12px;">
              Profile
            </button>
          </td>
        </tr>
      `;
    }).join('');
  },

  renderPagination(data) {
    const info = document.getElementById('pagination-info');
    const prevBtn = document.getElementById('btn-prev-page');
    const nextBtn = document.getElementById('btn-next-page');
    const pagesContainer = document.getElementById('pagination-pages-list');

    if (info) {
      const start = data.total === 0 ? 0 : (data.page - 1) * data.limit + 1;
      const end = Math.min(data.page * data.limit, data.total);
      info.innerText = `Showing ${start}-${end} of ${data.total} records`;
    }

    if (prevBtn) prevBtn.disabled = data.page <= 1;
    if (nextBtn) nextBtn.disabled = data.page >= data.total_pages;

    if (pagesContainer) {
      pagesContainer.innerHTML = '';
      for (let i = 1; i <= data.total_pages; i++) {
        const btn = document.createElement('button');
        btn.className = `btn-page ${i === data.page ? 'active' : ''}`;
        btn.innerText = i;
        btn.addEventListener('click', () => {
          this.state.page = i;
          this.load();
        });
        pagesContainer.appendChild(btn);
      }
    }
  },

  async openCompanyDetail(companyId) {
    try {
      const res = await fetch(`/api/companies/${companyId}`);
      if (!res.ok) throw new Error('Company not found');
      const c = await res.json();

      document.getElementById('modal-company-name').innerText = c.name;
      document.getElementById('modal-company-sub').innerText = `${c.parent_company || c.name} • ${c.sector}`;
      document.getElementById('modal-city').innerText = c.city_name;
      document.getElementById('modal-hq').innerText = c.hq_country;
      document.getElementById('modal-year').innerText = c.year_established || 'Data unavailable in verified source';
      document.getElementById('modal-headcount').innerText = c.headcount_bracket || 'Confidential / Data unavailable';
      document.getElementById('modal-status').innerHTML = c.verification_status === 'Verified'
        ? '<span class="badge badge-verified">● Verified Record</span>'
        : '<span class="badge badge-under-review">● Under Review</span>';
      document.getElementById('modal-last-verified').innerText = c.last_verified_date || 'Recent';

      // Functions tags
      const funcContainer = document.getElementById('modal-functions');
      if (funcContainer) {
        const funcs = c.business_functions.split(',').map(f => f.trim());
        funcContainer.innerHTML = funcs.map(f => `<span class="badge badge-sector" style="padding: 4px 10px; font-size: 12px;">${f}</span>`).join('');
      }

      document.getElementById('modal-description').innerText = c.short_description;
      document.getElementById('modal-source-name').innerText = c.source_name;
      
      const linkEl = document.getElementById('modal-evidence-link');
      if (linkEl) {
        linkEl.href = c.evidence_url;
      }

      const modal = document.getElementById('company-detail-modal');
      if (modal) modal.classList.add('open');
    } catch (err) {
      console.error('Error loading company details:', err);
      app.showToast('Could not load company details', 'error');
    }
  }
};

window.companiesModule = companiesModule;
window.addEventListener('DOMContentLoaded', () => {
  companiesModule.init();
});

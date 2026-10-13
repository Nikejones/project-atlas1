/**
 * GCC Atlas Main Application Controller
 * Handles client-side navigation, global search, system health, and toasts.
 */

const app = {
  currentPage: 'dashboard',
  systemStatus: {
    healthy: false,
    aiMode: 'demo_mode',
    totalCompanies: 28,
    totalCities: 6
  },

  init() {
    this.setupNavigation();
    this.setupGlobalSearch();
    this.setupQuickActions();
    this.checkHealth();

    // Check hash for direct route
    const hash = window.location.hash.replace('#', '');
    if (hash && ['dashboard', 'companies', 'cities', 'assistant', 'sources'].includes(hash)) {
      this.navigateTo(hash);
    } else {
      this.navigateTo('dashboard');
    }
  },

  setupNavigation() {
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const page = item.getAttribute('data-page');
        if (page) {
          this.navigateTo(page);
        }
      });
    });
  },

  setupGlobalSearch() {
    const searchInput = document.getElementById('global-search-input');
    if (!searchInput) return;

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const query = searchInput.value.trim();
        if (query) {
          this.navigateTo('companies');
          if (window.companiesModule) {
            companiesModule.setSearchQuery(query);
          }
        }
      }
    });
  },

  setupQuickActions() {
    const askAiBtn = document.getElementById('quick-ask-ai-btn');
    if (askAiBtn) {
      askAiBtn.addEventListener('click', () => {
        this.navigateTo('assistant');
      });
    }
  },

  async checkHealth() {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        this.systemStatus = {
          healthy: data.database_connected,
          aiMode: data.ai_mode,
          totalCompanies: data.total_companies,
          totalCities: data.total_cities
        };
        this.updateSystemUI();
      }
    } catch (err) {
      console.warn('Backend health check error:', err);
    }
  },

  updateSystemUI() {
    const dot = document.getElementById('system-status-dot');
    const text = document.getElementById('system-status-text');
    const pill = document.getElementById('ai-mode-pill');
    const assistantPill = document.getElementById('assistant-badge-pill');

    if (dot && text) {
      if (this.systemStatus.healthy) {
        dot.className = 'status-dot';
        text.innerText = `${this.systemStatus.totalCompanies} Verified GCCs`;
      } else {
        dot.className = 'status-dot warning';
        text.innerText = 'Service Degraded';
      }
    }

    const isLive = this.systemStatus.aiMode === 'live_llm';
    const badgeClass = isLive ? 'badge badge-live' : 'badge badge-demo';
    const badgeText = isLive ? 'Live Gemini AI Active' : 'Rule-Based Demo Mode';

    if (pill) {
      pill.className = badgeClass;
      pill.innerText = badgeText;
    }
    if (assistantPill) {
      assistantPill.className = badgeClass;
      assistantPill.innerText = badgeText;
    }
  },

  navigateTo(pageId) {
    if (!['dashboard', 'companies', 'cities', 'assistant', 'sources'].includes(pageId)) {
      pageId = 'dashboard';
    }

    this.currentPage = pageId;
    window.location.hash = pageId;

    // Update nav links active state
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(item => {
      if (item.getAttribute('data-page') === pageId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Update view containers
    document.querySelectorAll('.page-view').forEach(view => {
      view.classList.remove('active');
    });

    const targetView = document.getElementById(`view-${pageId}`);
    if (targetView) {
      targetView.classList.add('active');
    }

    // Update titles
    const headings = {
      dashboard: {
        title: 'GCC Intelligence Dashboard',
        sub: "Macro analytics on India's capability centre landscape"
      },
      companies: {
        title: 'GCC Company Directory',
        sub: 'Searchable database of multinational GCC operations in India'
      },
      cities: {
        title: 'GCC City Comparison',
        sub: 'Side-by-side strategic benchmarking of Indian tech corridors'
      },
      assistant: {
        title: 'AI GCC Research Assistant',
        sub: 'Retrieval-augmented conversational intelligence grounded in database records'
      },
      sources: {
        title: 'Sources & Data Quality',
        sub: 'Public data provenance, verification metrics, and integrity governance'
      }
    };

    const h = headings[pageId] || headings.dashboard;
    const titleEl = document.getElementById('page-heading');
    const subEl = document.getElementById('page-subheading');
    if (titleEl) titleEl.innerText = h.title;
    if (subEl) subEl.innerText = h.sub;

    // Trigger module loading
    if (pageId === 'dashboard' && window.dashboardModule) {
      dashboardModule.load();
    } else if (pageId === 'companies' && window.companiesModule) {
      companiesModule.load();
    } else if (pageId === 'cities' && window.citiesModule) {
      citiesModule.load();
    } else if (pageId === 'sources' && window.sourcesModule) {
      sourcesModule.load();
    }
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${type === 'success' ? '✅' : type === 'error' ? '⚠️' : 'ℹ️'}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.2s ease';
      setTimeout(() => toast.remove(), 200);
    }, 3500);
  }
};

window.addEventListener('DOMContentLoaded', () => {
  app.init();
});

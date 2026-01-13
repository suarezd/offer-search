import { ScrapeJobsCommand } from '../../../application/commands/ScrapeJobsCommand';
import { SearchJobsQuery } from '../../../application/queries/SearchJobsQuery';
import { GetStatsQuery } from '../../../application/queries/GetStatsQuery';
import { GetAvailableScrapersQuery } from '../../../application/queries/GetAvailableScrapersQuery';
import { LinkedInScraper } from '../../api/scrapers/LinkedInScraper';
import { IndeedScraper } from '../../api/scrapers/IndeedScraper';
import { ApiJobRepository } from '../../api/ApiJobRepository';

const API_URL = "https://offer-search-production.up.railway.app";
const PAGE_SIZE = 20;

const repository = new ApiJobRepository(API_URL);
const linkedInScraper = new LinkedInScraper();
const indeedScraper = new IndeedScraper();

const scrapeJobsCommand = new ScrapeJobsCommand([linkedInScraper, indeedScraper], repository);
const searchJobsQuery = new SearchJobsQuery(repository);
const getStatsQuery = new GetStatsQuery(repository);
const getAvailableScrapersQuery = new GetAvailableScrapersQuery([linkedInScraper, indeedScraper]);

// Pagination state
let currentPage = 1;
let totalJobs = 0;

document.addEventListener("DOMContentLoaded", () => {
  const btnScrapeLinkedIn = document.getElementById("scrape-linkedin") as HTMLButtonElement;
  const btnRefresh = document.getElementById("refresh") as HTMLButtonElement;
  const btnLoadCache = document.getElementById("load-cache") as HTMLButtonElement;
  const btnPrevPage = document.getElementById("prev-page") as HTMLButtonElement;
  const btnNextPage = document.getElementById("next-page") as HTMLButtonElement;
  const pageInfo = document.getElementById("page-info") as HTMLSpanElement;
  const status = document.getElementById("status") as HTMLDivElement;
  const results = document.getElementById("results") as HTMLDivElement;
  const searchInput = document.getElementById("search") as HTMLInputElement;
  const locationInput = document.getElementById("location") as HTMLInputElement;
  const companyInput = document.getElementById("company") as HTMLInputElement;
  const sourceSelect = document.getElementById("source") as HTMLSelectElement;

  btnScrapeLinkedIn.onclick = async () => {
    btnScrapeLinkedIn.disabled = true;
    btnScrapeLinkedIn.textContent = "Récupération en cours...";
    status.textContent = "Analyse de la page...";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab?.id || !tab.url) {
      status.textContent = "Impossible de récupérer l'URL de l'onglet actif";
      btnScrapeLinkedIn.disabled = false;
      btnScrapeLinkedIn.textContent = "Récupérer les offres";
      return;
    }

    const supportedSources = getAvailableScrapersQuery.getSupportedSources();
    const canScrape = getAvailableScrapersQuery.execute().some(s => s.canScrape(tab.url!));

    if (!canScrape) {
      status.textContent = `Source non supportée. Sources disponibles: ${supportedSources.join(', ')}`;
      btnScrapeLinkedIn.disabled = false;
      btnScrapeLinkedIn.textContent = "Récupérer les offres";
      return;
    }

    try {
      const jobs = await scrapeJobsCommand.execute(tab.url, tab.id);

      if (jobs.length > 0) {
        const stored = await chrome.storage.local.get(['offers']);
        const existingOffers = (stored.offers || []) as Array<any>;

        const offersMap = new Map();
        existingOffers.forEach(job => offersMap.set(job.id, job));
        jobs.forEach(job => offersMap.set(job.id, job));

        const aggregatedOffers = Array.from(offersMap.values());
        const newJobsCount = jobs.length;
        const totalCount = aggregatedOffers.length;

        await chrome.storage.local.set({
          offers: aggregatedOffers,
          lastUpdate: new Date().toLocaleString("fr-FR"),
          total: totalCount
        });

        const newCount = totalCount - existingOffers.length;
        status.textContent = `${newJobsCount} offres scrapées (+${newCount} nouvelles) - Total: ${totalCount}`;
        displayJobs(aggregatedOffers);
      } else {
        status.textContent = "Aucune offre trouvée - scroll la page pour charger plus d'offres";
      }
    } catch (err) {
      console.error(err);
      status.textContent = `Erreur – ${(err as Error).message}`;
    }

    btnScrapeLinkedIn.disabled = false;
    btnScrapeLinkedIn.textContent = "Récupérer les offres";
  };

  btnRefresh.onclick = async () => {
    await searchJobsFromAPI();
    await loadDynamicFilters();
  };

  btnLoadCache.onclick = async () => {
    await loadStoredOffers();
  };

  btnPrevPage.onclick = () => {
    if (currentPage > 1) {
      currentPage--;
      searchJobsFromAPI();
    }
  };

  btnNextPage.onclick = () => {
    const totalPages = Math.ceil(totalJobs / PAGE_SIZE);
    if (currentPage < totalPages) {
      currentPage++;
      searchJobsFromAPI();
    }
  };

  searchInput.addEventListener('input', debounce(() => {
    currentPage = 1;  // Reset to page 1 on filter change
    searchJobsFromAPI();
  }, 500));
  locationInput.addEventListener('input', debounce(() => {
    currentPage = 1;
    searchJobsFromAPI();
  }, 500));
  companyInput.addEventListener('input', debounce(() => {
    currentPage = 1;
    searchJobsFromAPI();
  }, 500));
  sourceSelect.addEventListener('change', () => {
    currentPage = 1;
    searchJobsFromAPI();
  });

  const resetFiltersBtn = document.createElement('button');
  resetFiltersBtn.textContent = 'Réinitialiser les filtres';
  resetFiltersBtn.className = 'btn-secondary';
  resetFiltersBtn.onclick = () => {
    searchInput.value = '';
    locationInput.value = '';
    companyInput.value = '';
    sourceSelect.value = '';
    searchJobsFromAPI();
  };
  document.querySelector('.filters')?.appendChild(resetFiltersBtn);

  async function searchJobsFromAPI() {
    try {
      status.textContent = "Recherche en cours...";

      const offset = (currentPage - 1) * PAGE_SIZE;

      const filters = {
        search: searchInput.value.trim() || undefined,
        location: locationInput.value.trim() || undefined,
        company: companyInput.value.trim() || undefined,
        source: sourceSelect.value || undefined,
        limit: PAGE_SIZE,
        offset: offset
      };

      const response = await fetch(`${API_URL}/api/jobs/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        status.textContent = "Erreur de connexion à l'API";
        loadStoredOffers();
        return;
      }

      const jobs = await response.json();

      // Get total count for pagination (fetch stats)
      const statsResponse = await fetch(`${API_URL}/api/jobs/stats`);
      if (statsResponse.ok) {
        const stats = await statsResponse.json();
        totalJobs = stats.total_jobs;
      }

      // Sync cache with first page if no filters applied
      const hasFilters = filters.search || filters.location || filters.company || filters.source;
      if (!hasFilters && currentPage === 1 && jobs.length > 0) {
        await chrome.storage.local.set({
          offers: jobs,
          lastUpdate: new Date().toLocaleString("fr-FR"),
          total: totalJobs
        });
        console.log(`[Popup] Synced ${jobs.length} jobs (page 1) from API to local cache`);
      }

      updatePaginationUI();

      if (jobs.length > 0) {
        const totalPages = Math.ceil(totalJobs / PAGE_SIZE);
        status.textContent = `${jobs.length} offres (page ${currentPage}/${totalPages}) - Total: ${totalJobs}`;
        displayJobs(jobs);
      } else {
        status.textContent = "Aucune offre trouvée avec ces filtres";
        results.innerHTML = "";
      }
    } catch (err) {
      console.error('Erreur API:', err);
      status.textContent = "API non disponible - chargement du cache local";
      loadStoredOffers();
    }
  }

  function updatePaginationUI() {
    const totalPages = Math.ceil(totalJobs / PAGE_SIZE);
    pageInfo.textContent = `Page ${currentPage}/${totalPages || 1}`;
    btnPrevPage.disabled = currentPage <= 1;
    btnNextPage.disabled = currentPage >= totalPages;
  }

  function displayJobs(jobs: any[]) {
    results.innerHTML = jobs
      .map(
        (j: any) => `
      <div class="offer">
        <h4><a href="${j.url}" target="_blank">${j.title}</a></h4>
        <div class="offer-company">
          ${j.company}
          ${j.source ? `<span class="tag tag-source">${j.source.charAt(0).toUpperCase() + j.source.slice(1)}</span>` : ''}
        </div>
        <div class="tags">
          <span class="tag">${j.location}</span>
          <span class="tag">${j.posted_date || j.postedDate}</span>
        </div>
        ${j.description ? `<div class="offer-description">${j.description}</div>` : ''}
      </div>
    `
      )
      .join("");
  }

  async function loadStoredOffers() {
    try {
      const data = await chrome.storage.local.get(['offers', 'lastUpdate', 'total']);

      if (data.offers && Array.isArray(data.offers) && data.offers.length > 0) {
        status.textContent = `${data.total || data.offers.length} offres en cache (dernière màj: ${data.lastUpdate || 'inconnue'})`;
        displayJobs(data.offers);
      } else {
        status.textContent = "Aucune offre en cache. Va sur LinkedIn ou Indeed et clique sur 'Récupérer les offres'";
        results.innerHTML = "";
      }
    } catch (err) {
      console.error('Erreur lors du chargement des offres:', err);
      status.textContent = "Erreur lors du chargement des offres";
    }
  }

  function formatSourceName(jobSourceName: string): string {
    const sourceNames: Record<string, string> = {
      'linkedin': 'LinkedIn',
      'indeed': 'Indeed',
      'monster': 'Monster',
      'apec': 'APEC',
    };

    return sourceNames[jobSourceName] || jobSourceName;
  }

  function populateSourceFilter(jobsBySource: any[]) {
    sourceSelect.innerHTML = '';

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Toutes les sources';
    sourceSelect.appendChild(defaultOption);

    Object.keys(jobsBySource).forEach((source) => {
      const option = document.createElement('option');
      option.value = source;
      option.textContent = formatSourceName(source);
      sourceSelect.appendChild(option);
    });
  }

  function debounce(func: Function, wait: number) {
    let timeout: number;
    return (...args: any[]) => {
      clearTimeout(timeout);
      timeout = window.setTimeout(() => func(...args), wait);
    };
  }

  async function loadDynamicFilters() {
    try {
      const response = await fetch(`${API_URL}/api/jobs/stats`);

      if (!response.ok) {
        console.error('Failed to load dynamic filters');
        return;
      }

      const stats = await response.json();

      if (stats.jobs_by_source) {
        populateSourceFilter(stats.jobs_by_source);
      }
    } catch (err) {
      console.error('Error loading dynamic filters:', err);
    }
  }

  // Initial state - show welcome message
  status.textContent = "Prêt ! Utilise les boutons ci-dessus pour charger ou scraper des offres.";

  // Load dynamic filters only
  loadDynamicFilters();
});

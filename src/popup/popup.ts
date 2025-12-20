import { JobScraperService } from '../application/services/JobScraperService';
import { LinkedInScraper } from '../infrastructure/secondary/scrapers/LinkedInScraper';
import { ApiJobRepository } from '../infrastructure/secondary/ApiJobRepository';

const API_URL = "http://localhost:8000";

const repository = new ApiJobRepository(API_URL);
const linkedInScraper = new LinkedInScraper();
const scraperService = new JobScraperService([linkedInScraper], repository);

document.addEventListener("DOMContentLoaded", () => {
  const btnScrapeLinkedIn = document.getElementById("scrape-linkedin") as HTMLButtonElement;
  const btnRefresh = document.getElementById("refresh") as HTMLButtonElement;
  const status = document.getElementById("status") as HTMLDivElement;
  const results = document.getElementById("results") as HTMLDivElement;
  const searchInput = document.getElementById("search") as HTMLInputElement;
  const locationInput = document.getElementById("location") as HTMLInputElement;
  const contractSelect = document.getElementById("contract") as HTMLSelectElement;

  btnScrapeLinkedIn.onclick = async () => {
    btnScrapeLinkedIn.disabled = true;
    btnScrapeLinkedIn.textContent = "Récupération en cours...";
    status.textContent = "Analyse de la page...";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab?.id || !tab.url) {
      status.textContent = "⚠️ Impossible de récupérer l'URL de l'onglet actif";
      btnScrapeLinkedIn.disabled = false;
      btnScrapeLinkedIn.textContent = "Récupérer mes offres LinkedIn";
      return;
    }

    const supportedSources = scraperService.getSupportedSources();
    const canScrape = scraperService.getAvailableScrapers().some(s => s.canScrape(tab.url!));

    if (!canScrape) {
      status.textContent = `⚠️ Source non supportée. Sources disponibles: ${supportedSources.join(', ')}`;
      btnScrapeLinkedIn.disabled = false;
      btnScrapeLinkedIn.textContent = "Récupérer mes offres LinkedIn";
      return;
    }

    try {
      const jobs = await scraperService.scrapeCurrentPage(tab.url, tab.id);

      if (jobs.length > 0) {
        await chrome.storage.local.set({
          offers: jobs,
          lastUpdate: new Date().toLocaleString("fr-FR"),
          total: jobs.length
        });

        status.textContent = `✓ ${jobs.length} offres récupérées avec succès !`;
        displayJobs(jobs);
      } else {
        status.textContent = "⚠️ Aucune offre trouvée – scroll la page pour charger plus d'offres";
      }
    } catch (err) {
      console.error(err);
      status.textContent = `Erreur – ${(err as Error).message}`;
    }

    btnScrapeLinkedIn.disabled = false;
    btnScrapeLinkedIn.textContent = "Récupérer mes offres LinkedIn";
  };

  btnRefresh.onclick = async () => {
    await searchJobsFromAPI();
  };

  searchInput.addEventListener('input', debounce(() => searchJobsFromAPI(), 500));
  locationInput.addEventListener('input', debounce(() => searchJobsFromAPI(), 500));
  contractSelect.addEventListener('change', () => searchJobsFromAPI());

  const resetFiltersBtn = document.createElement('button');
  resetFiltersBtn.textContent = 'Réinitialiser les filtres';
  resetFiltersBtn.style.cssText = 'background:#6c757d;margin-top:8px;';
  resetFiltersBtn.onclick = () => {
    searchInput.value = '';
    locationInput.value = '';
    contractSelect.value = '';
    searchJobsFromAPI();
  };
  document.querySelector('.filters')?.appendChild(resetFiltersBtn);

  async function searchJobsFromAPI() {
    try {
      status.textContent = "🔍 Recherche en cours...";

      const filters = {
        search: searchInput.value.trim() || undefined,
        location: locationInput.value.trim() || undefined,
        company: undefined,
        limit: 50,
        offset: 0
      };

      const response = await fetch(`${API_URL}/api/jobs/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        status.textContent = "⚠️ Erreur de connexion à l'API";
        loadStoredOffers();
        return;
      }

      const jobs = await response.json();

      if (jobs.length > 0) {
        status.textContent = `✓ ${jobs.length} offres trouvées`;
        displayJobs(jobs);
      } else {
        status.textContent = "Aucune offre trouvée avec ces filtres";
        results.innerHTML = "";
      }
    } catch (err) {
      console.error('Erreur API:', err);
      status.textContent = "⚠️ API non disponible - chargement du cache local";
      loadStoredOffers();
    }
  }

  function displayJobs(jobs: any[]) {
    results.innerHTML = jobs
      .map(
        (j: any) => `
      <div class="offer">
        <h4><a href="${j.url}" target="_blank">${j.title}</a></h4>
        <div style="color:#0a66c2;font-weight:500;margin:4px 0;">${j.company}</div>
        <div class="tags">
          <span class="tag">📍 ${j.location}</span>
          <span class="tag">🕒 ${j.posted_date || j.postedDate}</span>
        </div>
        ${j.description ? `<div style="font-size:12px;color:#666;margin-top:6px;">${j.description}</div>` : ''}
      </div>
    `
      )
      .join("");
  }

  async function loadStoredOffers() {
    try {
      const data = await chrome.storage.local.get(['offers', 'lastUpdate', 'total']);

      if (data.offers && Array.isArray(data.offers) && data.offers.length > 0) {
        status.textContent = `📦 ${data.total || data.offers.length} offres en cache (dernière màj: ${data.lastUpdate || 'inconnue'})`;
        displayJobs(data.offers);
      } else {
        status.textContent = "Aucune offre en cache. Va sur LinkedIn Jobs et clique sur 'Récupérer mes offres'";
        results.innerHTML = "";
      }
    } catch (err) {
      console.error('Erreur lors du chargement des offres:', err);
      status.textContent = "Erreur lors du chargement des offres";
    }
  }

  function debounce(func: Function, wait: number) {
    let timeout: number;
    return (...args: any[]) => {
      clearTimeout(timeout);
      timeout = window.setTimeout(() => func(...args), wait);
    };
  }

  searchJobsFromAPI();
});
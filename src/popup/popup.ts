document.addEventListener("DOMContentLoaded", () => {
  const btnScrapeLinkedIn = document.getElementById("scrape-linkedin") as HTMLButtonElement;
  const btnRefresh = document.getElementById("refresh") as HTMLButtonElement;
  const status = document.getElementById("status") as HTMLDivElement;
  const results = document.getElementById("results") as HTMLDivElement;

  btnScrapeLinkedIn.onclick = async () => {
    btnScrapeLinkedIn.disabled = true;
    btnScrapeLinkedIn.textContent = "Récupération en cours...";
    status.textContent = "Analyse de la page LinkedIn...";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab?.id || !(tab.url?.includes("linkedin.com/jobs") || tab.url?.includes("linkedin.com/jobs/collections"))) {
      status.textContent = "⚠️ Va sur LinkedIn Emplois d'abord (linkedin.com/jobs)";
      btnScrapeLinkedIn.disabled = false;
      btnScrapeLinkedIn.textContent = "Récupérer mes offres LinkedIn";
      return;
    }

    try {
      const response = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          interface Job {
            id: string;
            title: string;
            company: string;
            location: string;
            url: string;
            postedDate: string;
            description: string;
            scrapedAt: string;
          }

          const jobs: Job[] = [];

          const cardSelectors = [
            'li[data-occludable-job-id]',
            'div.scaffold-layout__list-container li',
            '.job-card-container',
            '.jobs-search-results__list-item',
            'ul.scaffold-layout__list-container > li'
          ];

          let cards: NodeListOf<Element> | null = null;
          for (const selector of cardSelectors) {
            const found = document.querySelectorAll(selector);
            if (found.length > 0) {
              cards = found;
              console.log(`[Offer Search] Utilisation du sélecteur: ${selector}`);
              break;
            }
          }

          if (!cards || cards.length === 0) {
            console.error('[Offer Search] Aucune carte trouvée avec les sélecteurs disponibles');
            return [];
          }

          console.log(`[Offer Search] ${cards.length} cartes d'offres détectées`);

          cards.forEach((card: Element) => {
            const link = card.querySelector(
              'a.job-card-container__link, ' +
              'a.base-card__full-link, ' +
              'a[href*="/jobs/view/"], ' +
              'a.job-card-list__title, ' +
              'a[data-tracking-control-name*="job"], ' +
              'div.artdeco-entity-lockup a'
            ) as HTMLAnchorElement | null;

            if (!link) {
              console.log('[Offer Search] Pas de lien trouvé pour cette carte');
              return;
            }

            const titleEl = card.querySelector(
              'h3.base-search-card__title, ' +
              '.job-card-list__title strong, ' +
              'strong.job-card-list__title, ' +
              '.artdeco-entity-lockup__title, ' +
              'a[href*="/jobs/view/"] strong, ' +
              'div[class*="job-card"] strong, ' +
              'h3, h4'
            ) as HTMLElement | null;

            if (!titleEl?.innerText.trim()) {
              console.log('[Offer Search] Pas de titre trouvé pour cette carte');
              return;
            }

            const companyEl = card.querySelector(
              '.base-search-card__subtitle, ' +
              'h4.base-search-card__subtitle, ' +
              '.artdeco-entity-lockup__subtitle, ' +
              '.job-card-container__company-name, ' +
              'div[class*="subtitle"] span, ' +
              'a.hidden-nested-link'
            ) as HTMLElement | null;

            const locationEl = card.querySelector(
              '.job-search-card__location, ' +
              '.artdeco-entity-lockup__caption, ' +
              'span[class*="location"], ' +
              '.job-card-container__metadata-item'
            ) as HTMLElement | null;

            const dateEl = card.querySelector(
              'time, ' +
              '.job-search-card__listdate, ' +
              '[class*="job-card"]  time, ' +
              'span[class*="date"]'
            ) as HTMLElement | null;

            const descEl = card.querySelector(
              '.base-search-card__metadata, ' +
              '.job-card-container__metadata-wrapper, ' +
              '[class*="snippet"]'
            ) as HTMLElement | null;

            const occludableId = (card as HTMLElement).dataset?.occludableJobId;
            const urlIdMatch = link.href.match(/currentJobId=(\d+)/) ||
                              link.href.match(/jobs\/view\/(\d+)/) ||
                              link.href.match(/jobPosting:(\d+)/);
            const jobId = occludableId ||
                          urlIdMatch?.[1] ||
                          `job-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;

            console.log(`[Offer Search] Offre trouvée: ${titleEl.innerText.trim()} - ID: ${jobId}`);

            jobs.push({
              id: jobId,
              title: titleEl.innerText.trim(),
              company: companyEl?.innerText.trim() || "Entreprise non spécifiée",
              location: locationEl?.innerText.trim() || "Localisation non précisée",
              url: link.href.split('?')[0],
              postedDate: dateEl?.getAttribute('datetime') || dateEl?.innerText.trim() || "Date inconnue",
              description: descEl?.innerText.trim() || "",
              scrapedAt: new Date().toISOString()
            });
          });

          console.log(`[Offer Search] ${jobs.length} offres extraites avec succès`);
          return jobs;
        }
      });

      const jobs = response[0].result || [];

      if (jobs.length > 0) {
        await chrome.storage.local.set({
          offers: jobs,
          lastUpdate: new Date().toLocaleString("fr-FR"),
          total: jobs.length
        });

        status.textContent = `✓ ${jobs.length} offres récupérées avec succès !`;
        results.innerHTML = jobs
          .map(
            (j: any) => `
          <div class="offer">
            <h4><a href="${j.url}" target="_blank">${j.title}</a></h4>
            <div style="color:#0a66c2;font-weight:500;margin:4px 0;">${j.company}</div>
            <div class="tags">
              <span class="tag">📍 ${j.location}</span>
              <span class="tag">🕒 ${j.postedDate}</span>
            </div>
            ${j.description ? `<div style="font-size:12px;color:#666;margin-top:6px;">${j.description}</div>` : ''}
          </div>
        `
          )
          .join("");
      } else {
        status.textContent = "⚠️ Aucune offre trouvée – scroll la page pour charger plus d'offres";
      }
    } catch (err) {
      console.error(err);
      status.textContent = "Erreur – vérifie que tu es sur LinkedIn Jobs";
    }

    btnScrapeLinkedIn.disabled = false;
    btnScrapeLinkedIn.textContent = "Récupérer mes offres LinkedIn";
  };

  btnRefresh.onclick = async () => {
    loadStoredOffers();
  };

  async function loadStoredOffers() {
    try {
      const data = await chrome.storage.local.get(['offers', 'lastUpdate', 'total']);

      if (data.offers && Array.isArray(data.offers) && data.offers.length > 0) {
        status.textContent = `📦 ${data.total || data.offers.length} offres en cache (dernière màj: ${data.lastUpdate || 'inconnue'})`;
        results.innerHTML = data.offers
          .map(
            (j: any) => `
          <div class="offer">
            <h4><a href="${j.url}" target="_blank">${j.title}</a></h4>
            <div style="color:#0a66c2;font-weight:500;margin:4px 0;">${j.company}</div>
            <div class="tags">
              <span class="tag">📍 ${j.location}</span>
              <span class="tag">🕒 ${j.postedDate}</span>
            </div>
            ${j.description ? `<div style="font-size:12px;color:#666;margin-top:6px;">${j.description}</div>` : ''}
          </div>
        `
          )
          .join("");
      } else {
        status.textContent = "Aucune offre en cache. Va sur LinkedIn Jobs et clique sur 'Récupérer mes offres'";
        results.innerHTML = "";
      }
    } catch (err) {
      console.error('Erreur lors du chargement des offres:', err);
      status.textContent = "Erreur lors du chargement des offres";
    }
  }

  loadStoredOffers();
});
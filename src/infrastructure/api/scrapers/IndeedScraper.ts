import { IJobScraper, ScraperSelectors } from '../../../domain/ports/IJobScraper';
import { Job, JobSource } from '../../../domain/entities/Job';

export class IndeedScraper implements IJobScraper {
  readonly source = JobSource.INDEED;

  private selectors: ScraperSelectors = {
    cardContainer: [
      '.cardOutline.tapItem',
      'div[class*="result job_"]',
      'div.job_seen_beacon',
      '.slider_container .slider_item',
      'div[data-jk]'
    ],
    link: [
      'a.jcs-JobTitle',
      'h2.jobTitle a',
      'a[data-jk]',
      'a[id^="job_"]',
      'a[href*="/viewjob"]',
      'a[href*="/rc/clk"]'
    ],
    title: [
      'a.jcs-JobTitle span',
      'h2.jobTitle a span',
      'span[title]',
      'h2.jobTitle span',
      '.jcs-JobTitle span'
    ],
    company: [
      'span[data-testid="company-name"]',
      'span.css-1h7lukg',
      '[data-testid="company-name"]',
      '.companyName',
      'span.company'
    ],
    location: [
      'div[data-testid="text-location"]',
      '.css-1p0sjhy',
      '[data-testid="text-location"]',
      '.companyLocation',
      'div.location'
    ],
    date: [
      'span[data-testid="myJobsStateDate"]',
      'span.date',
      '.css-qvloho',
      'span.css-kyg8or'
    ],
    description: [
      'div.job-snippet',
      'div[class*="snippet"]',
      '.jobCardShelfContainer ul',
      'ul.css-1dvlnfr',
      '.jobMetaDataGroup'
    ]
  };

  canScrape(url: string): boolean {
    return url.includes('indeed.com/jobs') || url.includes('indeed.fr/jobs');
  }

  getSourceName(): string {
    return 'Indeed';
  }

  async scrape(tabId: number): Promise<Job[]> {
    console.log('[IndeedScraper] Starting scrape for tabId:', tabId);

    try {
      const response = await chrome.scripting.executeScript({
        target: { tabId },
        func: (selectors: ScraperSelectors, source: JobSource) => {
          const jobs: any[] = [];

          console.log('[Offer Search] ===== DÉBUT DU SCRAPING INDEED =====');
          console.log('[Offer Search] URL:', window.location.href);
          console.log('[Offer Search] Tentative de détection des cartes d\'offres Indeed...');

          let cards: NodeListOf<Element> | null = null;
          let usedSelector = '';

          for (const selector of selectors.cardContainer) {
            const found = document.querySelectorAll(selector);
            console.log(`[Offer Search] Sélecteur testé: "${selector}" - ${found.length} éléments trouvés`);
            if (found.length > 0) {
              cards = found;
              usedSelector = selector;
              console.log(`[Offer Search] Sélecteur retenu: ${selector}`);
              break;
            }
          }

          if (!cards || cards.length === 0) {
            console.error('[Offer Search] AUCUNE CARTE TROUVÉE');
            console.log('[Offer Search] Structure HTML actuelle:', document.body.innerHTML.substring(0, 500));
            return [];
          }

          console.log(`[Offer Search] ${cards.length} cartes détectées avec "${usedSelector}"`);

          const querySelector = (parent: Element, selectors: string[]): Element | null => {
            for (const selector of selectors) {
              const element = parent.querySelector(selector);
              if (element) return element;
            }
            return null;
          };

          cards.forEach((card: Element, index: number) => {
            const link = querySelector(card, selectors.link) as HTMLAnchorElement | null;
            if (!link) {
              console.log(`[Offer Search] Carte ${index}: Pas de lien trouvé`);
              return;
            }

            const titleEl = querySelector(card, selectors.title) as HTMLElement | null;
            if (!titleEl?.innerText.trim()) {
              console.log(`[Offer Search] Carte ${index}: Pas de titre trouvé`);
              return;
            }

            const companyEl = querySelector(card, selectors.company) as HTMLElement | null;
            const locationEl = querySelector(card, selectors.location) as HTMLElement | null;
            const dateEl = querySelector(card, selectors.date) as HTMLElement | null;
            const descEl = querySelector(card, selectors.description) as HTMLElement | null;

            // Extract job ID from data-jk attribute or from class name
            const dataJk = (card as HTMLElement).dataset?.jk;
            const classMatch = card.className.match(/job_([a-zA-Z0-9]+)/);
            const urlIdMatch = link.href.match(/jk=([a-zA-Z0-9]+)/);

            const jobId = dataJk ||
                          classMatch?.[1] ||
                          urlIdMatch?.[1] ||
                          `${source}-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;

            console.log(`[Offer Search] Offre ${index} trouvée: ${titleEl.innerText.trim()} - ID: ${jobId}`);

            // Build full URL if relative
            let fullUrl = link.href;
            if (!fullUrl.startsWith('http')) {
              fullUrl = new URL(link.href, window.location.origin).href;
            }

            jobs.push({
              id: jobId,
              title: titleEl.innerText.trim(),
              company: companyEl?.innerText.trim() || "Entreprise non spécifiée",
              location: locationEl?.innerText.trim() || "Localisation non précisée",
              url: fullUrl,  // Keep full URL with query params for Indeed (jk= param is essential)
              postedDate: dateEl?.innerText.trim() || "Date inconnue",
              description: descEl?.innerText.trim() || "",
              scrapedAt: new Date().toISOString(),
              source: source
            });
          });

          console.log(`[Offer Search] ${jobs.length} offres Indeed extraites`);
          return jobs;
        },
        args: [this.selectors, this.source]
      });

      console.log('[IndeedScraper] Script execution response:', response);
      const result = response[0]?.result || [];
      console.log('[IndeedScraper] Extracted jobs count:', result.length);

      return result;
    } catch (error) {
      console.error('[IndeedScraper] Error during script execution:', error);
      throw error;
    }
  }
}

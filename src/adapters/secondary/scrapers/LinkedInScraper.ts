import { IJobScraper, ScraperSelectors } from '../../../domain/ports/IJobScraper';
import { Job, JobSource } from '../../../domain/entities/Job';

export class LinkedInScraper implements IJobScraper {
  readonly source = JobSource.LINKEDIN;

  private selectors: ScraperSelectors = {
    cardContainer: [
      'li[data-occludable-job-id]',
      'div.scaffold-layout__list-container li',
      '.job-card-container',
      '.jobs-search-results__list-item',
      'ul.scaffold-layout__list-container > li'
    ],
    link: [
      'a.job-card-container__link',
      'a.base-card__full-link',
      'a[href*="/jobs/view/"]',
      'a.job-card-list__title',
      'a[data-tracking-control-name*="job"]',
      'div.artdeco-entity-lockup a'
    ],
    title: [
      'h3.base-search-card__title',
      '.job-card-list__title strong',
      'strong.job-card-list__title',
      '.artdeco-entity-lockup__title',
      'a[href*="/jobs/view/"] strong',
      'div[class*="job-card"] strong',
      'h3', 'h4'
    ],
    company: [
      '.base-search-card__subtitle',
      'h4.base-search-card__subtitle',
      '.artdeco-entity-lockup__subtitle',
      '.job-card-container__company-name',
      'div[class*="subtitle"] span',
      'a.hidden-nested-link'
    ],
    location: [
      '.job-search-card__location',
      '.artdeco-entity-lockup__caption',
      'span[class*="location"]',
      '.job-card-container__metadata-item'
    ],
    date: [
      'time',
      '.job-search-card__listdate',
      '[class*="job-card"] time',
      'span[class*="date"]'
    ],
    description: [
      '.base-search-card__metadata',
      '.job-card-container__metadata-wrapper',
      '[class*="snippet"]'
    ]
  };

  canScrape(url: string): boolean {
    return url.includes('linkedin.com/jobs');
  }

  getSourceName(): string {
    return 'LinkedIn';
  }

  async scrape(tabId: number): Promise<Job[]> {
    const response = await chrome.scripting.executeScript({
      target: { tabId },
      func: this.extractJobsFromPage,
      args: [this.selectors, this.source]
    });

    return response[0].result || [];
  }

  private extractJobsFromPage(selectors: ScraperSelectors, source: JobSource): Job[] {
    const jobs: Job[] = [];

    let cards: NodeListOf<Element> | null = null;
    for (const selector of selectors.cardContainer) {
      const found = document.querySelectorAll(selector);
      if (found.length > 0) {
        cards = found;
        console.log(`[Offer Search] Utilisation du sélecteur: ${selector}`);
        break;
      }
    }

    if (!cards || cards.length === 0) {
      console.error('[Offer Search] Aucune carte trouvée');
      return [];
    }

    console.log(`[Offer Search] ${cards.length} cartes détectées`);

    cards.forEach((card: Element) => {
      const link = this.querySelector(card, selectors.link) as HTMLAnchorElement | null;
      if (!link) {
        console.log('[Offer Search] Pas de lien trouvé');
        return;
      }

      const titleEl = this.querySelector(card, selectors.title) as HTMLElement | null;
      if (!titleEl?.innerText.trim()) {
        console.log('[Offer Search] Pas de titre trouvé');
        return;
      }

      const companyEl = this.querySelector(card, selectors.company) as HTMLElement | null;
      const locationEl = this.querySelector(card, selectors.location) as HTMLElement | null;
      const dateEl = this.querySelector(card, selectors.date) as HTMLElement | null;
      const descEl = this.querySelector(card, selectors.description) as HTMLElement | null;

      const occludableId = (card as HTMLElement).dataset?.occludableJobId;
      const urlIdMatch = link.href.match(/currentJobId=(\d+)/) ||
                        link.href.match(/jobs\/view\/(\d+)/) ||
                        link.href.match(/jobPosting:(\d+)/);
      const jobId = occludableId ||
                    urlIdMatch?.[1] ||
                    `${source}-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;

      console.log(`[Offer Search] Offre trouvée: ${titleEl.innerText.trim()} - ID: ${jobId}`);

      jobs.push({
        id: jobId,
        title: titleEl.innerText.trim(),
        company: companyEl?.innerText.trim() || "Entreprise non spécifiée",
        location: locationEl?.innerText.trim() || "Localisation non précisée",
        url: link.href.split('?')[0],
        postedDate: dateEl?.getAttribute('datetime') || dateEl?.innerText.trim() || "Date inconnue",
        description: descEl?.innerText.trim() || "",
        scrapedAt: new Date().toISOString(),
        source: source
      });
    });

    console.log(`[Offer Search] ${jobs.length} offres extraites`);
    return jobs;
  }

  private querySelector(parent: Element, selectors: string[]): Element | null {
    for (const selector of selectors) {
      const element = parent.querySelector(selector);
      if (element) return element;
    }
    return null;
  }
}

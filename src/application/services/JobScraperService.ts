import { IJobScraper } from '../../domain/ports/IJobScraper';
import { IJobRepository } from '../../domain/ports/IJobRepository';
import { Job, JobFilter } from '../../domain/entities/Job';

export class JobScraperService {
  private scrapers: Map<string, IJobScraper> = new Map();

  constructor(
    scrapers: IJobScraper[],
    private repository: IJobRepository
  ) {
    scrapers.forEach(scraper => {
      this.scrapers.set(scraper.source, scraper);
    });
  }

  async scrapeCurrentPage(url: string, tabId: number): Promise<Job[]> {
    console.log('[JobScraperService] scrapeCurrentPage called with:', { url, tabId });

    const scraper = this.findScraperForUrl(url);

    if (!scraper) {
      console.error('[JobScraperService] No scraper found for URL:', url);
      throw new Error(`No scraper found for URL: ${url}`);
    }

    console.log(`[JobScraperService] Using ${scraper.getSourceName()} scraper`);
    console.log('[JobScraperService] About to call scraper.scrape() with tabId:', tabId);

    const jobs = await scraper.scrape(tabId);

    console.log('[JobScraperService] scraper.scrape() returned', jobs.length, 'jobs');

    if (jobs.length > 0) {
      try {
        const result = await this.repository.submitJobs(jobs);
        console.log(`[JobScraperService] Submitted: ${result.inserted} new, ${result.duplicates} duplicates`);
      } catch (error) {
        console.error('[JobScraperService] Failed to submit jobs to API:', error);
      }
    }

    return jobs;
  }

  async searchJobs(filters: JobFilter): Promise<Job[]> {
    try {
      return await this.repository.searchJobs(filters);
    } catch (error) {
      console.error('[JobScraperService] Search failed:', error);
      throw error;
    }
  }

  async getStats() {
    return await this.repository.getStats();
  }

  private findScraperForUrl(url: string): IJobScraper | undefined {
    return Array.from(this.scrapers.values()).find(scraper => scraper.canScrape(url));
  }

  getAvailableScrapers(): IJobScraper[] {
    return Array.from(this.scrapers.values());
  }

  getSupportedSources(): string[] {
    return Array.from(this.scrapers.values()).map(s => s.getSourceName());
  }
}

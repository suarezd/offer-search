import { IJobScraper } from '../../domain/ports/IJobScraper';
import { IJobRepository } from '../../domain/ports/IJobRepository';
import { Job } from '../../domain/entities/Job';

export class ScrapeJobsCommand {
  private scrapers: Map<string, IJobScraper> = new Map();

  constructor(
    scrapers: IJobScraper[],
    private repository: IJobRepository
  ) {
    scrapers.forEach(scraper => {
      this.scrapers.set(scraper.source, scraper);
    });
  }

  async execute(url: string, tabId: number): Promise<Job[]> {
    console.log('[ScrapeJobsCommand] Executing with:', { url, tabId });

    const scraper = this.findScraperForUrl(url);

    if (!scraper) {
      console.error('[ScrapeJobsCommand] No scraper found for URL:', url);
      throw new Error(`No scraper found for URL: ${url}`);
    }

    console.log(`[ScrapeJobsCommand] Using ${scraper.getSourceName()} scraper`);
    console.log('[ScrapeJobsCommand] About to call scraper.scrape() with tabId:', tabId);

    const jobs = await scraper.scrape(tabId);

    console.log('[ScrapeJobsCommand] Scraper returned', jobs.length, 'jobs');

    if (jobs.length > 0) {
      console.log('[ScrapeJobsCommand] Starting API submission...');
      try {
        console.log('[ScrapeJobsCommand] Calling repository.submitJobs() with', jobs.length, 'jobs');
        const result = await this.repository.submitJobs(jobs);
        console.log('[ScrapeJobsCommand] submitJobs() returned result:', result);
        console.log(`[ScrapeJobsCommand] Submitted: ${result.inserted} new, ${result.duplicates} duplicates`);
      } catch (error) {
        console.error('[ScrapeJobsCommand] Failed to submit jobs to API:', error);
        console.error('[ScrapeJobsCommand] Error details:', error instanceof Error ? error.message : String(error));
        console.error('[ScrapeJobsCommand] Error stack:', error instanceof Error ? error.stack : 'No stack trace');
      }
    } else {
      console.log('[ScrapeJobsCommand] No jobs to submit (jobs.length = 0)');
    }

    return jobs;
  }

  private findScraperForUrl(url: string): IJobScraper | undefined {
    return Array.from(this.scrapers.values()).find(scraper => scraper.canScrape(url));
  }
}

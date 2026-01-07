import { IJobScraper } from '../../domain/ports/IJobScraper';

export class GetAvailableScrapersQuery {
  private scrapers: Map<string, IJobScraper> = new Map();

  constructor(scrapers: IJobScraper[]) {
    scrapers.forEach(scraper => {
      this.scrapers.set(scraper.source, scraper);
    });
  }

  execute(): IJobScraper[] {
    console.log('[GetAvailableScrapersQuery] Executing');
    const scrapers = Array.from(this.scrapers.values());
    console.log('[GetAvailableScrapersQuery] Found', scrapers.length, 'scrapers');
    return scrapers;
  }

  getSupportedSources(): string[] {
    const sources = Array.from(this.scrapers.values()).map(s => s.getSourceName());
    console.log('[GetAvailableScrapersQuery] Supported sources:', sources);
    return sources;
  }
}

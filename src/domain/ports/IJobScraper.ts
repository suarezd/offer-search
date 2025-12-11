import { Job, JobSource } from '../entities/Job';

export interface IJobScraper {
  readonly source: JobSource;

  canScrape(url: string): boolean;

  scrape(tabId: number): Promise<Job[]>;

  getSourceName(): string;
}

export interface ScraperSelectors {
  cardContainer: string[];
  link: string[];
  title: string[];
  company: string[];
  location: string[];
  date: string[];
  description: string[];
}

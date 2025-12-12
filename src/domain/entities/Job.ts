export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  url: string;
  postedDate: string;
  description: string;
  scrapedAt: string;
  source: JobSource;
}

export enum JobSource {
  LINKEDIN = 'linkedin',
  INDEED = 'indeed',
  LEBONCOIN = 'leboncoin',
  WELCOME_TO_THE_JUNGLE = 'welcome_to_the_jungle',
  MONSTER = 'monster',
  APEC = 'apec'
}

export interface JobFilter {
  search?: string;
  location?: string;
  company?: string;
  source?: JobSource;
  limit?: number;
  offset?: number;
}

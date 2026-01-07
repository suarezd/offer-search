import { IJobRepository } from '../../domain/ports/IJobRepository';
import { Job, JobFilter } from '../../domain/entities/Job';

export class SearchJobsQuery {
  constructor(private repository: IJobRepository) {}

  async execute(filters: JobFilter): Promise<Job[]> {
    console.log('[SearchJobsQuery] Executing with filters:', filters);

    try {
      const jobs = await this.repository.searchJobs(filters);
      console.log('[SearchJobsQuery] Found', jobs.length, 'jobs');
      return jobs;
    } catch (error) {
      console.error('[SearchJobsQuery] Search failed:', error);
      throw error;
    }
  }
}

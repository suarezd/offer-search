import { IJobRepository, SubmitResult } from '../../domain/ports/IJobRepository';
import { Job } from '../../domain/entities/Job';

export class SubmitJobsCommand {
  constructor(private repository: IJobRepository) {}

  async execute(jobs: Job[]): Promise<SubmitResult> {
    console.log('[SubmitJobsCommand] Executing with', jobs.length, 'jobs');

    try {
      const result = await this.repository.submitJobs(jobs);
      console.log('[SubmitJobsCommand] Submitted:', result.inserted, 'new,', result.duplicates, 'duplicates');
      return result;
    } catch (error) {
      console.error('[SubmitJobsCommand] Failed to submit jobs:', error);
      throw error;
    }
  }
}

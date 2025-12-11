import { Job, JobFilter } from '../entities/Job';

export interface IJobRepository {
  submitJobs(jobs: Job[]): Promise<SubmitResult>;

  searchJobs(filters: JobFilter): Promise<Job[]>;

  getStats(): Promise<JobStats>;
}

export interface SubmitResult {
  success: boolean;
  inserted: number;
  duplicates: number;
  total: number;
}

export interface JobStats {
  total_jobs: number;
  total_companies: number;
  total_locations: number;
  jobs_by_source?: Record<string, number>;
}

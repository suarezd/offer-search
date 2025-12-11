import { IJobRepository, SubmitResult, JobStats } from '../../domain/ports/IJobRepository';
import { Job, JobFilter } from '../../domain/entities/Job';

export class ApiJobRepository implements IJobRepository {
  constructor(private apiUrl: string) {}

  async submitJobs(jobs: Job[]): Promise<SubmitResult> {
    try {
      const response = await fetch(`${this.apiUrl}/api/jobs/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jobs })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting jobs:', error);
      throw error;
    }
  }

  async searchJobs(filters: JobFilter): Promise<Job[]> {
    try {
      const response = await fetch(`${this.apiUrl}/api/jobs/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error searching jobs:', error);
      throw error;
    }
  }

  async getStats(): Promise<JobStats> {
    try {
      const response = await fetch(`${this.apiUrl}/api/jobs/stats`);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  }
}

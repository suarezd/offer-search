import { IJobRepository, SubmitResult, JobStats } from '../../domain/ports/IJobRepository';
import { Job, JobFilter } from '../../domain/entities/Job';

export class ApiJobRepository implements IJobRepository {
  constructor(private apiUrl: string) {}

  async submitJobs(jobs: Job[]): Promise<SubmitResult> {
    console.log('[ApiJobRepository] submitJobs() called with', jobs.length, 'jobs');
    console.log('[ApiJobRepository] API URL:', this.apiUrl);

    try {
      const url = `${this.apiUrl}/api/jobs/submit`;
      console.log('[ApiJobRepository] Sending POST request to:', url);
      console.log('[ApiJobRepository] Request body:', { jobs: jobs.slice(0, 2) }); // Log first 2 jobs only

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jobs })
      });

      console.log('[ApiJobRepository] Response received - Status:', response.status, response.statusText);
      console.log('[ApiJobRepository] Response OK?:', response.ok);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[ApiJobRepository] Error response body:', errorText);
        throw new Error(`API error: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      console.log('[ApiJobRepository] Parsed response:', result);
      return result;
    } catch (error) {
      console.error('[ApiJobRepository] Exception during submitJobs:', error);
      console.error('[ApiJobRepository] Error type:', error?.constructor?.name);
      console.error('[ApiJobRepository] Error message:', error instanceof Error ? error.message : String(error));
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

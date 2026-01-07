import { IJobRepository, JobStats } from '../../domain/ports/IJobRepository';

export class GetStatsQuery {
  constructor(private repository: IJobRepository) {}

  async execute(): Promise<JobStats> {
    console.log('[GetStatsQuery] Executing');

    try {
      const stats = await this.repository.getStats();
      console.log('[GetStatsQuery] Stats retrieved:', stats);
      return stats;
    } catch (error) {
      console.error('[GetStatsQuery] Failed to get stats:', error);
      throw error;
    }
  }
}

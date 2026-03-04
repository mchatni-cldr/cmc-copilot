import axios from 'axios';
import { InvestigationStatus } from '@/types/agent.types';
import { BatchInfo } from '@/types/domain.types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Get batch information
  getBatchInfo: async (): Promise<BatchInfo> => {
    const response = await api.get('/batch-info');
    return response.data;
  },

  // Start investigation
  startInvestigation: async (batchId: string) => {
    const response = await api.post('/investigation/start', { batch_id: batchId });
    return response.data;
  },

  // Get investigation status
  getInvestigationStatus: async (investigationId: string): Promise<InvestigationStatus> => {
    const response = await api.get(`/investigation/${investigationId}/status`);
    return response.data;
  },

  // Get investigation report
  getInvestigationReport: async (investigationId: string) => {
    const response = await api.get(`/investigation/${investigationId}/report`);
    return response.data;
  },

  // Poll investigation status (helper function)
  pollInvestigationStatus: async (
    investigationId: string,
    onUpdate: (status: InvestigationStatus) => void,
    intervalMs: number = 2000
  ): Promise<void> => {
    const poll = async () => {
      try {
        const status = await apiService.getInvestigationStatus(investigationId);
        onUpdate(status);

        if (status.status === 'complete' || status.status === 'error') {
          return; // Stop polling
        }

        setTimeout(poll, intervalMs);
      } catch (error) {
        console.error('Error polling investigation status:', error);
        setTimeout(poll, intervalMs); // Continue polling on error
      }
    };

    await poll();
  },
};
import { useState, useEffect } from 'react';
import { Play, AlertCircle, Lightbulb, BarChart3, FileText } from 'lucide-react';
import { apiService } from '@/services/api';
import { InvestigationStatus, StatusEnum } from '@/types/agent.types';
import { BatchInfo } from '@/types/domain.types';
import AgentStatusCard from './AgentStatusCard';
import OutputViewer from './OutputViewer';

export default function Dashboard() {
  const [batchInfo, setBatchInfo] = useState<BatchInfo | null>(null);
  const [investigating, setInvestigating] = useState(false);
  const [investigationId, setInvestigationId] = useState<string | null>(null);
  const [investigationStatus, setInvestigationStatus] = useState<InvestigationStatus | null>(null);
  const [showResults, setShowResults] = useState(false);

  // Agent configurations
  const agentConfigs = [
    { id: 'agent1', icon: <BarChart3 className="w-6 h-6 text-purple-600" />, color: 'purple' as const },
    { id: 'agent2', icon: <Lightbulb className="w-6 h-6 text-emerald-600" />, color: 'emerald' as const },
    { id: 'agent3', icon: <FileText className="w-6 h-6 text-blue-600" />, color: 'blue' as const },
  ];

  // Load batch info on mount
  useEffect(() => {
    loadBatchInfo();
  }, []);

  const loadBatchInfo = async () => {
    try {
      const data = await apiService.getBatchInfo();
      setBatchInfo(data);
    } catch (error) {
      console.error('Error loading batch info:', error);
    }
  };

  const startInvestigation = async () => {
    if (!batchInfo) return;

    setInvestigating(true);
    setShowResults(false);
    setInvestigationStatus(null);

    try {
      const response = await apiService.startInvestigation(batchInfo.batch_id);
      setInvestigationId(response.investigation_id);

      // Start polling for status updates
      apiService.pollInvestigationStatus(response.investigation_id, (status) => {
        setInvestigationStatus(status);

        if (status.status === StatusEnum.COMPLETE) {
          setShowResults(true);
          setInvestigating(false);
        }
      });
    } catch (error) {
      console.error('Error starting investigation:', error);
      setInvestigating(false);
    }
  };

  const resetDemo = () => {
    setInvestigating(false);
    setInvestigationId(null);
    setInvestigationStatus(null);
    setShowResults(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-gray-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
                <Lightbulb className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">CMC Co-Pilot</h1>
                <p className="text-sm text-gray-600">Automated Batch Deviation Analysis | Powered by Cloudera AI</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-700">System Active</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 lg:px-8 py-8 space-y-6">
        {/* Batch Information */}
        {batchInfo && (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
            <div className="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">Batch Information</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="space-y-1">
                  <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Batch ID</p>
                  <p className="text-2xl font-bold text-gray-900">{batchInfo.batch_id}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Product</p>
                  <p className="text-2xl font-bold text-gray-900">{batchInfo.product}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</p>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                    <span className="text-2xl font-bold text-red-600">{batchInfo.status}</span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-red-50 to-red-50/50 border-2 border-red-200 rounded-xl p-5">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <AlertCircle className="w-6 h-6 text-red-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-base font-bold text-red-900 mb-2">Out-of-Specification Result Detected</h3>
                    <p className="text-sm text-red-800 leading-relaxed">{batchInfo.qc_failure_description}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Investigation Control */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex-1">
              <h3 className="text-xl font-bold text-gray-900 mb-2">Root Cause Investigation</h3>
              <p className="text-sm text-gray-600">
                Deploy AI agents to automatically analyze sensor data, material logs, and scientific literature
              </p>
            </div>
            <button
              onClick={startInvestigation}
              disabled={investigating || showResults}
              className={`px-8 py-4 rounded-xl font-semibold text-white shadow-lg transition-all duration-200 flex items-center gap-3 ${
                investigating || showResults
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 hover:shadow-xl hover:scale-105'
              }`}
            >
              <Play className="w-5 h-5" />
              <span>{investigating ? 'Investigation Running...' : 'Start Investigation'}</span>
            </button>
          </div>
        </div>

        {/* Agent Progress */}
        {investigationStatus && investigationStatus.agents.length > 0 && (
          <div className="space-y-4 animate-in slide-in-from-top">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
              <div className="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
                <h3 className="text-xl font-bold text-gray-900">Investigation Progress</h3>
              </div>
              <div className="p-6 space-y-4">
                {investigationStatus.agents.map((agent, idx) => (
                  <AgentStatusCard
                    key={agent.agent_id}
                    agent={agent}
                    icon={agentConfigs[idx]?.icon}
                    color={agentConfigs[idx]?.color}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {showResults && investigationStatus?.final_report && (
          <OutputViewer report={investigationStatus.final_report} onReset={resetDemo} />
        )}
      </main>
    </div>
  );
}
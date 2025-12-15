// ============================================================
// FILE: frontend/src/components/AgentStatusCard.tsx (WITH ANIMATIONS)
// ============================================================
import { CheckCircle2, Clock } from 'lucide-react';
import { AgentStatus, StatusEnum } from '@/types/agent.types';

interface AgentStatusCardProps {
  agent: AgentStatus;
  icon: React.ReactNode;
  color: 'purple' | 'emerald' | 'blue';
}

const colorClasses = {
  purple: {
    bg: 'bg-purple-50',
    iconBg: 'bg-purple-100',
    iconText: 'text-purple-600',
    border: 'border-purple-200',
    text: 'text-purple-900',
    glow: 'shadow-purple-200',
  },
  emerald: {
    bg: 'bg-emerald-50',
    iconBg: 'bg-emerald-100',
    iconText: 'text-emerald-600',
    border: 'border-emerald-200',
    text: 'text-emerald-900',
    glow: 'shadow-emerald-200',
  },
  blue: {
    bg: 'bg-blue-50',
    iconBg: 'bg-blue-100',
    iconText: 'text-blue-600',
    border: 'border-blue-200',
    text: 'text-blue-900',
    glow: 'shadow-blue-200',
  },
};

const StatusBadge = ({ status }: { status: StatusEnum }) => {
  const styles = {
    [StatusEnum.PENDING]: 'bg-gray-100 text-gray-600',
    [StatusEnum.RUNNING]: 'bg-amber-100 text-amber-700',
    [StatusEnum.COMPLETE]: 'bg-emerald-100 text-emerald-700',
    [StatusEnum.ERROR]: 'bg-red-100 text-red-700',
  };

  const icons = {
    [StatusEnum.PENDING]: null,
    [StatusEnum.RUNNING]: <Clock className="w-3 h-3 animate-pulse" />,
    [StatusEnum.COMPLETE]: <CheckCircle2 className="w-3 h-3" />,
    [StatusEnum.ERROR]: null,
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 ${styles[status]}`}>
      {icons[status]}
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

export default function AgentStatusCard({ agent, icon, color }: AgentStatusCardProps) {
  const colors = colorClasses[color];

  // Determine card styling based on status
  const getCardClasses = () => {
    if (agent.status === StatusEnum.PENDING) {
      return 'bg-white border-gray-200 opacity-60';
    } else if (agent.status === StatusEnum.RUNNING) {
      return `${colors.bg} ${colors.border} shadow-2xl animate-pulse-glow`;
    } else {
      return `bg-white ${colors.border} shadow-md`;
    }
  };

  return (
    <div
      className={`rounded-xl border-2 transition-all duration-500 ${getCardClasses()}`}
    >
      <div className="p-5">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div 
              className={`w-12 h-12 rounded-xl ${colors.iconBg} flex items-center justify-center shadow-sm transition-all duration-300 ${
                agent.status === StatusEnum.RUNNING ? 'animate-bounce-slow' : ''
              }`}
            >
              {icon}
            </div>
            <div>
              <h4 className={`font-bold text-lg ${colors.text}`}>{agent.agent_name}</h4>
              <p className="text-sm text-gray-600">{agent.role}</p>
            </div>
          </div>
          <StatusBadge status={agent.status} />
        </div>

        {agent.tasks.length > 0 && (
          <div className="space-y-2.5 mt-4 pt-4 border-t border-gray-200">
            {agent.tasks.map((task, idx) => (
              <div 
                key={idx} 
                className="flex items-start gap-2.5 animate-in slide-in-from-top"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-gray-700 leading-relaxed">{task.task_name}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
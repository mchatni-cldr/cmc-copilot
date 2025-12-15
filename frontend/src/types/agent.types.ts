export enum StatusEnum {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETE = 'complete',
  ERROR = 'error',
}

export interface TaskStatus {
  task_name: string;
  status: StatusEnum;
  output?: string;
  started_at?: string;
  completed_at?: string;
}

export interface AgentStatus {
  agent_id: string;
  agent_name: string;
  role: string;
  status: StatusEnum;
  tasks: TaskStatus[];
  started_at?: string;
  completed_at?: string;
}

export interface InvestigationStatus {
  investigation_id: string;
  status: StatusEnum;
  agents: AgentStatus[];
  started_at: string;
  completed_at?: string;
  final_report?: any;
}
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from models.status_model import InvestigationStatus, AgentStatus, TaskStatus, StatusEnum
from agents.crew_setup import create_investigation_crew
import threading

class InvestigationService:
    def __init__(self):
        self.investigations: Dict[str, InvestigationStatus] = {}
        
    def start_investigation(self, batch_id: str) -> str:
        """Start a new batch deviation investigation"""
        investigation_id = str(uuid.uuid4())
        
        # Initialize investigation status
        investigation = InvestigationStatus(
            investigation_id=investigation_id,
            status=StatusEnum.RUNNING,
            started_at=datetime.now(),
            agents=[]
        )
        
        self.investigations[investigation_id] = investigation
        
        # Start the crew in background thread
        def run_investigation():
            try:
                crew = create_investigation_crew(
                    investigation_id,
                    self._update_status
                )
                result = crew.kickoff()
                
                # Update with final report
                self.investigations[investigation_id].final_report = result
                self.investigations[investigation_id].status = StatusEnum.COMPLETE
                self.investigations[investigation_id].completed_at = datetime.now()
                
                # Mark all agents as complete
                for agent in self.investigations[investigation_id].agents:
                    if agent.status != StatusEnum.COMPLETE:
                        agent.status = StatusEnum.COMPLETE
                        agent.completed_at = datetime.now()
                
                print(f"[SERVICE] Investigation {investigation_id} completed successfully")
                
            except Exception as e:
                print(f"[SERVICE ERROR] Investigation {investigation_id} failed: {str(e)}")
                import traceback
                traceback.print_exc()
                self.investigations[investigation_id].status = StatusEnum.ERROR
                self.investigations[investigation_id].completed_at = datetime.now()
        
        thread = threading.Thread(target=run_investigation, daemon=True)
        thread.start()
        
        return investigation_id
    
    def get_investigation_status(self, investigation_id: str) -> Optional[InvestigationStatus]:
        """Get current status of an investigation"""
        return self.investigations.get(investigation_id)
    
    def _update_status(self, investigation_id: str, agent_id: str, event_type: str, data: Dict[str, Any]):
        """Update investigation status based on callback events"""
        investigation = self.investigations.get(investigation_id)
        if not investigation:
            print(f"[UPDATE ERROR] Investigation {investigation_id} not found")
            return
        
        print(f"[UPDATE] Investigation: {investigation_id}, Agent: {agent_id}, Event: {event_type}")
        
        # Find or create agent status
        agent_status = next((a for a in investigation.agents if a.agent_id == agent_id), None)
        
        if event_type == "agent_registered":
            # Initial agent registration
            if not agent_status:
                agent_status = AgentStatus(**data)
                investigation.agents.append(agent_status)
                print(f"[UPDATE] Registered agent {agent_id}")
            
        elif event_type == "agent_start":
            if agent_status:
                agent_status.status = StatusEnum.RUNNING
                agent_status.started_at = data.get("started_at")
                print(f"[UPDATE] Agent {agent_id} started")
            
        elif event_type == "task_complete":
            if agent_status:
                # Add task to agent's task list
                task = TaskStatus(
                    task_name=data["task_name"],
                    status=StatusEnum.COMPLETE,
                    output=data.get("output"),
                    completed_at=data.get("completed_at")
                )
                agent_status.tasks.append(task)
                
                # Mark current agent as complete
                agent_status.status = StatusEnum.COMPLETE
                agent_status.completed_at = data.get("completed_at")
                
                print(f"[UPDATE] Agent {agent_id} completed task: {data['task_name'][:50]}")
                
                # Start next agent
                agent_index = int(agent_id.replace("agent", ""))
                next_agent_id = f"agent{agent_index + 1}"
                next_agent = next((a for a in investigation.agents if a.agent_id == next_agent_id), None)
                
                if next_agent and next_agent.status == StatusEnum.PENDING:
                    next_agent.status = StatusEnum.RUNNING
                    next_agent.started_at = datetime.now()
                    print(f"[UPDATE] Started next agent: {next_agent_id}")

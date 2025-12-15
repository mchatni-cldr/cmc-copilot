from typing import Dict, Any, Callable
from datetime import datetime

class CrewCallbackHandler:
    """Callback handler that integrates with CrewAI's task_callback system"""
    
    def __init__(self, investigation_id: str, update_callback: Callable):
        """
        Initialize callback handler
        
        Args:
            investigation_id: ID of the investigation
            update_callback: Function to call with status updates
        """
        self.investigation_id = investigation_id
        self.update_callback = update_callback
        self.agent_task_map = {}  # Maps task description to agent_id
        self.current_agent_index = 0
        
    def register_task_to_agent(self, task_description: str, agent_id: str):
        """Register a task to agent mapping"""
        # Use first 50 chars of description as key
        task_key = task_description[:50].strip()
        self.agent_task_map[task_key] = agent_id
        print(f"[CALLBACK] Registered task '{task_key}' to {agent_id}")
        
    def task_callback(self, task_output):
        """
        Called by CrewAI when a task completes
        This is the callback function passed to Crew(task_callback=...)
        """
        try:
            # Extract task information from task_output
            if hasattr(task_output, 'description'):
                task_description = str(task_output.description)
            else:
                task_description = str(task_output)
                
            if hasattr(task_output, 'raw'):
                task_result = str(task_output.raw)
            else:
                task_result = str(task_output)
            
            # Find which agent this task belongs to
            task_key = task_description[:50].strip()
            agent_id = self.agent_task_map.get(task_key, f"agent{self.current_agent_index + 1}")
            
            # Extract a clean task name (first line, max 100 chars)
            task_lines = task_description.split('\n')
            task_name = task_lines[0][:100] if task_lines else "Task completed"
            
            print(f"[CALLBACK] Task completed for {agent_id}: {task_name}")
            
            # Notify about task completion
            self.update_callback(
                self.investigation_id,
                agent_id,
                "task_complete",
                {
                    "task_name": task_name,
                    "output": task_result[:500],  # Limit output length
                    "completed_at": datetime.now()
                }
            )
            
            # Move to next agent
            self.current_agent_index += 1
            
        except Exception as e:
            print(f"[CALLBACK ERROR] {str(e)}")
            import traceback
            traceback.print_exc()
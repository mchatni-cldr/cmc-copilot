from crewai import Crew, Process
from .agent_definitions import (
    create_analytix_bot, 
    create_rootcause_ai, 
    create_qa_reporting_agent,
    create_data_analysis_task,
    create_root_cause_task,
    create_qa_report_task
)
from .tools import SensorDataAnalyzer, MaterialLogReader, ScientificKnowledgeBase
from utils.callbacks import CrewCallbackHandler
from models.status_model import AgentStatus, StatusEnum
from datetime import datetime

def create_investigation_crew(investigation_id: str, update_callback):
    """Create and configure the CMC investigation crew with task_callback"""
    
    # Create callback handler
    callback_handler = CrewCallbackHandler(investigation_id, update_callback)
    
    # Initialize tools
    sensor_tool = SensorDataAnalyzer()
    material_tool = MaterialLogReader()
    knowledge_tool = ScientificKnowledgeBase()
    
    # Create agents
    analytix_bot = create_analytix_bot([sensor_tool, material_tool])
    rootcause_ai = create_rootcause_ai([knowledge_tool])
    qa_agent = create_qa_reporting_agent()
    
    # Create tasks
    batch_id = "P25-003"
    data_task = create_data_analysis_task(analytix_bot, batch_id)
    root_cause_task = create_root_cause_task(rootcause_ai)
    report_task = create_qa_report_task(qa_agent, batch_id)
    
    # Register task-to-agent mappings
    callback_handler.register_task_to_agent(data_task.description, "agent1")
    callback_handler.register_task_to_agent(root_cause_task.description, "agent2")
    callback_handler.register_task_to_agent(report_task.description, "agent3")
    
    # Initialize agent statuses
    agent_statuses = [
        AgentStatus(
            agent_id="agent1",
            agent_name="Analytix-Bot",
            role="Data Scientist Agent",
            status=StatusEnum.PENDING,
            tasks=[],
            started_at=None
        ),
        AgentStatus(
            agent_id="agent2",
            agent_name="RootCause-AI",
            role="Process Expert Agent",
            status=StatusEnum.PENDING,
            tasks=[],
            started_at=None
        ),
        AgentStatus(
            agent_id="agent3",
            agent_name="QAReportingAgent",
            role="QA Specialist Agent",
            status=StatusEnum.PENDING,
            tasks=[],
            started_at=None
        )
    ]
    
    # Notify about initial agent setup
    for agent_status in agent_statuses:
        update_callback(
            investigation_id,
            agent_status.agent_id,
            "agent_registered",
            agent_status.dict()
        )
    
    # Mark first agent as running
    update_callback(
        investigation_id,
        "agent1",
        "agent_start",
        {"status": StatusEnum.RUNNING, "started_at": datetime.now()}
    )
    
    # Create crew with task_callback
    crew = Crew(
        agents=[analytix_bot, rootcause_ai, qa_agent],
        tasks=[data_task, root_cause_task, report_task],
        process=Process.sequential,
        verbose=True,
        task_callback=callback_handler.task_callback  # Use task_callback here
    )
    
    return crew
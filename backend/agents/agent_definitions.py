from crewai import Agent, Task, LLM
from typing import List
from config import Config
from .tools import SensorDataAnalyzer, MaterialLogReader, ScientificKnowledgeBase

def get_claude_llm():
    """Get configured Claude LLM"""
    return LLM(
        model=Config.LLM_MODEL,
        temperature=Config.LLM_TEMPERATURE,
        max_tokens=Config.LLM_MAX_TOKENS,
        api_key=Config.ANTHROPIC_API_KEY
    )

def create_analytix_bot(tools: List) -> Agent:
    """Create the Analytix-Bot agent (Data Scientist)"""
    return Agent(
        role='Data Scientist Agent',
        goal='Analyze sensor data and material logs to identify deviations and correlations',
        backstory="""You are Analytix-Bot, an expert data scientist specializing in 
        biopharmaceutical manufacturing data analysis. You excel at finding patterns 
        in time-series sensor data, identifying statistical anomalies, and correlating 
        events with material usage logs. Your analysis is thorough, precise, and 
        evidence-based.""",
        tools=tools,
        llm=get_claude_llm(),
        verbose=True
    )

def create_rootcause_ai(tools: List) -> Agent:
    """Create the RootCause-AI agent (Process Expert)"""
    return Agent(
        role='Process Expert Agent',
        goal='Determine the scientific root cause of quality deviations using biochemical knowledge',
        backstory="""You are RootCause-AI, a biochemistry and process engineering expert 
        with deep knowledge of protein chemistry, monoclonal antibody manufacturing, and 
        purification processes. You understand how process parameters like pH affect 
        protein stability and can explain complex biochemical mechanisms. You excel at 
        connecting process deviations to quality outcomes.""",
        tools=tools,
        llm=get_claude_llm(),
        verbose=True
    )

def create_qa_reporting_agent() -> Agent:
    """Create the QA Reporting Agent (QA Specialist)"""
    return Agent(
        role='QA Specialist Agent',
        goal='Compile investigation findings into a clear, compliant quality report with actionable recommendations',
        backstory="""You are a Quality Assurance specialist with extensive experience 
        in pharmaceutical manufacturing compliance. You excel at taking complex technical 
        findings and organizing them into clear, structured reports that meet regulatory 
        requirements. You provide actionable CAPA recommendations based on root cause 
        analysis.""",
        tools=[],  # No tools needed, compiles info from other agents
        llm=get_claude_llm(),
        verbose=True
    )

# Task Definitions

def create_data_analysis_task(agent: Agent, batch_id: str) -> Task:
    """Task for Analytix-Bot to analyze sensor and material data"""
    return Task(
        description=f"""Analyze batch {batch_id} to identify the root cause of the QC failure.

Your analysis must include:
1. Analyze pH sensor data using the Sensor Data Analyzer tool
2. Identify any deviations from normal operating ranges
3. Query material logs using the Material Log Reader tool to find what materials were used during deviation periods
4. Establish temporal correlations between material usage and deviations

Provide specific timestamps, values, and lot numbers in your findings.""",
        agent=agent,
        expected_output="""A detailed analysis report containing:
- Specific pH deviation detected (values, timestamps, duration)
- Material lot number correlated with the deviation
- Timeline of events
- Statistical significance of findings"""
    )

def create_root_cause_task(agent: Agent) -> Task:
    """Task for RootCause-AI to determine scientific root cause"""
    return Task(
        description="""Based on the data analysis findings, determine the scientific root cause.

Your analysis must include:
1. Query the Scientific Knowledge Base about deamidation and pH sensitivity
2. Explain the biochemical mechanism linking the pH deviation to the impurity
3. Validate that the proposed root cause explains all observed data
4. Provide scientific justification for your conclusion

Focus on the relationship between pH, buffer composition, and antibody deamidation.""",
        agent=agent,
        expected_output="""A scientific root cause analysis containing:
- Identified material lot causing the issue
- Biochemical mechanism (deamidation pathway)
- Explanation of how pH affects antibody stability
- Scientific validation of the root cause"""
    )

def create_qa_report_task(agent: Agent, batch_id: str) -> Task:
    """Task for QA Reporting Agent to create final report"""
    return Task(
        description=f"""Compile a comprehensive investigation report for batch {batch_id}.

Your report must include:
1. EVIDENCE section: Summarize the data findings (pH deviation, material correlation)
2. ROOT CAUSE section: Explain the scientific root cause (buffer preparation error leading to deamidation)
3. RECOMMENDATIONS section: Provide 3 specific CAPA actions (immediate, corrective, preventive)

Format the report in a clear, structured manner suitable for QA documentation.""",
        agent=agent,
        expected_output="""A complete investigation report with three sections:

EVIDENCE:
- pH deviation details (7.0 to 6.5, 45 minutes, Protein A step)
- Material correlation (Buffer Lot #B44-78)

ROOT CAUSE:
- Incorrectly prepared Elution Buffer Lot #B44-78
- Low pH accelerated deamidation of antibody
- Acidic variants produced

RECOMMENDATIONS:
1. Immediate Action: Quarantine buffer lot, verify pH
2. Corrective Action: Re-manufacture buffer, enhance QC
3. CAPA: Process review for buffer preparation"""
    )
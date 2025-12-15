from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from services.data_service import DataService

class SensorDataInput(BaseModel):
    """Input for Sensor Data Analyzer"""
    parameter: str = Field(..., description="The parameter to analyze (e.g., 'pH', 'temperature', 'pressure')")

class SensorDataAnalyzer(BaseTool):
    name: str = "Sensor Data Analyzer"
    description: str = "Analyzes time-series sensor data from batch manufacturing to detect deviations and anomalies"
    args_schema: Type[BaseModel] = SensorDataInput
    
    def _run(self, parameter: str) -> str:
        """Analyze sensor data for deviations"""
        data_service = DataService()
        sensor_data = data_service.generate_sensor_data()
        
        deviation = sensor_data['deviation_detected']
        
        if parameter.lower() == 'ph':
            return f"""Sensor Data Analysis Results:
            
Total Data Points Analyzed: {sensor_data['total_points']:,}
Parameter: {deviation['parameter']}

DEVIATION DETECTED:
- Start Time: {deviation['start_time']}
- End Time: {deviation['end_time']}
- Duration: {deviation['duration_minutes']} minutes
- Normal Value: {deviation['normal_value']}
- Deviated Value: {deviation['deviated_value']}
- Deviation Magnitude: {abs(deviation['normal_value'] - deviation['deviated_value'])} units

The pH dropped significantly during the Protein A purification step, deviating from the normal operating range of 7.0 ± 0.1 to approximately 6.5."""
        
        return f"No significant deviations detected for {parameter}"


class MaterialLogInput(BaseModel):
    """Input for Material Log Reader"""
    time_window: str = Field(..., description="Time window to search (e.g., 'deviation period', 'all')")

class MaterialLogReader(BaseTool):
    name: str = "Material Log Reader"
    description: str = "Queries batch material logs to identify which materials were used during specific time periods"
    args_schema: Type[BaseModel] = MaterialLogInput
    
    def _run(self, time_window: str) -> str:
        """Read material usage logs"""
        data_service = DataService()
        logs = data_service.get_material_logs()
        
        result = "Material Usage Logs:\n\n"
        for log in logs:
            result += f"Material: {log['material']}\n"
            result += f"Lot Number: {log['lot_number']}\n"
            result += f"Usage Time: {log['usage_time']}\n"
            result += f"Process Step: {log['step']}\n"
            result += "-" * 50 + "\n"
        
        result += "\nKEY FINDING: Elution Buffer Lot #B44-78 was introduced at the exact start of the pH deviation period during Protein A Purification."
        
        return result


class ScientificQueryInput(BaseModel):
    """Input for Scientific Knowledge Base"""
    query: str = Field(..., description="Scientific query about deamidation, pH effects, or antibody stability")

class ScientificKnowledgeBase(BaseTool):
    name: str = "Scientific Knowledge Base"
    description: str = "Searches scientific literature and knowledge base for information about deamidation, pH sensitivity, and antibody chemistry"
    args_schema: Type[BaseModel] = ScientificQueryInput
    
    def _run(self, query: str) -> str:
        """Query scientific knowledge base"""
        data_service = DataService()
        knowledge = data_service.get_scientific_knowledge()
        
        if 'deamidation' in query.lower() or 'ph' in query.lower():
            info = knowledge['deamidation']
            return f"""Scientific Knowledge Base Results:

DEAMIDATION OF MONOCLONAL ANTIBODIES:

Definition: {info['definition']}

pH Sensitivity: {info['ph_sensitivity']}

Impact on Monoclonal Antibodies: {info['monoclonal_antibodies']}

Detection Methods: {info['detection']}

Mitigation Strategies: {info['mitigation']}

CONCLUSION: The observed pH drop to 6.5 is within the range that significantly accelerates deamidation. This is consistent with the acidic variant impurity detected in the Cation Exchange Chromatography assay."""
        
        return "No relevant scientific information found for this query."

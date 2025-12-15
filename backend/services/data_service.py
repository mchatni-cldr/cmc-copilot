import random
from datetime import datetime, timedelta
import numpy as np
from models.domain_model import BatchInfo

class DataService:
    """Generates simulated batch and sensor data for CMC deviation analysis"""
    
    @staticmethod
    def get_batch_info():
        """Get current batch information"""
        return BatchInfo(
            batch_id="P25-003",
            product="Monoclonal Antibody",
            status="QC Failure",
            qc_failure_description="Cation Exchange Chromatography detected unexpected impurity peak"
        )
    
    @staticmethod
    def generate_sensor_data():
        """Generate simulated time-series sensor data"""
        base_time = datetime.now() - timedelta(hours=24)
        
        # Normal operation data (first 8 hours)
        normal_data = []
        for i in range(480):  # 8 hours at 1-min intervals
            normal_data.append({
                'timestamp': (base_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'),
                'pH': round(7.0 + random.uniform(-0.05, 0.05), 2),
                'temperature': round(25.0 + random.uniform(-0.2, 0.2), 1),
                'pressure': round(1.2 + random.uniform(-0.05, 0.05), 2)
            })
        
        # Deviation period (45 minutes during Protein A purification)
        deviation_start_idx = 480
        deviation_data = []
        for i in range(45):
            deviation_data.append({
                'timestamp': (base_time + timedelta(minutes=deviation_start_idx + i)).strftime('%Y-%m-%d %H:%M:%S'),
                'pH': round(6.5 + random.uniform(-0.1, 0.1), 2),  # Lower pH
                'temperature': round(25.0 + random.uniform(-0.2, 0.2), 1),
                'pressure': round(1.2 + random.uniform(-0.05, 0.05), 2)
            })
        
        # Return to normal (remaining time)
        recovery_data = []
        for i in range(435):  # Rest of the run
            recovery_data.append({
                'timestamp': (base_time + timedelta(minutes=deviation_start_idx + 45 + i)).strftime('%Y-%m-%d %H:%M:%S'),
                'pH': round(7.0 + random.uniform(-0.05, 0.05), 2),
                'temperature': round(25.0 + random.uniform(-0.2, 0.2), 1),
                'pressure': round(1.2 + random.uniform(-0.05, 0.05), 2)
            })
        
        all_data = normal_data + deviation_data + recovery_data
        
        return {
            'data_points': all_data,
            'total_points': len(all_data),
            'deviation_detected': {
                'parameter': 'pH',
                'start_time': deviation_data[0]['timestamp'],
                'end_time': deviation_data[-1]['timestamp'],
                'normal_value': 7.0,
                'deviated_value': 6.5,
                'duration_minutes': 45
            }
        }
    
    @staticmethod
    def get_material_logs():
        """Get material usage logs for the batch"""
        base_time = datetime.now() - timedelta(hours=24)
        
        return [
            {
                'material': 'Cell Culture Media',
                'lot_number': 'M23-445',
                'usage_time': (base_time + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                'step': 'Bioreactor Inoculation'
            },
            {
                'material': 'Elution Buffer',
                'lot_number': 'B44-78',
                'usage_time': (base_time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                'step': 'Protein A Purification'
            },
            {
                'material': 'Wash Buffer',
                'lot_number': 'W89-12',
                'usage_time': (base_time + timedelta(hours=10)).strftime('%Y-%m-%d %H:%M:%S'),
                'step': 'Column Wash'
            }
        ]
    
    @staticmethod
    def get_scientific_knowledge():
        """Simulated scientific knowledge base about deamidation"""
        return {
            'deamidation': {
                'definition': 'Deamidation is a chemical reaction where asparagine or glutamine residues lose their amide group, converting to aspartic acid or glutamic acid.',
                'ph_sensitivity': 'Deamidation rates increase significantly at pH values below 6.0 and above 8.0. Optimal stability is typically between pH 6.5-7.5.',
                'monoclonal_antibodies': 'Monoclonal antibodies are particularly susceptible to deamidation in the CDR regions, which can affect binding affinity.',
                'detection': 'Deamidation products appear as acidic variants in cation exchange chromatography due to the gain of negative charge.',
                'mitigation': 'Control pH within optimal range, minimize temperature exposure, and ensure proper buffer preparation.'
            }
        }
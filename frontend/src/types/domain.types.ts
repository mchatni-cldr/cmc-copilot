export interface BatchInfo {
  batch_id: string;
  product: string;
  status: string;
  qc_failure_description: string;
}

export interface SensorDeviation {
  parameter: string;
  normal_value: number;
  deviated_value: number;
  timestamp_start: string;
  timestamp_end: string;
  duration_minutes: number;
}

export interface Evidence {
  deviation: SensorDeviation;
  data_points_analyzed: string;
  material_lot_correlated: string;
}

export interface RootCause {
  material_lot: string;
  failure_mechanism: string;
  scientific_explanation: string;
}

export interface Recommendation {
  priority: string;
  action: string;
  description: string;
}

export interface DeviationReport {
  batch_info: BatchInfo;
  evidence: Evidence;
  root_cause: RootCause;
  recommendations: Recommendation[];
  timestamp: string;
}
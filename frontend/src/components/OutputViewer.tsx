import { BarChart3, Lightbulb, FileText, Download, FileWarning, RotateCcw, CheckCircle2 } from 'lucide-react';

interface OutputViewerProps {
  report: any;
  onReset: () => void;
}

export default function OutputViewer({ report, onReset }: OutputViewerProps) {
  // Parse the report output (this is a simplified version)
  // In production, you'd parse the actual crew output format
  
  const evidence = {
    ph_drop: "7.0 to 6.5",
    step: "Protein A purification step",
    timeframe: "14:23 and 15:08",
    data_points: "2.3M data points analyzed",
    duration: "45-minute deviation"
  };

  const rootCause = {
    material: "Elution Buffer Lot #B44-78",
    mechanism: "Buffer preparation error",
    scientific: "Low pH conditions accelerated deamidation of the antibody, producing the detected acidic variants."
  };

  const recommendations = [
    {
      priority: "Immediate Action",
      action: "Quarantine Elution Buffer Lot #B44-78 and perform pH verification testing."
    },
    {
      priority: "Corrective Action",
      action: "Re-manufacture buffer with verified pH control. Implement enhanced buffer preparation QC checks."
    },
    {
      priority: "CAPA Required",
      action: "Initiate formal Corrective and Preventive Action for buffer preparation process review."
    }
  ];

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden animate-in slide-in-from-bottom">
      <div className="bg-gradient-to-r from-emerald-50 to-white p-6 border-b border-gray-200">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <h3 className="text-xl font-bold text-gray-900">Investigation Report</h3>
          <span className="px-4 py-2 bg-emerald-100 text-emerald-800 text-sm font-bold rounded-full flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            Analysis Complete
          </span>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Evidence Section */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-purple-600" />
            </div>
            <h4 className="text-lg font-bold text-gray-900">Evidence</h4>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-50/30 border-2 border-purple-200 rounded-xl p-5 space-y-4">
            <p className="text-sm text-gray-800 leading-relaxed">
              A severe pH drop from <strong className="text-purple-900">{evidence.ph_drop}</strong> was detected during the{' '}
              <strong className="text-purple-900">{evidence.step}</strong> between{' '}
              <strong className="text-purple-900">{evidence.timeframe}</strong> on the manufacturing run.
            </p>
            <div className="bg-white/80 backdrop-blur rounded-lg p-4 border border-purple-200">
              <p className="text-xs font-semibold text-purple-600 uppercase tracking-wider mb-1">Sensor Data Analysis</p>
              <p className="text-sm text-gray-700">{evidence.duration} detected in {evidence.data_points}</p>
            </div>
          </div>
        </div>

        {/* Root Cause Section */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
              <Lightbulb className="w-5 h-5 text-emerald-600" />
            </div>
            <h4 className="text-lg font-bold text-gray-900">Root Cause</h4>
          </div>
          <div className="bg-gradient-to-br from-emerald-50 to-emerald-50/30 border-2 border-emerald-200 rounded-xl p-5 space-y-4">
            <p className="text-sm text-gray-800 leading-relaxed">
              The pH deviation directly correlates with the use of{' '}
              <strong className="text-emerald-900">{rootCause.material}</strong>. This indicates an{' '}
              {rootCause.mechanism} is the root cause of the acidic variant impurity.
            </p>
            <div className="bg-white/80 backdrop-blur rounded-lg p-4 border border-emerald-200">
              <p className="text-xs font-semibold text-emerald-600 uppercase tracking-wider mb-1">Scientific Analysis</p>
              <p className="text-sm text-gray-700">{rootCause.scientific}</p>
            </div>
          </div>
        </div>

        {/* Recommendations Section */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <h4 className="text-lg font-bold text-gray-900">Recommendations</h4>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-blue-50/30 border-2 border-blue-200 rounded-xl p-5 space-y-4">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold shadow-md">
                  {idx + 1}
                </div>
                <div className="flex-1 pt-1">
                  <p className="text-sm font-bold text-blue-900 mb-1">{rec.priority}:</p>
                  <p className="text-sm text-gray-700 leading-relaxed">{rec.action}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-4">
          <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2">
            <Download className="w-4 h-4" />
            Download Report
          </button>
          <button className="px-6 py-3 bg-white border-2 border-gray-300 hover:bg-gray-50 text-gray-700 font-semibold rounded-xl shadow-sm hover:shadow-md transition-all duration-200 flex items-center justify-center gap-2">
            <FileWarning className="w-4 h-4" />
            Generate CAPA
          </button>
          <button
            onClick={onReset}
            className="px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl shadow-sm hover:shadow-md transition-all duration-200 flex items-center justify-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            New Analysis
          </button>
        </div>
      </div>
    </div>
  );
}
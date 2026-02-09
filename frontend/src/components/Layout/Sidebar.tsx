import { useAppStore } from '@/store/useAppStore';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const classColors = [
  { id: 0, name: 'Non-tumor', color: '#000000', bgColor: 'bg-gray-900' },
  { id: 1, name: 'Necrotic/Core', color: '#0000FF', bgColor: 'bg-blue-600' },
  { id: 2, name: 'Edema', color: '#FFC0CB', bgColor: 'bg-pink-300' },
  { id: 3, name: 'Enhancing Tumor', color: '#00FFFF', bgColor: 'bg-cyan-400' },
];

export function Sidebar() {
  const { modelStatus, health } = useAppStore();

  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-64px)] p-4">
      {/* Model Status */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Model Status
        </h3>
        <div className="card p-4">
          {modelStatus ? (
            <div className="flex items-center gap-3">
              {modelStatus.loaded ? (
                <CheckCircle className="w-6 h-6 text-green-500" />
              ) : modelStatus.exists ? (
                <AlertCircle className="w-6 h-6 text-amber-500" />
              ) : (
                <XCircle className="w-6 h-6 text-red-500" />
              )}
              <div>
                <p className="font-medium text-gray-900">
                  {modelStatus.loaded ? 'Ready' : modelStatus.exists ? 'Not Loaded' : 'Not Found'}
                </p>
                <p className="text-xs text-gray-500">
                  {modelStatus.loaded ? 'Model is active' : 'Place model in models/saved_models/'}
                </p>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 border-2 border-gray-300 border-t-medical-500 rounded-full animate-spin" />
              <p className="text-gray-500">Checking...</p>
            </div>
          )}
        </div>
      </div>

      {/* Class Legend */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Tumor Classes
        </h3>
        <div className="space-y-2">
          {classColors.map((cls) => (
            <div
              key={cls.id}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div
                className={`w-5 h-5 rounded ${cls.bgColor} border border-gray-200`}
                style={{ backgroundColor: cls.color }}
              />
              <span className="text-sm text-gray-700">{cls.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      {health && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3">
            System Info
          </h3>
          <div className="card p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Version</span>
              <span className="font-medium">{health.version}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Status</span>
              <span className={`font-medium ${health.status === 'healthy' ? 'text-green-600' : 'text-red-600'}`}>
                {health.status}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Footer Links */}
      <div className="mt-auto pt-6 border-t border-gray-200">
        <div className="text-xs text-gray-500 space-y-1">
          <a 
            href="https://www.med.upenn.edu/cbica/brats/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="block hover:text-medical-600 transition-colors"
          >
            BraTS Challenge
          </a>
          <a 
            href="https://arxiv.org/abs/1505.04597" 
            target="_blank" 
            rel="noopener noreferrer"
            className="block hover:text-medical-600 transition-colors"
          >
            U-Net Paper
          </a>
          <a 
            href="https://arxiv.org/abs/1905.11946" 
            target="_blank" 
            rel="noopener noreferrer"
            className="block hover:text-medical-600 transition-colors"
          >
            EfficientNet Paper
          </a>
        </div>
      </div>
    </aside>
  );
}

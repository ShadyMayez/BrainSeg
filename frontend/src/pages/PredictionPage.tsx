import { useState, useEffect } from 'react';
import { Brain, Info, FileText, Activity } from 'lucide-react';
import { predictionApi, healthApi } from '@/services/api';
import type { PredictionResponse, FileUploadState } from '@/types';

// UI Components (simplified inline versions)
const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white rounded-xl shadow-lg border border-gray-200 ${className}`}>
    {children}
  </div>
);

const CardHeader = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4 border-b border-gray-100">{children}</div>
);

const CardTitle = ({ children }: { children: React.ReactNode }) => (
  <h3 className="text-lg font-semibold text-gray-900">{children}</h3>
);

const CardDescription = ({ children }: { children: React.ReactNode }) => (
  <p className="text-sm text-gray-500 mt-1">{children}</p>
);

const CardContent = ({ children }: { children: React.ReactNode }) => (
  <div className="p-6">{children}</div>
);

const Button = ({ 
  children, 
  onClick, 
  disabled = false, 
  variant = 'primary',
  className = ''
}: { 
  children: React.ReactNode; 
  onClick?: () => void; 
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'outline';
  className?: string;
}) => {
  const baseStyles = 'px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2';
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300',
    secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:bg-gray-100',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 disabled:border-gray-300 disabled:text-gray-400'
  };
  
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={`${baseStyles} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
};

const Alert = ({ type, title, message }: { type: 'error' | 'success'; title: string; message: string }) => {
  const styles = {
    error: 'bg-red-50 border-red-200 text-red-800',
    success: 'bg-green-50 border-green-200 text-green-800'
  };
  
  return (
    <div className={`p-4 rounded-lg border ${styles[type]} mb-4`}>
      <h4 className="font-semibold">{title}</h4>
      <p className="text-sm mt-1">{message}</p>
    </div>
  );
};

const LoadingSpinner = () => (
  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
);

// File Upload Component
const FileUpload = ({
  label,
  description,
  file,
  onChange,
  accept = '.nii,.nii.gz,.gz'
}: {
  label: string;
  description: string;
  file: File | null;
  onChange: (file: File | null) => void;
  accept?: string;
}) => (
  <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-blue-400 transition-colors">
    <label className="block cursor-pointer">
      <input
        type="file"
        accept={accept}
        onChange={(e) => onChange(e.target.files?.[0] || null)}
        className="hidden"
      />
      <div className="text-center">
        <FileText className="w-8 h-8 mx-auto text-gray-400 mb-2" />
        <p className="font-medium text-gray-700">{label}</p>
        <p className="text-xs text-gray-500 mt-1">{description}</p>
        {file && (
          <p className="text-sm text-blue-600 mt-2 font-medium">
            ✓ {file.name}
          </p>
        )}
      </div>
    </label>
  </div>
);

// Results Panel Component
const ResultsPanel = ({ results }: { results: PredictionResponse }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-blue-50 p-4 rounded-lg">
        <p className="text-sm text-blue-600 font-medium">Processed Slices</p>
        <p className="text-2xl font-bold text-blue-900">{results.processed_slices}</p>
      </div>
      <div className="bg-green-50 p-4 rounded-lg">
        <p className="text-sm text-green-600 font-medium">Model Used</p>
        <p className="text-lg font-bold text-green-900 truncate">{results.model_used}</p>
      </div>
    </div>
    
    <div>
      <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
        <Activity className="w-4 h-4" />
        Tumor Statistics
      </h4>
      <div className="space-y-2">
        {Object.entries(results.tumor_stats).map(([label, stats]) => (
          <div key={label} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <span className="text-gray-700">{label}</span>
            <div className="text-right">
              <span className="font-semibold text-gray-900">{stats.percentage.toFixed(2)}%</span>
              <span className="text-sm text-gray-500 ml-2">({stats.pixel_count.toLocaleString()} px)</span>
            </div>
          </div>
        ))}
      </div>
    </div>
    
    {results.overlay_image && (
      <div>
        <h4 className="font-semibold text-gray-900 mb-3">Segmentation Overlay</h4>
        <img 
          src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${results.overlay_image}`}
          alt="Segmentation overlay"
          className="w-full rounded-lg border"
        />
      </div>
    )}
    
    {results.segmentation_mask && (
      <div className="p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          Segmentation mask saved. Download from:
        </p>
        <a 
          href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${results.segmentation_mask}`}
          className="text-blue-600 hover:underline text-sm break-all"
          download
        >
          {results.segmentation_mask}
        </a>
      </div>
    )}
  </div>
);

export function PredictionPage() {
  const [files, setFiles] = useState<FileUploadState>({
    flair: null,
    t1: null,
    t1ce: null,
    t2: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<PredictionResponse | null>(null);
  const [modelInfo, setModelInfo] = useState<any>(null);

  // Fetch model info on mount
  useEffect(() => {
    const fetchModelInfo = async () => {
      try {
        const info = await predictionApi.getModelInfo();
        setModelInfo(info);
      } catch (err) {
        console.error('Failed to fetch model info:', err);
      }
    };
    fetchModelInfo();
  }, []);

  const allFilesSelected = files.flair && files.t1 && files.t1ce && files.t2;

  const handlePredict = async () => {
    if (!allFilesSelected) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await predictionApi.predict({
        flair: files.flair!,
        t1: files.t1!,
        t1ce: files.t1ce!,
        t2: files.t2!,
      });
      setResults(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFiles({ flair: null, t1: null, t1ce: null, t2: null });
    setResults(null);
    setError(null);
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl mb-4">
          <Brain className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Tumor Segmentation Prediction
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Upload all 4 MRI modalities to perform brain tumor segmentation using our PyTorch deep learning model.
        </p>
        
        {/* Model Status */}
        {modelInfo && (
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm mt-4 ${
            modelInfo.model_loaded 
              ? 'bg-green-100 text-green-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              modelInfo.model_loaded ? 'bg-green-500' : 'bg-yellow-500'
            }`} />
            {modelInfo.model_loaded 
              ? `Model loaded (${modelInfo.input_channels} channels)` 
              : 'Model not loaded'}
          </div>
        )}
      </div>

      {/* Error Alert */}
      {error && (
        <Alert type="error" title="Prediction Failed" message={error} />
      )}

      {/* Results */}
      {results && (
        <Card className="border-green-200">
          <CardHeader>
            <CardTitle className="text-green-800 flex items-center gap-2">
              ✓ Prediction Complete
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResultsPanel results={results} />
          </CardContent>
        </Card>
      )}

      {/* Upload Form */}
      {!results && (
        <Card>
          <CardHeader>
            <CardTitle>Upload MRI Modalities</CardTitle>
            <CardDescription>
              All 4 modalities are required for accurate segmentation. Files should be in NIfTI format (.nii or .nii.gz).
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <FileUpload
                label="FLAIR"
                description="T2-FLAIR modality"
                file={files.flair}
                onChange={(file) => setFiles(prev => ({ ...prev, flair: file }))}
              />
              <FileUpload
                label="T1"
                description="Native T1-weighted"
                file={files.t1}
                onChange={(file) => setFiles(prev => ({ ...prev, t1: file }))}
              />
              <FileUpload
                label="T1CE"
                description="T1 with contrast enhancement"
                file={files.t1ce}
                onChange={(file) => setFiles(prev => ({ ...prev, t1ce: file }))}
              />
              <FileUpload
                label="T2"
                description="T2-weighted modality"
                file={files.t2}
                onChange={(file) => setFiles(prev => ({ ...prev, t2: file }))}
              />
            </div>

            {/* File Summary */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-2">
                <Info className="w-4 h-4" />
                Upload Status
              </h4>
              <div className="space-y-1">
                {Object.entries(files).map(([key, file]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-gray-600 capitalize">{key}:</span>
                    <span className={file ? 'text-green-600 font-medium' : 'text-gray-400'}>
                      {file ? `✓ ${file.name}` : 'Not selected'}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <Button
                onClick={handlePredict}
                disabled={!allFilesSelected || loading}
                className="flex-1 justify-center"
              >
                {loading ? (
                  <>
                    <LoadingSpinner />
                    Processing...
                  </>
                ) : (
                  <>
                    <Brain className="w-5 h-5" />
                    Run Prediction
                  </>
                )}
              </Button>
              <Button
                onClick={handleReset}
                variant="outline"
                disabled={loading}
              >
                Reset
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Reset Button when showing results */}
      {results && (
        <div className="flex justify-center">
          <Button onClick={handleReset} variant="outline">
            Start New Prediction
          </Button>
        </div>
      )}

      {/* Info Card */}
      <Card className="bg-blue-50 border-blue-100">
        <CardContent className="py-4">
          <h4 className="font-medium text-blue-900 mb-2 flex items-center gap-2">
            <Info className="w-4 h-4" />
            About the 4-Channel Model
          </h4>
          <p className="text-sm text-blue-800">
            This PyTorch U-Net model was trained on the BraTS 2020 dataset and uses all 4 MRI modalities 
            (FLAIR, T1, T1CE, T2) for improved tumor segmentation accuracy. Each modality provides 
            complementary information about different tissue characteristics.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

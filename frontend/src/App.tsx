import { PredictionPage } from '@/pages/PredictionPage';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">BTS</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Brain Tumor Segmentation</h1>
                <p className="text-xs text-gray-500">PyTorch 4-Channel U-Net</p>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              v2.0.0
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <PredictionPage />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <p className="text-center text-sm text-gray-500">
            Brain Tumor Segmentation System - Powered by PyTorch
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

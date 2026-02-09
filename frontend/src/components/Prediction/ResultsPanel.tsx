import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/UI/Card';
import { Badge } from '@/components/UI/Badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './Tabs';
import type { PredictionResponse } from '@/types';

interface ResultsPanelProps {
  results: PredictionResponse;
}

export function ResultsPanel({ results }: ResultsPanelProps) {
  const [activeTab, setActiveTab] = useState('modalities');

  if (!results.success) {
    return (
      <Card className="border-red-200">
        <CardContent className="p-6">
          <p className="text-red-600">{results.message}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Status */}
      <div className="flex items-center gap-3">
        <Badge variant={results.model_loaded ? 'success' : 'warning'}>
          {results.model_loaded ? 'Model Active' : 'Preprocessing Only'}
        </Badge>
        <span className="text-sm text-gray-600">{results.message}</span>
      </div>

      {/* Image Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid grid-cols-4">
          <TabsTrigger value="modalities">Modalities</TabsTrigger>
          <TabsTrigger value="mask">Mask</TabsTrigger>
          <TabsTrigger value="overlay">Overlay</TabsTrigger>
          <TabsTrigger value="comparison">Comparison</TabsTrigger>
        </TabsList>

        <TabsContent value="modalities" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Input Modalities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                {results.modality_images.map((img, idx) => (
                  <div key={idx} className="space-y-2">
                    <img
                      src={img}
                      alt={`Modality ${idx + 1}`}
                      className="w-full rounded-lg border border-gray-200"
                    />
                    <p className="text-center text-sm text-gray-600">
                      {['FLAIR', 'T1ce', 'T2'][idx]}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="mask" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Predicted Segmentation Mask</CardTitle>
            </CardHeader>
            <CardContent className="flex justify-center">
              {results.mask_image ? (
                <img
                  src={results.mask_image}
                  alt="Segmentation Mask"
                  className="max-w-md rounded-lg border border-gray-200"
                />
              ) : (
                <p className="text-gray-500">No mask available (model not loaded)</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="overlay" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>MRI with Tumor Overlay</CardTitle>
            </CardHeader>
            <CardContent className="flex justify-center">
              {results.overlay_image ? (
                <img
                  src={results.overlay_image}
                  alt="Overlay"
                  className="max-w-md rounded-lg border border-gray-200"
                />
              ) : (
                <p className="text-gray-500">No overlay available (model not loaded)</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="comparison" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Comparison View</CardTitle>
            </CardHeader>
            <CardContent>
              {results.comparison_images.length > 0 ? (
                <div className="grid grid-cols-3 gap-4">
                  {results.comparison_images.map((img, idx) => (
                    <div key={idx} className="space-y-2">
                      <img
                        src={img}
                        alt={`Comparison ${idx + 1}`}
                        className="w-full rounded-lg border border-gray-200"
                      />
                      <p className="text-center text-sm text-gray-600">
                        {['Original', 'Mask', 'Overlay'][idx]}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No comparison available (model not loaded)</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Statistics */}
      {Object.keys(results.statistics).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Tumor Region Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              {Object.entries(results.statistics).map(([label, stats]) => (
                <div key={label} className="stat-card">
                  <p className="stat-value">{stats.percentage.toFixed(1)}%</p>
                  <p className="stat-label">{label}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {stats.pixel_count.toLocaleString()} pixels
                  </p>
                </div>
              ))}
            </div>
            {results.statistics_chart && (
              <div className="flex justify-center">
                <img
                  src={results.statistics_chart}
                  alt="Statistics Chart"
                  className="max-w-lg rounded-lg"
                />
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

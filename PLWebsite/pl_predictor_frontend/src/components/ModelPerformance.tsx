'use client';

import { useState, useEffect } from 'react';
import { ModelPerformance as ModelPerformanceType, modelApi, PaginatedResponse } from '@/lib/api';
import { formatDate } from '@/lib/utils';

export default function ModelPerformance() {
  const [performance, setPerformance] = useState<ModelPerformanceType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPerformance = async () => {
      try {
        const response = await modelApi.getPerformance();
        // Handle paginated response from Django REST Framework
        const performanceData = response.data.results || response.data;
        setPerformance(Array.isArray(performanceData) ? performanceData : []);
      } catch (err: any) {
        setError(err.response?.data?.error || 'Failed to load model performance');
        setPerformance([]); // Ensure performance is always an array
      } finally {
        setLoading(false);
      }
    };

    fetchPerformance();
  }, []);

  const handleTrainModel = async () => {
    setLoading(true);
    try {
      await modelApi.train();
      // Refresh performance data
      const response = await modelApi.getPerformance();
      const performanceData = response.data.results || response.data;
      setPerformance(Array.isArray(performanceData) ? performanceData : []);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to train model');
      setPerformance([]); // Ensure performance is always an array
    } finally {
      setLoading(false);
    }
  };

  if (loading && performance.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Model Performance</h2>
        <button
          onClick={handleTrainModel}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Training...' : 'Train Model'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {!performance || !Array.isArray(performance) || performance.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">No model performance data available.</p>
          <p className="text-sm text-gray-500">Train the model to see performance metrics.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {performance.map((perf) => (
            <div key={perf.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-800">
                  {perf.model_version}
                </h3>
                <span className="text-sm text-gray-600">
                  {formatDate(perf.training_date)}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Accuracy</p>
                  <p className="text-xl font-bold text-blue-600">
                    {(perf.accuracy * 100).toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Precision</p>
                  <p className="text-xl font-bold text-green-600">
                    {(perf.precision * 100).toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Recall</p>
                  <p className="text-xl font-bold text-yellow-600">
                    {(perf.recall * 100).toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">F1 Score</p>
                  <p className="text-xl font-bold text-purple-600">
                    {(perf.f1_score * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Test Set Size:</span>{' '}
                    <span className="font-semibold">{perf.test_set_size}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Features:</span>{' '}
                    <span className="font-semibold">{perf.feature_count}</span>
                  </div>
                </div>
                {perf.notes && (
                  <div className="mt-2">
                    <p className="text-sm text-gray-600">{perf.notes}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


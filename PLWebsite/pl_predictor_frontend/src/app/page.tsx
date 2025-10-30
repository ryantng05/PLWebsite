'use client';

import { useState } from 'react';
import PredictionForm from '@/components/PredictionForm';
import PredictionCard from '@/components/PredictionCard';
import TeamStats from '@/components/TeamStats';
import ModelPerformance from '@/components/ModelPerformance';
import { PredictionResponse } from '@/lib/api';

type Tab = 'predict' | 'teams' | 'model';

export default function Home() {
  const [activeTab, setActiveTab] = useState<Tab>('predict');
  const [predictions, setPredictions] = useState<PredictionResponse[]>([]);

  const handlePredictionMade = (prediction: PredictionResponse) => {
    setPredictions([prediction, ...predictions]);
  };

  const tabs = [
    { id: 'predict' as Tab, label: 'Predict', icon: '⚽' },
    { id: 'teams' as Tab, label: 'Teams', icon: '📊' },
    { id: 'model' as Tab, label: 'Model', icon: '🤖' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-2">
            ⚽ Premier League Predictor
          </h1>
          <p className="text-lg text-gray-600">
            AI-powered match outcome predictions using machine learning
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-md mb-6">
          <div className="flex border-b border-gray-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 py-4 px-6 text-center font-semibold transition-colors ${
                  activeTab === tab.id
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="max-w-6xl mx-auto">
          {activeTab === 'predict' && (
            <div className="space-y-6">
              <PredictionForm onPredictionMade={handlePredictionMade} />
              
              {predictions.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">Recent Predictions</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {predictions.map((prediction, index) => (
                      <PredictionCard key={index} prediction={prediction} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'teams' && <TeamStats />}

          {activeTab === 'model' && <ModelPerformance />}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-600 text-sm">
          <p>Powered by Random Forest Machine Learning</p>
          <p className="mt-2">Data from Premier League historical matches</p>
        </div>
      </div>
    </div>
  );
}


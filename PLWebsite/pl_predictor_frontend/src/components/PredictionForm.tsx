'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { teamsApi, predictionsApi, Team, PredictionResponse, PaginatedResponse } from '@/lib/api';
import { formatDate } from '@/lib/utils';

interface PredictionFormProps {
  onPredictionMade: (prediction: PredictionResponse) => void;
}

export default function PredictionForm({ onPredictionMade }: PredictionFormProps) {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<number | null>(null);
  const [selectedOpponent, setSelectedOpponent] = useState<number | null>(null);
  const [matchDate, setMatchDate] = useState<string>('');
  const [venue, setVenue] = useState<'H' | 'A'>('H');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [teamsLoading, setTeamsLoading] = useState(true);
  
  // Load teams on component mount
  useEffect(() => {
    const loadTeams = async () => {
      try {
        setTeamsLoading(true);
        const response = await teamsApi.getAll();
        // Handle paginated response from Django REST Framework
        const teamsData = response.data.results || response.data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
      } catch (err: any) {
        setError('Failed to load teams');
        console.error('Error loading teams:', err);
        setTeams([]); // Ensure teams is always an array
      } finally {
        setTeamsLoading(false);
      }
    };

    loadTeams();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedTeam || !selectedOpponent || !matchDate) {
      setError('Please fill in all fields');
      return;
    }

    if (selectedTeam === selectedOpponent) {
      setError('Team and opponent must be different');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await predictionsApi.predict({
        team_id: selectedTeam,
        opponent_id: selectedOpponent,
        venue,
        match_date: matchDate,
      });
      
      onPredictionMade(response.data);
      
      // Reset form
      setSelectedTeam(null);
      setSelectedOpponent(null);
      setMatchDate('');
      setVenue('H');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to make prediction');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Predict Match Result</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Team
            </label>
            <select
              value={selectedTeam || ''}
              onChange={(e) => setSelectedTeam(Number(e.target.value))}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
              disabled={teamsLoading}
            >
              <option value="">
                {teamsLoading ? 'Loading teams...' : 'Select a team'}
              </option>
              {teams && Array.isArray(teams) && teams.map(team => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Opponent
            </label>
            <select
              value={selectedOpponent || ''}
              onChange={(e) => setSelectedOpponent(Number(e.target.value))}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
              disabled={teamsLoading}
            >
              <option value="">
                {teamsLoading ? 'Loading teams...' : 'Select opponent'}
              </option>
              {teams && Array.isArray(teams) && teams.map(team => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Match Date
            </label>
            <input
              type="date"
              value={matchDate}
              onChange={(e) => setMatchDate(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Venue
            </label>
            <select
              value={venue}
              onChange={(e) => setVenue(e.target.value as 'H' | 'A')}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="H">Home</option>
              <option value="A">Away</option>
            </select>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <Button
          type="submit"
          disabled={isLoading || teamsLoading || teams.length === 0}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-md disabled:opacity-50"
        >
          {isLoading ? 'Making Prediction...' : teamsLoading ? 'Loading Teams...' : 'Predict Match'}
        </Button>
      </form>
    </div>
  );
}


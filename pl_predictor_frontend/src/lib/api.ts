import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Team {
  id: number;
  name: string;
  matches_played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
  win_rate: number;
  avg_goals_scored: number;
  avg_goals_conceded: number;
}

export interface Match {
  id: number;
  date: string;
  team: string;
  opponent: string;
  venue: 'H' | 'A';
  result: 'W' | 'D' | 'L';
  goals_for: number;
  goals_against: number;
  team_xg: number;
  opponent_xg: number;
  possession: number;
  shots: number;
  shots_on_target: number;
  deep_passes: number;
  passes_completed_percentage: number;
}

export interface PredictionRequest {
  team_id: number;
  opponent_id: number;
  venue: 'H' | 'A';
  date: string;
}

export interface PredictionResponse {
  id: number;
  team: string;
  opponent: string;
  venue: 'H' | 'A';
  match_date: string;
  predicted_result: 'W' | 'D' | 'L';
  win_probability: number;
  draw_probability: number;
  loss_probability: number;
  confidence: number;
  created_at: string;
}

export interface Prediction {
  id: number;
  team: number;
  opponent: number;
  match_date: string;
  venue: 'H' | 'A';
  predicted_result: 'W' | 'D' | 'L';
  win_probability: number;
  draw_probability: number;
  loss_probability: number;
  confidence: number;
  actual_result?: 'W' | 'D' | 'L';
  is_correct?: boolean;
  created_at: string;
}

export interface ModelPerformance {
  id: number;
  model_version: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  training_date: string;
  test_set_size: number;
  feature_count: number;
  notes?: string;
}

export interface TeamStats {
  team: Team;
  win_rate: number;
  recent_form: string[];
  recent_matches: Match[];
}

// API response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// API functions
export const teamsApi = {
  getAll: () => api.get<PaginatedResponse<Team>>('/teams/'),
  getById: (id: number) => api.get<Team>(`/teams/${id}/`),
  getStats: (id: number) => api.get<TeamStats>(`/teams/${id}/stats/`),
};

export const matchesApi = {
  getAll: (params?: {
    team?: string;
    start_date?: string;
    end_date?: string;
  }) => api.get<Match[]>('/matches/', { params }),
  getById: (id: number) => api.get<Match>(`/matches/${id}/`),
};

export const predictionsApi = {
  getAll: () => api.get<Prediction[]>('/predictions/'),
  getById: (id: number) => api.get<Prediction>(`/predictions/${id}/`),
  predict: (data: PredictionRequest) => 
    api.post<PredictionResponse>('/predict/', data),
};

export const modelApi = {
  train: () => api.post('/model/train/'),
  getInfo: () => api.get('/model/info/'),
  getPerformance: () => api.get<PaginatedResponse<ModelPerformance>>('/model/performance/'),
};

export default api;


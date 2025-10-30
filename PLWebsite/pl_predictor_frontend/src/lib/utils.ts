import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function formatPercentage(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export function getResultColor(result: 'W' | 'D' | 'L'): string {
  switch (result) {
    case 'W':
      return 'text-green-600 bg-green-100';
    case 'D':
      return 'text-yellow-600 bg-yellow-100';
    case 'L':
      return 'text-red-600 bg-red-100';
  }
}

export function getResultText(result: 'W' | 'D' | 'L'): string {
  switch (result) {
    case 'W':
      return 'Win';
    case 'D':
      return 'Draw';
    case 'L':
      return 'Loss';
  }
}


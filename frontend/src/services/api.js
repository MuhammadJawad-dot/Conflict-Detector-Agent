import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const searchGoogle = async (query) => {
    const response = await api.post('/search/google', { query });
    return response.data.results;
};

export const searchReddit = async (query) => {
    const response = await api.post('/search/reddit', { query });
    return response.data;
};

export const analyzeConflicts = async (googleResults, redditResults) => {
    const response = await api.post('/analyze/conflicts', {
        google_results: googleResults,
        reddit_results: redditResults,
    });
    return response.data;
};

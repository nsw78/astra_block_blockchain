import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_ASTRA_API_URL || 'http://localhost:8080';

export interface ContractAnalysisResult {
  // Define based on backend response, e.g.
  risk_score?: number;
  issues?: string[];
  [key: string]: any;
}

export interface RagSearchResult {
  query: string;
  results: any[];
}

export const analyzeContract = async (address: string): Promise<ContractAnalysisResult> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/analyze_contract`, {
      params: { address },
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to analyze contract');
  }
};

export const searchRag = async (query: string): Promise<RagSearchResult> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/rag_query`, {
      params: { q: query },
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to perform RAG search');
  }
};
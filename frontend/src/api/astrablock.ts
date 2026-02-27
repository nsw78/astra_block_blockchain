import axios, { type AxiosInstance, type AxiosError, type AxiosResponse } from 'axios';

// ── Configuration ──

// Empty string = same origin (works with nginx reverse proxy in Docker)
const API_BASE_URL = import.meta.env.VITE_ASTRA_API_URL || '';
const API_VERSION = '/api/v1';

// ── Types ──

export interface Finding {
  pattern: string;
  snippet: string;
}

export interface ContractRiskAnalysis {
  score: number;
  findings: Finding[];
  error?: string;
}

export interface ContractAnalysisResult {
  address: string;
  source_available: boolean;
  analysis: ContractRiskAnalysis;
}

export interface RagResult {
  doc_id: string;
  score: number;
}

export interface RagSearchResponse {
  query: string;
  results: RagResult[];
}

export interface IndexDocsRequest {
  docs: string[];
  ids?: string[];
}

export interface IndexDocsResponse {
  indexed: number;
  total_docs: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
}

export interface ApiKeyInfo {
  key: string;
  name: string | null;
  created_at: string | null;
}

export interface ErrorResponse {
  success: false;
  error_code: string;
  message: string;
  details?: unknown;
  request_id?: string;
}

// ── API Client ──

class AstraBlockClient {
  private http: AxiosInstance;

  constructor(baseURL: string = API_BASE_URL, apiKey?: string) {
    this.http = axios.create({
      baseURL: `${baseURL}${API_VERSION}`,
      timeout: 30_000,
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey ? { 'X-API-Key': apiKey } : {}),
      },
    });

    this.http.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError<ErrorResponse>) => {
        const msg = error.response?.data?.message || error.message;
        return Promise.reject(new Error(msg));
      },
    );
  }

  setApiKey(key: string): void {
    this.http.defaults.headers.common['X-API-Key'] = key;
  }

  // ── Health ──

  async health(): Promise<HealthResponse> {
    const { data } = await this.http.get<HealthResponse>('/health');
    return data;
  }

  // ── Contracts ──

  async analyzeContract(address: string): Promise<ContractAnalysisResult> {
    const { data } = await this.http.get<ContractAnalysisResult>('/contracts/analyze', {
      params: { address },
    });
    return data;
  }

  // ── Documents / RAG ──

  async searchDocuments(query: string, k: number = 5): Promise<RagSearchResponse> {
    const { data } = await this.http.get<RagSearchResponse>('/documents/search', {
      params: { q: query, k },
    });
    return data;
  }

  async indexDocuments(req: IndexDocsRequest): Promise<IndexDocsResponse> {
    const { data } = await this.http.post<IndexDocsResponse>('/documents/', req);
    return data;
  }

  async listDocuments(): Promise<{ docs: string[] }> {
    const { data } = await this.http.get<{ docs: string[] }>('/documents/');
    return data;
  }

  // ── Admin ──

  async createApiKey(name?: string): Promise<{ key: string; name: string | null }> {
    const { data } = await this.http.post('/admin/keys', { name });
    return data;
  }

  async listApiKeys(): Promise<{ keys: ApiKeyInfo[] }> {
    const { data } = await this.http.get('/admin/keys');
    return data;
  }

  async deleteApiKey(key: string): Promise<{ deleted: boolean }> {
    const { data } = await this.http.delete(`/admin/keys/${key}`);
    return data;
  }
}

// ── Singleton export ──

export const astraClient = new AstraBlockClient();

// ── Legacy compat (kept for existing components) ──

export const analyzeContract = (address: string) => astraClient.analyzeContract(address);
export const searchRag = (query: string) => astraClient.searchDocuments(query);

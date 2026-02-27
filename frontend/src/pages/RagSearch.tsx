import React, { useState } from 'react';
import { searchRag, type RagSearchResponse } from '../api/astrablock';

const RagSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<RagSearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchHistory, setSearchHistory] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await searchRag(query.trim());
      setResult(data);
      setSearchHistory(prev => [query.trim(), ...prev.slice(0, 4)]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">RAG Search</h1>
        <p className="text-gray-600 mb-6">
          Perform intelligent semantic searches across indexed documents using Retrieval-Augmented Generation technology.
        </p>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                Search Query
              </label>
              <input
                type="text"
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your question or search term (e.g., 'smart contract vulnerabilities')"
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:opacity-50 font-medium transition-colors"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </div>
        </form>

        {searchHistory.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-700 mb-3">Recent Searches</h3>
            <div className="flex flex-wrap gap-2">
              {searchHistory.map((q, index) => (
                <button
                  key={index}
                  onClick={() => setQuery(q)}
                  className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors"
                >
                  {q.length > 20 ? q.slice(0, 20) + '...' : q}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          <div className="flex items-center">
            <span className="mr-2">!</span>
            {error}
          </div>
        </div>
      )}

      {result && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold text-gray-800">Search Results</h2>
            <div className="text-sm text-gray-500">
              Found {result.results.length} result{result.results.length !== 1 ? 's' : ''}
            </div>
          </div>

          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
            <h3 className="font-medium text-blue-800 mb-1">Query</h3>
            <p className="text-blue-700">"{result.query}"</p>
          </div>

          <div className="space-y-4">
            {result.results.map((item, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-gray-900">Doc: {item.doc_id}</h4>
                  <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                    Score: {item.score.toFixed(4)}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {result.results.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-600">No results found for your query</p>
              <p className="text-sm text-gray-500 mt-1">Try refining your search terms</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RagSearch;

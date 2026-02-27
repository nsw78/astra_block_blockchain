import React, { useState } from 'react';
import { analyzeContract, ContractAnalysisResult } from '../api/astrablock';

const ContractAnalysis: React.FC = () => {
  const [address, setAddress] = useState('');
  const [result, setResult] = useState<ContractAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisHistory, setAnalysisHistory] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!address.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeContract(address.trim());
      setResult(data);
      setAnalysisHistory(prev => [address.trim(), ...prev.slice(0, 4)]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score?: number) => {
    if (score === undefined || score === null) return 'text-gray-600';
    if (score < 30) return 'text-green-600';
    if (score < 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRiskLevel = (score?: number) => {
    if (score === undefined || score === null) return 'Unknown';
    if (score < 30) return 'Low';
    if (score < 70) return 'Medium';
    return 'High';
  };

  const riskScore = result?.analysis?.score ?? 0;
  const findings = result?.analysis?.findings ?? [];

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Contract Analysis</h1>
        <p className="text-gray-600 mb-6">
          Perform comprehensive security analysis on smart contracts with enterprise-grade risk assessment.
        </p>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-2">
                Contract Address
              </label>
              <input
                type="text"
                id="address"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Enter smart contract address (e.g., 0x...)"
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
                {loading ? 'Analyzing...' : 'Analyze Contract'}
              </button>
            </div>
          </div>
        </form>

        {analysisHistory.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-700 mb-3">Recent Analyses</h3>
            <div className="flex flex-wrap gap-2">
              {analysisHistory.map((addr, index) => (
                <button
                  key={index}
                  onClick={() => setAddress(addr)}
                  className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors"
                >
                  {addr.slice(0, 10)}...
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
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Risk Summary */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Risk Assessment</h2>
            <div className="text-center">
              <div className={`text-4xl font-bold ${getRiskColor(riskScore)} mb-2`}>
                {riskScore}%
              </div>
              <div className={`text-lg font-medium ${getRiskColor(riskScore)}`}>
                {getRiskLevel(riskScore)} Risk
              </div>
            </div>
            <div className="mt-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Security Score</span>
                <span className="text-sm font-medium">{100 - riskScore}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${100 - riskScore}%` }}
                ></div>
              </div>
            </div>
            {!result.source_available && (
              <div className="mt-4 p-2 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-700">
                Source code not available on Etherscan
              </div>
            )}
          </div>

          {/* Findings */}
          <div className="bg-white rounded-lg shadow-md p-6 lg:col-span-2">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Analysis Details</h2>
            {findings.length > 0 ? (
              <div className="space-y-3">
                {findings.map((finding, index) => (
                  <div key={index} className="flex items-start p-3 bg-red-50 border border-red-200 rounded-md">
                    <span className="text-red-500 mr-3 mt-0.5">!</span>
                    <div>
                      <p className="text-red-800 font-medium">Pattern: {finding.pattern}</p>
                      <p className="text-red-700 text-sm font-mono">{finding.snippet}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <span className="text-4xl mb-2 block">OK</span>
                <p className="text-gray-600">No critical issues found</p>
              </div>
            )}

            {result.analysis?.error && (
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md text-sm text-yellow-800">
                {result.analysis.error}
              </div>
            )}

            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-700 mb-3">Raw Analysis Data</h3>
              <div className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                <pre className="text-sm text-gray-800">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContractAnalysis;

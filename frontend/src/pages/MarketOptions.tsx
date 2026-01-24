import React, { useState } from 'react';

interface OptionAnalysisResult {
  optionType: string;
  strikePrice: number;
  expirationDate: string;
  riskMetrics: {
    delta: number;
    gamma: number;
    theta: number;
    vega: number;
    rho: number;
  };
  recommendations: string[];
}

const MarketOptions: React.FC = () => {
  const [formData, setFormData] = useState({
    underlyingAsset: '',
    strikePrice: '',
    expirationDate: '',
    optionType: 'call',
    volatility: '',
    riskFreeRate: '',
    currentPrice: '',
  });
  const [result, setResult] = useState<OptionAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Simulate analysis - in real app, call API
    try {
      // Mock result for demonstration
      const mockResult: OptionAnalysisResult = {
        optionType: formData.optionType,
        strikePrice: parseFloat(formData.strikePrice),
        expirationDate: formData.expirationDate,
        riskMetrics: {
          delta: Math.random() * 2 - 1,
          gamma: Math.random() * 0.5,
          theta: Math.random() * -0.1,
          vega: Math.random() * 0.2,
          rho: Math.random() * 0.1,
        },
        recommendations: [
          'Monitor volatility changes closely',
          'Consider hedging strategies',
          'Review expiration timing',
        ],
      };
      setResult(mockResult);
    } catch (err) {
      setError('Failed to analyze market options');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Market Options Analysis</h1>
        <p className="text-gray-600 mb-6">
          Analyze financial options contracts with advanced risk metrics and enterprise-grade insights.
        </p>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Underlying Asset
            </label>
            <input
              type="text"
              name="underlyingAsset"
              value={formData.underlyingAsset}
              onChange={handleInputChange}
              placeholder="e.g., AAPL, BTC"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Current Price
            </label>
            <input
              type="number"
              name="currentPrice"
              value={formData.currentPrice}
              onChange={handleInputChange}
              placeholder="100.00"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Strike Price
            </label>
            <input
              type="number"
              name="strikePrice"
              value={formData.strikePrice}
              onChange={handleInputChange}
              placeholder="105.00"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Expiration Date
            </label>
            <input
              type="date"
              name="expirationDate"
              value={formData.expirationDate}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Option Type
            </label>
            <select
              name="optionType"
              value={formData.optionType}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="call">Call</option>
              <option value="put">Put</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Volatility (%)
            </label>
            <input
              type="number"
              name="volatility"
              value={formData.volatility}
              onChange={handleInputChange}
              placeholder="20.00"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Risk-Free Rate (%)
            </label>
            <input
              type="number"
              name="riskFreeRate"
              value={formData.riskFreeRate}
              onChange={handleInputChange}
              placeholder="5.00"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="md:col-span-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:opacity-50 font-medium"
            >
              {loading ? 'Analyzing...' : 'Analyze Options'}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-6 text-gray-800">Analysis Results</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-lg font-medium text-gray-700 mb-3">Option Details</h3>
              <div className="space-y-2">
                <p><span className="font-medium">Type:</span> {result.optionType.toUpperCase()}</p>
                <p><span className="font-medium">Strike Price:</span> ${result.strikePrice.toFixed(2)}</p>
                <p><span className="font-medium">Expiration:</span> {new Date(result.expirationDate).toLocaleDateString()}</p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium text-gray-700 mb-3">Risk Metrics (Greeks)</h3>
              <div className="space-y-2">
                <p><span className="font-medium">Delta:</span> {result.riskMetrics.delta.toFixed(4)}</p>
                <p><span className="font-medium">Gamma:</span> {result.riskMetrics.gamma.toFixed(4)}</p>
                <p><span className="font-medium">Theta:</span> {result.riskMetrics.theta.toFixed(4)}</p>
                <p><span className="font-medium">Vega:</span> {result.riskMetrics.vega.toFixed(4)}</p>
                <p><span className="font-medium">Rho:</span> {result.riskMetrics.rho.toFixed(4)}</p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-gray-700 mb-3">Recommendations</h3>
            <ul className="list-disc list-inside space-y-1 text-gray-600">
              {result.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketOptions;
import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  const stats = [
    { label: 'Contracts Analyzed', value: '1,234', change: '+12%', icon: '📄' },
    { label: 'Risk Alerts', value: '23', change: '-5%', icon: '⚠️' },
    { label: 'Market Options', value: '89', change: '+8%', icon: '📈' },
    { label: 'Search Queries', value: '567', change: '+15%', icon: '🔍' },
  ];

  const recentActivities = [
    { action: 'Contract analyzed', target: '0x1234...abcd', time: '2 minutes ago' },
    { action: 'Options evaluated', target: 'AAPL Call 150', time: '5 minutes ago' },
    { action: 'RAG search performed', target: 'smart contract risks', time: '10 minutes ago' },
    { action: 'Report generated', target: 'Q4 Analysis', time: '1 hour ago' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleString()}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className={`text-sm ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                  {stat.change} from last month
                </p>
              </div>
              <div className="text-3xl">{stat.icon}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/analyze"
            className="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <span className="text-2xl mr-3">📄</span>
            <div>
              <h3 className="font-medium text-gray-900">Analyze Contract</h3>
              <p className="text-sm text-gray-600">Check smart contract security</p>
            </div>
          </Link>
          <Link
            to="/market-options"
            className="flex items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
          >
            <span className="text-2xl mr-3">📈</span>
            <div>
              <h3 className="font-medium text-gray-900">Market Options</h3>
              <p className="text-sm text-gray-600">Evaluate financial options</p>
            </div>
          </Link>
          <Link
            to="/search"
            className="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
          >
            <span className="text-2xl mr-3">🔍</span>
            <div>
              <h3 className="font-medium text-gray-900">RAG Search</h3>
              <p className="text-sm text-gray-600">Semantic document search</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          {recentActivities.map((activity, index) => (
            <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
              <div>
                <p className="font-medium text-gray-900">{activity.action}</p>
                <p className="text-sm text-gray-600">{activity.target}</p>
              </div>
              <span className="text-sm text-gray-500">{activity.time}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Enterprise Features */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-md p-6 text-white">
        <h2 className="text-xl font-semibold mb-2">Enterprise Features</h2>
        <p className="mb-4">Unlock advanced analytics, custom reporting, and priority support with AstraBlock Enterprise.</p>
        <button className="bg-white text-blue-600 px-4 py-2 rounded-md font-medium hover:bg-gray-100 transition-colors">
          Upgrade to Enterprise
        </button>
      </div>
    </div>
  );
};

export default Home;
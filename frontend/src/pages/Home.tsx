import React from 'react';

const Home: React.FC = () => {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to AstraBlock</h1>
      <p className="text-lg text-gray-600 mb-8">
        AstraBlock is a platform for analyzing smart contracts and performing semantic searches using Retrieval-Augmented Generation (RAG).
      </p>
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-2">Contract Analysis</h2>
          <p className="text-gray-600 mb-4">Analyze smart contracts for potential risks and issues.</p>
          <a href="/analyze" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Analyze Now</a>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-2">RAG Search</h2>
          <p className="text-gray-600 mb-4">Perform semantic searches on indexed documents using AI.</p>
          <a href="/search" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Search Now</a>
        </div>
      </div>
    </div>
  );
};

export default Home;
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import ContractAnalysis from './pages/ContractAnalysis';
import RagSearch from './pages/RagSearch';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-blue-600 p-4">
          <div className="container mx-auto flex justify-between items-center">
            <Link to="/" className="text-white text-xl font-bold">AstraBlock</Link>
            <div className="space-x-4">
              <Link to="/" className="text-white hover:text-blue-200">Home</Link>
              <Link to="/analyze" className="text-white hover:text-blue-200">Analyze Contract</Link>
              <Link to="/search" className="text-white hover:text-blue-200">RAG Search</Link>
            </div>
          </div>
        </nav>
        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyze" element={<ContractAnalysis />} />
            <Route path="/search" element={<RagSearch />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
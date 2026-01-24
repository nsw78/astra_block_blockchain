import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import ContractAnalysis from './pages/ContractAnalysis';
import MarketOptions from './pages/MarketOptions';
import RagSearch from './pages/RagSearch';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<ContractAnalysis />} />
          <Route path="/market-options" element={<MarketOptions />} />
          <Route path="/search" element={<RagSearch />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
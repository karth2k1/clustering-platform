import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AIMode from './components/AIMode/AIMode';
import AdvancedMode from './components/AdvancedMode/AdvancedMode';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function Navigation() {
  const location = useLocation();
  
  return (
    <nav className="navbar">
      <div className="nav-container">
        <h1 className="nav-title">Clustering Platform</h1>
        <div className="nav-links">
          <Link 
            to="/ai-mode" 
            className={location.pathname === '/ai-mode' ? 'active' : ''}
          >
            AI-Assisted Mode
          </Link>
          <Link 
            to="/advanced-mode" 
            className={location.pathname === '/advanced-mode' ? 'active' : ''}
          >
            Advanced Mode
          </Link>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="app">
          <Navigation />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<AIMode />} />
              <Route path="/ai-mode" element={<AIMode />} />
              <Route path="/advanced-mode" element={<AdvancedMode />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;

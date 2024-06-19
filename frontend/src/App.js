import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Sidebar from './components/Sidebar';
import Feed from './components/feed';
import ProfileDashboard from './components/dashboard';
import Search from './components/search';

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <div style={{ flexGrow: 1 }}>
        <Search />
    <Routes>
      <Route path="/" element={<Feed />} />
      <Route path="/profile/:username" element={<ProfileDashboard />} />
    </Routes>
    </div>
      </div>
    </Router>
  );
}

export default App;

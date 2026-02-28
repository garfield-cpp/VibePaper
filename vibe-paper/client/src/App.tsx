import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PaperEditor from './pages/PaperEditor';
import AIConversation from './pages/AIConversation';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PaperListPage from './pages/PaperListPage';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen w-full bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/papers" element={
              <ProtectedRoute>
                <PaperListPage />
              </ProtectedRoute>
            } />
            <Route path="/editor/:id?" element={
              <ProtectedRoute>
                <PaperEditor />
              </ProtectedRoute>
            } />
            <Route path="/ai" element={
              <ProtectedRoute>
                <AIConversation />
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

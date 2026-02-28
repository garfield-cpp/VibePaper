import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
  const { user } = useAuth();

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold mb-4">Vibe Paper</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          AI 辅助论文写作工具
        </p>
      </div>
      
      {user ? (
        // 已登录用户
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Link to="/papers" className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-center">
              <div className="text-4xl mb-4">📄</div>
              <h2 className="text-xl font-semibold mb-2">我的论文</h2>
              <p className="text-gray-600 dark:text-gray-400">
                查看和管理你的论文
              </p>
            </div>
          </Link>
          
          <Link to="/editor" className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-center">
              <div className="text-4xl mb-4">✏️</div>
              <h2 className="text-xl font-semibold mb-2">新建论文</h2>
              <p className="text-gray-600 dark:text-gray-400">
                创建一篇新论文
              </p>
            </div>
          </Link>
        </div>
      ) : (
        // 未登录用户
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Link to="/login" className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-center">
              <div className="text-4xl mb-4">🔐</div>
              <h2 className="text-xl font-semibold mb-2">登录</h2>
              <p className="text-gray-600 dark:text-gray-400">
                登录后管理你的论文
              </p>
            </div>
          </Link>
          
          <Link to="/register" className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-center">
              <div className="text-4xl mb-4">📝</div>
              <h2 className="text-xl font-semibold mb-2">注册</h2>
              <p className="text-gray-600 dark:text-gray-400">
                创建新账号，开始使用 Vibe Paper
              </p>
            </div>
          </Link>
        </div>
      )}
    </div>
  );
};

export default HomePage;
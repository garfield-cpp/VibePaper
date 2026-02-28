import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface Paper {
  id: string;
  title: string;
  content: string;
  outline: string | null;
  user_id: string;
  created_at: string;
  updated_at: string;
}

const PaperListPage = () => {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchPapers();
  }, []);

  const fetchPapers = async () => {
    try {
      const response = await fetch('http://localhost:8000/papers', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setPapers(data);
      } else {
        setError('获取论文列表失败');
      }
    } catch (err) {
      setError('网络错误，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (paperId: string) => {
    if (window.confirm('确定要删除这篇论文吗？')) {
      try {
        const response = await fetch(`http://localhost:8000/papers/${paperId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        if (response.ok) {
          fetchPapers();
        } else {
          setError('删除论文失败');
        }
      } catch (err) {
        setError('网络错误，请稍后重试');
      }
    }
  };

  const handleCreatePaper = async () => {
    try {
      const response = await fetch('http://localhost:8000/papers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          title: '新论文',
          content: '',
          outline: null,
        }),
      });
      if (response.ok) {
        const newPaper = await response.json();
        navigate(`/editor/${newPaper.id}`);
      } else {
        setError('创建论文失败');
      }
    } catch (err) {
      setError('网络错误，请稍后重试');
    }
  };

  if (loading) {
    return <div className="container mx-auto px-4 py-8">加载中...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* 顶部导航栏 */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">我的论文</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm">欢迎，{user?.username}</span>
          <button
            onClick={logout}
            className="text-blue-600 dark:text-blue-400 hover:underline"
          >
            注销
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 p-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* 操作按钮 */}
      <div className="mb-6">
        <button
          onClick={handleCreatePaper}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          创建新论文
        </button>
      </div>

      {/* 论文列表 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {papers.map((paper) => (
          <div key={paper.id} className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-2">{paper.title}</h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
              创建于: {new Date(paper.created_at).toLocaleString()}
            </p>
            <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
              {paper.content.substring(0, 100)}...
            </p>
            <div className="flex justify-between">
              <Link
                to={`/editor/${paper.id}`}
                className="text-blue-600 dark:text-blue-400 hover:underline"
              >
                编辑
              </Link>
              <button
                onClick={() => handleDelete(paper.id)}
                className="text-red-600 dark:text-red-400 hover:underline"
              >
                删除
              </button>
            </div>
          </div>
        ))}
      </div>

      {papers.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 dark:text-gray-400">还没有论文，点击"创建新论文"开始写作</p>
        </div>
      )}
    </div>
  );
};

export default PaperListPage;

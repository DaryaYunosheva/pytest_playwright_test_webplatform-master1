import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getNewsDetail, getComments, createComment } from '../services/news';
import { useAuth } from '../context/AuthContext';

const NewsDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [news, setNews] = useState<any>(null);
  const [comments, setComments] = useState<any[]>([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [newsData, commentsData] = await Promise.all([
          getNewsDetail(Number(id)),
          getComments(Number(id))
        ]);
        setNews(newsData);
        setComments(commentsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    try {
      const comment = await createComment(Number(id), newComment);
      setComments([comment, ...comments]);
      setNewComment('');
    } catch (error) {
      console.error('Error creating comment:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  if (!news) return <div className="text-center py-12">Новость не найдена</div>;

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <h1 className="text-4xl font-bold mb-4">{news.title}</h1>
      {news.subtitle && <h2 className="text-xl text-gray-600 mb-4">{news.subtitle}</h2>}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-sm text-gray-500">{news.author.first_name} {news.author.last_name}</span>
        <span className="text-sm text-gray-400">•</span>
        <span className="text-sm text-gray-500">{new Date(news.created_at).toLocaleDateString()}</span>
      </div>
      {news.image_path && (
        <img src={`http://backend:8888${news.image_path}`} alt={news.title} className="w-full rounded-lg mb-6" />
      )}
      <div className="prose max-w-none">
        <p className="whitespace-pre-wrap">{news.text}</p>
      </div>
      <div className="flex gap-2 my-6">
        {news.tags.map((tag: any) => (
          <span key={tag.id} className="badge badge-outline">{tag.name}</span>
        ))}
      </div>
      <div className="divider">Комментарии ({comments.length})</div>
      {isAuthenticated && (
        <form onSubmit={handleAddComment} className="mb-6">
          <textarea className="textarea textarea-bordered w-full" placeholder="Оставьте комментарий..." value={newComment} onChange={(e) => setNewComment(e.target.value)} required />
          <button type="submit" className="btn btn-primary mt-2">Отправить</button>
        </form>
      )}
      <div className="space-y-4">
        {comments.map((comment) => (
          <div key={comment.id} className="card bg-base-100 shadow">
            <div className="card-body">
              <div className="flex items-center gap-2">
                <span className="font-semibold">{comment.author.first_name} {comment.author.last_name}</span>
                <span className="text-sm text-gray-400">{new Date(comment.created_at).toLocaleDateString()}</span>
              </div>
              <p>{comment.text}</p>
            </div>
          </div>
        ))}
        {comments.length === 0 && <p className="text-center text-gray-500">Пока нет комментариев</p>}
      </div>
    </div>
  );
};

export default NewsDetail;

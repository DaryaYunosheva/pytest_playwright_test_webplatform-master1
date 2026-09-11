import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createNews } from '../services/news';

const NewsCreate: React.FC = () => {
  const [formData, setFormData] = useState({
    title: '',
    subtitle: '',
    text: '',
    tags: '',
  });
  const [image, setImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await createNews({
        ...formData,
        image: image || undefined,
      });
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания новости');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <h1 className="text-3xl font-bold mb-6">Создать новость</h1>
      {error && <div className="alert alert-error mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Заголовок *</span></label>
          <input type="text" name="title" className="input input-bordered" value={formData.title} onChange={handleChange} required />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Подзаголовок</span></label>
          <input type="text" name="subtitle" className="input input-bordered" value={formData.subtitle} onChange={handleChange} />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Текст *</span></label>
          <textarea name="text" className="textarea textarea-bordered h-40" value={formData.text} onChange={handleChange} required />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Теги (через запятую)</span></label>
          <input type="text" name="tags" className="input input-bordered" placeholder="технологии, наука, спорт" value={formData.tags} onChange={handleChange} />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Изображение</span></label>
          <input type="file" className="file-input file-input-bordered w-full" accept="image/*" onChange={handleFileChange} />
        </div>
        <button type="submit" className="btn btn-primary w-full" disabled={loading}>
          {loading ? <span className="loading loading-spinner"></span> : 'Создать'}
        </button>
      </form>
    </div>
  );
};

export default NewsCreate;

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { updateUser, uploadPhoto } from '../services/auth';

const Profile: React.FC = () => {
  const { user, isAuthenticated, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
    if (user) {
      setFormData({
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        phone: user.phone || '',
        password: '',
      });
    }
  }, [isAuthenticated, user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccess('');
    try {
      await updateUser(formData);
      await refreshUser();
      setSuccess('Профиль обновлён');
      setFormData({ ...formData, password: '' });
    } catch (err) {
      console.error('Error updating profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      try {
        await uploadPhoto(e.target.files[0]);
        await refreshUser();
      } catch (err) {
        console.error('Error uploading photo:', err);
      }
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Профиль</h1>
      {success && <div className="alert alert-success mb-4">{success}</div>}

      <div className="card bg-base-100 shadow-xl mb-6">
        <div className="card-body items-center">
          {user?.photo_path ? (
            <img src={`http://backend:8888${user.photo_path}`} alt="Фото" className="w-32 h-32 rounded-full object-cover" />
          ) : (
            <div className="avatar placeholder">
              <div className="bg-neutral text-neutral-content w-32 rounded-full">
                <span className="text-3xl">{user?.first_name?.[0] || 'U'}</span>
              </div>
            </div>
          )}
          <input type="file" className="file-input file-input-bordered max-w-xs mt-4" accept="image/*" onChange={handlePhotoUpload} />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="card bg-base-100 shadow-xl">
        <div className="card-body space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="form-control">
              <label className="label"><span className="label-text">Имя</span></label>
              <input type="text" name="first_name" className="input input-bordered" value={formData.first_name} onChange={handleChange} required />
            </div>
            <div className="form-control">
              <label className="label"><span className="label-text">Фамилия</span></label>
              <input type="text" name="last_name" className="input input-bordered" value={formData.last_name} onChange={handleChange} required />
            </div>
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Email</span></label>
            <input type="email" name="email" className="input input-bordered" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Телефон</span></label>
            <input type="tel" name="phone" className="input input-bordered" value={formData.phone} onChange={handleChange} />
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Новый пароль (оставьте пустым, чтобы не менять)</span></label>
            <input type="password" name="password" className="input input-bordered" value={formData.password} onChange={handleChange} minLength={6} />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? <span className="loading loading-spinner"></span> : 'Сохранить'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Profile;

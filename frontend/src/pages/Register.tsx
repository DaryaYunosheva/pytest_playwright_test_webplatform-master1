import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../services/auth';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await register(formData);
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="card w-96 bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title justify-center mb-4">Регистрация</h2>
          {error && <div className="alert alert-error">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-control">
              <label className="label"><span className="label-text">Имя</span></label>
              <input type="text" name="first_name" className="input input-bordered" value={formData.first_name} onChange={handleChange} required />
            </div>
            <div className="form-control mt-3">
              <label className="label"><span className="label-text">Фамилия</span></label>
              <input type="text" name="last_name" className="input input-bordered" value={formData.last_name} onChange={handleChange} required />
            </div>
            <div className="form-control mt-3">
              <label className="label"><span className="label-text">Email</span></label>
              <input type="email" name="email" className="input input-bordered" value={formData.email} onChange={handleChange} required />
            </div>
            <div className="form-control mt-3">
              <label className="label"><span className="label-text">Телефон</span></label>
              <input type="tel" name="phone" className="input input-bordered" value={formData.phone} onChange={handleChange} />
            </div>
            <div className="form-control mt-3">
              <label className="label"><span className="label-text">Пароль</span></label>
              <input type="password" name="password" className="input input-bordered" value={formData.password} onChange={handleChange} required minLength={6} />
            </div>
            <button type="submit" className="btn btn-primary w-full mt-6" disabled={loading}>
              {loading ? <span className="loading loading-spinner"></span> : 'Зарегистрироваться'}
            </button>
          </form>
          <p className="text-center mt-4">
            Уже есть аккаунт? <Link to="/login" className="link link-primary">Войти</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="navbar bg-base-100 shadow-lg px-4">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">📰 NewsPlatform</Link>
      </div>

      <div className="flex-none gap-2">
        {isAuthenticated ? (
          <>
            <Link to="/news/create" className="btn btn-primary">+ Добавить новость</Link>
            <div className="dropdown dropdown-end">
              <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
                {user?.photo_path ? (
                  <div className="w-10 rounded-full">
                    <img src={`http://backend:8888${user.photo_path}`} alt="Avatar" />
                  </div>
                ) : (
                  <div className="avatar placeholder">
                    <div className="bg-neutral text-neutral-content w-10 rounded-full">
                      <span>{user?.first_name?.[0] || 'U'}</span>
                    </div>
                  </div>
                )}
              </div>
              <ul tabIndex={0} className="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                <li><Link to="/profile">Профиль</Link></li>
                <li><button onClick={handleLogout}>Выйти</button></li>
              </ul>
            </div>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-ghost">Войти</Link>
            <Link to="/register" className="btn btn-primary">Регистрация</Link>
          </>
        )}
      </div>
    </div>
  );
};

export default Navbar;

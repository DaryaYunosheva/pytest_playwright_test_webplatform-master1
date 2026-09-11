import api from './api';

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  password: string;
}

export const login = async (data: LoginData) => {
  const formData = new FormData();
  formData.append('username', data.username);
  formData.append('password', data.password);
  
  const response = await api.post('/api/auth/login', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const register = async (data: RegisterData) => {
  const response = await api.post('/api/auth/register', data);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/api/users/me');
  return response.data;
};

export const updateUser = async (data: Partial<RegisterData>) => {
  const response = await api.put('/api/users/me', data);
  return response.data;
};

export const uploadPhoto = async (file: File) => {
  const formData = new FormData();
  formData.append('photo', file);
  const response = await api.post('/api/users/me/photo', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

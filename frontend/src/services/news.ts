import api from './api';

export interface NewsItem {
  id: number;
  title: string;
  subtitle?: string;
  text: string;
  image_path?: string;
  author: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    photo_path?: string;
  };
  tags: Array<{ id: number; name: string }>;
  created_at: string;
  comments_count: number;
}

export interface PaginatedNews {
  items: NewsItem[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export const getNews = async (page = 1, perPage = 10, tag?: string, search?: string) => {
  const params = new URLSearchParams();
  params.append('page', page.toString());
  params.append('per_page', perPage.toString());
  if (tag) params.append('tag', tag);
  if (search) params.append('search', search);
  
  const response = await api.get(`/api/news/?${params.toString()}`);
  return response.data as PaginatedNews;
};

export const getNewsDetail = async (id: number) => {
  const response = await api.get(`/api/news/${id}`);
  return response.data as NewsItem;
};

export const createNews = async (data: {
  title: string;
  subtitle?: string;
  text: string;
  tags?: string;
  image?: File;
}) => {
  const formData = new FormData();
  formData.append('title', data.title);
  if (data.subtitle) formData.append('subtitle', data.subtitle);
  formData.append('text', data.text);
  if (data.tags) formData.append('tags', data.tags);
  if (data.image) formData.append('image', data.image);
  
  const response = await api.post('/api/news/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const getComments = async (newsId: number) => {
  const response = await api.get(`/api/news/${newsId}/comments`);
  return response.data;
};

export const createComment = async (newsId: number, text: string) => {
  const response = await api.post(`/api/news/${newsId}/comments`, { text });
  return response.data;
};

import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Link } from 'react-router-dom';
import { getNews, NewsItem } from '../services/news';

const NewsList: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const abortControllerRef = useRef<AbortController | null>(null);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1); // Reset to first page on new search
    }, 500); // Wait 500ms after user stops typing

    return () => clearTimeout(timer);
  }, [search]);

  // Fetch news with debounced search
  useEffect(() => {
    const fetchNews = async () => {
      // Cancel previous request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      const abortController = new AbortController();
      abortControllerRef.current = abortController;

      setLoading(true);
      try {
        const data = await getNews(page, 10, undefined, debouncedSearch || undefined);
        setNews(data.items);
        setTotalPages(data.total_pages);
      } catch (error: any) {
        // Don't show error for aborted requests
        if (error.name !== 'AbortError') {
          console.error('Error fetching news:', error);
        }
      } finally {
        if (abortControllerRef.current === abortController) {
          setLoading(false);
        }
      }
    };

    fetchNews();

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [page, debouncedSearch]);

  // Get gradient placeholder
  const getPlaceholderGradient = (id: number) => {
    const gradients = [
      'from-purple-500 to-pink-500',
      'from-cyan-500 to-blue-500',
      'from-emerald-500 to-teal-500',
      'from-orange-500 to-red-500',
      'from-indigo-500 to-purple-500',
      'from-green-500 to-lime-500',
    ];
    return gradients[id % gradients.length];
  };

  // Determine number of columns based on screen width
  const getColumnCount = () => {
    if (typeof window === 'undefined') return 4;
    const width = window.innerWidth;
    if (width < 640) return 1;      // mobile
    if (width < 1024) return 2;     // sm
    if (width < 1280) return 3;     // lg
    return 4;                        // xl
  };

  const [columnCount, setColumnCount] = useState(getColumnCount());

  // Update column count on window resize
  useEffect(() => {
    const handleResize = () => {
      setColumnCount(getColumnCount());
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Estimate height of each card for balanced distribution
  const getCardEstimatedHeight = (item: NewsItem, index: number): number => {
    let height = 200; // Base height for card padding and footer

    // Image height
    if (item.image_path) {
      height += 180;
    } else {
      height += 120; // Placeholder height
    }

    // Title length
    if (item.title.length > 60) height += 40;
    else if (item.title.length > 30) height += 20;

    // Subtitle
    if (item.subtitle && item.subtitle.length > 40) height += 30;

    // Tags
    if (item.tags.length > 0) height += 25;

    // Text length
    if (item.text.length > 200) height += 60;
    else if (item.text.length > 100) height += 30;

    return height;
  };

  // Distribute items into balanced columns
  const distributeItems = useMemo(() => {
    const columns: NewsItem[][] = Array.from({ length: columnCount }, () => []);
    const columnHeights: number[] = Array.from({ length: columnCount }, () => 0);

    news.forEach((item, index) => {
      // Find the column with minimum height
      const minHeightIndex = columnHeights.indexOf(Math.min(...columnHeights));

      // Add item to that column
      columns[minHeightIndex].push(item);

      // Update column height
      columnHeights[minHeightIndex] += getCardEstimatedHeight(item, index);
    });

    return columns;
  }, [news, columnCount]);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <h1 className="text-3xl font-bold">Новости</h1>
        <div className="join w-full sm:w-auto">
          <input
            type="text"
            placeholder="Поиск..."
            className="input input-bordered join-item w-full sm:w-64"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          {search && (
            <button
              className="btn btn-ghost join-item"
              onClick={() => setSearch('')}
              aria-label="Очистить поиск"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      ) : (
        <>
          {/* Balanced Masonry Grid */}
          <div
            className="grid gap-4 items-start"
            style={{
              gridTemplateColumns: `repeat(${columnCount}, minmax(0, 1fr))`
            }}
          >
            {distributeItems.map((columnItems, colIndex) => (
              <div key={colIndex} className="flex flex-col gap-4">
                {columnItems.map((item, itemIndex) => (
                  <div key={item.id} className="w-full">
                    <div className="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 cursor-pointer overflow-hidden group">
                      {/* Image or Placeholder */}
                      {item.image_path ? (
                        <figure className="w-full overflow-hidden">
                          <img
                            src={`http://backend:8888${item.image_path}`}
                            alt={item.title}
                            className="w-full object-cover transition-transform duration-300 group-hover:scale-105"
                            style={{
                              minHeight: '150px',
                              maxHeight: '250px'
                            }}
                            loading="lazy"
                          />
                        </figure>
                      ) : (
                        <div
                          className={`w-full h-32 bg-gradient-to-br ${getPlaceholderGradient(item.id)} flex items-center justify-center`}
                        >
                          <span className="text-3xl text-white/70 font-bold">
                            📰
                          </span>
                        </div>
                      )}

                      <div className="card-body p-4 sm:p-5 flex flex-col">
                        {/* Tags */}
                        {item.tags.length > 0 && (
                          <div className="flex flex-wrap gap-1.5 mb-2">
                            {item.tags.slice(0, 3).map(tag => (
                              <span key={tag.id} className="badge badge-sm badge-outline badge-primary">
                                {tag.name}
                              </span>
                            ))}
                            {item.tags.length > 3 && (
                              <span className="badge badge-sm badge-ghost">
                                +{item.tags.length - 3}
                              </span>
                            )}
                          </div>
                        )}

                        {/* Title */}
                        <h2 className="card-title text-base sm:text-lg leading-tight">
                          <Link
                            to={`/news/${item.id}`}
                            className="hover:text-primary transition-colors"
                            onClick={(e) => e.stopPropagation()}
                          >
                            {item.title}
                          </Link>
                        </h2>

                        {/* Subtitle */}
                        {item.subtitle && (
                          <p className="text-xs sm:text-sm text-gray-500 line-clamp-2">
                            {item.subtitle}
                          </p>
                        )}

                        {/* Text Preview */}
                        <p className="text-xs sm:text-sm text-gray-400 line-clamp-3">
                          {item.text}
                        </p>

                        {/* Footer */}
                        <div className="flex justify-between items-center mt-auto pt-3 border-t border-base-300">
                          <div className="flex items-center gap-2 min-w-0">
                            {item.author.photo_path ? (
                              <div className="avatar">
                                <div className="w-6 h-6 rounded-full">
                                  <img
                                    src={`http://backend:8888${item.author.photo_path}`}
                                    alt={item.author.first_name}
                                  />
                                </div>
                              </div>
                            ) : (
                              <div className="avatar placeholder">
                                <div className="bg-neutral text-neutral-content w-6 h-6 rounded-full">
                                  <span className="text-xs">
                                    {item.author.first_name?.[0] || 'U'}
                                  </span>
                                </div>
                              </div>
                            )}
                            <span className="text-xs text-gray-500 truncate">
                              {item.author.first_name} {item.author.last_name}
                            </span>
                          </div>

                          <div className="flex items-center gap-1.5 text-xs text-gray-500 shrink-0">
                            <span>{new Date(item.created_at).toLocaleDateString()}</span>
                            <span>•</span>
                            <span className="flex items-center gap-0.5">
                              💬 {item.comments_count}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>

          {/* Empty State */}
          {news.length === 0 && (
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-bold mb-2">Ничего не найдено</h3>
              <p className="text-gray-500">
                Попробуйте изменить поисковый запрос
              </p>
              {search && (
                <button
                  className="btn btn-primary mt-4"
                  onClick={() => setSearch('')}
                >
                  Сбросить поиск
                </button>
              )}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="join mt-8 flex justify-center">
              <button
                className="join-item btn"
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                «
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(p => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                .map((p, index, arr) => (
                  <React.Fragment key={p}>
                    {index > 0 && arr[index - 1] !== p - 1 && (
                      <button className="join-item btn btn-disabled">...</button>
                    )}
                    <button
                      className={`join-item btn ${p === page ? 'btn-primary' : ''}`}
                      onClick={() => setPage(p)}
                    >
                      {p}
                    </button>
                  </React.Fragment>
                ))}
              <button
                className="join-item btn"
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                »
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default NewsList;
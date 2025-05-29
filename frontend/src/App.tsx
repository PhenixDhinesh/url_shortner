import React, { useState } from 'react';

function App() {
  const [longUrl, setLongUrl] = useState<string>('');
  const [shortUrl, setShortUrl] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  // Get backend URL from environment variables
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const isValidUrl = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setShortUrl('');
    setLoading(true);

    if (!backendUrl) {
      setError("Backend URL is not configured. Check your .env file (REACT_APP_BACKEND_URL).");
      setLoading(false);
      return;
    }

    if (!longUrl) {
      setError('Please enter a URL to shorten.');
      setLoading(false);
      return;
    }

    if (!isValidUrl(longUrl)) {
      setError('Please enter a valid URL (e.g., https://example.com).');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/v1/shorten`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ long_url: longUrl }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to shorten URL.');
      }

      const data = await response.json();
      setShortUrl(data.short_url);
      setLongUrl(''); // Clear the input field
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h1 className="text-3xl font-bold text-teal-700 mb-6 text-center">URL Shortener</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="longUrl" className="block text-stone-700 text-sm font-semibold mb-2">
              Enter Long URL:
            </label>
            <input
              type="url"
              id="longUrl"
              className="shadow-sm appearance-none border border-stone-300 rounded-lg w-full py-3 px-4 text-stone-700 leading-tight focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition duration-200"
              placeholder="https://your-very-long-url.com"
              value={longUrl}
              onChange={(e) => setLongUrl(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className={`w-full py-3 px-4 rounded-lg text-white font-bold transition duration-200
                        ${loading ? 'bg-teal-400 cursor-not-allowed' : 'bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-opacity-75'}`}
            disabled={loading}
          >
            {loading ? 'Shortening...' : 'Shorten URL'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg" role="alert">
            <p className="font-bold">Error:</p>
            <p>{error}</p>
          </div>
        )}

        {shortUrl && (
          <div className="mt-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg break-words" role="alert">
            <p className="font-bold">Shortened URL:</p>
            <a
              href={shortUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-green-800 hover:underline font-medium"
            >
              {shortUrl}
            </a>
            <button
              onClick={() => navigator.clipboard.writeText(shortUrl)}
              className="ml-4 px-3 py-1 bg-green-200 text-green-800 rounded-md text-sm hover:bg-green-300 transition duration-150"
            >
              Copy
            </button>
          </div>
        )}

        <p className="text-sm text-stone-500 mt-8 text-center">
          Powered by Flask Backend
        </p>
      </div>
    </div>
  );
}

export default App;
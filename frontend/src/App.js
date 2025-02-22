import logo from './logo.svg';
import './App.css';

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [songs, setSongs] = useState([]);
  const [isSuccess, setIsSuccess] = useState(false);
  const [successType, setSuccessType] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/songs/')
      .then(response => setSongs(response.data))
      .catch(error => console.error('Error fetching songs:', error));
  }, []);

  const handleScrape = () => {
    axios.post('http://localhost:8000/api/scrape/', { url: 'dummy-url' })
      .then(response => {
        console.log('Scraping successful:', response.data);
        setIsSuccess(true);
        setSuccessType('scrape');
        axios.get('http://localhost:8000/api/songs/')
          .then(response => setSongs(response.data))
          .catch(error => console.error('Error fetching songs:', error));
      })
      .catch(error => {
        console.error('Error scraping:', error);
        alert('Error occurred while scraping. Please try again.');
      });
  };

  const handleSearch = () => {
    axios.post('http://localhost:8000/api/search-spotify/')
      .then(response => {
        console.log('Search successful:', response.data);
        setIsSuccess(true);
        setSuccessType('search');
        axios.get('http://localhost:8000/api/songs/')
          .then(response => setSongs(response.data))
          .catch(error => console.error('Error fetching songs:', error));
      })
      .catch(error => {
        console.error('Error searching:', error);
        alert('Error occurred while searching. Please try again.');
      });
  };

  const handleReset = () => {
    setIsSuccess(false);
    setSuccessType('');
  };

  if (isSuccess) {
    return (
      <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <h2>{successType === 'scrape' ? 'Scrape Success!' : 'Search Success!'}</h2>
        <button 
          onClick={handleReset}
          style={{ marginTop: '20px', padding: '10px 20px' }}
        >
          {successType === 'scrape' ? 'Scrape another URL' : 'Search more songs'}
        </button>
      </div>
    );
  }

  return (
    <div>
      <h1>Spotilistas</h1>
      <div style={{ margin: '20px 0' }}>
        <button 
          onClick={handleScrape}
          style={{ padding: '10px 20px', marginRight: '10px' }}
        >
          Scrape
        </button>
        <button 
          onClick={handleSearch}
          style={{ padding: '10px 20px' }}
        >
          Search
        </button>
      </div>
      <ul>
        {songs.map(song => (
          <li key={song.id}>{song.title} by {song.artist}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

import Home from "./pages/Home";
import { useState } from 'react';
import About from "./pages/About";

function App() {
  const [page, setPage] = useState('home');

  return (
    <>
      {page === 'home' && <Home onNavigate={setPage} />}
      {page === 'about' && <About onNavigate={setPage} />}
    </>
  );
}

export default App;

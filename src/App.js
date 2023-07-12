import './App.css';
import './components/Header';
import './components/Footer';
import './components/ItemsDisplay';
import ItemsDisplay from './components/ItemsDisplay';
import SearchBar from './components/SearchBar';
import { useState, useEffect } from "react";


function App() {
  const [items, setItems] = useState([])
  
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/search/auction=Stow&name=Harmon%253+in+1')
        console.log(res)
        if (res.ok) {
          const data = await res.json()
          setItems(data)
        }
      } catch (e) {
        console.log(e);
      }
    }
    fetchItems();
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <SearchBar onSearch={(params)=>{return null;}}/>
        <ItemsDisplay data={items}/>
      </header>
    </div>
  );
}

export default App;

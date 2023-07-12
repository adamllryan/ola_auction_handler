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
        const res = await fetch('https://localhost:8000/api/v1/items/page/1')
        console.log(res)
        const data = await res.json()

        console.log(res)
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

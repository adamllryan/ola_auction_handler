import logo from './logo.svg';
import './App.css';
import './components/Header';
import './components/Footer';
import './components/ItemsDisplay';
import ItemsDisplay from './components/ItemsDisplay';
import SearchBar from './components/SearchBar';
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <SearchBar onSearch={()=>{return null;}}/>
        <ItemsDisplay />
      </header>
    </div>
  );
}

export default App;

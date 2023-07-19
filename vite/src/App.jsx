import './App.css';
import './components/Header';
import './components/Footer';
import './components/ItemsDisplay';
import ItemsDisplay from './components/ItemsDisplay';
import SearchBar from './components/SearchBar';
import { useState, useEffect } from "react";
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
//import io from 'socket.io'

function App() {

  //TODO: 
  //Finish Refresh with web socket
  //Add Alerts
  //Add saving search into cookies
  //Add setting owner button to each item
  //Fix backend

  const baseURL = 'http://localhost:8000/api/v1'        // Base URL
  const wsURL = 'wss://localhost:8000/api/v1'
  //DISPLAY VARS
  const [items, setItems] = useState([]);               // All items displayed
  const [more, setMore] = useState(true);               // Are there more items available to load
  const [page, setPage] = useState(0);                  // Page Number
  
  const [search, setSearch] = useState('');             // Search terms in URL string

  const [refreshTimer, setRefreshTimer] = useState();   // All refresh vars, replace
  const [refreshTimeout, setRefreshTimeout] = useState();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [progress, setProgress] = useState(1);

  useEffect(() => {
    const getItems = async () => {
      const items = await fetchItems();
      setItems(items);
    }
    getItems();
  }, [])

  //fetch items
  const fetchItems = async (paramsStr) => {
    setIsRefreshing(true)

    try {
      let res = await fetch(baseURL + "/search/&_pgn=0")
      
      //const res = await fetch(baseURL + "/search/auction=Stow&name=Harmon%253+in+1")
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.log(e)
    }
    setIsRefreshing(false)
  }
  //update owner

  //submit query
  const newSearch = async (params) => {
    setIsRefreshing(true)
    try {
      const res = await fetch(baseURL + '/search/' + params + '&_pgn=0', {
        method: 'GET',
        headers: {
          Accept: 'application/json'
        },
      })
      if (!res.ok) {
        throw new Error(res.status)
      }
      setItems(await res.json())
      setSearch(params)
      setPage(1)
      setMore(true)
    } catch (err) {
      console.log(err)
    }

    setIsRefreshing(false)
  }
  const getNextPage = async () => {
    setIsRefreshing(true)
    try {
      const res = await fetch(baseURL + '/search/' + search + '&_pgn=' + page)
      if (!res.ok) {
        throw new Error(res.status)
      }
      let json = await res.json()
      if (json.length !== 0) {
        console.log(json)
        setItems(items => [...items, ...json])
        setPage(page+1)
      } else {
        setMore(false)
      }
    } catch (err) {
      console.log(err)
    }
    setIsRefreshing(false)
  }
  const getSetProgress = async () => {
    try {
      const res = await fetch(baseURL + '/refresh', {
        method: 'POST',
        headers: {
          Accept: 'application/json'
        }
      })
      if (!res.ok) {
        throw new Error(res.status)
      }
      let json = await res.json()
      setProgress(json.progress)
      console.log(json)
    } catch (err) {
      console.log(err)
    }
  }

  const refreshPage = () => {
    console.log("REFRESH CALLED")
    getSetProgress()
    // if (refreshTimer != null) {
    //   clearInterval(refreshTimer)
      
    // }
    // setRefreshTimer(setInterval(() => {
    //   getProgress()
    // }, 1000))
    // setTimeout(setTimeout(() => {
    //   set
    // }, 2000))
  }

  // let socket = new WebSocket(wsURL+'/websocket')

  const refreshOnClick = (e) => {
    e.disabled = true;
  }
  return (
    <>
      <Header refreshPage={refreshOnClick} progress={progress}/> 
      <div className="App">
          <SearchBar submitQuery={newSearch}/>
          <ItemsDisplay page={page} onLoadNext={getNextPage} data={items}/>
          
      </div>
      <Footer />
    </>
  );
}

export default App;

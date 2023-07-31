import './App.css';
import './components/Header';
import './components/Footer';
import './components/ItemsDisplay';
import ItemsDisplay from './components/ItemsDisplay';
import SearchBar from './components/SearchBar';
import { useState, useEffect, useRef } from "react";
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import { io } from 'socket.io-client'



const App = ( ) => {

  //TODO: 
  //Finish Refresh with web socket
  //Add Alerts
  //Add saving search into cookies
  //Add setting owner button to each item
  //Fix backend

  const baseURL = 'http://100.108.92.57:8000/api/v1'        // Base URL
  const wsURL = 'wss://localhost:8000/api/v1'
  //DISPLAY VARS
  const [items, setItems] = useState([]);               // All items displayed
  const [more, setMore] = useState(true);               // Are there more items available to load
  const [page, setPage] = useState(0);                  // Page Number
  const [owners, setOwners] = useState([])
  const [search, setSearch] = useState('');             // Search terms in URL string

  const [refreshTimer, setRefreshTimer] = useState();   // All refresh vars, replace
  const [refreshTimeout, setRefreshTimeout] = useState();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [progress, setProgress] = useState(1);

  const client = useRef();
  let notificationPermission;
  useEffect(() => {
    const getOwners = async () => {
      let ownersQuery = [{id: 0, name: 'None', password: null}]
      try {
        const res = await fetch(baseURL + '/users')
        if (!res.ok) {
          throw new Error(res.status)
        }
        ownersQuery = [...ownersQuery, ...(await res.json())]
      } catch (err) {
        console.log(err)
      }
      setOwners(ownersQuery)
    }
    getOwners()
    const getItems = async () => {
      const items = await fetchItems();
      setItems(items);
    }
    getItems();

    const URL = process.env.NODE_ENV === 'prod' ? undefined : 'ws://100.108.92.57:8000'
    const socket = io(URL);

    socket.on('refresh_progress', (data) => {
      if (typeof data === 'string' && data==='completed') {
        setProgress(1)
        setIsRefreshing(false)
        setItems([])
        setPage(0)
        getNextPage()
      } else {
        setProgress(data)
      }

    })

    client.current = socket;
    const requestPermission = async () => {
      let permission = await Notification.requestPermission();
      return permission
    }
    notificationPermission = requestPermission();
  }, [])

  //fetch items
  const fetchItems = async (paramsStr) => {

    try {
      let res = await fetch(baseURL + "/search/&_pgn=0")
      
      //const res = await fetch(baseURL + "/search/auction=Stow&name=Harmon%253+in+1")
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.log(e)
    }
  }
  //update owner

  //submit query
  const newSearch = async (params) => {
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
  }
  const getNextPage = async () => {
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

  const setOwner = async (item_id, owner_id) => {
    try {
      const res = await fetch(baseURL + '/items/' + item_id, {
        method: 'POST',
        headers: {
          'Content-type':'application/json', 
          Accept: 'application/json'
        },
        body: JSON.stringify({owner_id: owner_id})
      })
      if (!res.ok) {
        throw new Error(res.status)
      }
    } catch (err) {
      console.log(err)
    }
  }
  
  
  const refresh = () => {
    setProgress(0)
    setIsRefreshing(true)
    client.current.emit('refresh_page')
  }
  
  return (
    <>
      
      <div className="grid grid-cols-3">
        <div>
          <Header refreshPage={refresh} progress={progress > 1? .95 : progress} isRefreshing={isRefreshing}/> 
          <SearchBar submitQuery={newSearch} ownersData={owners}/>
        </div>
          
          <ItemsDisplay page={page} onLoadNext={getNextPage} data={items} setOwner={setOwner} owners={owners}/>
      </div>
      <Footer />
    </>
  );
}

export default App;

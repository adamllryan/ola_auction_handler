import './App.css';
import './components/Header';
import './components/Footer';
import './components/ItemsDisplay';
import ItemsDisplay from './components/ItemsDisplay';
import SearchBar from './components/SearchBar';
import { useState, useEffect } from "react";
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'

function App() {

  const baseURL = 'http://localhost:8000/api/v1'
  //DISPLAY VARS
  const [items, setItems] = useState([]);
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [timeElapsed, setTimeElapsed] = useState(0)
  const [page, setPage] = useState(0)
  const [search, setSearch] = useState('')
  const [more, setMore] = useState(true)
  const [refreshTimer, setRefreshTimer] = useState()
  const [refreshTimeout, setRefreshTimeout] = useState()
  //SEARCH VARS

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
        // create sample data for testing
        return [
          {
            id:1,
            name:'Item 1',
            auction:'Auction 1 stow',
            owner_id:null,
            condition:'new',
            ends_at:'',
            url:'',
            src:'https://s3.amazonaws.com/bwpaperclip-production/item_images/assets/056/171/277/web_small/RackMultipart20230713-4035-15wyvg6?1689276574;https://s3.amazonaws.com/bwpaperclip-production/item_images/assets/056/171/881/web_small/RackMultipart20230713-4034-10tc05x?1689276625;https://s3.amazonaws.com/bwpaperclip-production/item_images/assets/056/171/883/web_small/RackMultipart20230713-26669-1bf58im?1689276625'
          },{
            id:2,
            name:'Item 2',
            auction:'Auction 1 stow',
            owner_id:'adam',
            condition:'used',
            ends_at:'',
            url:'',
            src:'https://s3.amazonaws.com/bwpaperclip-production/item_images/assets/056/171/277/web_small/RackMultipart20230713-4035-15wyvg6?1689276574'
          },{
            id:3,
            name:'Item 3',
            auction:'Auction 2 brookpark',
            owner_id:'todd',
            condition:'salvage',
            ends_at:'',
            url:'',
            src:'https://s3.amazonaws.com/bwpaperclip-production/item_images/assets/056/171/277/web_small/RackMultipart20230713-4035-15wyvg6?1689276574'
          },
        ]
    
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
      const res = await fetch(baseURL + '/search/' + search + '&_pgn=' + page, {
        method: 'GET',
        headers: {
          Accept: 'application/json'
        },
      })
      if (!res.ok) {
        throw new Error(res.status)
      }
      let json = await res.json()
      if (json !== []) {
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
  const getProgress = async () => {
    try {
      const res = await fetch(baseURL + '/refresh/progress')
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
    getProgress()
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
  return (
    <>
      <Header refreshPage={refreshPage}/> 
      <div className="App">
          <SearchBar submitQuery={newSearch}/>
          <ItemsDisplay page={page} onLoadNext={getNextPage} data={items}/>
          
      </div>
      <Footer />
    </>
  );
}

export default App;

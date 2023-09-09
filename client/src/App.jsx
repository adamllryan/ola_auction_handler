import "./components/Header";
import "./components/Footer";
import "./components/ItemsDisplay";
import ItemsDisplay from "./components/ItemsDisplay";
import { useState, useEffect, useRef } from "react";
import Header from "./components/Header.jsx";
import { io } from "socket.io-client";
import { sampleItems, sampleOwners } from './sample.js'
const App = () => {

  // Data States

  const [items, setItems] = useState([]); // All items displayed
  const [more, setMore] = useState(true); // Are there more items available to load
  const [page, setPage] = useState(0); // Page Number
  const [owners, setOwners] = useState([]);
  const [search, setSearch] = useState(""); // Search terms in URL string

  // Refresh States

  const [isRefreshing, setIsRefreshing] = useState(false);
  const [progress, setProgress] = useState(1);

  // Websocket Client setup

  const client = useRef();

  // URL bases
  let url_items = window.location.href
    .replace("http://", "")
    .replace("/", "")
    .split(":");
  let PORT = "5004";
  let API_URL = url_items[0];

  if (process.env.NODE_ENV === "production") {
    PORT = url_items[1];
    setItems(sample)
  }
  const baseURL = `http://${API_URL}:${PORT}/api/v1`; // Base URL
  const wsURL = `ws://${API_URL}:${PORT}`;

  // Render away from state

  useEffect(() => {
    // Get owners initially

    const getOwners = async () => {
      let ownersQuery = [{ id: 0, name: "None", password: null }];
      try {
        const res = await fetch(baseURL + "/users");
        if (!res.ok) {
          throw new Error(res.status);
        }
        ownersQuery = [...ownersQuery, ...(await res.json())];
      } catch (err) {
        console.log(err);
      }
      setOwners(ownersQuery);
    };
    if (process.env.NODE_ENV === "production") {
      getOwners();
    } else {
      setOwners(sampleOwners)
    }

    // Get items initially

    const getItems = async () => {
      await newSearch();
    };

    if (process.env.NODE_ENV === "production") {
      getItems();
    } else {
      setItems(sampleItems  )
    }

    // Set up websocket the right way
    const URL = process.env.NODE_ENV === "prod" ? undefined : wsURL;
    const socket = io(URL);

    // Socket on refresh progress update

    socket.on("refresh_progress", (data) => {
      if (typeof data === "string" && data === "completed") {
        setProgress(1);
        setIsRefreshing(false);
        setItems([]);
        setPage(0);
        getNextPage();
      } else {
        setProgress(data);
      }
    });

    client.current = socket;

    // Request permission at the start

    const requestPermission = async () => {
      let permission = await Notification.requestPermission();
      return permission;
    };
    let notificationPermission = requestPermission();
  }, []);

  // Fetch first 50 results given search param string

  const newSearch = async (params = "") => {
    try {
      const res = await fetch(baseURL + "/search/" + params + "&_pgn=0", {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });
      if (!res.ok) {
        throw new Error(res.status);
      }
      setItems([]);
      setItems(await res.json());
      setSearch(params);
      setPage(1);
      setMore(true);
    } catch (err) {
      console.log(err);
    }
  };

  // Get next 50 items on click

  const getNextPage = async () => {
    try {
      const res = await fetch(baseURL + "/search/" + search + "&_pgn=" + page);
      if (!res.ok) {
        throw new Error(res.status);
      }
      let json = await res.json();
      if (json.length !== 0) {
        console.log(json);
        setItems((items) => [...items, ...json]);
        setPage(page + 1);
      } else {
        setMore(false);
      }
    } catch (err) {
      console.log(err);
    }
  };

  // Post request to set owner of individual item

  const setOwner = async (item_id, owner_id) => {
    try {
      const res = await fetch(baseURL + "/items/" + item_id, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ owner_id: owner_id === 0 ? null : owner_id }),
      });
      if (!res.ok) {
        throw new Error(res.status);
      }
    } catch (err) {
      console.log(err);
    }
  };

  // Web socket refresh on click

  const refresh = () => {
    setProgress(0);
    setIsRefreshing(true);
    client.current.emit("refresh_page", "");
  };

  return (
    <>
      <div className="flex flex-col h-screen max-w-4xl m-auto">
        {/*Left side panel*/}
        <div className="z-50">
          <Header
            refreshPage={refresh}
            progress={progress > 1 ? 0.95 : progress}
            isRefreshing={isRefreshing}
            newSearch={newSearch}
            owners={owners}
          />
        </div>
        {/*Item display panel*/}
        <ItemsDisplay
          page={page}
          onLoadNext={getNextPage}
          data={items}
          setOwner={setOwner}
          owners={owners}
          more={more}
        />
      </div>
    </>
  );
};

export default App;

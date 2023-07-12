import React from 'react'
//import { ReactDOM } from 'react-dom'
import { useState } from 'react'
// 

import './SearchBar.css'
import SearchTagsInput from './SearchTagsInput'

const SearchBar = ({ onSearch }) => {
  const [search, setSearch] = useState({
    name: [],
    auction: [],
    owner: [],
    current_price: [0,0],
    retail_price: [0,0]

  })
  const onSubmit = (e) => {
    onSearch(search);
  }

  return (
    <div>
        <SearchTagsInput id='Name' value={search.name}/>
        <SearchTagsInput id='Auction'/>
        <SearchTagsInput id='Owner'/>
    </div>
  );
}

export default SearchBar
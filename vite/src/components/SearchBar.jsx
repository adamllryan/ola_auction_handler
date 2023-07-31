import React from 'react'
//import { ReactDOM } from 'react-dom'
import { useState } from 'react'
import { TagsInput } from 'react-tag-input-component';
// 

import './SearchBar.css'
import SearchTagsInput from './SearchTagsInput'
import Tag from './Tag'

const SearchBar = ({ submitQuery, ownersData }) => {
  const [names, setNames] = useState([])
  const [auctions, setAuctions] = useState([])
  const [owners, setOwners] = useState([])
  const [currentPrices, setCurrentPrices] = useState([0,0])
  const [retailPrices, setRetailPrices] = useState([])
  const onSubmit = () => {
    const formatQuery = (title, list) => {
      return title + '=' + list.join('%25')
    }
    let result = []
    if (names.length>0) {
      result.push(formatQuery('name', names))
    }
    console.log(result)
    if (auctions.length>0) {
      result.push(formatQuery('auction', auctions))
    }
    console.log(result)
    if (owners.length>0) {
      //need to convert to ids for db
      console.log(ownersData)
      let filtered = ownersData.filter((owner) => {return owners.indexOf(owner.name) !== -1})
      filtered = filtered.map((owner) => owner.id)
      result.push(formatQuery('owner_id', filtered))
    }
    console.log(result)
    result = result.join('&').replaceAll(' ', '+')
    console.log(result)
    //TODO: setup currentPrices, retailPrices
    submitQuery(result)
    
  }
  const listAdd = (state, addState) => {
    return (param) => {
      addState([...state, param])
    }
  }
  const listDel = (state, delState) => {
    return (param) => {
      delState(state.filter((i) => {
        i!==param
      }))
    }
  }
  return (
    <div className='col-span-1'>
        <TagsInput value={names} onChange={setNames} name='names' placeHolder='Add Keywords e.g. Power Strip' />
        <TagsInput value={auctions} onChange={setAuctions} name='auctions' placeHolder='Add Auction keywords e.g. Stow or 3010' />
        <div className='grid'>
          <TagsInput value={owners} onChange={setOwners} name='owners' placeHolder='Add Users e.g. John' />
          <button type="button" className="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700" onClick={onSubmit}>Apply</button>
        </div>
        
    </div>
  );
}

export default SearchBar
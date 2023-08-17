import React from 'react'
import { useState } from 'react'
import { TagsInput } from 'react-tag-input-component';
import './TagsInput.css'
import OwnerDropdown from './OwnerDropdown';

const SearchBar = ({ submitQuery, ownersData }) => {

  // App states

  const [names, setNames] = useState([])        // Name tags selected
  const [auctions, setAuctions] = useState([])  // Auction tags selected
  const [conditions, setConditions] = useState([]) // Item Conditions selected
  const [ownerId, setOwnerId] = useState(0)      // Owner tags selected
  
  // Format search query string

  const onSubmit = () => {

    // Format key with values arrow function

    const formatQuery = (title, list) => {
      return title + '=' + list.join('%25')
    }

    let result = []

    // Format name

    if (names.length>0) {
      result.push(formatQuery('name', names))
    }

    // Format Auctions

    if (auctions.length>0) {
      result.push(formatQuery('auction', auctions))
    }

    if (conditions.length>0) {
      result.push(formatQuery('condition', conditions))
    }

    // Format Owners

    if (ownerId !== 0) {

      // Remove non-matches

      //let filtered = ownersData.filter((owner) => {return owners.indexOf(owner.name) !== -1})

      // Map owners to their ids

      //filtered = filtered.map((owner) => owner.id)

      //result.push(formatQuery('owner_id', filtered))
      result.push('owner_id=' + ownerId)
    }
    
    // Format for url 

    result = result.join('&').replaceAll(' ', '+')

    submitQuery(result)
  }
  
  return (
    <div className='col-span-1 left-1/4 right-1/4 -top-1/2 group-hover/header:top-16  absolute p-4 shadow-xl duration-300 ease-in-out z-30 bg-slate-50'>

        {/* Search Terms*/}

        <TagsInput className='rounded-none' value={names} onChange={setNames} name='names' placeHolder='Add Keywords e.g. Power Strip' />
        <TagsInput className='' value={auctions} onChange={setAuctions} name='auctions' placeHolder='Add Auction keywords e.g. Stow or 3010' />
        <TagsInput className='' value={conditions} onChange={setConditions} name='conditions' placeHolder='Add Condition Keywords e.g. New' />
        <div className='inline-flex items-center gap-x-2 m-2 border border-slate-400 rounded-md p-1 bg-slate-50'>
          <label>Filter by Owner: </label>
          <OwnerDropdown owners={ownersData} owner_id={ownerId} updateOwner={setOwnerId}/>
        </div>
        {/* Submit Button */}

        <button type="button" className="w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700" onClick={onSubmit}>Apply</button>
        
    </div>
  );
}

export default SearchBar
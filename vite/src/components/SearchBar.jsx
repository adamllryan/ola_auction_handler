import React from 'react'
import { useState } from 'react'
import { TagsInput } from 'react-tag-input-component';
import './TagsInput.css'
const SearchBar = ({ submitQuery, ownersData }) => {

  // App states

  const [names, setNames] = useState([])        // Name tags selected
  const [auctions, setAuctions] = useState([])  // Auction tags selected
  const [owners, setOwners] = useState([])      // Owner tags selected

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

    // Format Owners

    if (owners.length>0) {

      // Remove non-matches

      let filtered = ownersData.filter((owner) => {return owners.indexOf(owner.name) !== -1})

      // Map owners to their ids

      filtered = filtered.map((owner) => owner.id)

      result.push(formatQuery('owner_id', filtered))
    }
    
    // Format for url 

    result = result.join('&').replaceAll(' ', '+')

    submitQuery(result)
  }
  
  return (
    <div className='col-span-1 p-4 shadow-md hover:shadow-xl duration-300 m-4 hover:m-2 '>

        {/* Search Terms*/}

        <TagsInput className='rti--container' value={names} onChange={setNames} name='names' placeHolder='Add Keywords e.g. Power Strip' />
        <TagsInput className='item-tag' value={auctions} onChange={setAuctions} name='auctions' placeHolder='Add Auction keywords e.g. Stow or 3010' />
        <TagsInput className='item-tag' value={owners} onChange={setOwners} name='owners' placeHolder='Add Users e.g. John' />
        
        {/* Submit Button */}

        <button type="button" className="w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700" onClick={onSubmit}>Apply</button>
        
    </div>
  );
}

export default SearchBar
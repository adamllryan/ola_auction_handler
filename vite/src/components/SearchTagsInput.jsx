import {React, useState} from 'react'
import Tag from './Tag'


const SearchTagsInput = ({ state, id, sample, addSearch}) => {

  const handleEnter = (e) => {
    if (e.key === 'Enter' && !state.includes(e.target.value) && e.target.value !== '') {
      addSearch(e.target.value)
    }
  }
  return (
    <div key = {id} className=''>
      <label htmlFor={id} className="block mb-2 text-sm font-medium text-light-gray-900 dark:text-white">{id}</label>
      <input name={id} type="text" id="first_name" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 m-1" placeholder={sample} onKeyUp={handleEnter} required />
      
    </div>
  )
}

export default SearchTagsInput
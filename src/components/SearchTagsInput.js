import {React, useState} from 'react'
import Tag from './Tag'


const SearchTagsInput = ({id}) => {
  let [search, setSearch] = useState([])

  let handleEnter = (e) => {
    if (e.key === 'Enter' && !search.includes(e.target.value) && e.target.value !== '') {
      setSearch(search => [...search, e.target.value])
      
    }
  }

  return (
    <div key = {id} className='search-element'>
      <label className='search-label'>{id}</label>
      <input name={id} type="text" onKeyUp={handleEnter} />
      <div className='search-tags'>
        {
          search.map(item => <Tag id={item} onPress={() => {setSearch(search.filter((i) => i !== item))}}/>)
        }
      </div>
    </div>
  )
}

export default SearchTagsInput
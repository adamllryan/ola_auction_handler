import React from 'react'
import ItemCard from './ItemCard.jsx'
import {useState} from 'react'
import './ItemsDisplay.css'
const ItemsDisplay = ({page, onLoadNext, data}) => {
  const [owners, setOwners] = useState(['Adam', 'Todd'])

  return (
    <div className='divide-y divide-gray-100 col-span-2 overflow-auto h-screen'>
        {
            data.map((i, index) => {
                return <ItemCard owners={owners} key={index} item={i} />
                //console.log(index + i.src.split(';'))
            })
            
        }
        {
          
          <button onClick={onLoadNext} >Load Page {page+2}</button>
        }
    </div>
  )
}

export default ItemsDisplay
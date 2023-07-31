import React from 'react'
import ItemCard from './ItemCard.jsx'
import {useState} from 'react'
import './ItemsDisplay.css'
const ItemsDisplay = ({page, onLoadNext, data, setOwner, owners}) => {

  return (
    <div className='divide-y divide-gray-100 col-span-2 overflow-auto h-screen'>
        {
          (data.length === 0) ? <div>No items found. </div> : data.map((i, index) => {return <ItemCard owners={owners} key={index} item={i} setOwner={setOwner} />})
            
        }
        {
          (data.length > 0) ? <button onClick={onLoadNext} >Load Page {page+2}</button> : null
        }
    </div>
  )
}

export default ItemsDisplay
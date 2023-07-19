import React from 'react'
import ItemCard from './ItemCard.jsx'
import {useState} from 'react'
import './ItemsDisplay.css'
const ItemsDisplay = ({page, onLoadNext, data}) => {
  return (
    <div className='divide-y divide-gray-100'>
        {
            data.map((i, index) => {
                return <ItemCard key={index} item={i} />
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
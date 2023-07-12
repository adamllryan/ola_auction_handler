import React from 'react'
import ItemCard from './ItemCard.js'
import {useState} from 'react'
import './ItemsDisplay.css'
const ItemsDisplay = ({data}) => {
  return (
    <div className='item-display-frame'>
        {
            data.map((i) => {
                return <ItemCard item={i} />
            })
            
        }
    </div>
  )
}

export default ItemsDisplay
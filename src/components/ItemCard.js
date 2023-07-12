import React from 'react'
import './ItemCard.css'

const ItemCard = ({ item }) => {
  return (
    <div key={item.id} className='item-card-frame'>Item{item.id}</div>
  )
}

export default ItemCard
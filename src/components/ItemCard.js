import {React, useState} from 'react'
import './ItemCard.css'

const ItemCard = ({ item }) => {
  return (
    <div key={item.id} className='item-card-frame'>
      <div className='item-card-img-frame'>
        {
          item.src.split(';').map((i, index) => {
            return <img key={index} className='item-card-img' src={i} alt={index}/>
          })
        }
      </div>
      <div className='item-card-text-frame'>
        <div className='item-card-title'><a className='item-card-title' href={item.url}>{item.name}</a></div>
        <div className='item-card-location'>{item.auction}</div>
        <div className='item-card-info'>
          {item.condition}
          Ends at: {item.ends_at}
          {item.owner_id === null ? null : "Owner: " + item.owner_id}
        </div>
      </div>
    </div>
  )
}

export default ItemCard
import React from 'react'
import ItemCard from './ItemCard.jsx'

const ItemsDisplay = ({page, onLoadNext, data, setOwner, owners, more}) => {

  return (

    <div className='divide-y divide-gray-100 col-span-2 overflow-auto h-auto'>
        {
          (data.length === 0) ? <div>No items found. </div> : data.map((i, index) => {return <ItemCard owners={owners} key={index} item={i} setOwner={setOwner} />})
        }
        
        {
          (data.length > 0 && more) ? <button className='content-center m-16'onClick={onLoadNext} >Load Page {page+1}</button> : null
        }
    </div>
  )
}

export default ItemsDisplay
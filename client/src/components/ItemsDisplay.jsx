import React from 'react'
import ItemCard from './ItemCard.jsx'

const ItemsDisplay = ({page, onLoadNext, data, setOwner, owners, more}) => {

  return (

    <div className='group/display divide-black overflow-auto duration-300 hover:border-2 border-black'>
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
import React from 'react'
import ItemCard from './ItemCard.jsx'

const ItemsDisplay = ({page, onLoadNext, data, setOwner, owners, more}) => {

  return (

    <div className='group/display divide-black overflow-auto duration-300 text-center h-full border'>
        {
          (data.length === 0) ? <div className='p-4'>No items found. </div> : data.map((i, index) => {return <ItemCard owners={owners} key={index} item={i} setOwner={setOwner} />})
        }
        
        {
          (data.length > 0 && more) ? <button className='content-center m-16'onClick={onLoadNext} >Load Page {page+1}</button> : null
        }
    </div>
  )
}

export default ItemsDisplay
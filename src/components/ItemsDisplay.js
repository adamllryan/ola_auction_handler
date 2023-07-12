import React from 'react'
import ItemCard from './ItemCard.js'
import {useState} from 'react'
const ItemsDisplay = ({data}) => {
  return (
    <>
        {
            data.map((i) => {
                return <ItemCard item={i} />
            })
            
        }
    </>
  )
}

export default ItemsDisplay
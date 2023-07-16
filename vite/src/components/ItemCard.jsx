import {React, useState} from 'react'
import './ItemCard.css'
import CardCarousel from './CardCarousel'

const ItemCard = ({ item }) => {
  const getConditionColor = () => {
    if (item.condition==='New') {
      return 'bg-lime-300'
    } else if (item.condition==='Open Box, Like New') {
      return 'bg-yellow-200'
    } else if (item.condition==='Open Box, Used') {
      return 'bg-amber-600'
    } else {
      return 'bg-orange-600'//TODO: complete these
    }
  }
  return (
    <div key={item.id} className='flex justify-between gap-x-6 py-2'>
      <CardCarousel src={item.src.includes(';')?item.src.split(';'):''}/>
      <div className='inline-grid grid-cols-5 gap-x-2'>
        <div className='min-w-0 flex-auto col-span-4'>
          <a className='text-sm font-semibold leading-none text-gray-900' href={item.url}>
            {item.name}
          </a>
        </div>
        <div className={'mx-2 p-2 mt-1  flex items-center justify-normal text-sm leading-5 text-gray-900 bg-gray-100 rounded-full m-8'}>
          <span className={'flex mr-1 w-5 h-4 rounded-full ' + getConditionColor()} ></span>
          {item.condition}
        </div>
        <div className='flex-wrap text-xs  text-gray-500'>
          {item.auction}
        </div>
        <div className='text-xs col-span-3'>
          Owner: {item.owner_id === null ? 'None' : item.owner_id}
        </div>
        <div className='text-xs '>
            <label>Ends in:</label> 
            <span className=''>
              {item.ends_at}
            </span>
        </div>
        
        
        
        
      </div>
    </div>
  )
}

export default ItemCard
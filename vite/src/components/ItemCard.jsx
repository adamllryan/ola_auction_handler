import {React, useState} from 'react'
import './ItemCard.css'
import CardCarousel from './CardCarousel'
import Countdown from 'react-countdown'
import OwnerDropdown from './OwnerDropdown'
const ItemCard = ({ owners, item }) => {
  //console.log(new Date(Date.parse(item.ends_at)))
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
  if (Date.parse(item.ends_at)-Date.now()<0)
    return (<div>Auction Ended</div>)
  else
    return (
      <div key={item.id} className='flex justify-between gap-x-6 py-2'>
        <CardCarousel src={item.src.includes(';')?item.src.split(';'):''}/>
        <div className='inline-grid grid-cols-5 gap-x-2'>
          <div className='min-w-0 flex-auto col-span-4'>
            <a className='text-sm font-semibold leading-none text-gray-900' href={item.url}>
              {item.name}
            </a>
          </div>
          <div className={'mx-2 p-2 mt-1 flex justify-normal text-sm leading-5 text-gray-900 bg-gray-100 rounded-full m-8'}>
            <span className={'flex mr-1 w-5 h-5 rounded-full ' + getConditionColor()} ></span>
            {item.condition}
          </div>
          <div className='flex text-xs  text-gray-500'>
            {item.auction}
          </div>
          <div className='text-xs col-span-3'>
            Owner: {item.owner_id === null ? 'None' : item.owner_id}
          </div>
          <div className='text-xs '>
              <label>Last (Recorded) Price: ${item.last_price}</label><br/>
              <label>Retail Price: ${item.retail_price}</label><br/>

              <label>Ends in: </label><Countdown date={new Date(Date.parse(item.ends_at + ' UTC'))}/>
              <OwnerDropdown owners={owners} owner_id={item.owner_id}/>
          </div>
          
          
          
          
        </div>
      </div>
    )
}

export default ItemCard
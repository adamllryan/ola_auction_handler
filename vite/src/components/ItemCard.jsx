import {React, useState} from 'react'
import CardCarousel from './CardCarousel'
import Countdown, { calcTimeDelta } from 'react-countdown'
import OwnerDropdown from './OwnerDropdown'

const ItemCard = ({ owners, item, setOwner }) => {

  // State

  const [ownerId, setOwnerId] = useState(item.owner_id !== null ? item.owner_id : 0)

  // Color based on Item Condition

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

  // Push Notification when 5 minutes remaining

  const displayNotif = () => {

    if (Notification.permission === 'granted') {

      if (ownerId!==0) {
        const notification = new Notification('Owned item ending soon', { body: item.name + ' is ending soon', icon:null})
      }

    } else {

      console.log('missing notif permissions')

    }

  }

  // renderer so we can display push notif

  const renderer = ({ hours, minutes, seconds, completed}) => {

    // get time until

    let time = calcTimeDelta(new Date(Date.parse(item.ends_at + ' UTC')))

    // push notif if 5 minutes left

    if (time.days===0 && time.hours ===0 && time.minutes===5 && time.seconds===0) displayNotif()

    return <label>{hours}h {minutes}m {seconds}s</label>
  }

  // update owner

  const updateOwnerId = (item_id, owner_id) => {

    setOwner(item_id, owner_id)

    setOwnerId(owner_id)

  }

  if (Date.parse(item.ends_at)-Date.now()<0)

    return (
      <div>Auction Ended</div>
    )

  else

    return (
      <div key={item.id} className='flex gap-x-6 py-2'>

        <CardCarousel src={item.src.includes(';')?item.src.split(';'):''}/>

        <div className='inline-grid basis-full grid-cols-5 gap-x-2'>

          <div className='min-w-0 flex-auto col-span-4'>
            <a className='text-sm font-semibold leading-none text-gray-900' href={item.url} target='_blank'>
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

              <label>Ends in: </label>

              <Countdown date={new Date(Date.parse(item.ends_at + ' UTC'))} renderer={renderer}/>
              
              <OwnerDropdown owners={owners} owner_id={ownerId} updateOwner={updateOwnerId} id={item.id}/>
          </div>

        </div>

      </div>
    )
}

export default ItemCard
import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import React from 'react'
function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}


const OwnerDropdown = ( { owners, owner_id, updateOwner, id } ) => {

    //Update owner method

    const ownerOnclick = (newOwnerIdx) => {
        if (id !== undefined) 
            updateOwner(id, owners[newOwnerIdx].id)
        else 
            updateOwner(owners[newOwnerIdx].id)
        //console.log("ownerId" + owners[owner_id].id + "id" + id)
    } 

    return (

        <Listbox value={owner_id} onChange={ownerOnclick}>

        <Listbox.Button className='flex bg-slate-50 border-slate-200 rounded-lg border-2 content-center text-center justify-center p-2 cursor-pointer'>{owners !== null && owners[owner_id] !== undefined ?owners[owner_id].name:'Loading'}</Listbox.Button>

        <Listbox.Options className='bg-slate-50 border-slate-200 rounded-lg border-2 p-2 '>

            {
                owners.map((o, index) => (
                    <Listbox.Option className='hover:bg-slate-200 duration-300 hover:border-2 hover:border-slate-400 cursor-pointer' key={o.id} value={index} disabled={false}>
                        {o.name}
                    </Listbox.Option>
                ))
            }

        </Listbox.Options>
        
        </Listbox>
      )
}

export default OwnerDropdown
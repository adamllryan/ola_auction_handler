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
        updateOwner(id, owners[newOwnerIdx].id)
        console.log("ownerId" + owners[owner_id].id + "id" + id)
    } 

    return (

        <Listbox value={owner_id} onChange={ownerOnclick}>

        <Listbox.Button>{owners !== null && owners[owner_id] !== undefined ?owners[owner_id].name:'Loading'}</Listbox.Button>

        <Listbox.Options>

            {
                owners.map((o, index) => (
                    <Listbox.Option key={o.id} value={index} disabled={false}>
                        {o.name}
                    </Listbox.Option>
                ))
            }

        </Listbox.Options>
        
        </Listbox>
      )
}

export default OwnerDropdown
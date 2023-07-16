import React from 'react'
const Tag = ({id, onPress}) => {
  return (
    <div key={id+'Tag'} className='rounded-md border-2 border-slate-900 backdrop-blur-1 bg-slate-950 grid grid-cols-2'>
        <div className='flex flex-wrap bg bg-red'>
            {id}
        </div>
        <div className=' hover:bg-slate-900' onClick={onPress(id)}>
            X
        </div>
    </div>
  )
}

export default Tag
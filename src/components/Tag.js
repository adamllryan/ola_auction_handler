import React from 'react'

const Tag = ({id, onPress}) => {
  return (
    <div id={id+'Tag'} className='tag-element'>
        <div className='tag-content'>
            {id}
        </div>
        <div className='tag-x' onClick={onPress}>
            X
        </div>
    </div>
  )
}

export default Tag
import React from 'react'
const CardCarousel = ({ src }) => {
  return (
    <div className='group relative text-2xl hover: grid grid-flow-col auto-cols-max'>
        <img className='m-2 hover:scale-250 hover:z-10 hover:shadow-outline duration-200 inline-flex items-center h-12 w-12 flex-none rounded-md bg-gray-50' src={src[0]}/>
        
            {
                src==''?
                  <img className='m-2 transform hidden hover:scale-250 hover:z-10 hover:shadow-outline duration-300 group-hover:block cursor-pointer h-12 w-12 flex-none rounded-md bg-gray-50' src='' alt="..." />
                :
                  src.slice(1).map((i, index) => {
                    return <img className='m-2 transform hidden hover:scale-250 hover:z-10 hover:shadow-outline duration-300 group-hover:block cursor-pointer h-12 w-12 flex-none rounded-md bg-gray-50'key={index} src={i} alt="..." />
                })
            }
        
    </div>
  )
}

export default CardCarousel
import React from 'react'
const CardCarousel = ({ src }) => {
  return (
    
    <div className='  group text-2xl duration-500'>
        <img className='m-2 hover:border-t-4 border-blue-900 hover:scale-110 hover:z-50 hover:static duration-200 inline-flex items-center h-48 w-48 rounded-md bg-gray-50' src={src[0]}/>
        
            {
                src==''?
                  <img className='m-2 hover:scale-110 transform hidden hover:z-10 duration-300 group-hover:block cursor-pointer h-12 w-12 rounded-md bg-gray-50' src='' alt="..." />
                :
                  
                    src.slice(1).map((i, index) => {
                      return <img className='m-2 hover:border-t-4 border-blue-900 hover:scale-110 transform hidden hover:z-10 duration-300 group-hover:inline-flex cursor-pointer h-48 w-48 flex-none rounded-md bg-gray-50'key={index} src={i} alt="..." />
                    })
                  
            }
        
    </div>
  )
}

export default CardCarousel
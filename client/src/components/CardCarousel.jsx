import React from 'react'
const CardCarousel = ({ src }) => {
  return (
    
    <div className='group relative text-2xl h-fit ease-out transition-height duration-500'>
        <img className='m-2 hover:border-t-4 border-blue-900 hover:scale-110 hover:z-50 hover:static hover:shadow-outline duration-200 inline-flex items-center h-48 w-48 rounded-md bg-gray-50' src={src[0]}/>
        
            {
                src==''?
                  <img className='m-2 hover:scale-110 transform hidden hover:z-10 hover:shadow-outline duration-300 group-hover:block cursor-pointer h-12 w-12 flex-none rounded-md bg-gray-50' src='' alt="..." />
                :
                  
                    src.slice(1).map((i, index) => {
                      return <img className='m-2 hover:border-t-4 border-blue-900 hover:scale-110 transform hidden hover:z-10 hover:shadow-outline duration-300 group-hover:block cursor-pointer h-48 w-48 flex-none rounded-md bg-gray-50'key={index} src={i} alt="..." />
                    })
                  
            }
        
    </div>
  )
}

export default CardCarousel
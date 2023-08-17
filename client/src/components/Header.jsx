import {React, useState, useEffect} from 'react'
import {
  Navbar, 
  Typography,
  Button,
} from '@material-tailwind/react'

const Header = ({ refreshPage, progress, isRefreshing}) => {  

  return (
    <Navbar className="w-full p-4 z-30">
      
      <div className="flex items-center justify-between text-blue-gray-900">
        <Typography as="a" href="" variant="h6" className="mr-4 text-black py-1.5 z-10" >
          Online Liquidation Auction Handler
        </Typography>
        <div className='text-black absolute left-0 right-0 z-0 text-center'>
          <label className='peer/dropdown hover:cursor-pointer p-8'>Settings</label>
        </div>
        <div className="items-center gap-4">
          <Button
            variant="gradient"
            size="sm"
            className="inline-block z-10"
            onClick={refreshPage}
            disabled={isRefreshing}
          >
            <span className='text-black'>{isRefreshing ? (progress*100).toFixed(2) + '%': 'Refresh Items'}</span>
          </Button>
          
        </div>
        
      </div>
    </Navbar>
  );
}

export default Header
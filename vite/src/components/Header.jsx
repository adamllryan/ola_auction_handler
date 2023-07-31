import {React, useState, useEffect} from 'react'
import {
  Navbar, 
  Typography,
  Button,
} from '@material-tailwind/react'

const Header = ({ refreshPage, progress, isRefreshing}) => {  

  return (
    <Navbar className="mx-auto max-w-screen-xl px-6 py-3">

      <div className="flex items-center justify-between text-blue-gray-900">
        <Typography as="a" href="" variant="h6" className="mr-4 text-black py-1.5" >
          Online Liquidation Auction Handler
        </Typography>
        
        <div className="flex items-center gap-4">

          <Button
            variant="gradient"
            size="sm"
            className="hidden lg:inline-block"
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
import {React, useState, useEffect} from 'react'
import {
  Navbar, 
  MobileNav,
  Typography, 
  IconButton,
  Button,
  Input,
} from '@material-tailwind/react'
const Header = ({ refreshPage, progress}) => {  

  return (
    <Navbar className="mx-auto max-w-screen-xl px-6 py-3">
      <div className="flex items-center justify-between text-blue-gray-900">
        <Typography
          as="a"
          href="#"
          variant="h6"
          className="mr-4 text-black py-1.5"
        >
        
          Online Liquidation Auction Handler
        </Typography>
        
        <div className="flex items-center gap-4">
            <Button
              variant="gradient"
              size="sm"
              className="hidden lg:inline-block"
              onClick={refreshPage}
            >
              <span className='text-black'>Refresh Items</span>
          </Button>
        </div>
        
      </div>
      <div className='flex position-absolute'>{progress}</div>
    </Navbar>
  );
}

export default Header
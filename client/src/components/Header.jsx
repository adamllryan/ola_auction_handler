import { React, useState, useEffect } from "react";
import {
  Navbar,
  Typography,
  Button,
  Menu,
  MenuHandler,
  MenuList,
  MenuItem,
} from "@material-tailwind/react";
import SearchBar from "./SearchBar";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSpinner } from "@fortawesome/free-solid-svg-icons";
/* Title Component */

const HeaderTitle = () => {
  return (
    <Typography variant="h6" className="text-black z-10">
      Online Liquidation Auction Handler
    </Typography>
  );
};

/* Search Button Component */

const SearchButton = ({ newSearch, owners }) => {
  return (
    <Menu placement="bottom" dismiss={{ itemPress: false }}>
      <MenuHandler className="rounded-none border-y-0 border-r-0 text-center">
        <Button variant="outlined">Search</Button>
      </MenuHandler>
      <MenuList className="z-50 rounded-none border border-gray-500 bg-white p-0">
        <SearchBar
          className="z-50"
          submitQuery={newSearch}
          ownersData={owners}
        />
      </MenuList>
    </Menu>
  );
};

/* Refresh Button Component */

const RefreshButton = ({ refreshPage, isRefreshing, progress }) => {
  return (
    <Button
      variant="outlined"
      className="h-full z-10 rounded-none border-y-0 border-r-0"
      onClick={refreshPage}
      disabled={isRefreshing}
    >
      <span className="text-black">
        {isRefreshing ? (
          <div
            className="inline-flex items-center justify-center content-center gap-x-1"
            role="status"
          >
            <FontAwesomeIcon icon={faSpinner} spinPulse />
            <span className="sr-only">Loading...</span>
            <label>{(progress * 100).toFixed(2) + "%"}</label>
          </div>
        ) : (
          "Refresh Items"
        )}
      </span>
    </Button>
  );
};

/* Main Header Component */

const Header = ({ refreshPage, progress, isRefreshing, newSearch, owners }) => {
  return (
    <Navbar className="w-full pl-4 pr-0 py-0 z-50 border border-gray-900 rounded-none ">
      <div className="container inline-flex justify-between items-center text-blue-gray-900 ">
        <HeaderTitle />
        <div className="inline-flex h-full">
          <SearchButton newSearch={newSearch} owners={owners} />

          <RefreshButton
            refreshPage={refreshPage}
            progress={progress}
            isRefreshing={isRefreshing}
          />
        </div>
      </div>
    </Navbar>
  );
};

export default Header;

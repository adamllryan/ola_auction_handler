import React from "react";
import { useState } from "react";
import { TagsInput } from "react-tag-input-component";
import "./TagsInput.css";
import OwnerDropdown from "./OwnerDropdown";
import { Menu, MenuItem, Button } from "@material-tailwind/react";

const SearchBar = ({ submitQuery, ownersData }) => {
  // App states

  const [names, setNames] = useState([]); // Name tags selected
  const [auctions, setAuctions] = useState([]); // Auction tags selected
  const [conditions, setConditions] = useState([]); // Item Conditions selected
  const [ownerId, setOwnerId] = useState(0); // Owner tags selected

  // Format search query string

  const onSubmit = () => {
    const formatQuery = (title, list) => {
      return title + "=" + list.join("%25");
    };

    let result = [];
    if (names.length > 0) {
      /* Format names */
      result.push(formatQuery("name", names));
    }
    if (auctions.length > 0) {
      /* Format auctions */
      result.push(formatQuery("auction", auctions));
    }
    if (conditions.length > 0) {
      /* Format conditions */
      result.push(formatQuery("condition", conditions));
    }
    if (ownerId !== 0) {
      /* Format owner query */
      result.push("owner_id=" + ownerId);
    }
    /* Join all queries */

    result = result.join("&").replaceAll(" ", "+");

    submitQuery(result);
  };

  return (
    <>
      {/* Search Terms*/}

      <MenuItem color="lightBlue" className="p-0 m-0 rounded-none">
        <TagsInput
          className="rounded-none"
          value={names}
          onChange={setNames}
          name="names"
          placeHolder="Filter by item name"
        />
      </MenuItem>

      <MenuItem color="lightBlue" className="p-0 rounded-none">
        <TagsInput
          className=""
          value={auctions}
          onChange={setAuctions}
          name="auctions"
          placeHolder="Filter by auction location and number"
        />
      </MenuItem>

      <MenuItem color="lightBlue" className="p-0 rounded-none">
        <TagsInput
          className=""
          value={conditions}
          onChange={setConditions}
          name="conditions"
          placeHolder="Filter by item condition"
        />
      </MenuItem>

      {/* Owner Dropdown */}

      <MenuItem color="lightBlue" className="p-0">
        <div className="inline-flex items-center justify-center gap-x-2 border-t border-t-slate-400 w-full">
          <label>Filter by Owner: </label>
          <OwnerDropdown
            owners={ownersData}
            owner_id={ownerId}
            updateOwner={setOwnerId}
          />
        </div>
      </MenuItem>

      {/* Submit Button */}

      <MenuItem color="lightBlue" className="p-0">
        <Button
          variant="outlined"
          className="rounded-none text-black bg-white border-slate-400 border-x-0 border-b-0 w-full"
          onClick={onSubmit}
        >
          Apply
        </Button>
      </MenuItem>
    </>
  );
};

export default SearchBar;

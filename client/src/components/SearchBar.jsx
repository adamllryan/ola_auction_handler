import React from "react";
import { useState } from "react";
import { TagsInput } from "react-tag-input-component";
import "./TagsInput.css";
import OwnerDropdown from "./OwnerDropdown";
import { Menu, MenuItem } from "@material-tailwind/react";

const SearchBar = ({ submitQuery, ownersData }) => {
  // App states

  const [names, setNames] = useState([]); // Name tags selected
  const [auctions, setAuctions] = useState([]); // Auction tags selected
  const [conditions, setConditions] = useState([]); // Item Conditions selected
  const [ownerId, setOwnerId] = useState(0); // Owner tags selected

  // Format search query string

  const onSubmit = () => {
    // Format key with values arrow function

    const formatQuery = (title, list) => {
      return title + "=" + list.join("%25");
    };

    let result = [];

    // Format name

    if (names.length > 0) {
      result.push(formatQuery("name", names));
    }

    // Format Auctions

    if (auctions.length > 0) {
      result.push(formatQuery("auction", auctions));
    }

    if (conditions.length > 0) {
      result.push(formatQuery("condition", conditions));
    }

    // Format Owners

    if (ownerId !== 0) {
      // Remove non-matches

      //let filtered = ownersData.filter((owner) => {return owners.indexOf(owner.name) !== -1})

      // Map owners to their ids

      //filtered = filtered.map((owner) => owner.id)

      //result.push(formatQuery('owner_id', filtered))
      result.push("owner_id=" + ownerId);
    }

    // Format for url

    result = result.join("&").replaceAll(" ", "+");

    submitQuery(result);
  };

  return (
    <>
      {/* Search Terms*/}

      <MenuItem color="lightBlue">
        <TagsInput
          className="rounded-none"
          value={names}
          onChange={setNames}
          name="names"
          placeHolder="Add Keywords e.g. Power Strip"
        />
      </MenuItem>

      <MenuItem color="lightBlue">
        <TagsInput
          className=""
          value={auctions}
          onChange={setAuctions}
          name="auctions"
          placeHolder="Add Auction keywords e.g. Stow or 3010"
        />
      </MenuItem>

      <MenuItem color="lightBlue">
        <TagsInput
          className=""
          value={conditions}
          onChange={setConditions}
          name="conditions"
          placeHolder="Add Condition Keywords e.g. New"
        />
      </MenuItem>
      <MenuItem color="lightBlue">
        <div className="inline-flex items-center gap-x-2 m-2 border border-slate-400 rounded-md p-1 bg-slate-50">
          <label>Filter by Owner: </label>
          <OwnerDropdown
            owners={ownersData}
            owner_id={ownerId}
            updateOwner={setOwnerId}
          />
        </div>
      </MenuItem>
      {/* Submit Button */}
      <MenuItem color="lightBlue">
        <button
          type="button"
          className="w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
          onClick={onSubmit}
        >
          Apply
        </button>
      </MenuItem>
    </>
  );
};

export default SearchBar;

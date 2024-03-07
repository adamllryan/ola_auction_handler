import React from "react";
import ItemCard from "./ItemCard.jsx";
import { Button } from "@material-tailwind/react";
const ItemsDisplay = ({ page, onLoadNext, data, setOwner, owners, more }) => {
  return (
    <div className="overflow-auto m-3 mr-0 border-t border-slate-400 portrait:mx-0">
      {data.length === 0 ? (
        <div className="p-4">No items found. </div>
      ) : (
        data.map((i, index) => {
          return (
            <ItemCard
              owners={owners}
              key={index}
              item={i}
              setOwner={setOwner}
            />
          );
        })
      )}

      {data.length > 0 && more ? (
        <Button
          className="content-center m-16"
          onClick={onLoadNext}
          variant="gradient"
          color="white"
        >
          Load Page {page + 1}
        </Button>
      ) : null}
    </div>
  );
};

export default ItemsDisplay;

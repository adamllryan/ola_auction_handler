import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { ChevronDownIcon } from "@heroicons/react/20/solid";
import React from "react";
import { Select, Option } from "@material-tailwind/react";
function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

const OwnerDropdown = ({ owners, owner_id, updateOwner, id }) => {
  //Update owner method
  const [isOpen, setIsOpen] = useState(false);
  const ownerOnclick = (newOwnerIdx) => {
    if (id !== undefined) updateOwner(id, owners[newOwnerIdx].id);
    else updateOwner(owners[newOwnerIdx].id);
    //console.log("ownerId" + owners[owner_id].id + "id" + id)
  };

  return (
    <div className="whitespace-nowrap z-50">
      <Listbox value={owner_id} onChange={ownerOnclick}>
        <Listbox.Button
          className="whitespace-nowrap w-fit bg-slate-50 border-gray-500 border content-center text-center justify-center p-1 cursor-pointer"
          onClick={() => {
            setIsOpen(!isOpen);
          }}
        >
          {owners !== null && owners[owner_id] !== undefined
            ? owners[owner_id].name
            : "Loading"}
        </Listbox.Button>

        <Transition
          show={isOpen}
          enter="transition duration-150 ease-out"
          enterFrom="opacity-0"
          enterTo="opacity=100"
          leave="transition-opacity duration-150"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="relative">
            <Listbox.Options className="-translate-y-3/4 absolute bg-white border-gray-500 border p-2 w-fit">
              {owners.map((o, index) => (
                <Listbox.Option
                  className="hover:bg-gray-300 duration-300 hover:border hover:border-gray-500 text-center cursor-pointer"
                  key={o.id}
                  value={index}
                  disabled={false}
                  onClick={() => {
                    setIsOpen(false);
                  }}
                >
                  {o.name}
                </Listbox.Option>
              ))}
            </Listbox.Options>
          </div>
        </Transition>
      </Listbox>
    </div>
  );
};

/*const OwnerDropdown = ({ owners, owner_id, updateOwner, id }) => {
  
  const ownerOnClick = (newOwnerIdx) => {
    console.log(newOwnerIdx);
    if (id !== undefined) updateOwner(id, owners[newOwnerIdx].id);
    else updateOwner(owners[newOwnerIdx].id);
    console.log("ownerId" + owners[owner_id].id + "id" + id);
  };

  return (
    <div className="flex w-72 flex-col gap-6 ">
      <Select
        variant="outlined"
        label="Select Owner"
        className=""
        onChange={ownerOnClick}
      >
        {owners.map((o, index) => (
          <Option key={index}>{o.name}</Option>
        ))}
      </Select>
    </div>
  );
};
*/
export default OwnerDropdown;

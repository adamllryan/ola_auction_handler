import { React, useState } from "react";
import CardCarousel from "./CardCarousel";
import Countdown, { calcTimeDelta } from "react-countdown";
import OwnerDropdown from "./OwnerDropdown";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheck,
  faCircleCheck,
  faCheckDouble,
  faExclamation,
  faCircleQuestion,
} from "@fortawesome/free-solid-svg-icons";
const ItemCard = ({ owners, item, setOwner }) => {
  // State

  const [ownerId, setOwnerId] = useState(
    item.owner_id !== null ? item.owner_id : 0
  );
  const [lowTime, setLowTime] = useState(false);

  // Color based on Item Condition

  const getConditionColor = () => {
    if (item.condition === "New") {
      return "bg-lime-300";
    } else if (item.condition === "Open Box, Like New") {
      return "bg-yellow-200";
    } else if (item.condition === "Open Box, Used") {
      return "bg-amber-600";
    } else {
      return "bg-orange-600"; //TODO: complete these
    }
  };
  const getConditionMark = () => {
    if (item.condition === "New") {
      return (
        <FontAwesomeIcon style={{ color: "#00ff11" }} icon={faCheckDouble} />
      );
    } else if (item.condition === "Open Box, Like New") {
      return <FontAwesomeIcon style={{ color: "#00ff11" }} icon={faCheck} />;
    } else if (item.condition === "Open Box, Used") {
      return (
        <FontAwesomeIcon style={{ color: "#ffea00" }} icon={faExclamation} />
      );
    } else {
      return (
        <FontAwesomeIcon style={{ color: "ff0000" }} icon={faCircleQuestion} />
      );
    }
  };
  // Push Notification when 5 minutes remaining

  const displayNotif = () => {
    if (Notification.permission === "granted") {
      if (ownerId !== 0) {
        const notification = new Notification("Saved item ending soon", {
          body: `${item.name} is ending soon`,
          icon: null,
        });
      }
    } else {
      console.log("missing notif permissions");
    }
  };

  // renderer so we can display push notif

  const renderer = ({ days, hours, minutes, seconds, completed }) => {
    // get time until

    let time = calcTimeDelta(new Date(Date.parse(item.ends_at + " UTC")));

    // push notif if 5 minutes left

    if (
      time.days === 0 &&
      time.hours === 0 &&
      time.minutes === 5 &&
      time.seconds === 0
    )
      displayNotif();
    if (time.days === 0 && time.hours === 0 && time.minutes < 30)
      setLowTime(true);

    return (
      <label>
        {days}d {hours}h {minutes}m {seconds}s
      </label>
    );
  };

  // update owner

  const updateOwnerId = (item_id, owner_id) => {
    setOwner(item_id, owner_id);

    setOwnerId(owner_id);
  };
  return (
    <div className="border border-t-0 border-gray-500 grid grid-cols-4 bg-white shadow-md p-2 ">
      <CardCarousel className="col-span-1" src={item.src} />
      <div className="w-full col-span-3 h-full">
        <div className="grid grid-flow-row col-span-3 w-full">
          <a
            className="ml-2 text-sm font-semibold leading-none text-gray-800 border-b border-gray-500 pb-2"
            href={item.url}
            target="_blank"
          >
            {item.name}
          </a>
          <div className="grid grid-rows-2 grid-cols-3 text-xs ml-2 pt-2">
            <label>Listed Retail: ${item.retail_price}</label>
            <label>{item.auction}</label>
            <label>
              <div className="flex border border-t-0 border-gray-500 gap-1 w-fit items-center px-2 -mt-2">
                <div className="text-xl rounded-full aspect-square">
                  {getConditionMark()}
                </div>
                <div className="align-sub">{item.condition}</div>
              </div>
            </label>
            <label>Recorded price: ${item.last_price}</label>

            <label className={`${lowTime ? "text-red-500" : ""}`}>
              <Countdown
                date={new Date(Date.parse(item.ends_at + " UTC"))}
                renderer={renderer}
              />
            </label>

            <OwnerDropdown
              owners={owners}
              owner_id={ownerId}
              updateOwner={updateOwnerId}
              id={item.id}
            />
          </div>
        </div>
      </div>
    </div>
  );
  /*if (Date.parse(item.ends_at) - Date.now() < 0)
    return <div>Auction Ended</div>;
  else
    return (
      <div
        key={item.id}
        className="flex group/wrap gap-x-6 bg-slate-50 border-b-2 border-black py-2 duration-100 gap-y-2 h-fit ease-in transition-all "
      >
        <CardCarousel src={item.src} />

        <div className=" inline-grid basis-full grid-cols-5 gap-x-2">
          <div className="min-w-0 flex-auto col-span-4">
            <a
              className="text-sm font-semibold leading-none text-gray-900"
              href={item.url}
              target="_blank"
            >
              {item.name}
            </a>
          </div>

          <div
            className={
              "mx-2 p-2 mt-1 flex h-fit justify-normal text-sm leading-5 text-gray-900 bg-gray-100 rounded-lg m-8 duration-300 hover:" +
              getConditionColor()
            }
          >
            <span
              className={
                "flex mr-1 w-5 h-5 rounded-full " + getConditionColor()
              }
            ></span>
            {item.condition}
          </div>

          <div className="flex text-xs  text-gray-500">{item.auction}</div>

          <div className="grid text-xs col-span-3 grid-cols-1">
            <div className="inline-block justify-center align-middle">
              <label>Ends in: </label>
              <Countdown
                date={new Date(Date.parse(item.ends_at + " UTC"))}
                renderer={renderer}
              />
            </div>
            <div>
              <label>Owner: </label>
              <OwnerDropdown
                owners={owners}
                owner_id={ownerId}
                updateOwner={updateOwnerId}
                id={item.id}
              />
            </div>
          </div>

          <div className="text-xs ">
            <label>Last (Recorded) Price: ${item.last_price}</label>
            <br />

            <label>Retail Price: ${item.retail_price}</label>
            <br />
          </div>
        </div>
      </div>
    );
    */
};

export default ItemCard;

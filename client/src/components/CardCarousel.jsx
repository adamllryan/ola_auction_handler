import React from "react";
import { Carousel, IconButton } from "@material-tailwind/react";
const CardCarousel = ({ src }) => {
  return (
    <div className="aspect-square">
      <Carousel
        className="rounded-none border border-gray-500 w-full shadow-md"
        navigation={({ setActiveIndex, activeIndex, length }) => (
          <div className="absolute bottom-1 left-2/4 z-50 flex w-3/4 justify-center flex-wrap  -translate-x-2/4 gap-2">
            {new Array(length).fill("").map((_, i) => (
              <span
                key={i}
                className={`border block h-1 cursor-pointer rounded-none transition-all content-[''] ${
                  activeIndex === i
                    ? "w-8 bg-white border-black"
                    : "w-4 bg-white/50 border-black/50"
                }`}
                onClick={() => setActiveIndex(i)}
              />
            ))}
          </div>
        )}
        prevArrow={({ handlePrev }) => <></>}
        nextArrow={({ handleNext }) => <></>}
      >
        {src.split(";").map((s, index) => {
          return (
            <img
              src={s}
              key={index}
              className="object-cover h-full w-full"
              onError={(e) => {
                e.target.onError = null;
                e.target.src = "https://via.placeholder.com/300";
              }}
            />
          );
        })}
      </Carousel>
    </div>
  );
};

export default CardCarousel;

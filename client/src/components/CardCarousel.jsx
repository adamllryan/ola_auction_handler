import React from "react";
import { Carousel, IconButton } from "@material-tailwind/react";
const CardCarousel = ({ src }) => {
  return (
    <Carousel className="rounded-xl">
      {src.split(";").map((s, index) => {
        return <img src={s} key={index} className="object-scale-down" />;
      })}
    </Carousel>
  );
};

export default CardCarousel;

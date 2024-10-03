import * as React from "react";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

const Slider = ({ slides }) => {
  return (
    <Carousel className="max-lg:flex max-lg:pt-6 md:pt-6 px-0">
      {" "}
      {/* Added ml-auto to move to the right */}
      <CarouselContent className="transform translate-x-4">
        {" "}
        {/* Added translate-x to shift further to the right */}
        {slides.map((_, index) => (
          <CarouselItem key={index} className="fade-in " loop>
            <div className="p-4">
              <Card className=" h-56 sm:h-64 md:h-80 lg:h-96 xl:h-[30rem]">
                {" "}
                {/* Responsive height */}
                <CardContent className="w-full h-full pt-4">
                  {" "}
                  {/* Ensure card content takes full height */}
                  <img
                    src={slides[index].imgURL}
                    className="w-full h-full object-cover"
                    alt={`Slide ${index}`}
                  />
                </CardContent>
              </Card>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
     
    </Carousel>
  );
};

export default Slider;

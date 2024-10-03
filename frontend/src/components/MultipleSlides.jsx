import * as React from "react";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

const handleNext = () => {
  const carousel = document.querySelector(".carousel-content");
  const scrollAmount = carousel.offsetWidth; // Scroll by the width of the carousel
  carousel.scrollLeft += scrollAmount;
};

const handlePrevious = () => {
  const carousel = document.querySelector(".carousel-content");
  const scrollAmount = carousel.offsetWidth;
  carousel.scrollLeft -= scrollAmount;
};
const MultipleSlides = ({ slides }) => {
  return (
    <div className="flex justify-center items-center w-full text-col">
      {/* Parent container to center carousel */}
      <Carousel
        opts={{
          align: "center",
        }}
        className="relative flex w-4/5 items-center max-lg:pt-6 md:pt-7 md:h-78- px-6"
      >
        <CarouselContent className="flex  sm:h-64 md:h-80 lg:h-96 xl:h-[25rem] max-w-screen-xl mx-auto px-4 space-x-2 fade-in">
          {slides.map((slide, index) => (
            <CarouselItem
              key={index}
              className="shrink-0 sm:basis-full md:basis-1/2 lg:basis-1/2 xl:basis-1/3 "
            >
              <div
                className="flex flex-row justify-center p-6"
                style={{ border: "none" }}
              >
                <Card className=" border-0">
                  <CardContent className="flex flex-col justify-center sm:h-[10rem] md:h-[16rem] xl:h-[20rem] blur-option pb-3 pl-3 pr-3 pt-3 text-white">
                    <a href={slide.href} className="h-full w-full">
                      <img
                        src={slide.imgURL}
                        className="h-full w-full object-cover transition-all duration-300 ease-in-out hover:opacity-70 hover:scale-105"
                        alt={`Slide ${index}`}
                      />
                    </a>
                    {/* Hyperlinked Label below the image */}
                    <div className="pt-2 text-center text-lg font-semibold">
                      <a href={slide.href}>{slide.label}</a>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>

        <CarouselNext className="absolute right-0 transform -translate-y-1/2 top-1/2" />
        <CarouselPrevious className="absolute left-0 transform -translate-y-1/2 top-1/2" />
      </Carousel>
    </div>
  );
};

export default MultipleSlides;

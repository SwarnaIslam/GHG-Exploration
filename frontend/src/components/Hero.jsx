import React from 'react'
import {   Slider } from "../components";
import { hero_pics } from "../assets/constants";
import { statistics } from "../assets/constants";



const Hero = () => {
  return (
    <section
      id='home'
      className='flex xl:flex-row  flex-col justify-center  gap-10 max-container w-4/5  '
    >
      <div className='relative  flex flex-col justify-start items-start w-full sm:pt-[4rem] lg:pt-[6.7rem] 2xl:pt-[6.2rem]'>

        <h1 className='font-palanquin  lg:text-3xl sm:text-xl lg:leading-[5rem] xl:leading-[40px] lg:pt-2 z-10 sm:pt-2 font-bold text-col'>
          <span className='xl:whitespace-nowrap relative z-10 pr-10'>
            Explore, Predict 
            and Act on 
          </span>
          <br />
          <span className='inline-block max-lg: mt-0 mx-xl:mt-1'>Greenhouse Gas Emissions</span> 
        </h1>
        <p className='font-montserrat  text-lg  leading-8 mt-6 mb-10 sm:max-w-m text-white'>
          Discover the natural and human caused greenhouse gas sources and sinks in the map, and know about the air quality around you.
        </p>

      <a href="/map">
      <button
          className="btn btn-outline-secondary  mb-5 w-[7rem] bg-[#4f5c34] text-white hover:bg-[#A1B770]"
          style={{ borderRadius: "10px" }}
          
        >
          View Map
       </button>
      </a>

      <h1 className="flex xl:flex-row flex-col justify-center items-center font-palanquin lg:text-3xl sm:text-xl lg:leading-[30px] xl:leading-[40px] lg:pt-2 z-10 sm:pt-5  text-col ">
       From OCO-2 MIP Annual carbon dioxide emissions
      </h1>

      <div className='flex flex-col md:flex-row justify-start items-start flex-wrap w-full mt-2 gap-4 md:gap-6 bg'>
        {statistics.map((stat, index) => (
          <div key={index} className="w-full md:w-auto">
           
            <p className='text-xl md:text-2xl font-palanquin font-bold text-col'>{stat.value}</p>
            <p className='leading-7 font-montserrat text-white'>
              {stat.label}
            </p>
            <p className='leading-7 font-montserrat text-white'>
              {stat.unit}
            </p>
          </div>
        ))}
      </div>

      </div>

      <div className='relative  flex flex-col justify-start items-start w-full sm:pt-[4rem] lg:pt-[5rem] 2xl:pt-[5rem] pb-[2rem]'>
      <div className="flex justify-end items-start">
      <Slider slides={hero_pics}/>
      </div>
      </div>
    </section>
  )
}

export default Hero

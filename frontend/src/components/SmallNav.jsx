import React, { useState } from 'react';
import { headerLogo } from '../assets/images';
import { hamburger } from '../assets/icons';
import { navLinks } from '../assets/constants';
import { useNavigate } from 'react-router-dom';

const SmallNav = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <header className="absolute lg:ml-[50rem] mx-auto sm:ml-[30rem] z-[2000] lg:w-[300px] sm:w-[70px] rounded-lg  bg-white top-[10px]  h-[3rem] flex center shadow-[0_0_40px_rgba(0,0,0,0.2)]">
      <nav className="flex w-4/5 mx-auto justify-between items-center relative">

    
        <ul className="hidden lg:flex flex-1 justify-end items-center gap-8 "> {/* Reduced spacing */}
          {navLinks.map((item) => (
             item.label !== "Explore Map" && (
            <li key={item.label}>
              <a href={item.href} className="font-montserrat text-base text-slate-gray  hover:text-green-500"> {/* Adjusted font size */}
                {item.label}
              </a>
            </li>
             )
          ))}
        </ul>

        <div className="lg:hidden flex items-center mx-auto"> {/* Adjusted margin */}
          <img
            src={hamburger}
            alt="Hamburger"
            width={20} 
            height={20}
            onClick={toggleMenu}
            className="cursor-pointer"
          />
        </div>

        {/* Mobile Menu Dropdown */}
        {isOpen && (
          <div className="absolute left-1/2 transform -translate-x-1/2 top-[3.1rem] z-20 right-0 w-[10rem] bg-white lg:hidden shadow-lg rounded-lg border border-gray-300">
            <ul className="flex flex-col items-center p-4">
              {navLinks.map((item) => (
                <div>
                <li key={item.label} className="py-2">
                  <a href={item.href} className="font-montserrat text-lg text-slate-gray  hover:text-green-500 ">
                    {item.label}
                  </a>
                </li>
                 <hr className="my-4 h-[2px] bg-[#e3dddd] border-0" />
                 </div>
              ))}
             
            </ul>
          </div>
        )}
      </nav>
    </header>
  );
};

export default SmallNav;

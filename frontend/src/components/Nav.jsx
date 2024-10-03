import React, { useState } from 'react';
import { headerLogo } from '../assets/images';
import { hamburger } from '../assets/icons';
import { navLinks } from '../assets/constants';
import { useNavigate } from 'react-router-dom';

const Nav = () => {
  const [isOpen, setIsOpen] = useState(false);
  

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <header className="top-0 z-[2000] w-full mx-auto bg-white h-[5rem] flex items-center shadow-[0_0_40px_rgba(0,0,0,0.2)]">
      <nav className="flex w-4/5 justify-between items-center  max-container  relative">
        {/* Logo on the left */}
        <a href="/">
          <img
            src={headerLogo}
            alt="logo"
            width={140}
            height={15}
            className="flex-shrink-0"
          />
        </a>

        {/* Nav Links - Hidden on smaller screens */}
        <ul className="hidden lg:flex flex-1 justify-end items-center gap-16 mr-[2]">
          {navLinks.map((item) => (
            <li key={item.label}>
              <a href={item.href} className="font-montserrat leading-normal text-lg text-slate-gray  hover:text-green-500">
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Hamburger Menu for smaller screens */}
        <div className="lg:hidden flex items-center ml-[2rem]">
          <img
            src={hamburger}
            alt="Hamburger"
            width={25}
            height={25}
            onClick={toggleMenu}
            className="cursor-pointer"
          />
        </div>

        {/* Mobile Menu Dropdown */}
        {isOpen && (
          <div className="absolute top-[5.7rem] z-20 right-0 w-[40%] bg-white lg:hidden shadow-lg rounded-lg border border-gray-300">
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

export default Nav;

import React, { useState } from "react";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { CO2, CH4, Fluorinates, IntroEdu } from "./index";
import { VideoPlayer, useScrollReveal } from "@/components";
import DraggableGame from "./DraggableGame/DraggableGame";
import { render } from "vue";

const Education = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [openDropdown, setOpenDropdown] = useState(null);
  useScrollReveal();

  const renderComponent = () => {
    switch (selectedOption) {
      case "CO2":
        return <CO2 />;
      case "CH4":
        return <CH4 />;
      case "Fluorinates":
        return <Fluorinates />;
      case "VideoPlayer":
        return <VideoPlayer />;

      default:
        return <VideoPlayer />;
    }
  };

  const toggleDropdown = (option) => {
    setOpenDropdown((prevOption) => (prevOption === option ? null : option));
  };

  return (
    <div
      className="flex min-h-screen "
      style={{
        backgroundImage: 'url("bg.jpg")',
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
      }}
    >
      <a
        className="fixed left-0 z-10 bg-[#7e9156] hover:bg-[#A1B770] text-white"
        data-bs-toggle="offcanvas"
        href="#offcanvasExample"
        role="button"
        aria-controls="offcanvasExample"
        style={{
          top: "85px",
          width: "auto",
          padding: "10px 0px 10px 0px",
          borderRadius: "0px 10px 10px 0px",
          writingMode: "vertical-lr",
        }}
      >
        View SideBar
      </a>
      <aside
        className="bg-[#A1B770] text-white w-64 p-4 offcanvas offcanvas-start"
        tabIndex="-1"
        id="offcanvasExample"
        aria-labelledby="offcanvasExampleLabel"
      >
        <nav>
          <ul className="space-y-2">
            <li className="opcion-con-desplegable">
              <div
                className="flex items-center justify-between p-2 hover:bg-[#B2C48C] cursor-pointer"
                onClick={() => toggleDropdown("contabilidad")}
              >
                <div className="flex items-center">
                  <i className="fas fa-solid fa-earth-americas mr-2"></i>
                  <span>Green House Effect</span>
                </div>
                <i
                  className={`fas fa-chevron-down transition-transform duration-200 ${
                    openDropdown === "contabilidad" ? "rotate-180" : ""
                  }`}
                ></i>
              </div>
              {openDropdown === "contabilidad" && (
                <ul className="ml-4">
                  <li
                    className="block p-2 hover:bg-[#B2C48C] cursor-pointer"
                    onClick={() => setSelectedOption("VideoPlayer")}
                  >
                    What is Green House Effect?
                  </li>
                </ul>
              )}
            </li>

            <li className="opcion-con-desplegable">
              <div
                className="flex items-center justify-between p-2 hover:bg-[#B2C48C] cursor-pointer"
                onClick={() => toggleDropdown("agenda")}
              >
                <div className="flex items-center">
                  <i className="fas fa-solid fa-gas-pump mr-2"></i>
                  <span>Learn through Comics.</span>
                </div>
                <i
                  className={`fas fa-chevron-down transition-transform duration-200 ${
                    openDropdown === "agenda" ? "rotate-180" : ""
                  }`}
                ></i>
              </div>
              {openDropdown === "agenda" && (
                <ul className="ml-4">
                  <li
                    className="block p-2 hover:bg-[#B2C48C] cursor-pointer"
                    onClick={() => setSelectedOption("CO2")}
                  >
                    Carbon Dioxide
                  </li>
                  <li
                    className="block p-2 hover:bg-[#B2C48C] cursor-pointer"
                    onClick={() => setSelectedOption("CH4")}
                  >
                    Methane
                  </li>
                  <li
                    className="block p-2 hover:bg-[#B2C48C] cursor-pointer"
                    onClick={() => setSelectedOption("Fluorinates")}
                  >
                    Fluorinates
                  </li>
                </ul>
              )}
            </li>
          </ul>
        </nav>
      </aside>

      <main className="flex-1 min-h-screen overflow-hidden">
        {renderComponent()}
      </main>
    </div>
  );
};

export default Education;

import React, { useState, useEffect } from "react";
import axios from "axios";
import Select from "react-select";
import "leaflet/dist/leaflet.css";
import MapComponent from "../../components/MapComponent";
import "./MapWrapper.css";
import SmallNav from "@/components/SmallNav";

const MapWrapper = () => {
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (!inputValue) return;

      setIsLoading(true);

      try {
        const response = await axios.get(
          `https://nominatim.openstreetmap.org/search?format=json&q=${inputValue}&addressdetails=1&limit=10`
        );
        console.log(response.data);

        const places = response.data.map((place) => ({
          label: place.display_name,
          value: place.display_name,
          lat: place.lat,
          lon: place.lon,
        }));
        setOptions(places);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }

      setIsLoading(false);
    };

    fetchSuggestions();
  }, [inputValue]);

  const handleInputChange = (input) => {
    setInputValue(input);
  };

  const handleChange = (option) => {
    setSelectedOption(option);
  };

  useEffect(() => {
    const handleScroll = (event) => {
      const isMapElement = event.target.closest(".leaflet-container");

      if (!isMapElement) {
        event.preventDefault();
      }
    };

    window.addEventListener("wheel", handleScroll, { passive: false });

    return () => {
      window.removeEventListener("wheel", handleScroll);
    };
  }, []);

  return (
    <div className="map-wrapper">
      
      <MapComponent />
    </div>
  );
};

export default MapWrapper;

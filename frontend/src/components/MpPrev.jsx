import React, { useEffect, useState } from "react";
import { useMap, GeoJSON } from "react-leaflet";
import "leaflet.locatecontrol";
import "leaflet.locatecontrol/dist/L.Control.Locate.min.css";
import L from "leaflet";

const MapComponent = ({ onSelectLocation }) => {
  const [currentGeoJson, setCurrentGeoJson] = useState(null);

  useEffect(() => {
    console.log(onSelectLocation);
  }, [onSelectLocation]);

  return (
    <>
      {/* {currentGeoJson && (
        
      )} */}
      <iframe
        src={`${import.meta.env.VITE_STREAMLIT_URL}?data=${JSON.stringify(
          onSelectLocation
        )}`}
        style={{ width: "100vw", height: "100vh", border: "none" }}
        title="Streamlit Dashboard"
      ></iframe>
    </>
  );
};

export default MapComponent;

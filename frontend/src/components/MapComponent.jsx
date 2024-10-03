import React from "react";

const MapComponent = () => {
  return (
    <>
      <iframe
        src={`${import.meta.env.VITE_STREAMLIT_URL}/?embedded=true`}
        style={{ width: "100vw", height: "100vh", border: "none" }}
        title="Streamlit Dashboard"
      ></iframe>
    </>
  );
};

export default MapComponent;

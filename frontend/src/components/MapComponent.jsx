import React from "react";

const MapComponent = () => {
  console.log(import.meta.env.VITE_STREAMLIT_URL);
  return (
    <>
      <iframe
        src={import.meta.env.VITE_STREAMLIT_URL}
        style={{ width: "100vw", height: "100vh", border: "none" }}
        title="Streamlit Dashboard"
      ></iframe>
    </>
  );
};

export default MapComponent;

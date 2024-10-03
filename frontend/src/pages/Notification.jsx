import React, { useEffect, useState } from "react";
import axios from "axios";
import Select from "react-select";

const Notification = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true); // Track loading state
  const [location, setLocation] = useState(null); // Track user location
  const [locationError, setLocationError] = useState(null); // Track location error

  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [isLocationLoading, setIsLocationLoading] = useState(false);
  const [locationNotify, setLocationNotify] = useState({});

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setLoading(false); // Stop loading since no token is found
        return;
      }

      try {
        const response = await axios.get(
          import.meta.env.VITE_USER_URL + "/auth/verify",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.data) {
          setIsLoggedIn(true); // User is logged in

          // Start watching the user's location
          if (navigator.geolocation) {
            navigator.geolocation.watchPosition(
              (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                setLocation({ latitude, longitude });
                console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
              },
              (error) => {
                setLocationError(error.message);
                console.error("Error getting location: ", error);
              },
              {
                enableHighAccuracy: true,
                timeout: 60000,
                maximumAge: 0,
              }
            );
          } else {
            setLocationError("Geolocation is not supported by this browser.");
          }
        }
      } catch (error) {
        console.error("Token verification failed:", error);
      } finally {
        setLoading(false);
      }
    };

    verifyToken();
  }, []);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (!inputValue) return;

      setIsLocationLoading(true);

      try {
        const response = await axios.get(
          `https://nominatim.openstreetmap.org/search?format=json&q=${inputValue}&addressdetails=1&limit=10&polygon_geojson=1`
        );
        console.log(response.data);

        const places = response.data.map((place) => ({
          label: place.display_name,
          lat: place.lat,
          lon: place.lon,
        }));
        setOptions(places);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }

      setIsLocationLoading(false);
    };

    fetchSuggestions();
  }, [inputValue]);
  async function updateLocationNotify() {
    if (!selectedOption) return;
    const token = localStorage.getItem("access_token");
    const res = await axios.post(
      import.meta.env.VITE_USER_URL + "/user/notify",
      selectedOption,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
  }
  const handleInputChange = (input) => {
    setInputValue(input);
  };

  const handleChange = (option) => {
    setSelectedOption(option);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="notification-container text-left p-6 max-container w-4/5 sm:pt-[4rem] lg:pt-[5rem] 2xl:pt-[5rem]">
      {isLoggedIn ? (
        <>
          <h1 className="text-4xl font-bold mb-4">
            Stay Updated on Air Quality
          </h1>
          <p className="text-lg mb-6">
            Share your location with us, and we'll notify you regularly about
            the air condition around you.
          </p>

          {/* Display location or error if available */}
          {location ? (
            <div>
              <p>Your current location:</p>
              <p>Latitude: {location.latitude}</p>
              <p>Longitude: {location.longitude}</p>
              <div>
                <Select
                  value={selectedOption}
                  onChange={handleChange}
                  onInputChange={handleInputChange}
                  options={options}
                  placeholder="Search for a location..."
                  isClearable
                  isSearchable
                  classNamePrefix="react-select"
                  isLoading={isLocationLoading}
                  loadingMessage={() => "Loading..."}
                  noOptionsMessage={() =>
                    !isLocationLoading && inputValue ? "No options" : null
                  }
                />
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => {
                    updateLocationNotify();
                  }}
                >
                  Select location
                </button>
              </div>
            </div>
          ) : locationError ? (
            <p className="text-red-500">Error: {locationError}</p>
          ) : (
            <p>Fetching your location...</p>
          )}
        </>
      ) : (
        <>
          <h1 className="text-4xl font-bold mb-4">
            Stay Updated on Air Quality
          </h1>
          <p className="text-lg mb-6">
            Share your location with us, and we'll notify you regularly about
            the air condition around you. To receive notifications, please log
            in first.
          </p>
          <a href="/login">
            <button className="bg-[#8a9d63] text-white px-4 py-2 rounded hover:bg-[#9ea68d]">
              Login to Enable Notifications
            </button>
          </a>
        </>
      )}
    </div>
  );
};

export default Notification;

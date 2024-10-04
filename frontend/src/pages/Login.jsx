import React from "react";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
import ScrollReveal from "scrollreveal";
import axios from "axios";

const Login = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  async function handleCredentialResponse(response) {
    try {
      const userObject = jwtDecode(response.credential);
      setUser(userObject);

      //setting tokenId
      const tokenId = response.credential;
      //positng and getting res from backend
      const res = await axios.post(
        import.meta.env.VITE_USER_URL + "/auth/login",
        {
          token: tokenId,
        }
      );
      //storing access token in local storage
      const { access_token } = res.data;
      localStorage.setItem("access_token", access_token);


      document.getElementById("g_id_onload").hidden = true;
      navigate("/");
    } catch (e) {
      console.error("Error decoding JWT: ", e);
    }
  }

  useEffect(() => {
    google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: handleCredentialResponse,
    });

    google.accounts.id.renderButton(document.getElementById("g_id_onload"), {
      theme: "outline",
      width: "500",
      text: "continue_with",
      shape: "rectangular",
      logo_alignment: "left",
      border: "solid",
    });

    const slideRight = {
      distance: "30px",
      origin: "right",
      opacity: 0,
      duration: 1500,
      reset: true, // Enables the animation to re-trigger on scroll
      mobile: false,
    };
    ScrollReveal().reveal(".slide-right", slideRight);
    const fadeIn = {
      distance: "0px",
      opacity: 0,
      duration: 1300,
      reset: true, // Re-triggers animation on scroll
      mobile: false,
    };
    ScrollReveal().reveal(".fade-in", fadeIn);
  }, []);

  return (
    <div className="w-4/5 mx-auto flex flex-row justify-center items-center mt-[2rem]">
      <div className="bg-white shadow-md border border-gray-200 rounded-lg w-[30rem] p-4 sm:p-6 lg:p-8 slide-right fade-in">
        <form className="space-y-6" action="#">
          {/* Conditionally show the logout button if the token is present */}
          {!localStorage.getItem("access_token") && (
            <div>
              <h3 className="text-xl font-medium text-gray-500 pb-[1.5rem]">
                Sign in using Google{" "}
              </h3>
              <div className="w-[25rem]">
                <div id="g_id_onload" className="w-full"></div>
              </div>
            </div>
          )}
          {/* Conditionally show the logout button if the token is present */}
          {localStorage.getItem("access_token") && (
            <div>
              <h3 className="text-xl font-medium text-gray-500 pb-[1.5rem]">
                You're Signed in. Sign Out from your Google account{" "}
              </h3>
              <a href="/logout">
                <button
                  type="button"
                  className="w-[25rem] flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-500 hover:bg-green-600"
                >
                  Sign Out
                </button>
              </a>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default Login;

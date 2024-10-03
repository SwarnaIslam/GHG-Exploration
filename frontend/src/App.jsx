import Nav from "./components/Nav";
import {
  Footer,
  Login,
  Home,
  Logout,
  Education,
  Notification,
  DraggableGame,
} from "./pages";
import { Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";

import "./index.css";
import Ogrobot from "./pages/chatbot/Ogrobot";
import MapComponent from "./components/MapComponent";

const App = () => {
  const location = useLocation();
  return (
    <>
      <div className="relative">
        <div className="absolute top-0 z-[-2] bg-white bg-[radial-gradient(100%_70%_at_70%_0%,rgba(0,163,255,0.13)_0,rgba(0,163,255,0)_50%,rgba(0,163,255,0)_100%)]"></div>

        {location.pathname !== "/map" && <Nav />}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/map" element={<MapComponent />} />
          <Route path="/education" element={<Education />} />
          <Route path="/notif" element={<Notification />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/game" element={<DraggableGame />} />
          <Route path="/ogrobot" element={<Ogrobot />} />
        </Routes>
      </div>
    </>
  );
};

export default App;

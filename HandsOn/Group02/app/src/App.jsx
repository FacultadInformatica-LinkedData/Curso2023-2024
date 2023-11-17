import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Footer from "./components/Footer.jsx";
import Home from "./components/Home.jsx";
import LocationDetails from "./components/LocationDetails.jsx";
import "./App.css";

export default function App() {
  const [locationKind, setLocationKind] = useState("districts");

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <Home
              locationKind={locationKind}
              setLocationKind={setLocationKind}
            />
          }
        />
        <Route
          path="/districts/:name"
          element={
            <LocationDetails
              locationKind="districts"
              setLocationKind={setLocationKind}
            />
          }
        />
        <Route
          path="/neighbourhoods/:name"
          element={
            <LocationDetails
              locationKind="neighbourhoods"
              setLocationKind={setLocationKind}
            />
          }
        />
      </Routes>
      <Footer />
    </Router>
  );
}

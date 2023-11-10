import { useEffect, useState } from "react";
import * as neighbourhoodService from "./services/neighbourhoods.js";
import * as districtsService from "./services/districts.js";
import Filter from "./components/Filter.jsx";
import Footer from "./components/Footer.jsx";
import Header from "./components/Header.jsx";
import List from "./components/List.jsx";
import Picker from "./components/Picker.jsx";
import "./App.css";

const locationOpts = ["districts", "neighbourhoods"];
const measureTypesOpts = ["kWh", "kVArh", "m3"];

export default function App() {
  const [districts, setDistricts] = useState(null);
  const [neighbourhoods, setNeighbourhoods] = useState(null);
  const [locationKind, setLocationKind] = useState("districts");
  const [measureType, setMeasureType] = useState("kWh");
  const [filter, setFilter] = useState("");

  const handleInput = (e) => {
    e.preventDefault();
    setFilter(e.target.value);
  };

  const locationsToRender = (locations) => {
    return locations.filter((location) =>
      location.toLowerCase().startsWith(filter.toLowerCase())
    );
  };

  useEffect(() => {
    const fetchDistricts = async () => {
      const data = await districtsService.getAllNames();
      setDistricts(data);
    };

    const fetchNeighbourhoods = async () => {
      const data = await neighbourhoodService.getAllNames();
      setNeighbourhoods(data);
    };

    fetchDistricts();
    fetchNeighbourhoods();
  }, [locationKind]);

  return (
    <>
      <Header />
      <Filter handleInput={handleInput} />
      {/* Picker for DISTRICTS or NEIGHBOURHOODS */}
      <Picker
        value={locationKind}
        options={locationOpts}
        setValue={setLocationKind}
      />
      {/* Picker for measure types */}
      <Picker
        value={measureType}
        options={measureTypesOpts}
        setValue={setMeasureType}
      />
      <div>
        {!districts ? (
          <h3>Loading GREAT Data...</h3>
        ) : (
          <div>
            <List
              locations={locationsToRender(
                locationKind === "districts" ? districts : neighbourhoods
              )}
            />
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}

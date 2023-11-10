import { useEffect, useState } from "react";
import * as neighbourhoodService from "./services/neighbourhoods";
import * as districtsService from "./services/districts";
import List from "./components/List";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Picker from "./components/Picker";
import "./App.css";
import Filter from "./components/Filter";

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

import { useEffect, useState } from "react";
import * as neighbourhoodService from "../services/neighbourhoods.js";
import * as districtsService from "../services/districts.js";
import Filter from "./Filter.jsx";
import Picker from "./Picker.jsx";
import List from "./List.jsx";
import Header from "./Header.jsx";

const locationOpts = ["districts", "neighbourhoods"];

export default function Home({ locationKind, setLocationKind }) {
  const [districts, setDistricts] = useState(null);
  const [neighbourhoods, setNeighbourhoods] = useState(null);
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
  }, []);

  return (
    <div className="wrapper">
      <Header />
      <Filter handleInput={handleInput} />
      <Picker
        value={locationKind}
        options={locationOpts}
        setValue={setLocationKind}
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
              locationKind={locationKind}
            />
          </div>
        )}
      </div>
    </div>
  );
}

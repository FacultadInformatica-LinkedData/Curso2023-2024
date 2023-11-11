import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import * as neighbourhoodService from "../services/neighbourhoods.js";
import * as districtsService from "../services/districts.js";
import Map from "./Map.jsx";

export default function LocationDetails({ locationKind, setLocationKind }) {
  const { name } = useParams();
  const [map, setMap] = useState(null);
  const [population, setPopulation] = useState(null);
  const [location, setLocation] = useState(null);

  useEffect(() => {
    const getData = async () => {
      setLocationKind(locationKind);
      const service =
        locationKind === "districts" ? districtsService : neighbourhoodService;
      try {
        const data = await service.getWikiDataProperties(name);
        setPopulation(data.population);
        setLocation(data.location);
        setMap(data.map);
      } catch (err) {
        console.error(err);
      }
    };
    getData();
  }, []);

  return map && population && location ? (
    <div>
      <h1>{name}</h1>
      <h3>{population ? population : "None"}</h3>
      <img src={map} />
      <Map point={location} name={name} />
    </div>
  ) : (
    <p>Loading...</p>
  );
}

import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import * as neighbourhoodService from "../services/neighbourhoods.js";
import * as districtsService from "../services/districts.js";
import { calculateMean } from "../utils/calculateMean.js";
import Map from "./Map.jsx";
import Statistics from "./Statistics.jsx";

export default function LocationDetails({ locationKind, setLocationKind }) {
  const { name } = useParams();
  const [map, setMap] = useState(null);
  const [population, setPopulation] = useState(null);
  const [location, setLocation] = useState(null);
  const [energyMean, setEnergyMean] = useState(null);
  const [gasMean, setGasMean] = useState(0);

  useEffect(() => {
    const service =
      locationKind === "neighbourhoods"
        ? neighbourhoodService
        : districtsService;

    const getData = async () => {
      setLocationKind(locationKind);
      try {
        const data = await service.getWikiDataProperties(name);
        setPopulation(data.population);
        setLocation(data.location);
        setMap(data.map);
      } catch (err) {
        console.error(err);
      }
    };

    const getEnergy = async () => {
      try {
        const data = await service.getMeasurements(name, "kWh");
        setEnergyMean(calculateMean(data));
      } catch (err) {
        console.error(err);
      }
    };

    const getGas = async () => {
      try {
        const data = await service.getMeasurements(name, "m3");
        setGasMean(calculateMean(data));
      } catch (err) {
        console.error(err);
      }
    };

    getData();
    getEnergy();
    getGas();
  }, []);

  return map && population && location && energyMean ? (
    <>
      <h1>{name}</h1>
      <div className="details">
        <div className="statistics-and-map">
          <Statistics
            className="statistics"
            energyMean={energyMean}
            gasMean={gasMean}
            population={population}
          />
          <br />
          <Map point={location} name={name} />
        </div>
        <img className="image" src={map} />
      </div>
    </>
  ) : (
    <h3 style={{ textAlign: "center" }}>Loading...</h3>
  );
}

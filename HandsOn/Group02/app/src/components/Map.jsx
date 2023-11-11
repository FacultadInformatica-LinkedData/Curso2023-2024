import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const Map = ({ point, name }) => {
  return (
    <MapContainer
      center={point}
      zoom={13}
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <Marker position={point}>
        <Popup>
          <strong>{name}</strong>
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default Map;

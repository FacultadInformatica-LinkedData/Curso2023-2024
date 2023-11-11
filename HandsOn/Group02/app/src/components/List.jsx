import ListItem from "./ListItem";

export default function List({ locations, locationKind }) {
  return (
    <div className="list-container">
      {locations.map((name) => (
        <ListItem key={name} name={name} locationKind={locationKind} />
      ))}
    </div>
  );
}

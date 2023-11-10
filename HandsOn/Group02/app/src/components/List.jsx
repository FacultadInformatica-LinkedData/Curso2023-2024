import ListItem from "./ListItem";

export default function List({ locations }) {
  return (
    <div>
      {locations.map((name) => (
        <ListItem key={name} name={name} />
      ))}
    </div>
  );
}

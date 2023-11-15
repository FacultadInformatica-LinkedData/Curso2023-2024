import { Link } from "react-router-dom";

export default function ListItem({ name, locationKind }) {
  return (
    <Link to={`/${locationKind}/${name}`}>
      <button>{name}</button>
    </Link>
  );
}

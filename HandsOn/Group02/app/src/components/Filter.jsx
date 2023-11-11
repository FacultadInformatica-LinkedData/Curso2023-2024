export default function Filter({ handleInput }) {
  const selectStyles = {
    padding: "10px 10px",
    margin: "10px 0",
    borderRadius: "5px",
    border: "1px solid #0000d",
    outline: "none",
    fontSize: "16px",
    fontWeight: "bold",
    backgroundColor: "#d9dbda",
    color: "black",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    cursor: "pointer",
    transition: "all 0.3s ease",
  };

  return (
    <input
      placeholder="filter..."
      style={selectStyles}
      onChange={handleInput}
    />
  );
}

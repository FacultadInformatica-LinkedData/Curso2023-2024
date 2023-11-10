export default function Picker({ value, options, setValue }) {
  const handleChange = (e) => {
    e.preventDefault();
    setValue(e.target.value);
  };

  const selectStyles = {
    padding: "10px 15px",
    margin: "10px 0",
    borderRadius: "5px",
    border: "1px solid #ddd",
    outline: "none",
    fontSize: "16px",
    fontWeight: "bold",
    backgroundColor: "black",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    cursor: "pointer",
    transition: "all 0.3s ease",
  };

  return (
    <select value={value} onChange={handleChange} style={selectStyles}>
      {options.map((opt) => (
        <option key={opt} value={opt}>
          {opt}
        </option>
      ))}
    </select>
  );
}

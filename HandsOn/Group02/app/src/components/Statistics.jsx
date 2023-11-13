export default function Statistics({ energyMean, gasMean, population }) {
  return (
    <div className="statistics">
      <h2>Statistics</h2>
      <div className="stat-item">
        <span className="stat-label">Population: </span>
        <span className="stat-value">{population}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">Energy Consumption Mean: </span>
        <span className="stat-value">{energyMean} kWh</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">Gas Consumption Mean: </span>
        <span className="stat-value">{gasMean} m3</span>
      </div>
    </div>
  );
}

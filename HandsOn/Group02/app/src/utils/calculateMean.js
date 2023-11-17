export const calculateMean = (values = []) => {
  if (values.length === 0) {
    return NaN;
  }
  return Math.floor(values.reduce((acc, v) => acc + v) / values.length);
};

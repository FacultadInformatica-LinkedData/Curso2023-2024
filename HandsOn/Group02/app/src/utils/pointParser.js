export const parsePoint = (point) => {
  const regexp = /^Point\(([^ ]*) ([^ ]*)\)$/;
  let matches = null;
  if ((matches = regexp.exec(point))) {
    return [matches[2], matches[1]];
  }
  return [];
};

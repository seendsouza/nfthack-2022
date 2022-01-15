import type { Axie } from "./types";
export const getLentAxies = async (): Promise<Axie[]> => {
  return fetch("http://localhost:5000/list-lent-axies").then(res => res.json()).then(res => res.data);
};

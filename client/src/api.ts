import type { Axie } from "./types";
export const getLentAxies = async (): Promise<Axie[]> => {
  return new Promise((resolve) => resolve([{ id: "1",
  images:  [
    "https://cdn.tailgrids.com/1.0/assets/images/cards/card-01/image-02.jpg",
    "https://cdn.tailgrids.com/1.0/assets/images/cards/card-01/image-02.jpg",
    "https://cdn.tailgrids.com/1.0/assets/images/cards/card-01/image-02.jpg",
  ],
  tokenIds :["0001", "0002", "0003"],
  lenderAddress : 
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
  }]));
};

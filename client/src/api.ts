import type { Axie, LoginInfo } from "./types";

const serverUri = import.meta.env.VITE_SERVER_URI;

export const startLending = async (lenderWalletAddr: string): Promise<string> => {
  return fetch(`${serverUri}/start-lending/${lenderWalletAddr}`).then(res => res.json()).then(res => res.axieWalletAddr);
};

export const finishTransfer = async (lenderWalletAddr: string, axieWalletAddr: string): Promise<void> => {
  return fetch(`${serverUri}/finish-transfer/${lenderWalletAddr}/${axieWalletAddr}`).then(() => {return;});
}

export const returnAxies = async (axieWalletAddr: string): Promise<void> => {
  return fetch(`${serverUri}/return-axies/${axieWalletAddr}`).then(() => {return;});
}

export const getLentAxies = async (): Promise<Axie[]> => {
  console.log(serverUri);
  return fetch(`${serverUri}/list-lent-axies`).then(res => res.json()).then(res => res.data);
};

export const useAxieAccount = async (axieWalletAddr: string): Promise<LoginInfo> => {
  return fetch(`${serverUri}/axie-account/${axieWalletAddr}`).then(res => res.json()).then(res => res.data);
};


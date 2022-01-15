import type { Axie, LoginInfo } from "./types";

const serverUri = import.meta.env.VITE_SERVER_URI;

export const startLending = async (lenderWalletAddress: string): Promise<string> => {
  return fetch(`${serverUri}/start-lending/${lenderWalletAddress}`, { method: "POST" })
    .then(res => res.json())
    .then(res => res.axieWalletAddress);
};

export const finishTransfer = async (lenderWalletAddress: string, axieWalletAddress: string): Promise<void> => {
  return fetch(`${serverUri}/finish-transfer/${lenderWalletAddress}/${axieWalletAddress}`, { method: "POST" })
    .then(() => {return;});
}

export const returnAxies = async (axieWalletAddress: string): Promise<void> => {
  return fetch(`${serverUri}/return-axies/${axieWalletAddress}`)
    .then(() => {return;});
}

export const getLentAxies = async (): Promise<Axie[]> => {
  return fetch(`${serverUri}/list-lent-axies`)
    .then(res => res.json())
    .then(res => res.data);
};

export const useAxieAccount = async (axieWalletAddress: string): Promise<LoginInfo> => {
  return fetch(`${serverUri}/get-axie-account-info/${axieWalletAddress}`)
    .then(res => res.json())
    .then(res => res.data);
};


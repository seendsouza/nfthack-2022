import type { Axie, LoginInfo } from "./types";

const serverUri: string = "http://localhost:5000";

export const startLending = async (lenderWalletAddr: string): Promise<string> => {
  return fetch(`${serverUri}/start-lending/${lenderWalletAddr}`).then(res => res.json()).then(res => res.axieWalletAddr);
};

export const finishTransfer = async (lenderWalletAddr: string, axieWalletAddr: string): Promise<void> => {
  return fetch(`${serverUri}/finish-transfer/${lenderWalletAddr}/${axieWalletAddr}`).then(res => void);
}

export const returnAxies = async (axieWalletAddr: string): Promise<void> => {
  return fetch(`${serverUri}/return-axies/${axieWalletAddr}`).then(res => void);
}

export const getLentAxies = async (): Promise<Axie[]> => {
  return fetch(`${serverUri}/list-lent-axies`).then(res => res.json()).then(res => res.data);
};

export const useAxieAccount = async (axieWalletAddr: string): Promise<LoginInfo> => {
  return fetch(`${serverUri}/axie-account/${axieWalletAddr}`).then(res => res.json()).then(res => res.data);
};


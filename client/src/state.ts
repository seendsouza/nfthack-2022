import create, { SetState } from "zustand";
import { ethers } from "ethers";

export type WalletStore = {
  provider: ethers.providers.BaseProvider;
  setProvider: (state: ethers.providers.BaseProvider) => void;
};

export const useWalletStore = create((set: SetState<WalletStore>) => ({
  provider: ethers.providers.getDefaultProvider(),
  setProvider: (provider: ethers.providers.BaseProvider) => set({ provider }),
}));

export interface Axie {
  id: string;
  tokenIds: string[]
  lenderAddress: string
  axieWalletAddress: string;
  isCurrentlyUsed: boolean;
  rentedAt: number;
  renterAddress: string;
}

export interface LoginInfo {
  username: string;
  password: string;
}

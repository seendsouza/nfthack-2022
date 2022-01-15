export interface Axie {
  id: string;
  tokenIds: string[]
  lenderAddress: string
  axieWalletAddress: string;
  isCurrentlyUsed: boolean;
}

export interface LoginInfo {
  username: string;
  password: string;
}

import ScholarshipCard from "./ScholarshipCard";
import { useQuery } from "react-query";
import { getLentAxies } from "../api";
import { useWeb3React } from "@web3-react/core";
import { ethers } from "ethers";
import { getAxieUrl } from "../util";
import type { Axie } from "../types";
import { useState, useEffect } from "react";

// function useLentAxiesByKey(lenderAddress: string) {
//   if (!lenderAddress) {
//     return {
//       data: [],
//       error: null,
//       isError: false,
//       isLoading: false,
//     };
//   }

//   return useQuery<Axie[], Error>(
//     "lentAxies",
//     async () => await getLentAxies(lenderAddress)
//   );
// }

function Lendings() {
  const [lentAxies, setLentAxies] = useState<Axie[]>([]);
  const { account } = useWeb3React<ethers.providers.Web3Provider>();
  const lenderAddress = account as string;

  async function updateLentAxies() {
    if (!lenderAddress) {
      setLentAxies([]);
      return;
    }

    const axies: Axie[] = await getLentAxies(lenderAddress);
    setLentAxies(axies);
  }

  useEffect(() => {
    updateLentAxies();
  }, [lenderAddress]);

  // const { data, error, isError, isLoading } = useLentAxiesByKey(lenderAddress);

  // if (isLoading) {
  //   return <span>Loading...</span>;
  // }

  // if (isError) {
  //   return <span>Error: {error?.message}</span>;
  // }
  const cards = lentAxies?.map((lending) => (
    <ScholarshipCard
      key={lending.id}
      images={lending.tokenIds.map(getAxieUrl)}
      lendingId={lending.id}
      rentedAt={new Date()}
      revenue={32.41}
      currency={"USDC"}
      revshare={"70/30"}
      isLending={true}
      axieWalletAddress={lending.axieWalletAddress}
      updateAxies={updateLentAxies}
    />
  ));

  return (
    <div className="container mx-auto pt-5">
      <div className="flex flex-wrap justify-center">
        {cards === undefined || cards.length === 0 ? "No Lendings" : cards}
      </div>
    </div>
  );
}

export default Lendings;

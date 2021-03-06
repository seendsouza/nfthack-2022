import ScholarshipCard from "./ScholarshipCard";
//import { useQuery } from "react-query";
import { getRenterAxies } from "../api";
import { getAxieUrl } from "../util";
import { useWeb3React } from "@web3-react/core";
import { ethers } from "ethers";
import type { Axie } from "../types";
import { useState, useEffect } from "react";


function useRentedAxiesByKey(renterAddress: string) {
  return useQuery<Axie[], Error>(
    "rentedAxies",
    // TDOO: replace this with getRentedAxies
    async () => await getRenterAxies(renterAddress)
  );
}

function Rentings() {
  const [rentedAxies, setRentedAxies] = useState<Axie[]>([]);

  const { account } = useWeb3React<ethers.providers.Web3Provider>();
  const renterAddress = account as string;

  async function updateRentedAxies() {
    const axies: Axie[] = await getRenterAxies(renterAddress);
    setRentedAxies(axies);
  }

  // const { data, error, isError, isLoading } =
  //   useRentedAxiesByKey(renterAddress);

  // if (isLoading) {
  //   return <span>Loading...</span>;
  // }

  // if (isError) {
  //   return <span>Error: {error?.message}</span>;
  // }

  useEffect(() => {
    updateRentedAxies();
  }, [renterAddress]);

  const cards = rentedAxies?.map((lending) => (
    <ScholarshipCard
      key={lending.id}
      images={lending.tokenIds.map(getAxieUrl)}
      lendingId={lending.id}
      rentedAt={new Date()}
      revenue={32.41}
      currency={"USDC"}
      revshare={"70/30"}
      isLending={false}
      lenderAddress={lending.lenderAddress}
      axieWalletAddress={lending.axieWalletAddress}
      updateAxies={updateRentedAxies}
    />
  ));

  return (
    <div className="container mx-auto pt-5">
      <div className="flex flex-wrap justify-center">
        {cards === undefined || cards.length === 0 ? "No Rentings" : cards}
      </div>
    </div>
  );
}
export default Rentings;

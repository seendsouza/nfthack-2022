import ScholarshipCard from "./ScholarshipCard";
import { useQuery } from "react-query";
import { getLentAxies } from "../api";
import { getAxieUrl } from "../util";
import { useWeb3React } from "@web3-react/core";
import { ethers } from "ethers";
import type { Axie } from "../types";

function useRentedAxiesByKey(lenderAddress: string) {
  return useQuery<Axie[], Error>(
    "rentedAxies",
    // TDOO: replace this with getRentedAxies
    async () => await getLentAxies(lenderAddress)
  );
}

function Rentings() {
  const { account } = useWeb3React<ethers.providers.Web3Provider>();
  const renterAddress = account as string;
  if (account === undefined) {
    return <span>Connect wallet...</span>;
  }

  const { data, error, isError, isLoading } =
    useRentedAxiesByKey(renterAddress);

  if (isLoading) {
    return <span>Loading...</span>;
  }

  if (isError) {
    return <span>Error: {error?.message}</span>;
  }
  const cards = data?.map((lending) => (
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
    />
  ));

  return (
    <div className="container mx-auto pt-5">
      <div className="flex flex-wrap">
        {cards === undefined || cards.length === 0 ? "No Rentings" : cards}
      </div>
    </div>
  );
}
export default Rentings;

import { getLentAxies } from "../api";
//import { useQuery } from "react-query";
import { useState, useEffect } from "react";
import Card from "./Card";
import type { Axie } from "../types";

/*
function useLentAxies() {
  return useQuery<Axie[], Error>("lentAxies", async () => await getLentAxies());
}
*/

function Marketplace() {
  //const { data, error, isError, isLoading } = useLentAxies();
  const [lentAxies, setLentAxies] = useState<Axie[]>([]);
  async function updateAvailableAxies() {
    const axies: Axie[] = await getLentAxies();
    setLentAxies(axies);
  }

  useEffect(() => {
    updateAvailableAxies();
  }, []);

  function getAxieUrl(token: string) {
    return `https://storage.googleapis.com/assets.axieinfinity.com/axies/${token}/axie/axie-full-transparent.png`;
  }
  /*
  if (isLoading) {
    return <span>Loading...</span>;
  }

  if (isError) {
    return <span>Error: {error?.message}</span>;
  }
  */

  const cards = lentAxies.filter(c => !c.isCurrentlyUsed).map((lending) => (
    <Card
      key={lending.id}
      images={lending.tokenIds.map(getAxieUrl)}
      tokenIds={lending.tokenIds}
      lenderAddress={lending.lenderAddress}
      axieWalletAddress={lending.axieWalletAddress}
      updateLentAxies={updateAvailableAxies}
    />
  ));
  console.log(cards);
  return <div className="container mx-auto pt-5"> 
          <div className="flex flex-wrap">{cards}</div>
         </div>;
}

export default Marketplace;

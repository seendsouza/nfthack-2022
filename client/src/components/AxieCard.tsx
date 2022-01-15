import type { Dispatch, SetStateAction } from "react";
import { getAxieUrl } from "../util";
type CardProps = {
  axie: any;
  pickedAxies: any[];
  setPicked: Dispatch<SetStateAction<any[]>>;
};
function AxieCard(props: CardProps) {
  const { axie, pickedAxies, setPicked } = props;
  const isPicked = pickedAxies
    .map((pickedAxie: any) => pickedAxie.tokenId)
    .includes(axie.tokenId);
  const onClick = () => {
    if (isPicked) {
      const newAxies = pickedAxies.filter((a) => a.tokenId !== axie.tokenId);
      setPicked(newAxies);
    } else {
      setPicked([...pickedAxies, axie]);
    }
  };
  return (
    <div className="w-full md:w-1/2 xl:w-1/3 border border-grey rounded-lg">
      <div className="bg-white rounded-lg overflow-hidden mb-2 px-4">
        <div className="flex w-full items-center">
          <div className="flex flex-row w-2/3 justify-center">
            <img src={getAxieUrl(axie.tokenId)} alt="Axie" className="w-full" />
          </div>
        </div>
      </div>
      <button
        className="
            w-full
                     inline-block
                     py-2
                     px-7
                     rounded-lg
                     rounded-t-none
                     bg-black 
                     text-base
                     text-white
                     font-extrabold
                     font-medium
                     hover:border-primary hover:bg-primary
                     transition
                     "
      >
        onClick={onClick}
        disabled={!isPicked && pickedAxies.length === 3}
        {isPicked ? "Pick Axie" : "Unpick Axie"}
      </button>
    </div>
  );
}

export default AxieCard;

import { stopUsingAxie, returnAxiesToOwner } from "../api";

type CardProps = {
  images: string[];
  lendingId: string;
  rentedAt?: Date;
  revenue: number;
  currency: string;
  revshare: string;
  lenderAddress?: string;
  isLending: boolean;
  axieWalletAddress: string;
  updateAxies: () => Promise<void>;
};
function ScholarshipCard(props: CardProps) {
  const {
    images,
    lendingId,
    rentedAt,
    revenue,
    currency,
    revshare,
    isLending,
    lenderAddress,
    axieWalletAddress,
    updateAxies,
  } = props;

  async function handleReturnAxie() {
    if (isLending) {
      await returnAxiesToOwner(axieWalletAddress);
    } else {
      await stopUsingAxie(axieWalletAddress);
    }
    await updateAxies();
  }

  return (
    <div className="w-full md:w-[40%] xl:w-[32%] m-2 border border-grey rounded-lg">
      <div className="bg-white rounded-lg overflow-hidden mb-2 px-4">
        <div className="flex w-full items-center">
          <div className="flex flex-row w-2/3 justify-center">
            <img src={images[0]} alt="Axie" className="w-1/3" />
            <img src={images[1]} alt="Axie" className="w-1/3" />
            <img src={images[2]} alt="Axie" className="w-1/3" />
          </div>
          <div className="w-1/3 font-bold text-slate-400">#{lendingId}</div>
        </div>
        <div className="w-full flex flex-row text-slate-400 font-bold mt-2">
          <div className="w-1/3">Rented At</div>
          <div className="w-1/3">Profits</div>
          <div className="w-1/3">Split</div>
        </div>
        <div className="w-full flex flex-row text-slate-400 py-2">
          <div className="w-1/3">
            {rentedAt ? rentedAt.toISOString().slice(0, 10) : "-"}
          </div>
          <div className="w-1/3">
            {revenue} {currency}
          </div>
          <div className="w-1/3">{revshare}</div>
        </div>
        {lenderAddress ? (
          <div className="w-full flex flex-row text-slate-400 text-left py-2">
            Lender: {lenderAddress}
          </div>
        ) : (
          ""
        )}
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
        onClick={handleReturnAxie}
      >
        {isLending ? "Revoke Axies" : "Return Axies"}
      </button>
    </div>
  );
}

export default ScholarshipCard;

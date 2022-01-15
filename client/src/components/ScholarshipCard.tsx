type CardProps = {
  images: string[];
  lendingId: string;
  rentedAt?: Date;
  revenue: number;
  currency: string;
  revshare: string;
  lenderAddress?: string;
  isLending: boolean;
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
  } = props;
  return (
    <div className="w-full md:w-1/2 xl:w-1/3 border border-grey">
      <div className="bg-white rounded-lg overflow-hidden mb-2 px-4">
        <div className="flex w-full items-center">
          <div className="flex flex-row w-2/3 justify-center">
            <img src={images[0]} alt="Axie" className="w-1/3" />
            <img src={images[1]} alt="Axie" className="w-1/3" />
            <img src={images[2]} alt="Axie" className="w-1/3" />
          </div>
          <div className="w-1/3">#{lendingId}</div>
        </div>
        <div className="w-full flex flex-row text-slate-400 text-left">
          <div className="w-1/3">Rented At</div>
          <div className="w-1/3">Profits</div>
          <div className="w-1/3">Split</div>
        </div>
        <div className="w-full flex flex-row text-slate-400 text-left py-2">
          <div className="w-1/3">
            {rentedAt ? rentedAt.toDateString() : "-"}
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
                     bg-black 
                     text-base
                     text-white
                     font-extrabold
                     font-medium
                     hover:border-primary hover:bg-primary
                     transition
                     "
      >
        {isLending ? "Revoke Axies" : "Return Axies"}
      </button>
    </div>
  );
}

export default ScholarshipCard;

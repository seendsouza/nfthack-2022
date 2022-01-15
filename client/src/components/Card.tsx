const shortenAddress = (address: string) => {
  return `${address.slice(0, 6)}...${address.slice(-5, -1)}`;
};

type CardProps = {
  images: string[];
  tokenIds: string[];
  lenderAddress: string;
};
function Card(props: CardProps) {
  const { images, tokenIds, lenderAddress } = props;
  return (
    <div className="w-fit md:w-1/2 xl:w-1/3 px-4 drop-shadow-lg">
      <div className="bg-white rounded-lg overflow-hidden mb-10 flex flex-col items-center">
        <div className="h-screen max-h-72 max-w-md m-3 flex justify-center items-center">
          <img src={images[0]} alt="Axie" className="h-[55%] mt-[2.5rem]" />
          <img src={images[1]} alt="Axie" className="h-[55%] -mx-[9rem] -mt-[3rem]" />
          <img src={images[2]} alt="Axie" className="h-[55%] mt-[2.5rem]" />
        </div>
        <div className="p-8 sm:p-9 md:p-7 xl:p-9 text-center -mt-6">
          <p className="text-base text-body-color leading-relaxed mb-7">
            <strong>Token IDs:</strong>{" "}
            {tokenIds.map((t: string) => "#" + t.toString()).join(", ")}
          </p>
          <p className="text-base text-body-color leading-relaxed mb-7">
            <strong>Lender Address:</strong> {shortenAddress(lenderAddress)}
          </p>
          <button
            className="
                     inline-block
                     py-2
                     px-7
                     border
                     rounded-full
                     text-base text-body-color
                     font-medium
                     hover:border-primary hover:bg-primary
                     transition
                     "
          >
            Use Axie Team
          </button>
        </div>
      </div>
    </div>
  );
}

export default Card;

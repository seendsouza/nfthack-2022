type BannerProps = {
  title: string;
};
function Banner(props: BannerProps) {
  return (
    <div className="bg-black w-full h-1/2 text-white h-fit">
      <h1 className="w-80 pb-48 pt-96 text-4xl font-extrabold">
        {props.title}
      </h1>
    </div>
  );
}

export default Banner;

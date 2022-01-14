import { getLentAxies } from "../api";
import { useQuery } from "react-query";
import Card from "./Card";
function Marketplace() {
  const query = useQuery("get-lent-lendings", getLentAxies);

  return (
    <div>
      <h1>Marketplace</h1>
      {query.data === undefined ? (
        <div></div>
      ) : (
        <ul>
          {query.data.map((lending) => {
            <li key={lending.id}>
              <Card
                images={lending.images}
                tokenIds={lending.tokenIds}
                lenderAddress={lending.lenderAddress}
              />
            </li>;
          })}
        </ul>
      )}
    </div>
  );
}

export default Marketplace;

import { useState } from "react";
import { classNames } from "../util";
import { useWeb3React } from "@web3-react/core";
import { ethers } from "ethers";
import { Tab } from "@headlessui/react";
import Lendings from "./Lendings";
import Rentings from "./Rentings";
import Banner from "./Banner";

function Scholarships() {
  const { account } = useWeb3React();
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div>
      <Banner title={"Scholarships"} />
      <div className="py-16">
        <div className="w-full flex items-center justify-between">
          <div className="mr-auto ml-8">
            <Tab.Group
              onChange={(index) => {
                setSelectedIndex(index);
              }}
            >
              <Tab.List>
                <Tab
                  className={({ selected }) =>
                    classNames(
                      " py-2.5 px-2.5 text-sm leading-5 font-medium text-slate-700",
                      "focus:outline-none",
                      selected
                        ? "bg-white"
                        : "text-slate-300 hover:bg-white/[0.62] hover:text-slate-700"
                    )
                  }
                >
                  Lendings
                </Tab>
                <Tab
                  className={({ selected }) =>
                    classNames(
                      "py-2.5 px-2.5 text-sm leading-5 font-medium text-slate-700",
                      "focus:outline-none",
                      selected
                        ? "bg-white"
                        : "text-slate-300 hover:bg-white/[0.62] hover:text-slate-700"
                    )
                  }
                >
                  Rentings
                </Tab>
              </Tab.List>
            </Tab.Group>
          </div>
          <div className="ml-auto mr-8">
            <button
              className="btn float-right text-sm py-4 px-6 bg-black text-white rounded disabled:bg-slate-600"
              disabled={account === undefined || account === null}
            >
              Lend Out Axies
            </button>
          </div>
        </div>
        <div className="w-full flex items-center justify-between">
          <div className="mx-8 mt-4">
            {selectedIndex === 0 ? <Lendings /> : <Rentings />}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Scholarships;

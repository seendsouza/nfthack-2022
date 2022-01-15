import { useState } from "react";
import { classNames } from "../util";
import { Tab } from "@headlessui/react";
import Lendings from "./Lendings";
import Rentings from "./Rentings";

function Scholarships() {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div>
      <div className="w-full max-w-md px-2 py-16 sm:px-0 flex-col">
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
      <div>{selectedIndex === 0 ? <Lendings /> : <Rentings />}</div>
    </div>
  );
}

export default Scholarships;

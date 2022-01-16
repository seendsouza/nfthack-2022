import { Fragment, useState } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { useWeb3React } from "@web3-react/core";
import { ethers } from "ethers";
import AxieCard from "./AxieCard";
import axieAbi from "../axieAbi";
import { getAxiesInWallet, startLending, finishTransfer } from "../api";
import { useQuery } from "react-query";

function useMyAxies(walletAddress: string) {
  return useQuery<string[], Error>(
    "myAxies",
    async () => await getAxiesInWallet(walletAddress)
  );
}

type LendModalProps = {
  isOpen: boolean;
  close: () => void;
};
const AXIE_CONTRACT_ADDRESS = "";

function LendModal(props: LendModalProps) {
  const { account, library } = useWeb3React<ethers.providers.Web3Provider>();
  const { data } = useMyAxies(account as string);
  const axies = data === undefined ? [] : data;
  const sendAxiesToWallet = async (
    axies: string[],
    toWalletAddress: string
  ) => {
    const contract = new ethers.Contract(
      AXIE_CONTRACT_ADDRESS,
      axieAbi,
      library?.getSigner()
    );
    for (const axie of axies) {
      await contract.safeTransferFrom(
        ethers.utils.getAddress(account as string),
        ethers.utils.getAddress(toWalletAddress),
        axie
      );
    }
  };
  const [picked, setPicked] = useState<string[]>([]);

  const onClick = async () => {
    // Get wallet address to send Axies to
    const axieWalletAddress = await startLending(account as string);
    //const toWalletAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"; // for testing purposes
    await sendAxiesToWallet(axies, axieWalletAddress);
    // Tell backend we're done
    await finishTransfer(account as string, axieWalletAddress);
  };

  return (
    <Transition.Root show={props.isOpen} as={Fragment}>
      <Dialog
        className="fixed z-10 inset-0 overflow-y-auto"
        onClose={props.close}
        open={props.isOpen}
      >
        <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Dialog.Overlay className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
          </Transition.Child>

          {/* This element is to trick the browser into centering the modal contents. */}
          <span
            className="hidden sm:inline-block sm:align-middle sm:h-screen"
            aria-hidden="true"
          >
            &#8203;
          </span>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enterTo="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 translate-y-0 sm:scale-100"
            leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full p-5">
              <div className="bg-white px-4 pb-4 sm:p-6 sm:pb-4">
                <div className="flex justify-between items-center mb-3">
                  <h1 className="font-extrabold">Pick 3 Axies to Lend</h1>
                  <button
                    className="text-sm bg-black text-white px-6 py-2 rounded disabled:bg-slate-400"
                    onClick={onClick}
                    disabled={picked.length !== 1}
                  >
                    Proceed
                  </button>
                </div>
                <div className="flex justify-between items-center flex-wrap">
                  {axies.length === 0
                    ? "No Axies to lend"
                    : axies.map((axie) => (
                        <AxieCard
                          key={axie}
                          axie={axie}
                          pickedAxies={picked}
                          setPicked={setPicked}
                        />
                      ))}
                </div>
              </div>
            </div>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition.Root>
  );
}

export default LendModal;

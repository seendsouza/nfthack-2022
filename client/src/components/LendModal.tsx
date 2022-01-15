import { Fragment, useState } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { useWeb3React } from "@web3-react/core";
import { ethers } from "ethers";
import AxieCard from "./AxieCard";
import axieAbi from "../axieAbi";

type LendModalProps = {
  isOpen: boolean;
};
const AXIE_CONTRACT_ADDRESS = "";

function LendModal(props: LendModalProps) {
  const { account, library } = useWeb3React<ethers.providers.Web3Provider>();
  // TODO: Get axies by wallet address
  // TODO: Determine Axie type
  const axies: any[] = [];
  const sendAxiesToWallet = async (axies: any[], toWalletAddress: string) => {
    const contract = new ethers.Contract(
      AXIE_CONTRACT_ADDRESS,
      axieAbi,
      library
    );
    for (const axie of axies) {
      await contract.safeTransferFrom(
        ethers.utils.getAddress(account as string),
        ethers.utils.getAddress(toWalletAddress),
        axie.tokenId
      );
    }
  };
  const [picked, setPicked] = useState<any[]>([]);

  const onClick = async () => {
    // TODO: Get wallet address to send Axies to
    const toWalletAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
    await sendAxiesToWallet(axies, toWalletAddress);
    // TODO:: Tell backend we're done
  };

  return (
    <Transition.Root show={props.isOpen} as={Fragment}>
      <Dialog
        className="fixed z-10 inset-0 overflow-y-auto"
        onClose={() => {}}
        open={props.isOpen}
      >
        <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div className="flex justify-between">
            <h1>Lend Out Axies</h1>
            <button onClick={onClick}>Proceed</button>
          </div>
          <div>
            {axies.map((axie) => (
              <AxieCard
                axie={axie}
                pickedAxies={picked}
                setPicked={setPicked}
              />
            ))}
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}

export default LendModal;

import { Fragment, useRef, useEffect, useState } from 'react';
import type { LoginInfo } from "../types";
import { Dialog, Transition } from "@headlessui/react"

type UseAxieTeamModalProps = {
    isOpen: boolean
    hitClose: () => void
    loginInfo: LoginInfo
};


function UseAxieTeamModal(props: UseAxieTeamModalProps) {
  const cancelButtonRef = useRef(null)

  return (
    <Transition.Root show={props.isOpen} as={Fragment}>
      <Dialog as="div" className="fixed z-10 inset-0 overflow-y-auto" initialFocus={cancelButtonRef} open={props.isOpen} onClose={props.hitClose}>
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
          <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">
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
                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                    <Dialog.Title as="h3" className="text-lg leading-6 font-medium text-gray-900">
                      Use Axie Team
                    </Dialog.Title>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        Here are the user names and passwords for the Axie Team.
                        <br />
                        Username: {props.loginInfo.username}
                        <br />
                        Password: {props.loginInfo.password}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-center">
                <button className="inline-block py-2 px-7 text-base text-body-color border rounded-full transition hover:border-primary hover:bg-primary" onClick={props.hitClose}>
                  Done
                </button>
              </div>

            </div>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition.Root>
  )
}

export default UseAxieTeamModal;

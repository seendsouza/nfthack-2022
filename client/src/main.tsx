import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
import "./index.css";
import App from "./App";
import { ethers } from "ethers";
import { Web3ReactProvider } from "@web3-react/core";

function getLibrary(provider?: any) {
  return new ethers.providers.Web3Provider(provider);
}

const queryClient = new QueryClient();

ReactDOM.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <Web3ReactProvider getLibrary={getLibrary}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
        <ReactQueryDevtools initialIsOpen={false} />
      </Web3ReactProvider>
    </QueryClientProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

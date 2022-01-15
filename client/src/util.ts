export function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export function getAxieUrl(token: string) {
  return `https://storage.googleapis.com/assets.axieinfinity.com/axies/${token}/axie/axie-full-transparent.png`;
}

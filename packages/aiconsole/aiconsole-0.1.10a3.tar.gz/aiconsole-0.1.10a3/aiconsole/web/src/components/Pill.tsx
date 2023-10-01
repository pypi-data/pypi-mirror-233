import { ReactNode } from "react";

export type PillProps = {
  children: ReactNode;
  color?: string;
  title?: string;
};

export const Pill = ({ children, title }: PillProps) => {
  return (
    <span title={title} className="rounded-full align-middle px-2 py-1 ml-1 shadow-md overflow-ellipsis overflow-hidden h-8 w-24 max-w-xl bg-indigo-800 inline-block whitespace-nowrap">
      {children}
    </span>
  );
};

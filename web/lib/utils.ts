import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { OrderItem } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const groupedItemsUtils = (
  items: OrderItem[]
): {
  name: string;
  quantity: number;
  total: number;
}[] => {
  const grouped = items.reduce(
    (acc: { [key: string]: { quantity: number; total: number } }, item) => {
      if (!acc[item.name]) {
        acc[item.name] = { quantity: 0, total: 0 };
      }
      acc[item.name].quantity += item.quantity;
      acc[item.name].total += item.total;
      return acc;
    },
    {}
  );

  // Convert the grouped object back to an array of OrderItem
  return Object.entries(grouped).map(([name, { quantity, total }]) => ({
    name,
    quantity,
    total,
  }));
};

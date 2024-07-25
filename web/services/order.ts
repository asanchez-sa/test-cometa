import { API_ENDPOINTS } from "@/lib/routes";
import { Order } from "@/lib/types";
import axios from "axios";

const api = axios.create({
  baseURL: "http://0.0.0.0:8000/api/v1",
});

export const getOrder = async (): Promise<Order> => {
  const { data } = await api.get<Order>(API_ENDPOINTS.GET_ORDER);
  return data;
};

export const addRound = async (
  items: { name: string; quantity: number }[]
): Promise<Order> => {
  const { data } = await api.post<Order>(API_ENDPOINTS.ADD_ROUND, { items });
  return data;
};

export const payOrder = async (): Promise<Order> => {
  const { data } = await api.post<Order>(API_ENDPOINTS.PAY_ORDER);
  return data;
};

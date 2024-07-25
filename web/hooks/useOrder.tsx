import { Order } from "@/lib/types";
import { addRound, getOrder, payOrder } from "@/services/order";
import { useState, useCallback } from "react";

export const useOrder = () => {
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const fetchOrder = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getOrder();
      setOrder(data);
    } catch (err) {
      setError("Error fetching order");
    } finally {
      setLoading(false);
    }
  }, []);

  const addNewRound = useCallback(
    async (items: { name: string; quantity: number }[]) => {
      setLoading(true);
      setError(null);
      try {
        const updatedOrder = await addRound(items);
        setOrder(updatedOrder);
      } catch (err) {
        setError("Error adding new round");
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const payCurrentOrder = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      await payOrder();
      setOrder(null);
      setMessage(
        "Payment successful! The order is paid and ready for a new order."
      );
    } catch (err) {
      setError("Error paying order");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    order,
    loading,
    error,
    message,
    fetchOrder,
    addNewRound,
    payCurrentOrder,
  };
};

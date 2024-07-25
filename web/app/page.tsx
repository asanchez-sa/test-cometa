"use client";

import * as React from "react";
import { CircleDollarSign, Copy, RocketIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

import { Separator } from "@/components/ui/separator";

import { useOrder } from "@/hooks/useOrder";
import { groupedItemsUtils } from "@/lib/utils";
import ErrorComponent from "@/components/core/ErrorComponent";
import LoadingComponent from "@/components/core/LoadingComponent.tsx";
import { ProfileForm } from "@/components/modules/order/AddRoundFormComponent";

export default function Dashboard() {
  const [showForm, setShowForm] = React.useState<Boolean>(false);

  const {
    order,
    loading,
    error,
    message,
    addNewRound,
    payCurrentOrder,
    fetchOrder,
  } = useOrder();

  React.useEffect(() => {
    fetchOrder();
  }, [fetchOrder]);

  if (loading) {
    return <LoadingComponent />;
  }

  if (error) {
    return <ErrorComponent />;
  }

  return (
    <div className="container h-screen flex-col place-content-center items-center justify-center md:grid lg:max-w-none lg:px-0">
      <div className="mx-auto flex w-full flex-col justify-center space-y-6">
        {message && (
          <Alert>
            <RocketIcon className="h-4 w-4" />
            <AlertTitle>Heads up!</AlertTitle>
            <AlertDescription>{message}</AlertDescription>
          </Alert>
        )}

        <Card className="overflow-hidden" x-chunk="dashboard-05-chunk-4">
          <CardHeader className="flex flex-row items-start bg-muted/50">
            <div className="grid gap-0.5">
              <CardTitle className="group flex items-center gap-2 text-lg">
                Order #0000
                <Button
                  size="icon"
                  variant="outline"
                  className="h-6 w-6 opacity-0 transition-opacity group-hover:opacity-100"
                >
                  <Copy className="h-3 w-3" />
                  <span className="sr-only">Copy Order ID</span>
                </Button>
              </CardTitle>
              <CardDescription>
                Date: {new Date().toLocaleDateString()}
              </CardDescription>
            </div>
            <div className="ml-auto flex items-center gap-2 mr-5">
              <Button
                size="lg"
                className="h-8 gap-1"
                onClick={() => setShowForm(!showForm)}
              >
                <CircleDollarSign className="h-3.5 w-3.5" />
                <span className="lg:sr-only xl:not-sr-only xl:whitespace-nowrap">
                  {showForm ? "Hide" : "Add"} Round
                </span>
              </Button>
            </div>
            <div className="ml-auto flex items-center gap-1">
              <Button
                size="lg"
                variant="outline"
                className="h-8 gap-1"
                onClick={payCurrentOrder}
              >
                <CircleDollarSign className="h-3.5 w-3.5" />
                <span className="lg:sr-only xl:not-sr-only xl:whitespace-nowrap">
                  Pay
                </span>
              </Button>
            </div>
          </CardHeader>
          <CardContent className="p-6 text-sm">
            {showForm && (
              <ProfileForm
                onSubmit={async (items) => {
                  await addNewRound(items);
                  setShowForm(false);
                }}
              />
            )}

            <div className="grid gap-3">
              <div className="font-semibold">Order Details</div>
              <ul className="grid gap-3">
                {groupedItemsUtils(order?.items || []).map((e) => (
                  <li
                    className="flex items-center justify-between"
                    key={e.name}
                  >
                    <span className="text-muted-foreground">
                      {e.name} x <span>{e.quantity}</span>
                    </span>
                    <span>${e.total}</span>
                  </li>
                ))}
              </ul>
              <Separator className="my-2" />
              <ul className="grid gap-3">
                <li className="flex items-center justify-between">
                  <span className="text-muted-foreground">Subtotal</span>
                  <span>{order?.subtotal}</span>
                </li>
                <li className="flex items-center justify-between">
                  <span className="text-muted-foreground">Tax</span>
                  <span>
                    {order?.subtotal
                      ? (order.subtotal * 0.19).toFixed(2)
                      : "N/A"}
                  </span>
                </li>
                <li className="flex items-center justify-between font-semibold">
                  <span className="text-muted-foreground">Total</span>
                  <span>
                    {order?.subtotal
                      ? `$${(order.subtotal + order.subtotal * 0.19).toFixed(
                          2
                        )}`
                      : "N/A"}
                  </span>
                </li>
              </ul>
            </div>
            <Separator className="my-4" />
          </CardContent>
          <CardFooter className="flex flex-row items-center border-t bg-muted/50 px-6 py-3" />
        </Card>
      </div>
    </div>
  );
}

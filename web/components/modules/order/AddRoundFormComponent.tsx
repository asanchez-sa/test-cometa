"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useFieldArray, useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const profileFormSchema = z.object({
  items: z.array(
    z.object({
      beer: z.string(),
      quantity: z.string().min(1).or(z.number()),
    })
  ),
});

type ProfileFormValues = z.infer<typeof profileFormSchema>;

const defaultValues: Partial<ProfileFormValues> = {
  items: [{ beer: "", quantity: 1 }],
};

interface Props {
  onSubmit: (data: { name: string; quantity: number }[]) => void;
}

export function ProfileForm({ onSubmit }: Props) {
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues,
  });

  const { fields, append } = useFieldArray({
    name: "items",
    control: form.control,
  });

  const handleSubmit = (data: ProfileFormValues) => {
    onSubmit(
      data.items
        .filter((item) => item.beer)
        ?.map((item) => ({
          name: item.beer,
          quantity: Number(item.quantity),
        }))
    );
  };

  return (
    <Card className="mb-10">
      <CardHeader>
        <CardTitle>New round</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="space-y-8"
          >
            <div>
              {fields.map((field, index) => (
                <div
                  className="flex w-full justify-between max-w-sm items-center space-x-2"
                  key={field.id}
                >
                  <FormField
                    control={form.control}
                    name={`items.${index}.beer`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Bears</FormLabel>
                        <Select
                          onValueChange={field.onChange}
                          defaultValue={field.value}
                        >
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a beer" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="Corona">Corona</SelectItem>
                            <SelectItem value="Quilmes">Quilmes</SelectItem>
                            <SelectItem value="Club Colombia">
                              Club Colombia
                            </SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name={`items.${index}.quantity`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Quantity</FormLabel>
                        <FormControl>
                          <Input type="number" {...field} />
                        </FormControl>

                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              ))}
              <Button
                type="button"
                variant="outline"
                size="sm"
                className="mt-2"
                onClick={() => append({ beer: "", quantity: 1 })}
              >
                Add item
              </Button>
            </div>
            <Button type="submit">Create round</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

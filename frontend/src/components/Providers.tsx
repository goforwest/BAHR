/**
 * React Query Provider wrapper component
 * Must be a client component to use React Query hooks
 */

"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactNode, useState } from "react";

interface ProvidersProps {
  children: ReactNode;
}

/**
 * Providers component that wraps the app with React Query
 * Creates a new QueryClient instance per request to avoid sharing state between users
 */
export function Providers({ children }: ProvidersProps) {
  // Create a new QueryClient instance for each request
  // This prevents state sharing between different users
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Disable automatic refetching on window focus for better UX
            refetchOnWindowFocus: false,
            // Retry failed requests once
            retry: 1,
            // Cache time: 5 minutes
            gcTime: 5 * 60 * 1000,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

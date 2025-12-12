import * as React from "react";

import { cn } from "@/lib/utils";

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/20 border-input/50 h-12 w-full min-w-0 rounded-xl border bg-transparent px-4 py-3 text-base shadow-sm transition-all outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",
        "focus:border-primary focus:ring-4 focus:ring-primary/20 focus:bg-input/5",
        "hover:border-input hover:bg-input/5",
        "aria-invalid:ring-alert-orange/20 aria-invalid:border-alert-orange",
        className
      )}
      {...props}
    />
  );
}

export { Input };

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const statusBadgeVariants = cva(
  "inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-semibold transition-all",
  {
    variants: {
      status: {
        confirmed: "bg-primary/20 text-primary border border-primary/30",
        "in-transit":
          "bg-action-blue/20 text-action-blue border border-action-blue/30",
        loaded:
          "bg-success-green/20 text-success-green border border-success-green/30",
        alert:
          "bg-alert-orange/20 text-alert-orange border border-alert-orange/30",
        scheduled:
          "bg-muted text-muted-foreground border border-muted-foreground/30",
      },
    },
    defaultVariants: {
      status: "scheduled",
    },
  }
);

export interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof statusBadgeVariants> {
  /**
   * Show a pulsing dot indicator
   */
  showPulse?: boolean;
}

const StatusBadge = React.forwardRef<HTMLDivElement, StatusBadgeProps>(
  ({ className, status, showPulse = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(statusBadgeVariants({ status }), className)}
        {...props}
      >
        {showPulse && (
          <span className="relative flex size-2">
            <span
              className={cn(
                "absolute inline-flex h-full w-full animate-ping rounded-full opacity-75",
                status === "confirmed" && "bg-primary",
                status === "in-transit" && "bg-action-blue",
                status === "loaded" && "bg-success-green",
                status === "alert" && "bg-alert-orange",
                status === "scheduled" && "bg-muted-foreground"
              )}
            />
            <span
              className={cn(
                "relative inline-flex size-2 rounded-full",
                status === "confirmed" && "bg-primary",
                status === "in-transit" && "bg-action-blue",
                status === "loaded" && "bg-success-green",
                status === "alert" && "bg-alert-orange",
                status === "scheduled" && "bg-muted-foreground"
              )}
            />
          </span>
        )}
        {children}
      </div>
    );
  }
);
StatusBadge.displayName = "StatusBadge";

export { StatusBadge, statusBadgeVariants };

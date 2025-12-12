import { Outlet } from "react-router-dom";
import { SidebarProvider } from "@/components/ui/sidebar";
import { DashboardSidebar } from "@/components/dashboard/DashboardSidebar";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { Sun, Moon, X } from "lucide-react";
import { useTheme } from "@/components/theme-provider";
import { useState } from "react";

export default function DashboardLayout() {
  const { theme, setTheme } = useTheme();
  const [showThemeToggle, setShowThemeToggle] = useState(true);
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <DashboardSidebar />
        <div className="flex flex-1 flex-col">
          <DashboardHeader />
          <main className="flex-1 p-6">
            <Outlet />
          </main>
        </div>

        {/* Floating Theme Toggle Button */}
        {showThemeToggle && (
          <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2">
            <button
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
              className="flex size-11 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg hover:shadow-xl transition-all hover:scale-110 active:scale-95"
              aria-label="Changer de thème"
            >
              {theme === "light" ? (
                <Moon className="size-5" />
              ) : (
                <Sun className="size-5" />
              )}
            </button>
            <button
              onClick={() => setShowThemeToggle(false)}
              className="flex size-8 items-center justify-center rounded-full bg-muted/80 backdrop-blur-sm text-muted-foreground hover:text-foreground hover:bg-muted transition-all hover:scale-110 active:scale-95"
              aria-label="Cacher le bouton de thème"
            >
              <X className="size-4" />
            </button>
          </div>
        )}
      </div>
    </SidebarProvider>
  );
}

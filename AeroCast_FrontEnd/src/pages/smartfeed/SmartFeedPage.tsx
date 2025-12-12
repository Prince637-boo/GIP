import { GlassCard } from "@/components/ui/glass-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useAuthStore as useAuth } from "@/stores/useAuth";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Plane,
  Bell,
  Navigation as NavigationIcon,
  Briefcase,
} from "lucide-react";

export default function SmartFeedPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  // Mock flight data
  const flightInfo = {
    status: "confirmed" as const,
    flightNumber: "AF 890",
    departure: {
      code: "LFW",
      time: "14:30",
      gate: "B04",
      seat: "12F",
      boarding: "13:45",
    },
    arrival: {
      code: "CDG",
      time: "21:45",
    },
  };

  // Mock weather data
  const weather = {
    location: "Lomé",
    temperature: 28,
    condition: "Vent Fort",
    icon: "🌤️",
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-background/90 p-4 md:p-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <header className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate(-1)}
              className="flex size-10 items-center justify-center rounded-full bg-card/60 backdrop-blur-md border border-border/30 hover:bg-card/80 transition-all"
            >
              <ArrowLeft className="size-5 text-foreground" />
            </button>
            <Avatar className="size-12 border-2 border-primary/30 bg-primary/20">
              <AvatarFallback className="bg-primary/20 text-primary font-bold">
                {user ? getInitials(user.name) : "JK"}
              </AvatarFallback>
            </Avatar>
            <div>
              <p className="text-sm text-muted-foreground">Bonjour,</p>
              <h1 className="text-2xl font-bold text-foreground">
                {user?.name || "Jean K."}
              </h1>
            </div>
          </div>

          <button className="rounded-full p-2 hover:bg-accent/20 transition-colors">
            <Bell className="size-6 text-foreground" />
          </button>
        </header>

        {/* Flight Card */}
        <GlassCard variant="flight" className="mb-6 overflow-hidden">
          <div className="p-6">
            {/* Flight Status */}
            <div className="mb-4 flex items-center justify-between">
              <StatusBadge status="confirmed" showPulse>
                VOL CONFIRMÉ
              </StatusBadge>
              <span className="text-xl font-bold text-primary">
                {flightInfo.flightNumber}
              </span>
            </div>

            {/* Route */}
            <div className="mb-6 flex items-center justify-between">
              <div className="text-center">
                <div className="text-4xl font-bold text-foreground">
                  {flightInfo.departure.code}
                </div>
                <div className="text-sm text-muted-foreground">
                  {flightInfo.departure.time}
                </div>
              </div>

              <div className="flex-1 px-6">
                <div className="relative flex items-center justify-center">
                  <div className="h-0.5 w-full bg-primary/30" />
                  <Plane className="absolute size-6 text-primary" />
                </div>
              </div>

              <div className="text-center">
                <div className="text-4xl font-bold text-foreground">
                  {flightInfo.arrival.code}
                </div>
                <div className="text-sm text-muted-foreground">
                  {flightInfo.arrival.time}
                </div>
              </div>
            </div>

            {/* Flight Details Grid */}
            <div className="grid grid-cols-3 gap-4 border-t border-border/30 pt-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase">Porte</p>
                <p className="text-lg font-bold text-foreground">
                  {flightInfo.departure.gate}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground uppercase">Siège</p>
                <p className="text-lg font-bold text-foreground">
                  {flightInfo.departure.seat}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground uppercase">
                  Embarq.
                </p>
                <p className="text-lg font-bold text-success-green">
                  {flightInfo.departure.boarding}
                </p>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Weather Card */}
        <GlassCard variant="weather" className="mb-6">
          <div className="flex items-center justify-between p-6">
            <div>
              <p className="text-sm text-muted-foreground mb-1">
                Météo {weather.location}
              </p>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold text-foreground">
                  {weather.temperature}°C
                </span>
                <span className="text-lg text-alert-orange font-medium">
                  {weather.condition}
                </span>
              </div>
            </div>
            <div className="text-6xl">{weather.icon}</div>
          </div>
        </GlassCard>

        {/* Action Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Navigation Card */}
          <GlassCard className="group cursor-pointer transition-all hover:scale-[1.02]">
            <div className="flex flex-col items-center justify-center p-8 text-center">
              <div className="mb-4 flex size-20 items-center justify-center rounded-2xl bg-primary/20 group-hover:bg-primary/30 transition-colors">
                <NavigationIcon className="size-10 text-primary" />
              </div>
              <h3 className="text-xl font-bold text-foreground">Me Guider</h3>
              <p className="text-sm text-muted-foreground mt-2">
                Navigation en temps réel vers votre porte
              </p>
            </div>
          </GlassCard>

          {/* Baggage Card */}
          <GlassCard className="group cursor-pointer transition-all hover:scale-[1.02]">
            <div className="flex flex-col items-center justify-center p-8 text-center">
              <div className="mb-4 flex size-20 items-center justify-center rounded-2xl bg-success-green/20 group-hover:bg-success-green/30 transition-colors">
                <Briefcase className="size-10 text-success-green" />
              </div>
              <h3 className="text-xl font-bold text-foreground">Bagages</h3>
              <p className="text-sm text-muted-foreground mt-2">
                Suivez vos bagages en temps réel
              </p>
            </div>
          </GlassCard>
        </div>

        {/* Responsive Bottom Spacing */}
        <div className="h-8 md:h-16" />
      </div>
    </div>
  );
}

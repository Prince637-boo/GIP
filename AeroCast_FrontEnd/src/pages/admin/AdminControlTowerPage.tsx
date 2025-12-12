import { GlassCard } from "@/components/ui/glass-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Globe,
  TrendingUpIcon,
  Briefcase,
  Clock,
  PieChart,
  AlertCircle,
} from "lucide-react";
interface DensityZone {
  id: string;
  name: string;
  density: number;
  status: "normal" | "moderate" | "congested";
  x: number;
  y: number;
}

export default function AdminControlTowerPage() {
  const navigate = useNavigate();

  const airportInfo = {
    name: "Aéroport Gnassingbé Eyadéma",
    code: "LFW",
    time: "14:45 UTC",
    passengers: 1245,
    trend: "+12%",
    activeAlerts: 2,
  };

  const densityZones: DensityZone[] = [
    {
      id: "1",
      name: "Zone B (Check-in)",
      density: 45,
      status: "normal",
      x: 30,
      y: 40,
    },
    {
      id: "2",
      name: "Zone B (Enregistrement)",
      density: 78,
      status: "congested",
      x: 50,
      y: 60,
    },
  ];

  const criticalFlows = [
    {
      name: "Sécurité T1",
      status: "normal" as const,
      value: 85,
      color: "success-green",
    },
    {
      name: "Enreg. Zone B",
      status: "alert" as const,
      value: 45,
      color: "alert-orange",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-background/90">
      {/* Header */}
      <header className="border-b border-border/30 bg-card/20 backdrop-blur-md">
        <div className="container mx-auto flex items-center justify-between p-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate(-1)}
              className="flex size-10 items-center justify-center rounded-full hover:bg-accent/20 transition-colors"
            >
              <ArrowLeft className="size-5 text-foreground" />
            </button>
            <h1 className="text-xl font-bold text-foreground">
              GIP <span className="text-primary">ADMIN</span>
            </h1>
            <nav className="hidden md:flex items-center gap-6 ml-8">
              <a
                href="#"
                className="flex items-center gap-2 text-primary font-semibold border-b-2 border-primary pb-1"
              >
                <Globe className="size-4" />
                Vue Globale
              </a>
              <a
                href="#"
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <TrendingUpIcon className="size-4" />
                Gestion Flux
              </a>
              <a
                href="#"
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <Briefcase className="size-4" />
                Bagages
              </a>
              <a
                href="#"
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <PieChart className="size-4" />
                Analytics
              </a>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="size-4" />
              {airportInfo.time}
            </div>
            <StatusBadge status="alert" showPulse>
              {airportInfo.activeAlerts} Alertes Actives
            </StatusBadge>
          </div>
        </div>
      </header>

      <div className="container mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Airport Info */}
          <GlassCard>
            <div className="p-6">
              <h2 className="text-2xl font-bold text-foreground mb-1">
                {airportInfo.name} ({airportInfo.code})
              </h2>
              <div className="mt-4">
                <p className="text-sm text-muted-foreground uppercase mb-1">
                  Pax sur Site
                </p>
                <div className="flex items-baseline gap-2">
                  <p className="text-4xl font-bold text-primary">
                    {airportInfo.passengers.toLocaleString()}
                  </p>
                  <span className="text-lg font-semibold text-success-green">
                    {airportInfo.trend} prévision
                  </span>
                </div>
              </div>
            </div>
          </GlassCard>

          {/* Critical Flows */}
          <GlassCard className="lg:col-span-2">
            <div className="p-6">
              <h3 className="text-lg font-bold text-foreground mb-4">
                Flux Critiques
              </h3>
              <div className="space-y-4">
                {criticalFlows.map((flow) => (
                  <div key={flow.name}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-foreground">
                        {flow.name}
                      </span>
                      <div className="flex items-center gap-2">
                        <StatusBadge
                          status={flow.status === "normal" ? "loaded" : "alert"}
                        >
                          {flow.status === "normal" ? "Fluide" : "Chargé"}
                        </StatusBadge>
                      </div>
                    </div>
                    <div className="relative h-3 rounded-full bg-card/50 overflow-hidden">
                      <div
                        className={`absolute inset-y-0 left-0 rounded-full transition-all ${
                          flow.status === "normal"
                            ? "bg-success-green"
                            : "bg-alert-orange"
                        }`}
                        style={{ width: `${flow.value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Density Map */}
        <GlassCard className="mb-6">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold text-foreground">
                Zones de Densité
              </h3>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="size-3 rounded-full bg-success-green" />
                  <span className="text-xs text-muted-foreground">Normal</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="size-3 rounded-full bg-primary" />
                  <span className="text-xs text-muted-foreground">Modéré</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="size-3 rounded-full bg-alert-orange" />
                  <span className="text-xs text-muted-foreground">
                    Congestionné
                  </span>
                </div>
              </div>
            </div>

            {/* Map Visualization */}
            <div className="relative aspect-video rounded-xl bg-gradient-to-br from-card/30 to-card/10 border border-border/30 overflow-hidden">
              {/* Grid Background */}
              <div
                className="absolute inset-0 opacity-20"
                style={{
                  backgroundImage: `
                    linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px)
                  `,
                  backgroundSize: "40px 40px",
                }}
              />

              {/* Density Zones */}
              {densityZones.map((zone) => (
                <div
                  key={zone.id}
                  className="absolute"
                  style={{
                    left: `${zone.x}%`,
                    top: `${zone.y}%`,
                  }}
                >
                  {/* Pulse Effect */}
                  <div
                    className={`absolute size-32 rounded-full opacity-20 animate-ping ${
                      zone.status === "congested"
                        ? "bg-alert-orange"
                        : zone.status === "moderate"
                        ? "bg-primary"
                        : "bg-success-green"
                    }`}
                  />

                  {/* Zone Marker */}
                  <div
                    className={`relative size-24 rounded-full flex items-center justify-center ${
                      zone.status === "congested"
                        ? "bg-alert-orange/30 border-2 border-alert-orange"
                        : zone.status === "moderate"
                        ? "bg-primary/30 border-2 border-primary"
                        : "bg-success-green/30 border-2 border-success-green"
                    }`}
                  >
                    <span className="text-2xl font-bold text-foreground">
                      {zone.density}%
                    </span>
                  </div>

                  {/* Zone Label */}
                  <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap">
                    <div className="bg-card/80 backdrop-blur-sm px-3 py-1 rounded-lg border border-border/30">
                      <p className="text-xs font-semibold text-foreground">
                        {zone.name}
                      </p>
                    </div>
                  </div>
                </div>
              ))}

              {/* Congestion Alert Tooltip */}
              <div className="absolute bottom-4 right-4">
                <div className="bg-alert-orange/20 backdrop-blur-md px-4 py-2 rounded-xl border-2 border-alert-orange/50">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="size-5 text-alert-orange" />
                    <div>
                      <p className="text-sm font-bold text-alert-orange uppercase">
                        CONGESTION
                      </p>
                      <p className="text-xs text-foreground">
                        Zone B Enregistrement
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

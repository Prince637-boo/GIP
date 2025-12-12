import { GlassCard } from "@/components/ui/glass-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { cn } from "@/lib/utils";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  MoreVertical,
  Briefcase,
  CheckCircle2,
  Loader2,
  Circle,
  UserCheck,
  Info,
  QrCode,
} from "lucide-react";

interface BaggageStation {
  id: string;
  title: string;
  subtitle: string;
  time: string;
  status: "completed" | "current" | "pending";
  validatedBy?: string;
}

export default function BaggageTrackingPage() {
  const navigate = useNavigate();

  const baggageInfo = {
    id: "#2890",
    type: "Samsonite Noir",
    weight: "23kg",
    status: "in-transit" as const,
  };

  const timeline: BaggageStation[] = [
    {
      id: "1",
      title: "Chargé dans l'avion",
      subtitle: "Soute A",
      time: "14:02",
      status: "completed",
      validatedBy: "Agent ID-44",
    },
    {
      id: "2",
      title: "Contrôle Sûreté (RX)",
      subtitle: "Terminal 2",
      time: "13:45",
      status: "current",
    },
    {
      id: "3",
      title: "Enregistrement",
      subtitle: "Guichet 12",
      time: "13:10",
      status: "pending",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-background/90 p-4 md:p-8">
      <div className="mx-auto max-w-2xl">
        {/* Header */}
        <div className="mb-6 flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="flex size-12 items-center justify-center rounded-full bg-card/60 backdrop-blur-md border border-border/30 hover:bg-card/80 transition-all"
          >
            <ArrowLeft className="size-5 text-foreground" />
          </button>
          <h1 className="text-2xl font-bold text-foreground">Suivi Bagage</h1>
          <button className="ml-auto flex size-12 items-center justify-center rounded-full hover:bg-accent/20 transition-colors">
            <MoreVertical className="size-5 text-foreground" />
          </button>
        </div>

        {/* Baggage Info Card */}
        <GlassCard className="mb-6">
          <div className="flex items-center gap-4 p-4">
            <div className="flex size-16 shrink-0 items-center justify-center rounded-2xl bg-primary/20">
              <Briefcase className="size-8 text-primary" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h2 className="text-2xl font-bold text-foreground">
                  {baggageInfo.id}
                </h2>
                <StatusBadge status={baggageInfo.status} showPulse>
                  EN TRANSIT
                </StatusBadge>
              </div>
              <p className="text-sm text-muted-foreground">
                {baggageInfo.type} • {baggageInfo.weight}
              </p>
            </div>
          </div>
        </GlassCard>

        {/* Timeline Card */}
        <GlassCard>
          <div className="p-6">
            <h3 className="text-lg font-bold text-foreground mb-6">
              Suivi en temps réel
            </h3>

            <div className="relative">
              {timeline.map((station, index) => {
                const isLast = index === timeline.length - 1;
                const isCompleted = station.status === "completed";
                const isCurrent = station.status === "current";

                return (
                  <div key={station.id} className="relative flex gap-4 pb-8">
                    {/* Timeline Line */}
                    {!isLast && (
                      <div
                        className={cn(
                          "absolute left-6 top-12 h-full w-0.5 -ml-px",
                          isCompleted ? "bg-success-green" : "bg-border/30"
                        )}
                      />
                    )}

                    {/* Status Icon */}
                    <div className="relative z-10 flex shrink-0 flex-col items-center">
                      <div
                        className={cn(
                          "flex size-12 items-center justify-center rounded-full border-4 transition-all",
                          isCompleted &&
                            "bg-success-green border-success-green/30 shadow-lg shadow-success-green/20",
                          isCurrent &&
                            "bg-primary border-primary/30 shadow-lg shadow-primary/20 animate-pulse",
                          !isCompleted &&
                            !isCurrent &&
                            "bg-card border-border/30"
                        )}
                      >
                        {isCompleted && (
                          <CheckCircle2 className="size-6 text-white" />
                        )}
                        {isCurrent && (
                          <Loader2 className="size-6 text-white animate-spin" />
                        )}
                        {!isCompleted && !isCurrent && (
                          <Circle className="size-5 text-muted-foreground" />
                        )}
                      </div>
                    </div>

                    {/* Station Info */}
                    <div className="flex-1 pt-1">
                      <div className="flex items-start justify-between gap-4 mb-1">
                        <h4
                          className={cn(
                            "font-bold text-base",
                            isCompleted && "text-success-green",
                            isCurrent && "text-primary",
                            !isCompleted &&
                              !isCurrent &&
                              "text-muted-foreground"
                          )}
                        >
                          {station.title}
                        </h4>
                        <span
                          className={cn(
                            "text-sm font-medium",
                            isCompleted && "text-success-green",
                            isCurrent && "text-primary",
                            !isCompleted &&
                              !isCurrent &&
                              "text-muted-foreground"
                          )}
                        >
                          {station.time}
                        </span>
                      </div>

                      <p className="text-sm text-muted-foreground mb-2">
                        {station.subtitle}
                      </p>

                      {station.validatedBy && (
                        <div className="flex items-center gap-2 mt-2">
                          <UserCheck className="size-4 text-success-green" />
                          <p className="text-xs text-success-green font-medium">
                            Validé par {station.validatedBy}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Info Note */}
            <div className="mt-6 flex items-start gap-3 rounded-xl bg-primary/10 p-4 border border-primary/20">
              <Info className="size-5 text-primary shrink-0" />
              <p className="text-sm text-foreground">
                <strong className="font-semibold">Transparence Totale:</strong>{" "}
                Timeline verticale inspirée des apps de livraison (Uber/FedEx)
                pour rassurer le passager.
              </p>
            </div>
          </div>
        </GlassCard>

        {/* QR Code Card (Optional) */}
        <div className="mt-6">
          <GlassCard>
            <div className="flex items-center justify-between p-6">
              <div>
                <h4 className="font-bold text-foreground mb-1">Code bagage</h4>
                <p className="text-sm text-muted-foreground">
                  Scannez pour plus d'infos
                </p>
              </div>
              <div className="flex size-20 items-center justify-center rounded-xl bg-card border border-border">
                <QrCode className="size-10 text-foreground" />
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}

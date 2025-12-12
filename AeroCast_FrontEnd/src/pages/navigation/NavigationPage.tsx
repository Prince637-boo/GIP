import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { GlassCard } from "@/components/ui/glass-card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, AlertTriangle, Play, Zap, Eye } from "lucide-react";

export default function NavigationPage() {
  const navigate = useNavigate();
  const [estimatedTime, setEstimatedTime] = useState(8);

  // Simulate time countdown
  useEffect(() => {
    const interval = setInterval(() => {
      setEstimatedTime((prev) => Math.max(0, prev - 1));
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-background via-background/95 to-background/90 overflow-hidden">
      {/* Alert Banner */}
      <div className="absolute top-4 left-4 right-4 z-20 md:left-1/2 md:-translate-x-1/2 md:max-w-md">
        <GlassCard variant="alert" className="border-2">
          <div className="flex items-start gap-3 p-4">
            <div className="flex size-12 shrink-0 items-center justify-center rounded-full bg-alert-orange">
              <AlertTriangle className="size-6 text-white" />
            </div>
            <div className="flex-1">
              <p className="font-bold text-alert-orange uppercase text-sm mb-1">
                ALERTE : PORTE CHANGÉE
              </p>
              <p className="text-sm text-foreground font-medium">
                Allez vers Porte F12
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                3 min (250m) • Évitez la zone B
              </p>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Map Container */}
      <div className="relative h-screen w-full">
        {/* Simulated Map Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-muted/40 to-muted/60">
          {/* Map Grid Pattern */}
          <div
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: `
                linear-gradient(rgba(56, 189, 248, 0.3) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56, 189, 248, 0.3) 1px, transparent 1px)
              `,
              backgroundSize: "50px 50px",
            }}
          />

          {/* Route Path */}
          <svg
            className="absolute inset-0 w-full h-full"
            viewBox="0 0 400 800"
            preserveAspectRatio="xMidYMid meet"
          >
            {/* Animated Route Line */}
            <path
              d="M 200 700 Q 250 500 350 300"
              fill="none"
              stroke="url(#gradient)"
              strokeWidth="6"
              strokeLinecap="round"
              className="drop-shadow-[0_0_10px_rgba(56,189,248,0.5)]"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="100%" x2="0%" y2="0%">
                <stop offset="0%" stopColor="#38BDF8" stopOpacity="1" />
                <stop offset="100%" stopColor="#38BDF8" stopOpacity="0.3" />
              </linearGradient>
            </defs>

            {/* Current Position */}
            <circle cx="200" cy="700" r="12" fill="#38BDF8">
              <animate
                attributeName="r"
                values="12;16;12"
                dur="2s"
                repeatCount="indefinite"
              />
            </circle>
            <circle cx="200" cy="700" r="20" fill="#38BDF8" opacity="0.3">
              <animate
                attributeName="r"
                values="20;30;20"
                dur="2s"
                repeatCount="indefinite"
              />
            </circle>

            {/* Destination */}
            <circle
              cx="350"
              cy="300"
              r="10"
              fill="#F97316"
              stroke="#F97316"
              strokeWidth="2"
            />
          </svg>

          {/* Zone Labels */}
          <div className="absolute top-1/4 right-8 bg-card/60 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-border/30">
            <p className="text-xs font-semibold text-muted-foreground">
              Zone B (Check-In)
            </p>
          </div>

          <div className="absolute top-1/3 right-12 bg-primary/20 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-primary/50">
            <p className="text-xs font-semibold text-primary">Sécurité T1</p>
          </div>
        </div>

        {/* Bottom Info Card */}
        <div className="absolute bottom-6 left-4 right-4 z-10 md:left-1/2 md:-translate-x-1/2 md:max-w-md">
          <GlassCard className="overflow-hidden">
            <div className="p-6">
              {/* Time Estimate */}
              <div className="mb-4 flex items-baseline justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">
                    Temps estimé
                  </p>
                  <p className="text-5xl font-bold text-foreground">
                    {estimatedTime} min
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-muted-foreground mb-1">Distance</p>
                  <p className="text-2xl font-semibold text-muted-foreground">
                    250m
                  </p>
                </div>
              </div>

              {/* Action Button */}
              <Button size="lg" className="w-full group">
                <Play className="size-5 fill-current group-hover:scale-110 transition-transform" />
                Y aller
              </Button>

              {/* Features UX */}
              <div className="mt-6 space-y-3 border-t border-border/30 pt-4">
                <div className="flex items-start gap-3">
                  <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-alert-orange/20">
                    <Zap className="size-4 text-alert-orange" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-foreground">
                      Intervention IA
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Détecte la congestion et recalcule le chemin.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/20">
                    <Eye className="size-4 text-primary" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-foreground">
                      Clarté Visuelle
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Contraste élevé pour lisibilité en marchant.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>

      {/* Back Button */}
      <div className="absolute top-4 left-4 z-20">
        <button
          onClick={() => navigate(-1)}
          className="flex size-12 items-center justify-center rounded-full bg-card/60 backdrop-blur-md border border-border/30 hover:bg-card/80 transition-all"
        >
          <ArrowLeft className="size-5 text-foreground" />
        </button>
      </div>
    </div>
  );
}

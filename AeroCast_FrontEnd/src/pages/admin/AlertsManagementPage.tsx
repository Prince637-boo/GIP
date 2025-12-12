import { useState } from "react";
import { GlassCard } from "@/components/ui/glass-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Plus,
  Edit,
  Trash2,
  Send,
  Bell,
  CheckCircle,
  AlertTriangle,
  Clock,
  AlertCircle,
  Info,
  Cloud,
} from "lucide-react";

interface Alert {
  id: string;
  type: "gate-change" | "security" | "weather";
  typeLabel: string;
  message: string;
  impact: string;
  status: "sent" | "action-required" | "scheduled";
  statusLabel: string;
  timestamp: string;
}

export default function AlertsManagementPage() {
  const navigate = useNavigate();
  const [selectedAlert, setSelectedAlert] = useState<string | null>(null);

  const alerts: Alert[] = [
    {
      id: "#8901",
      type: "gate-change",
      typeLabel: "Changement Porte",
      message: "Vol AF890: Allez porte F12...",
      impact: "245 Pax",
      status: "sent",
      statusLabel: "ENVOYÉ",
      timestamp: "14:23",
    },
    {
      id: "#8902",
      type: "security",
      typeLabel: "Alerte Sécurité",
      message: "Bagage isolé Zone B...",
      impact: "1 Pax",
      status: "action-required",
      statusLabel: "ACTION REQUISE",
      timestamp: "14:20",
    },
    {
      id: "#8903",
      type: "weather",
      typeLabel: "Info Météo",
      message: "Orage prévu. Vols retardés.",
      impact: "All Pax",
      status: "scheduled",
      statusLabel: "PROGRAMMÉ",
      timestamp: "14:15",
    },
  ];

  const getAlertIcon = (type: Alert["type"]) => {
    switch (type) {
      case "gate-change":
        return Bell;
      case "security":
        return AlertCircle;
      case "weather":
        return Cloud;
    }
  };

  const getAlertColor = (type: Alert["type"]) => {
    switch (type) {
      case "gate-change":
        return "alert-orange";
      case "security":
        return "destructive";
      case "weather":
        return "primary";
    }
  };

  const getStatusBadgeStatus = (status: Alert["status"]) => {
    switch (status) {
      case "sent":
        return "loaded" as const;
      case "action-required":
        return "alert" as const;
      case "scheduled":
        return "scheduled" as const;
    }
  };

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
            <h1 className="text-2xl font-bold text-foreground">
              Centre de Gestion des Alertes
            </h1>
          </div>
          <Button>
            <Plus className="size-4 mr-2" />
            Nouvelle Notification
          </Button>
        </div>
      </header>

      <div className="container mx-auto p-6">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <GlassCard>
            <div className="p-4">
              <div className="flex items-center gap-3">
                <div className="flex size-12 items-center justify-center rounded-xl bg-success-green/20">
                  <CheckCircle className="size-6 text-success-green" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">12</p>
                  <p className="text-sm text-muted-foreground">
                    Alertes envoyées
                  </p>
                </div>
              </div>
            </div>
          </GlassCard>

          <GlassCard>
            <div className="p-4">
              <div className="flex items-center gap-3">
                <div className="flex size-12 items-center justify-center rounded-xl bg-alert-orange/20">
                  <AlertTriangle className="size-6 text-alert-orange" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">3</p>
                  <p className="text-sm text-muted-foreground">
                    Actions requises
                  </p>
                </div>
              </div>
            </div>
          </GlassCard>

          <GlassCard>
            <div className="p-4">
              <div className="flex items-center gap-3">
                <div className="flex size-12 items-center justify-center rounded-xl bg-primary/20">
                  <Clock className="size-6 text-primary" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">5</p>
                  <p className="text-sm text-muted-foreground">Programmées</p>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Alerts Table */}
        <GlassCard>
          <div className="overflow-hidden">
            {/* Table Header */}
            <div className="grid grid-cols-12 gap-4 p-4 bg-card/30 border-b border-border/30 text-sm font-semibold text-muted-foreground uppercase">
              <div className="col-span-1">ID</div>
              <div className="col-span-2">Type</div>
              <div className="col-span-4">Message Passager</div>
              <div className="col-span-2">Impact</div>
              <div className="col-span-2">Statut</div>
              <div className="col-span-1">Heure</div>
            </div>

            {/* Table Body */}
            <div className="divide-y divide-border/30">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={cn(
                    "grid grid-cols-12 gap-4 p-4 transition-all cursor-pointer hover:bg-card/30",
                    selectedAlert === alert.id && "bg-card/50"
                  )}
                  onClick={() =>
                    setSelectedAlert(
                      selectedAlert === alert.id ? null : alert.id
                    )
                  }
                >
                  <div className="col-span-1">
                    <span className="text-sm font-mono text-muted-foreground">
                      {alert.id}
                    </span>
                  </div>

                  <div className="col-span-2">
                    <div className="flex items-center gap-2">
                      {(() => {
                        const Icon = getAlertIcon(alert.type);
                        return (
                          <Icon
                            className="size-5"
                            style={{
                              color: `var(--color-${getAlertColor(
                                alert.type
                              )})`,
                            }}
                          />
                        );
                      })()}
                      <span
                        className={cn(
                          "text-sm font-semibold",
                          `text-${getAlertColor(alert.type)}`
                        )}
                      >
                        {alert.typeLabel}
                      </span>
                    </div>
                  </div>

                  <div className="col-span-4">
                    <p className="text-sm text-foreground">{alert.message}</p>
                  </div>

                  <div className="col-span-2">
                    <p className="text-sm text-foreground">{alert.impact}</p>
                  </div>

                  <div className="col-span-2">
                    <StatusBadge status={getStatusBadgeStatus(alert.status)}>
                      {alert.statusLabel}
                    </StatusBadge>
                  </div>

                  <div className="col-span-1">
                    <p className="text-sm text-muted-foreground">
                      {alert.timestamp}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons (when alert selected) */}
          {selectedAlert && (
            <div className="border-t border-border/30 p-4 bg-card/20">
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Alerte {selectedAlert} sélectionnée
                </p>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    <Edit className="size-4 mr-1" />
                    Modifier
                  </Button>
                  <Button variant="destructive" size="sm">
                    <Trash2 className="size-4 mr-1" />
                    Supprimer
                  </Button>
                  <Button size="sm">
                    <Send className="size-4 mr-1" />
                    Renvoyer
                  </Button>
                </div>
              </div>
            </div>
          )}
        </GlassCard>

        {/* Info Card */}
        <div className="mt-6">
          <GlassCard>
            <div className="flex items-start gap-4 p-6">
              <div className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary/20">
                <Info className="size-6 text-primary" />
              </div>
              <div>
                <h4 className="font-bold text-foreground mb-2">
                  Système de Notification Push
                </h4>
                <p className="text-sm text-muted-foreground">
                  Les alertes sont envoyées en temps réel aux passagers
                  concernés via l'application mobile. Le système priorise les
                  notifications critiques (changement de porte, sécurité) et
                  adapte le message selon le contexte du passager.
                </p>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}

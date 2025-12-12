export type SidebarItem = {
  title: string;
  href: string;
  icon: string;
  badge?: string | number;
  items?: SidebarItem[];
};

export const sidebarConfig: SidebarItem[] = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: "mdi-light--view-dashboard",
  },
  {
    title: "Smart Feed",
    href: "/feed",
    icon: "mdi-light--home",
    badge: "NEW",
  },
  {
    title: "Navigation",
    href: "/navigation",
    icon: "mdi-light--navigation",
    badge: "NEW",
  },
  {
    title: "Suivi Bagages",
    href: "/baggage-tracking",
    icon: "mdi-light--package-variant",
    badge: "NEW",
  },
  {
    title: "Météo",
    href: "/dashboard/meteo",
    icon: "mdi-light--weather-cloudy",
    items: [
      {
        title: "Prévisions",
        href: "/dashboard/meteo/predictions",
        icon: "mdi-light--chart-line",
      },
      {
        title: "Alertes",
        href: "/dashboard/meteo/alertes",
        icon: "mdi-light--alert",
      },
      {
        title: "Aéroports",
        href: "/dashboard/meteo/aeroports",
        icon: "mdi-light--airplane",
      },
    ],
  },
  {
    title: "Bagages",
    href: "/dashboard/bagages",
    icon: "mdi-light--bag-suitcase",
    items: [
      {
        title: "Suivi",
        href: "/dashboard/bagages/suivi",
        icon: "mdi-light--map-marker",
      },
      {
        title: "Scanner",
        href: "/dashboard/bagages/scanner",
        icon: "mdi-light--qrcode-scan",
      },
      {
        title: "Incidents",
        href: "/dashboard/bagages/incidents",
        icon: "mdi-light--alert-circle",
      },
    ],
  },
  {
    title: "Administration",
    href: "/admin",
    icon: "mdi-light--shield-account",
    badge: "ADMIN",
    items: [
      {
        title: "Tour de Contrôle",
        href: "/admin/control-tower",
        icon: "mdi-light--radar",
      },
      {
        title: "Gestion des Alertes",
        href: "/admin/alerts",
        icon: "mdi-light--bell-alert",
      },
    ],
  },
  {
    title: "Statistiques",
    href: "/dashboard/statistiques",
    icon: "mdi-light--chart-bar",
  },
  {
    title: "Paramètres",
    href: "/dashboard/settings",
    icon: "mdi-light--cog",
  },
];

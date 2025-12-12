import { Link } from "react-router-dom";
import {
  Cloud,
  Package,
  Navigation,
  AlertTriangle,
  Plane,
  QrCode,
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary/10 via-background to-background">
        <div className="container mx-auto px-6 py-24 lg:py-32">
          <div className="flex flex-col items-center text-center">
            <div className="mb-2 text-sm font-medium text-primary tracking-widest uppercase">
              Guide Intelligent des Passagers
            </div>
            <div className="mb-8 flex items-center gap-3">
              <Plane className="h-14 w-14 text-primary" />
              <h1 className="text-6xl font-bold tracking-tight lg:text-8xl">
                GIP
              </h1>
            </div>
            <p className="mb-4 text-2xl font-semibold text-foreground lg:text-3xl max-w-3xl">
              Voir votre voyage
            </p>
            <p className="mb-12 text-lg text-muted-foreground max-w-2xl">
              Maîtrisez le destin du voyageur avec des prévisions météo
              aéroportuaires et un suivi de bagages intelligent en temps réel
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                to="/dashboard"
                className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Accéder au tableau de bord
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center justify-center rounded-lg border border-border px-8 py-3 text-lg font-semibold hover:bg-accent transition-colors"
              >
                Se connecter
              </Link>
            </div>
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute top-20 left-10 opacity-10">
          <Cloud className="h-32 w-32 text-primary" />
        </div>
        <div className="absolute bottom-20 right-10 opacity-10">
          <Package className="h-28 w-28 text-chart-2" />
        </div>
      </section>

      {/* Problem Section - Le "Trou Noir" du voyageur */}
      <section className="py-24 bg-destructive/5 border-y border-destructive/20">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold mb-8 text-center">
              Le "Trou Noir" du Voyageur
            </h2>
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div>
                <p className="text-lg mb-6 leading-relaxed">
                  Le véritable danger n'est pas le retard, c'est{" "}
                  <span className="font-bold text-destructive">
                    l'ignorance
                  </span>
                  .
                </p>
                <p className="text-muted-foreground mb-6">
                  Sans information en temps réel sur les conditions
                  météorologiques et la localisation de leurs bagages, les
                  passagers naviguent à l'aveugle dans l'aéroport, source de
                  stress et de perte de contrôle.
                </p>
                <p className="text-muted-foreground">
                  C'est cette situation qui crée la frustration : ne pas pouvoir
                  anticiper ni planifier le déroulement du voyage.
                </p>
              </div>
              <div className="flex flex-col gap-4">
                <div className="p-6 rounded-lg bg-destructive/10 border border-destructive/30">
                  <div className="flex items-center gap-3 mb-2">
                    <AlertTriangle className="h-8 w-8 text-destructive" />
                    <span className="text-4xl font-bold text-destructive">
                      90%
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    des retards perçus ne sont pas dus au retard réel, mais au
                    manque d'information
                  </p>
                </div>
                <div className="p-6 rounded-lg bg-primary/10 border border-primary/30">
                  <div className="flex items-center gap-3 mb-2">
                    <Cloud className="h-8 w-8 text-primary" />
                    <span className="text-2xl font-bold text-primary">
                      Fluidité
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    L'information en temps réel transforme l'incertitude en
                    sérénité
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section - Orientation Dynamique */}
      <section className="py-24">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center mb-16">
            <h2 className="text-3xl font-bold mb-6">
              L'Orientation Dynamique : Zéro Friction
            </h2>
            <p className="text-lg text-muted-foreground">
              Des flux simples et intuitifs, sans préférences d'usagers,
              combinant les{" "}
              <span className="font-semibold text-foreground">
                conditions météo
              </span>{" "}
              avec le{" "}
              <span className="font-semibold text-foreground">
                suivi de bagages
              </span>{" "}
              pour un voyage sans stress.
            </p>
          </div>
          <div className="flex justify-center gap-8 flex-wrap">
            <div className="flex flex-col items-center gap-2">
              <div className="rounded-full bg-primary/10 p-6 border-4 border-primary/30">
                <Navigation className="h-10 w-10 text-primary" />
              </div>
              <span className="font-semibold">Direction</span>
            </div>
            <div className="flex items-center">
              <div className="h-1 w-12 bg-border"></div>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="rounded-full bg-chart-3/10 p-6 border-4 border-chart-3/30">
                <Cloud className="h-10 w-10 text-chart-3" />
              </div>
              <span className="font-semibold">Météo</span>
            </div>
            <div className="flex items-center">
              <div className="h-1 w-12 bg-border"></div>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="rounded-full bg-chart-2/10 p-6 border-4 border-chart-2/30">
                <Package className="h-10 w-10 text-chart-2" />
              </div>
              <span className="font-semibold">Bagages</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Le Cerveau GIP */}
      <section className="py-24 bg-muted/30">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-4">
            Le Cerveau GIP : Tout de Contrôlé
          </h2>
          <p className="text-center text-muted-foreground mb-16 max-w-2xl mx-auto">
            Une plateforme complète pour maîtriser chaque aspect de votre voyage
            aéroportuaire
          </p>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <div className="flex flex-col p-8 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-primary/10 p-4 w-fit">
                <Cloud className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">
                Météo Aéroportuaire
              </h3>
              <p className="text-muted-foreground">
                Prévisions météorologiques précises et en temps réel pour tous
                les aéroports, avec alertes automatiques en cas de conditions
                extrêmes
              </p>
            </div>

            <div className="flex flex-col p-8 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-2/10 p-4 w-fit">
                <QrCode className="h-8 w-8 text-chart-2" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Suivi de Bagages</h3>
              <p className="text-muted-foreground">
                Localisez vos bagages en temps réel grâce aux codes QR
                intelligents et recevez des notifications à chaque étape
              </p>
            </div>

            <div className="flex flex-col p-8 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-3/10 p-4 w-fit">
                <Navigation className="h-8 w-8 text-chart-3" />
              </div>
              <h3 className="text-xl font-semibold mb-3">
                Navigation Intelligente
              </h3>
              <p className="text-muted-foreground">
                Guidage dynamique dans l'aéroport avec calcul d'itinéraire
                optimal basé sur les conditions en temps réel
              </p>
            </div>

            <div className="flex flex-col p-8 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-4/10 p-4 w-fit">
                <AlertTriangle className="h-8 w-8 text-chart-4" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Alertes Proactives</h3>
              <p className="text-muted-foreground">
                Notifications intelligentes pour les changements de porte,
                retards et conditions météo impactant votre vol
              </p>
            </div>

            <div className="flex flex-col p-8 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-primary/10 p-4 w-fit">
                <Plane className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">
                Tableau de Bord Unifié
              </h3>
              <p className="text-muted-foreground">
                Vue centralisée de toutes vos informations de vol, météo et
                bagages dans une interface intuitive
              </p>
            </div>

            <div className="flex flex-col p-8 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-2/10 p-4 w-fit">
                <Package className="h-8 w-8 text-chart-2" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Solutions B2B</h3>
              <p className="text-muted-foreground">
                Abonnements professionnels pour compagnies aériennes et
                gestionnaires d'aéroports avec analytics avancés
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Roadmap Section */}
      <section className="py-24">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-16">
            Feuille de Route & Conformité
          </h2>
          <div className="grid gap-8 md:grid-cols-3 max-w-5xl mx-auto">
            <div className="relative p-8 rounded-lg border-2 border-primary/30 bg-card hover:border-primary transition-colors">
              <div className="text-5xl font-bold text-primary/20 mb-4 hover:text-primary">
                01
              </div>
              <h3 className="text-xl font-semibold mb-3">
                Fondation Immédiate
              </h3>
              <p className="text-muted-foreground">
                Déploiement du système de suivi météo et bagages avec
                authentification JWT sécurisée et tableau de bord intuitif
              </p>
            </div>

            <div className="relative p-8 rounded-lg border-2 border-chart-3/30 bg-card hover:border-chart-3 transition-colors">
              <div className="text-5xl font-bold text-chart-3/20 mb-4 hover:text-chart-3">
                02
              </div>
              <h3 className="text-xl font-semibold mb-3">
                Puissance & Conformité
              </h3>
              <p className="text-muted-foreground">
                Intégration des APIs temps réel, système d'alertes avancé et
                conformité RGPD pour la gestion des données passagers
              </p>
            </div>

            <div className="relative p-8 rounded-lg border-2 border-chart-2/30 bg-card hover:border-chart-2 transition-colors">
              <div className="text-5xl font-bold text-chart-2/20 mb-4 hover:text-chart-2">
                03
              </div>
              <h3 className="text-xl font-semibold mb-3">Richesse Accélérée</h3>
              <p className="text-muted-foreground">
                Expansion avec ML pour prédictions avancées, application mobile
                et intégration IoT pour tracking ultra-précis
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Why GIP Section */}
      <section className="py-24 bg-gradient-to-b from-primary/5 to-background">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">
            Pourquoi <span className="text-primary">GIP</span> ?
          </h2>
          <div className="grid md:grid-cols-2 gap-12 max-w-5xl mx-auto">
            <div>
              <h3 className="text-xl font-semibold mb-4 text-primary">
                Zéro Latence Mentale
              </h3>
              <p className="text-muted-foreground mb-6">
                Aucune friction : les informations arrivent au moment où vous en
                avez besoin. Le système anticipe vos questions avant même que
                vous les posiez.
              </p>
              <p className="text-muted-foreground">
                Météo, bagages, navigation - tout est synchronisé pour que votre
                cerveau puisse se concentrer sur l'essentiel : votre voyage.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4 text-chart-2">
                Une Confiance
              </h3>
              <p className="text-muted-foreground mb-6">
                Le système met en place la technologie et la confiance
                nécessaires pour que chaque passager se sente en contrôle, du
                décollage à l'atterrissage.
              </p>
              <p className="text-muted-foreground">
                Fini le stress de l'inconnu. Avec GIP, vous savez toujours où
                vous en êtes et ce qui vous attend.
              </p>
            </div>
          </div>
          <div className="mt-12 text-center">
            <p className="text-sm text-muted-foreground mb-6 max-w-2xl mx-auto">
              Simplement conçu par la Technologie de la Confiance
            </p>
            <Link
              to="/dashboard"
              className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Découvrir le système
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-muted/30">
        <div className="container mx-auto px-6">
          <div className="rounded-2xl bg-gradient-to-r from-primary/20 via-chart-2/20 to-primary/20 p-12 text-center border border-primary/20">
            <h2 className="text-3xl font-bold mb-4">
              Prêt à maîtriser votre voyage ?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Rejoignez les milliers de passagers qui voyagent en toute sérénité
              grâce à l'intelligence du GIP
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Créer un compte
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center justify-center rounded-lg border border-border px-8 py-3 text-lg font-semibold hover:bg-accent transition-colors"
              >
                Se connecter
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-6 text-center text-sm text-muted-foreground">
          <p>© 2025 AeroCast. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
}

import { Routes } from "@angular/router";
import { authGuard } from "@core/guards/auth.guard";

export const APP_ROUTES: Routes = [
  {
    path: "auth",
    loadChildren: () => import("./auth/auth.routes").then((m) => m.AUTH_ROUTES),
  },
  {
    path: "",
    loadComponent: () =>
      import("./layout/layout.component").then((m) => m.LayoutComponent),
    canActivate: [authGuard],
    children: [
      {
        path: "",
        redirectTo: "dashboard",
        pathMatch: "full",
      },
      {
        path: "dashboard",
        loadChildren: () =>
          import("./dashboard/dashboard.routes").then(
            (m) => m.DASHBOARD_ROUTES,
          ),
      },
      {
        path: "jobs",
        loadChildren: () =>
          import("./jobs/jobs.routes").then((m) => m.JOBS_ROUTES),
      },
      {
        path: "resumes",
        loadChildren: () =>
          import("./resumes/resumes.routes").then((m) => m.RESUMES_ROUTES),
      },
      {
        path: "providers",
        loadChildren: () =>
          import("./providers/providers.routes").then(
            (m) => m.PROVIDERS_ROUTES,
          ),
      },
      {
        path: "profiles",
        loadChildren: () =>
          import("./profiles/profiles.routes").then((m) => m.PROFILES_ROUTES),
      },
      {
        path: "applications",
        loadChildren: () =>
          import("./applications/applications.routes").then(
            (m) => m.APPLICATIONS_ROUTES,
          ),
      },
      {
        path: "analytics",
        loadChildren: () =>
          import("./analytics/analytics.routes").then(
            (m) => m.ANALYTICS_ROUTES,
          ),
      },
      {
        path: "notifications",
        loadChildren: () =>
          import("./notifications/notifications.routes").then(
            (m) => m.NOTIFICATIONS_ROUTES,
          ),
      },
      {
        path: "settings",
        loadChildren: () =>
          import("./settings/settings.routes").then((m) => m.SETTINGS_ROUTES),
      },
      {
        path: "admin",
        loadChildren: () =>
          import("./admin/admin.routes").then((m) => m.ADMIN_ROUTES),
      },
    ],
  },
  {
    path: "**",
    redirectTo: "dashboard",
  },
];

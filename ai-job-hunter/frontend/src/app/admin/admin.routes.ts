import { Routes } from "@angular/router";
import { adminGuard } from "@core/guards/auth.guard";
import { FeaturePageComponent } from "../shared/pages/feature-page.component";

export const ADMIN_ROUTES: Routes = [
  {
    path: "",
    component: FeaturePageComponent,
    canActivate: [adminGuard],
    data: {
      title: "Administration",
      description:
        "Manage providers, platform health, users, and operational settings.",
    },
  },
];

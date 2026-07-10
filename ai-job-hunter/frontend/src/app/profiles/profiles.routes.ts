import { Routes } from '@angular/router';
import { FeaturePageComponent } from '../shared/pages/feature-page.component';

export const PROFILES_ROUTES: Routes = [{
  path: '',
  component: FeaturePageComponent,
  data: { title: 'Profile', description: 'Manage skills, target roles, location, salary preferences, and resumes.' },
}];

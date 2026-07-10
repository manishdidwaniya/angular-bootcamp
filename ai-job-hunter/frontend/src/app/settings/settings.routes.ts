import { Routes } from '@angular/router';
import { FeaturePageComponent } from '../shared/pages/feature-page.component';

export const SETTINGS_ROUTES: Routes = [{
  path: '',
  component: FeaturePageComponent,
  data: { title: 'Settings', description: 'Configure search behavior, integrations, privacy, and account preferences.' },
}];

import { Routes } from '@angular/router';
import { FeaturePageComponent } from '../shared/pages/feature-page.component';

export const ANALYTICS_ROUTES: Routes = [{
  path: '',
  component: FeaturePageComponent,
  data: { title: 'Analytics', description: 'Review job-search activity, match quality, and application outcomes.' },
}];

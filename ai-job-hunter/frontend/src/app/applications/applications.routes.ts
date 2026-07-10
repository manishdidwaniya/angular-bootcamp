import { Routes } from '@angular/router';
import { FeaturePageComponent } from '../shared/pages/feature-page.component';

export const APPLICATIONS_ROUTES: Routes = [{
  path: '',
  component: FeaturePageComponent,
  data: { title: 'Applications', description: 'Track applications from submission through interview, offer, or closure.' },
}];

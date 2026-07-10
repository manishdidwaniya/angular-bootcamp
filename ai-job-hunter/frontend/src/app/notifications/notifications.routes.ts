import { Routes } from '@angular/router';
import { FeaturePageComponent } from '../shared/pages/feature-page.component';

export const NOTIFICATIONS_ROUTES: Routes = [{
  path: '',
  component: FeaturePageComponent,
  data: { title: 'Notifications', description: 'Review in-app alerts and configure email, Telegram, Slack, or Discord delivery.' },
}];

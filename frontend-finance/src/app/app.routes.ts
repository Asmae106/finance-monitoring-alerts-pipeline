import { Routes } from '@angular/router';
import { AlertsComponent } from './pages/alerts/alerts.component';
import { ReportsComponent } from './pages/reports/reports.component';

export const routes: Routes = [
  { path: 'alerts', component: AlertsComponent },
  { path: 'reports', component: ReportsComponent },
  { path: '', redirectTo: 'alerts', pathMatch: 'full' },
];

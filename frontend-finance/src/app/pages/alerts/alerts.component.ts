import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../services/alert.service';
import { Subscription } from 'rxjs';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './alerts.component.html',
  styleUrls: ['./alerts.component.scss']
})
export class AlertsComponent implements OnInit, OnDestroy {
  alerts: any[] = [];
  private sub!: Subscription;

  constructor(private alertService: AlertService) {}

 ngOnInit() {
  this.sub = this.alertService.alerts$.subscribe(data => {
    console.log('Données reçues dans AlertsComponent:', data);
    this.alerts = data;
  });
}


  ngOnDestroy() {
    this.sub.unsubscribe();
    this.alertService.stopPolling();
  }
}

// alert.service.ts
import { Injectable } from '@angular/core';
import axios from 'axios';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AlertService {
  private _alerts = new BehaviorSubject<any[]>([]);
  public alerts$ = this._alerts.asObservable();

  private timerId: any;

  constructor() {
    this.startPolling();
  }

  private async fetchAlerts() {
    try {
      const response = await axios.get('http://localhost:8000/alerts');
      this._alerts.next(response.data);
    } catch (error) {
      console.error('Erreur fetch alerts', error);
    }
  }

 startPolling(intervalMs = 1000) {
  this.fetchAlerts(); // appel unique au démarrage
  // this.timerId = setInterval(() => this.fetchAlerts(), intervalMs);
}



  stopPolling() {
    if (this.timerId) {
      clearInterval(this.timerId);
    }
  }
}

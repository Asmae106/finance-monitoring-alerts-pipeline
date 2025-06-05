import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// Import ng2-charts
import { NgChartsModule } from 'ng2-charts';
import {
  ChartConfiguration,
  ChartOptions,
  ChartType
} from 'chart.js';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, FormsModule, NgChartsModule],
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent {
  selectedDate: string = '';
  reportData: any = null;
  loading: boolean = false;
  error: string | null = null;

  // Chart config
  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [],
    datasets: [
      {
        data: [],
        label: 'Prix BTC',
        fill: false,
        borderColor: 'blue',
        tension: 0.1
      }
    ]
  };

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Heure'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Prix ($)'
        }
      }
    }
  };

   constructor(private api: ApiService) {
    // Initialiser selectedDate à la date d'aujourd'hui au format YYYY-MM-DD
    this.selectedDate = new Date().toISOString().slice(0, 10);
  }


  async fetchReport() {
    if (!this.selectedDate) return;
    this.loading = true;
    this.error = null;

    try {
      this.reportData = await this.api.getReport(this.selectedDate);

      if (this.reportData.data?.length) {
        // On va regrouper par minute pour le graphique
        const grouped: Record<string, number[]> = {};

        this.reportData.data.forEach((p: any) => {
          const date = new Date(p.timestamp);
          const key = date.getHours().toString().padStart(2, '0') + ':' +
                      date.getMinutes().toString().padStart(2, '0');
          if (!grouped[key]) grouped[key] = [];
          grouped[key].push(p.price);
        });

        // Moyenne par minute
        const labels = Object.keys(grouped).sort();
        const data = labels.map(label => {
          const prices = grouped[label];
          return prices.reduce((a, b) => a + b, 0) / prices.length;
        });

        this.lineChartData.labels = labels;
        this.lineChartData.datasets[0].data = data;
      }
    } catch (err) {
      this.error = 'Erreur lors de la récupération du rapport.';
    } finally {
      this.loading = false;
    }
  }
}

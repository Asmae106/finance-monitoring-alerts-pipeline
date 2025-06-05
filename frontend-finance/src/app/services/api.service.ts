import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  async getAlerts(): Promise<any[]> {
    const res = await axios.get(`${this.baseUrl}/alerts`);
    return res.data;
  }
async getReport(date: string) {
  const encodedDate = encodeURIComponent(date);
  const res = await axios.get(`${this.baseUrl}/report?date=${encodedDate}`);
  return res.data;
}

}


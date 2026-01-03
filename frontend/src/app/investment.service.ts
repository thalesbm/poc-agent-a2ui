import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface InvestmentResponse {
  success: boolean;
  data?: any;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class InvestmentService {
  private apiUrl = 'http://localhost:8000/';

  constructor(private http: HttpClient) {}

  getRecommendations(): Observable<InvestmentResponse> {
    let params = new HttpParams();    
    return this.http.get<InvestmentResponse>(this.apiUrl, { params });
  }
}


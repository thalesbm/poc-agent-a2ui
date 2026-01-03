import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import * as A2UITypes from '@a2ui/lit/0.8';

export interface InvestmentResponse {
  success: boolean;
  data?: A2UITypes.Types.ServerToClientMessage[] | any;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class InvestmentService {
  private apiUrl = 'http://localhost:8000/';

  constructor(private http: HttpClient) {}

  getRecommendations(): Observable<A2UITypes.Types.ServerToClientMessage[]> {
    let params = new HttpParams();    
    return this.http.get<InvestmentResponse>(this.apiUrl, { params }).pipe(
      map((response: InvestmentResponse) => {
        if (response.success && response.data && Array.isArray(response.data)) {
          return response.data as A2UITypes.Types.ServerToClientMessage[];
        }
        throw new Error(response.error || 'Invalid response format');
      })
    );
  }
}


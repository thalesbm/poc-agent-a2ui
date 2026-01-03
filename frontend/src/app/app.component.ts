import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InvestmentService } from './investment.service';
import * as A2UITypes from '@a2ui/lit/0.8';
import { InvestmentStocksComponent } from './investment-stocks/investment-stocks.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, InvestmentStocksComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'Investment Stock Recommendations';
  loading = signal(false);
  error = signal<string | null>(null);
  a2uiMessages = signal<A2UITypes.Types.ServerToClientMessage[]>([]);

  constructor(
    private investmentService: InvestmentService
  ) {}

  ngOnInit() {
    this.loadRecommendations();
  }

  loadRecommendations() {
    this.loading.set(true);
    this.error.set(null);
    
    this.investmentService.getRecommendations().subscribe({
      next: (messages) => {
        this.a2uiMessages.set(messages);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.message || 'Error loading recommendations');
        this.loading.set(false);
      }
    });
  }

  refresh() {
    this.loadRecommendations();
  }
}


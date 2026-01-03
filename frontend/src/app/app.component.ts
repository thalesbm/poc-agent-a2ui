import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InvestmentService } from './investment.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'Investment Recommendations';
  data: any = null;
  loading = false;
  error: string | null = null;

  constructor(private investmentService: InvestmentService) {}

  ngOnInit() {
    this.loadRecommendations();
  }

  loadRecommendations() {
    this.loading = true;
    this.error = null;
    
    this.investmentService.getRecommendations().subscribe({
      next: (response) => {
        this.data = response.data;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message || 'Error loading recommendations';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  refresh() {
    this.loadRecommendations();
  }
}


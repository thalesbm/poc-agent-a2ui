import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InvestmentService } from './investment.service';
import { A2UIMessage, Stock, DataModelUpdate, Content } from './a2ui.models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'Investment Stock Recommendations';
  stocks: Stock[] = [];
  pageTitle: string = '';
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
        if (response.data && Array.isArray(response.data)) {
          this.processA2UIData(response.data);
        }
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message || 'Error loading recommendations';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  processA2UIData(messages: A2UIMessage[]) {
    // Find dataModelUpdate message
    const dataModelUpdate = messages.find(msg => msg.dataModelUpdate);
    
    if (dataModelUpdate?.dataModelUpdate) {
      const data = dataModelUpdate.dataModelUpdate;
      
      // Extract title
      const titleContent = data.contents.find(c => c.key === 'title');
      if (titleContent?.valueString) {
        this.pageTitle = titleContent.valueString;
      }
      
      // Extract stocks
      const stocksContent = data.contents.find(c => c.key === 'stocks');
      if (stocksContent?.valueMap) {
        this.stocks = this.extractStocks(stocksContent.valueMap);
      }
    }
  }

  extractStocks(stockMaps: Content[]): Stock[] {
    return stockMaps.map(stockMap => {
      const stock: any = {};
      
      stockMap.valueMap?.forEach(item => {
        if (item.key === 'symbol' && item.valueString) {
          stock.symbol = item.valueString;
        } else if (item.key === 'company' && item.valueString) {
          stock.company = item.valueString;
        } else if (item.key === 'sector' && item.valueString) {
          stock.sector = item.valueString;
        } else if (item.key === 'currentPrice' && item.valueNumber !== undefined) {
          stock.currentPrice = item.valueNumber;
        } else if (item.key === 'recommendation' && item.valueString) {
          stock.recommendation = item.valueString;
        } else if (item.key === 'targetPrice' && item.valueNumber !== undefined) {
          stock.targetPrice = item.valueNumber;
        }
      });
      
      return stock as Stock;
    });
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  }

  getRecommendationClass(recommendation: string): string {
    return recommendation.toLowerCase();
  }

  refresh() {
    this.loadRecommendations();
  }
}


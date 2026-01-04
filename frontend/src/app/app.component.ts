import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { InvestmentService } from './investment.service';
import { MessageProcessor, Surface } from '@a2ui/angular';
import * as A2UITypes from '@a2ui/lit/0.8';
import { CurrencyFormatter } from './formatter/currency-formatter';
import { TextColorApplier } from './formatter/text-color-applier';
import { TextUsageHintApplier } from './formatter/text-usage-hint-applier';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, Surface],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent implements OnInit {
  title = 'Investment Stock Recommendations';
  loading = signal(false);
  error = signal<string | null>(null);
  surfaceId = signal<string | null>(null);
  surface = signal<A2UITypes.Types.Surface | null>(null);
  private currencyFormatter: CurrencyFormatter;
  private textColorApplier: TextColorApplier;
  private textUsageHintApplier: TextUsageHintApplier;

  constructor(
    private investmentService: InvestmentService,
    private messageProcessor: MessageProcessor,
    private currencyPipe: CurrencyPipe
  ) {
    this.currencyFormatter = new CurrencyFormatter(currencyPipe);
    this.textColorApplier = new TextColorApplier();
    this.textUsageHintApplier = new TextUsageHintApplier();
  }

  ngOnInit() {
    this.loadRecommendations();
  }

  loadRecommendations() {
    this.loading.set(true);
    this.error.set(null);
    
    this.investmentService.getRecommendations().subscribe({
      next: (messages) => {
        this.processA2UIMessages(messages);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.message || 'Error loading recommendations');
        this.loading.set(false);
      }
    });
  }

  processA2UIMessages(messages: A2UITypes.Types.ServerToClientMessage[]) {
    try {
      const styleMap = this.currencyFormatter.identifyTextStyles(messages);
      const usageHintMap = this.textUsageHintApplier.identifyUsageHints(messages);
      const formattedMessages = this.currencyFormatter.formatCurrencyValues(messages);
      
      this.messageProcessor.processMessages(formattedMessages);
      this.textColorApplier.applyTextStyles(styleMap);
      this.textUsageHintApplier.applyUsageHintStyles(usageHintMap);
      
    } catch (error) {
      this.error.set('Error processing A2UI messages: ' + (error as Error).message);
      return;
    }
    
    const surfaces = this.messageProcessor.getSurfaces();
    
    if (surfaces.size > 0) {
      let targetSurface: A2UITypes.Types.Surface | null = null;
      let targetSurfaceId: string | null = null;
      
      if (this.surfaceId()) {
        targetSurface = surfaces.get(this.surfaceId()!) || null;
        targetSurfaceId = this.surfaceId();
      }
      
      if (!targetSurface) {
        const firstEntry = surfaces.entries().next().value;
        if (firstEntry) {
          targetSurfaceId = firstEntry[0];
          targetSurface = firstEntry[1];
        }
      }

      this.surfaceId.set(targetSurfaceId);
      this.surface.set(targetSurface);
    }
  }

  refresh() {
    this.loadRecommendations();
  }
}


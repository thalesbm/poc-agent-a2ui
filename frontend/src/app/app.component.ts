import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InvestmentService } from './investment.service';
import { MessageProcessor, Surface } from '@a2ui/angular';
import * as A2UITypes from '@a2ui/lit/0.8';

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

  constructor(
    private investmentService: InvestmentService,
    private messageProcessor: MessageProcessor
  ) {}

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
      this.messageProcessor.processMessages(messages);
    } catch (error) {
      this.error.set('Error processing A2UI messages: ' + (error as Error).message);
      return;
    }
    
    const surfaces = this.messageProcessor.getSurfaces();
    
    if (surfaces.size > 0) {
      // Get the first surface (or find by surfaceId if we have one)
      let targetSurface: A2UITypes.Types.Surface | null = null;
      let targetSurfaceId: string | null = null;
      
      // Try to find surface by ID if we already have one
      if (this.surfaceId()) {
        targetSurface = surfaces.get(this.surfaceId()!) || null;
        targetSurfaceId = this.surfaceId();
      }
      
      // If not found, get the first surface
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


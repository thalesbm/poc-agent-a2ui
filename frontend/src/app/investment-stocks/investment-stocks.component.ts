import { Component, OnInit, signal, input, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MessageProcessor, Surface } from '@a2ui/angular';
import * as A2UITypes from '@a2ui/lit/0.8';

@Component({
  selector: 'app-investment-stocks',
  standalone: true,
  imports: [CommonModule, Surface],
  template: `
    <div class="investment-stocks-container">
      <div *ngIf="loading()" class="loading">
        <p>Loading recommendations...</p>
      </div>

      <div *ngIf="error()" class="error">
        <p>Error: {{ error() }}</p>
      </div>

      <a2ui-surface
        *ngIf="surfaceId() && surface() && !loading()"
        [surfaceId]="surfaceId()!"
        [surface]="surface()!"
      ></a2ui-surface>
    </div>
  `,
  styles: [`
    .investment-stocks-container {
      width: 100%;
    }

    .loading, .error {
      padding: 20px;
      text-align: center;
    }

    .error {
      color: #f44336;
    }
  `]
})
export class InvestmentStocksComponent implements OnInit {
  // Input: receives A2UI messages directly from API
  a2uiMessages = input<A2UITypes.Types.ServerToClientMessage[]>([]);

  // Internal state
  loading = signal(false);
  error = signal<string | null>(null);
  surfaceId = signal<string | null>(null);
  surface = signal<A2UITypes.Types.Surface | null>(null);

  constructor(
    private messageProcessor: MessageProcessor
  ) {
    // React to changes in a2uiMessages input
    effect(() => {
      const messages = this.a2uiMessages();
      if (messages && messages.length > 0) {
        this.processA2UIMessages(messages);
      }
    });
  }

  ngOnInit() {
    const messages = this.a2uiMessages();
    if (messages && messages.length > 0) {
      this.processA2UIMessages(messages);
    }
  }

  private processA2UIMessages(messages: A2UITypes.Types.ServerToClientMessage[]) {
    this.loading.set(true);
    this.error.set(null);

    try {
      this.messageProcessor.processMessages(messages);
    } catch (error) {
      this.error.set('Error processing A2UI messages: ' + (error as Error).message);
      this.loading.set(false);
      return;
    }

    const surfaces = this.messageProcessor.getSurfaces();

    if (surfaces.size > 0) {
      let targetSurface: A2UITypes.Types.Surface | null = null;
      let targetSurfaceId: string | null = null;

      // Try to find surface by ID from beginRendering message
      const beginRendering = messages.find(msg => msg.beginRendering);
      if (beginRendering?.beginRendering) {
        const requestedSurfaceId = beginRendering.beginRendering.surfaceId;
        targetSurface = surfaces.get(requestedSurfaceId) || null;
        targetSurfaceId = requestedSurfaceId;
      }

      // If not found, get the first surface
      if (!targetSurface) {
        const firstEntry = surfaces.entries().next().value;
        if (firstEntry) {
          targetSurfaceId = firstEntry[0];
          targetSurface = firstEntry[1];
        }
      }

      if (targetSurface && targetSurfaceId) {
        this.surfaceId.set(targetSurfaceId);
        this.surface.set(targetSurface);
        this.loading.set(false);
      } else {
        this.error.set('No valid surface found after processing messages');
        this.loading.set(false);
      }
    } else {
      this.error.set('No surfaces found after processing messages');
      this.loading.set(false);
    }
  }
}


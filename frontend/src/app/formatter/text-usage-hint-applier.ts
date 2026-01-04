import * as A2UITypes from '@a2ui/lit/0.8';

export class TextUsageHintApplier {
  identifyUsageHints(messages: A2UITypes.Types.ServerToClientMessage[]): Map<string, string> {
    const usageHintMap = new Map<string, string>();
    
    messages.forEach(msg => {
      if ('surfaceUpdate' in msg && msg.surfaceUpdate?.components) {
        msg.surfaceUpdate.components.forEach((comp: any) => {
          if (comp.component?.Text?.usageHint && comp.id) {
            usageHintMap.set(comp.id, comp.component.Text.usageHint);
          }
        });
      }
    });
    
    return usageHintMap;
  }

  applyUsageHintStyles(usageHintMap: Map<string, string>) {
    this.applyStylesToElements(usageHintMap);
    
    const observer = new MutationObserver(() => {
      this.applyStylesToElements(usageHintMap);
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  private applyStylesToElements(usageHintMap: Map<string, string>) {
    const surface = document.querySelector('a2ui-surface');
    const searchRoot = surface || document;

    usageHintMap.forEach((usageHint, componentId) => {
      let element = searchRoot.querySelector(`[id="${componentId}"]`) as HTMLElement ||
                    searchRoot.querySelector(`[data-id="${componentId}"]`) as HTMLElement;

      if (!element) {
        if (usageHint === 'h3' && componentId === 'symbol-text') {
          const cards = searchRoot.querySelectorAll('a2ui-card');
          const h3Elements: HTMLElement[] = [];
          
          cards.forEach((card) => {
            const rows = card.querySelectorAll('a2ui-row');
            rows.forEach((row) => {
              const textElements = row.querySelectorAll('a2ui-text');
              if (textElements.length > 0) {
                const firstText = textElements[0] as HTMLElement;
                if (!firstText.hasAttribute(`data-a2ui-${componentId}`)) {
                  h3Elements.push(firstText);
                }
              }
            });
          });
          
          if (h3Elements.length > 0) {
            h3Elements.forEach((h3Element) => {
              this.applyH3Styles(h3Element, componentId);
            });
            element = h3Elements[0];
          }
        }
      }

      if (element) {
        if (usageHint === 'h3') {
          this.applyH3Styles(element, componentId);
        }
      }
    });
  }

  private applyH3Styles(element: HTMLElement, componentId: string) {
    element.setAttribute(`data-a2ui-${componentId}`, 'true');
    
    const h3Styles: Record<string, string> = {
      'font-size': '1.25rem',
      'font-weight': '600',
      'line-height': '1.4',
      'margin': '0.5rem 0'
    };

    Object.entries(h3Styles).forEach(([property, value]) => {
      element.style.setProperty(property, value, 'important');
    });

    const innerP = element.querySelector('p');
    if (innerP) {
      Object.entries(h3Styles).forEach(([property, value]) => {
        (innerP as HTMLElement).style.setProperty(property, value, 'important');
      });
    }
  }
}


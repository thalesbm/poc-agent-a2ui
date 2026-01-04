export class TextColorApplier {
  applyTextStyles(styleMap: Map<string, Record<string, string>>) {
    const observer = new MutationObserver(() => {
      this.applyStylesToElements(styleMap);
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  private applyStylesToElements(styleMap: Map<string, Record<string, string>>) {
    const surface = document.querySelector('a2ui-surface');
    const searchRoot = surface || document;

    styleMap.forEach((styles, componentId) => {
      let element: HTMLElement | null = null;

      element = searchRoot.querySelector(`[id="${componentId}"]`) as HTMLElement ||
                searchRoot.querySelector(`[data-id="${componentId}"]`) as HTMLElement;

      if (!element && componentId === 'recommendation-badge') {
        const textElements = searchRoot.querySelectorAll('a2ui-text');
        const recommendationElements: HTMLElement[] = [];
        
        textElements.forEach((textEl) => {
          const textContent = textEl.textContent?.trim();
          if ((textContent === 'BUY' || textContent === 'HOLD' || textContent === 'SELL') &&
              !textEl.hasAttribute(`data-a2ui-${componentId}`)) {
            recommendationElements.push(textEl as HTMLElement);
          }
        });
        
        if (recommendationElements.length > 0) {
          recommendationElements.forEach((recElement) => {
            recElement.setAttribute(`data-a2ui-${componentId}`, 'true');

            Object.entries(styles).forEach(([property, value]) => {
              recElement.style.setProperty(property, value, 'important');
            });
          });
          element = recommendationElements[0];
        }
      }
    });
  }
}


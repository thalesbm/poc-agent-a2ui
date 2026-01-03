export class TextStyleApplier {

  applyTextStyles(styleMap: Map<string, Record<string, string>>) {
    this.injectDynamicStyles(styleMap);

    this.applyStylesToElements(styleMap);

    const observer = new MutationObserver(() => {
      this.applyStylesToElements(styleMap);
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
    
    setTimeout(() => {
      observer.disconnect();
    }, 5000);
  }

  private applyStylesToSingleElement(element: HTMLElement, styles: Record<string, string>, componentId: string) {
    const isCustomElement = element.tagName && element.tagName.toLowerCase().startsWith('a2ui-');
    
    element.setAttribute(`data-a2ui-${componentId}`, 'true');
    
    Object.entries(styles).forEach(([property, value]) => {
      element.style.setProperty(property, value, 'important');
    });
    
    const innerP = element.querySelector('p');
    if (innerP) {
      Object.entries(styles).forEach(([property, value]) => {
        (innerP as HTMLElement).style.setProperty(property, value, 'important');
      });
      console.log(`  Applied styles to inner <p> element:`, innerP);
      const pComputedStyle = window.getComputedStyle(innerP as HTMLElement);
      console.log(`  Inner <p> computed color:`, pComputedStyle.color);
      console.log(`  Inner <p> style attribute:`, (innerP as HTMLElement).style.cssText);
    } else {
      console.log(`  No <p> element found inside`);
    }
    
    const innerSection = element.querySelector('section');
    if (innerSection) {
      Object.entries(styles).forEach(([property, value]) => {
        (innerSection as HTMLElement).style.setProperty(property, value, 'important');
      });
      console.log(`  Applied styles to inner <section> element:`, innerSection);
    }
    
    if (isCustomElement && (element as any).shadowRoot) {
      const shadowRoot = (element as any).shadowRoot;
      
      console.log(`  Shadow DOM found, innerHTML:`, shadowRoot.innerHTML);
      
      const innerElements = shadowRoot.querySelectorAll('*');
      console.log(`  Found ${innerElements.length} elements in shadow DOM`);
      innerElements.forEach((innerEl: HTMLElement, index: number) => {
        Object.entries(styles).forEach(([property, value]) => {
          innerEl.style.setProperty(property, value, 'important');
        });
        console.log(`  Applied styles to inner element ${index}:`, innerEl.tagName, innerEl);
      });
      
      let shadowStyle = shadowRoot.getElementById(`a2ui-style-${componentId}`);
      if (!shadowStyle) {
        shadowStyle = document.createElement('style');
        shadowStyle.id = `a2ui-style-${componentId}`;
        shadowRoot.appendChild(shadowStyle);
      }
      
      const styleString = `
        :host { ${Object.entries(styles).map(([p, v]) => `${p}: ${v} !important;`).join(' ')} }
        * { ${Object.entries(styles).map(([p, v]) => `${p}: ${v} !important;`).join(' ')} }
        span { ${Object.entries(styles).map(([p, v]) => `${p}: ${v} !important;`).join(' ')} }
        p { ${Object.entries(styles).map(([p, v]) => `${p}: ${v} !important;`).join(' ')} }
        div { ${Object.entries(styles).map(([p, v]) => `${p}: ${v} !important;`).join(' ')} }
      `;
      shadowStyle.textContent = styleString;
      console.log(`  Injected shadow DOM style:`, styleString);
    } else if (isCustomElement) {
      console.log(`  Custom element but no shadow DOM found`);
    }
    
    const slot = element.querySelector('slot');
    if (slot) {
      console.log(`  Found slot element`);
      const assignedNodes = (slot as HTMLSlotElement).assignedNodes();
      console.log(`  Slot has ${assignedNodes.length} assigned nodes`);
      assignedNodes.forEach((node, index: number) => {
        if (node instanceof HTMLElement) {
          Object.entries(styles).forEach(([property, value]) => {
            node.style.setProperty(property, value, 'important');
          });
          console.log(`  Applied styles to assigned node ${index}:`, node);
        }
      });
    }
    
    console.log(`✓ Applied styles to component ${componentId}:`, styles);
    console.log(`  Element:`, element);
    console.log(`  Element tagName:`, element.tagName);
    console.log(`  Is custom element:`, isCustomElement);
    console.log(`  Has shadow DOM:`, isCustomElement && !!(element as any).shadowRoot);
    const computedStyle = window.getComputedStyle(element);
    console.log(`  Computed color:`, computedStyle.color);
    console.log(`  Element style:`, element.style.cssText);
    console.log(`  Element innerHTML:`, element.innerHTML);
  }

  private applyStylesToElements(styleMap: Map<string, Record<string, string>>) {
    styleMap.forEach((styles, componentId) => {
      let element: HTMLElement | null = null;
      
      const surface = document.querySelector('a2ui-surface');
      const searchRoot = surface || document;
      
      const allElements = searchRoot.querySelectorAll('*');
      
      allElements.forEach((el) => {
        const id = el.id || el.getAttribute('id') || el.getAttribute('data-id');
        if (id === componentId) {
          element = el as HTMLElement;
          console.log(`Found element for ${componentId} by ID attribute`);
        }
      });
      
      if (!element) {
        allElements.forEach((el) => {
          const dataId = el.getAttribute('data-component-id') || 
                        el.getAttribute('data-id') ||
                        el.getAttribute('component-id');
          if (dataId === componentId) {
            element = el as HTMLElement;
            console.log(`Found element for ${componentId} by data attribute`);
          }
        });
      }
      
      if (!element) {
        const customElements = searchRoot.querySelectorAll('a2ui-text, a2ui-surface, *');
        customElements.forEach((customEl) => {
          if (customEl.shadowRoot) {
            const shadowElements = customEl.shadowRoot.querySelectorAll('*');
            shadowElements.forEach((shadowEl) => {
              const id = shadowEl.id || shadowEl.getAttribute('id');
              if (id === componentId) {
                element = shadowEl as HTMLElement;
                console.log(`Found element for ${componentId} in shadow DOM`);
              }
            });
          }
        });
      }
      
      if (!element && componentId === 'recommendation-badge') {
        const stockDetails = searchRoot.querySelector('[id="stock-details"]') || 
                            searchRoot.querySelector('[data-id="stock-details"]');
        if (stockDetails) {
          // Look for the first text element inside stock-details
          const textElements = stockDetails.querySelectorAll('a2ui-text, span, p, div, h1, h2, h3, h4, h5');
          if (textElements.length > 0) {
            // The recommendation-badge is likely the first child
            element = textElements[0] as HTMLElement;
            console.log(`Found recommendation-badge by position in stock-details`);
          }
        }
      }
      
      // Strategy 5: Apply styles to all matching text elements if we can't find the specific one
      // This is a fallback - apply to elements that might be the target
      // For recommendation-badge, we need to apply to ALL elements that contain recommendation text
      // since each stock card has its own recommendation-badge
      if (!element && componentId === 'recommendation-badge') {
        const textElements = searchRoot.querySelectorAll('a2ui-text');
        // Find ALL elements with recommendation text and apply styles to each
        const recommendationElements: HTMLElement[] = [];
        textElements.forEach((textEl) => {
          const textContent = textEl.textContent?.trim();
          if (textContent === 'BUY' || textContent === 'HOLD' || textContent === 'SELL') {
            // Check if this element already has the data attribute (already styled)
            if (!textEl.hasAttribute(`data-a2ui-${componentId}`)) {
              recommendationElements.push(textEl as HTMLElement);
            }
          }
        });
        
        // Apply styles to all recommendation elements
        if (recommendationElements.length > 0) {
          recommendationElements.forEach((recElement) => {
            this.applyStylesToSingleElement(recElement, styles, componentId);
          });
          // Set element to first one for logging purposes
          element = recommendationElements[0];
          console.log(`Found ${recommendationElements.length} recommendation-badge elements by text content`);
        }
      }
      
      if (element) {
        // All styling logic is handled in applyStylesToSingleElement
        this.applyStylesToSingleElement(element, styles, componentId);
      } else {
        console.warn(`✗ Could not find element for component ID: ${componentId}`);
        // Log all available IDs and attributes for debugging
        const allIds: string[] = [];
        const allDataIds: string[] = [];
        const allElements = searchRoot.querySelectorAll('*');
        allElements.forEach((el) => {
          const id = el.id || el.getAttribute('id');
          if (id) allIds.push(id);
          const dataId = el.getAttribute('data-component-id') || el.getAttribute('data-id');
          if (dataId) allDataIds.push(dataId);
        });
        console.log('Available IDs in DOM:', allIds);
        console.log('Available data IDs in DOM:', allDataIds);
        console.log('All a2ui-text elements:', searchRoot.querySelectorAll('a2ui-text').length);
      }
    });
  }

  /**
   * Injects dynamic CSS styles for components
   */
  private injectDynamicStyles(styleMap: Map<string, Record<string, string>>) {
    // Remove existing style tag if it exists
    const existingStyle = document.getElementById('a2ui-dynamic-styles');
    if (existingStyle) {
      existingStyle.remove();
    }

    // Create new style tag
    const styleTag = document.createElement('style');
    styleTag.id = 'a2ui-dynamic-styles';
    
    let cssRules = '';
    styleMap.forEach((styles, componentId) => {
      const styleString = Object.entries(styles)
        .map(([property, value]) => `${property}: ${value} !important;`)
        .join(' ');
      
      // Try multiple selectors with higher specificity
      // Also include data attribute selector for elements we mark
      cssRules += `
        a2ui-surface [id="${componentId}"] { ${styleString} }
        a2ui-surface #${componentId} { ${styleString} }
        a2ui-surface a2ui-text[id="${componentId}"] { ${styleString} }
        a2ui-surface a2ui-text#${componentId} { ${styleString} }
        a2ui-surface a2ui-text[data-a2ui-${componentId}="true"] { ${styleString} }
        a2ui-text[id="${componentId}"] { ${styleString} }
        a2ui-text#${componentId} { ${styleString} }
        a2ui-text[data-a2ui-${componentId}="true"] { ${styleString} }
        [id="${componentId}"] { ${styleString} }
        #${componentId} { ${styleString} }
        [data-a2ui-${componentId}="true"] { ${styleString} }
        *[id="${componentId}"] { ${styleString} }
        span[id="${componentId}"] { ${styleString} }
        p[id="${componentId}"] { ${styleString} }
        div[id="${componentId}"] { ${styleString} }
        h1[id="${componentId}"] { ${styleString} }
        h2[id="${componentId}"] { ${styleString} }
        h3[id="${componentId}"] { ${styleString} }
        h4[id="${componentId}"] { ${styleString} }
        h5[id="${componentId}"] { ${styleString} }
      `;
      
      // Add CSS for elements that contain specific text using attribute selectors
      // Also target the inner <p> elements
      cssRules += `
        a2ui-text[data-a2ui-${componentId}="true"] p { ${styleString} }
        a2ui-text[data-a2ui-${componentId}="true"] section { ${styleString} }
        a2ui-text[data-a2ui-${componentId}="true"] section p { ${styleString} }
      `;
      
      if (componentId === 'recommendation-badge') {
        cssRules += `
          a2ui-text[data-a2ui-recommendation-badge="true"] { ${styleString} }
        `;
      }
    });
    
    styleTag.textContent = cssRules;
    document.head.appendChild(styleTag);
    
    console.log('Injected dynamic CSS styles:', cssRules);
    console.log('Style map:', Array.from(styleMap.entries()));
  }
}


import { CurrencyPipe } from '@angular/common';
import * as A2UITypes from '@a2ui/lit/0.8';

export interface ComponentStyle {
  componentId: string;
  styles: Record<string, string>;
}

export class CurrencyFormatter {
  constructor(private currencyPipe: CurrencyPipe) {}

  formatCurrencyValues(messages: A2UITypes.Types.ServerToClientMessage[]): A2UITypes.Types.ServerToClientMessage[] {

    const formattedMessages = JSON.parse(JSON.stringify(messages)) as A2UITypes.Types.ServerToClientMessage[];
    
    const currencyPaths = new Set<string>();
    
    formattedMessages.forEach(msg => {
      if ('surfaceUpdate' in msg && msg.surfaceUpdate?.components) {
        msg.surfaceUpdate.components.forEach((comp: any) => {
          if (comp.component?.Text?.text?.format === 'currency' && comp.component?.Text?.text?.path) {
            currencyPaths.add(comp.component.Text.text.path);
          }
        });
      }
    });
    
    formattedMessages.forEach(msg => {
      if ('dataModelUpdate' in msg && msg.dataModelUpdate?.contents) {
        this.formatCurrencyInContents(msg.dataModelUpdate.contents, currencyPaths);
      }
    });
    
    return formattedMessages;
  }

  private formatCurrencyInContents(contents: A2UITypes.Types.DataValue[], currencyPaths: Set<string>, pathPrefix = '') {
    contents.forEach(item => {
      if (!item || typeof item !== 'object') {
        return;
      }
      
      const itemObj = item as Record<string, any>;
      
      if (itemObj['key'] && typeof itemObj['valueNumber'] === 'number') {
        const key = itemObj['key'] as string;
        const fullPath = pathPrefix ? `${pathPrefix}/${key}` : `/${key}`;
        if (currencyPaths.has(fullPath) || currencyPaths.has(key)) {
          
          const formatted = this.currencyPipe.transform(itemObj['valueNumber'], 'USD', 'symbol', '1.2-2');
          if (formatted) {

            itemObj['valueString'] = formatted;
            delete itemObj['valueNumber'];
          }
        }
      } else if (itemObj['key'] && Array.isArray(itemObj['valueMap'])) {
        const key = itemObj['key'] as string;
        const newPrefix = pathPrefix ? `${pathPrefix}/${key}` : `/${key}`;
        this.formatCurrencyInContents(itemObj['valueMap'] as A2UITypes.Types.DataValue[], currencyPaths, newPrefix);
      }
    });
  }

 
  identifyTextStyles(messages: A2UITypes.Types.ServerToClientMessage[]): Map<string, Record<string, string>> {
    const styleMap = new Map<string, Record<string, string>>();
    
    messages.forEach(msg => {
      if ('surfaceUpdate' in msg && msg.surfaceUpdate?.components) {
        msg.surfaceUpdate.components.forEach((comp: any) => {
          if (comp.component?.Text?.style && comp.id) {

            const styles: Record<string, string> = {};
            const styleObj = comp.component.Text.style;
            
            Object.keys(styleObj).forEach(key => {
              const cssKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
              styles[cssKey] = styleObj[key];
            });
            
            if (Object.keys(styles).length > 0) {
              styleMap.set(comp.id, styles);
              console.log(`Identified styles for component ${comp.id}:`, styles);
            }
          }
        });
      }
    });
    
    console.log('Total components with styles:', styleMap.size);
    return styleMap;
  }
}


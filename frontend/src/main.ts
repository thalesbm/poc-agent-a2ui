import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { provideA2UI, DEFAULT_CATALOG, Catalog } from '@a2ui/angular';
import { a2uiTheme } from './app/a2ui-theme';

const customCatalog: Catalog = {
  ...DEFAULT_CATALOG,
};

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideA2UI({
      catalog: customCatalog,
      theme: a2uiTheme
    })
  ]
}).catch(err => console.error(err));

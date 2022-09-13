import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { Cell } from './cell/cell.component';
import { GridRow } from './grid-row/grid-row.component';

@NgModule({
  declarations: [
    AppComponent,
    Cell,
    GridRow
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

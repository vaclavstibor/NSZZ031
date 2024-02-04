import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';

import { RouterModule } from '@angular/router';
import { GraphComponent } from './graph/graph.component';
import { TickersComponent } from './tickers/tickers.component';

import { FormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';
import { NgPipesModule } from 'ngx-pipes';
import { TickerGraphComponent } from './ticker-graph/ticker-graph.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    GraphComponent,
    TickersComponent,
    TickerGraphComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent},
      { path: 'home', component: HomeComponent },
      { path: 'graph', component: GraphComponent},
      { path: 'tickers', component: TickersComponent},
      { path: 'ticker-graph/:name', component: TickerGraphComponent},
    ]),
    FormsModule,
    NgxPaginationModule,
    NgPipesModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';

import { RouterModule } from '@angular/router';
import { GraphComponent } from './graph/graph.component';
import { GraphCosmosComponent } from './graph-cosmos/graph-cosmos.component';
import { TickersComponent } from './tickers/tickers.component';

import { FormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    GraphComponent,
    GraphCosmosComponent,
    TickersComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent},
      { path: 'home', component: HomeComponent },
      { path: 'graph', component: GraphComponent},
      { path: 'graph-cosmos', component: GraphCosmosComponent},
      { path: 'tickers', component: TickersComponent},
    ]),
    FormsModule,
    NgxPaginationModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

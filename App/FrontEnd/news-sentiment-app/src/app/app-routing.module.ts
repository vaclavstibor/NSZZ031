import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { GraphComponent } from './graph/graph.component';
import { TickersComponent } from './tickers/tickers.component';
import { TickerGraphComponent } from './ticker-graph/ticker-graph.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'graph',
    component: GraphComponent
  },
  {
    path: 'tickers',
    component: TickersComponent
  },
  {
    path: 'ticker-graph/:name',
    component: TickerGraphComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

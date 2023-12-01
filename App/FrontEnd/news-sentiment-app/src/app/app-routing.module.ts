import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { GraphComponent } from './graph/graph.component';
import { GraphCosmosComponent } from './graph-cosmos/graph-cosmos.component';
import { TickersComponent } from './tickers/tickers.component';

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
    path: 'graph-cosmos',
    component: GraphCosmosComponent
  },
  {
    path: 'tickers',
    component: TickersComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

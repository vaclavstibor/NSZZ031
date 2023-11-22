import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';

import { RouterModule } from '@angular/router';
import { GraphComponent } from './graph/graph.component';
import { GraphCosmosComponent } from './graph-cosmos/graph-cosmos.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    GraphComponent,
    GraphCosmosComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent},
      { path: 'home', component: HomeComponent },
      { path: 'graph', component: GraphComponent},
      { path: 'graph-cosmos', component: GraphCosmosComponent}
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnalyticsComponent } from './components/analytics/analytics.component';

const routes: Routes = [
  {
    path: '',
    component: AnalyticsComponent, // until homepage is not created
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

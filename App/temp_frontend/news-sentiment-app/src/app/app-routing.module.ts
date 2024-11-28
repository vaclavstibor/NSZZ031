import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { GraphsComponent } from './graphs/graphs.component';
import { CompaniesComponent } from './companies/companies.component';
import { GraphComponent } from './company/graph/graph.component';
import { DashboardComponent } from './company/dashboard/dashboard.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'companies',
    component: CompaniesComponent,
  },
  {
    path: 'companies/graphs',
    component: GraphsComponent,
  },
  {
    path: 'company/:ticker/graph',
    component: GraphComponent,
  },
  {
    path: 'company/:ticker/dashboard',
    component: DashboardComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator'; 

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';

import { RouterModule } from '@angular/router';
import { GraphsComponent } from './graphs/graphs.component';
import { CompaniesComponent } from './companies/companies.component';

import { FormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';
import { NgPipesModule } from 'ngx-pipes';
import { GraphComponent } from './company/graph/graph.component';
import { HttpClientModule } from '@angular/common/http';
import { DashboardComponent } from './company/dashboard/dashboard.component';
import { ArticleListComponent } from './company/dashboard/components/article-list/article-list.component';
import { CompanyInfoComponent } from './company/dashboard/components/company-info/company-info.component';
import { PieChartComponent } from './company/dashboard/components/charts/pie-chart/pie-chart.component';
import { SplineChartComponent } from './company/dashboard/components/charts/spline-chart/spline-chart.component';
import { StockChartComponent } from './company/dashboard/components/charts/stock-chart/stock-chart.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    GraphsComponent,
    CompaniesComponent,
    GraphComponent,
    DashboardComponent,
    ArticleListComponent,
    CompanyInfoComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatFormFieldModule,
    MatInputModule,
    MatTableModule,
    MatSortModule,   
    MatPaginatorModule, 
    AppRoutingModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent },
      { path: 'home', component: HomeComponent },
      { path: 'companies', component: CompaniesComponent },
      { path: 'companies/graphs', component: GraphsComponent },
      { path: 'company/:ticker/graph', component: GraphComponent },
      { path: 'comapny/:ticker/dashboard', component: DashboardComponent },
    ]),
    FormsModule,
    NgxPaginationModule,
    NgPipesModule,
    HttpClientModule,
    PieChartComponent,
    SplineChartComponent,
    StockChartComponent
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}

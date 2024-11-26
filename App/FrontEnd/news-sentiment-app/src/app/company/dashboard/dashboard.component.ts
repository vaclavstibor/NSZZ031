import { Component, OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { ActivatedRoute } from '@angular/router';
import { HomeComponent } from 'src/app/home/home.component';

import { CompanyInfo } from 'src/app/models/CompanyInfo.model';
import { CompanyChart } from 'src/app/models/CompanyChart.model';
import { CompanyArticleList } from 'src/app/models/CompanyArticleList.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css', '../../app.component.css'],
})
export class DashboardComponent extends HomeComponent implements OnInit {
  ticker: string = '';

  chartData!: CompanyChart;
  chartLoading: boolean = false;

  infoData!: CompanyInfo;
  infoLoading: boolean = false;

  articlesData: CompanyArticleList = [];
  articlesLoading: boolean = false;

  constructor(private httpService: HttpService, private route: ActivatedRoute) {
    super();
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.ticker = params['ticker'];
      this.fetchChartData(this.ticker);
      this.fetchInfoData(this.ticker);
      this.fetchArticlesData(this.ticker);
    });
  }

  async fetchInfoData(ticker: string) {
    /**
     * Fetch company info data from the API and update 
     * the infoData variable with the response.
     * 
     */
    this.infoLoading = true;
    this.httpService.getCompanyInfoData(ticker).subscribe({
      next: (res: CompanyInfo) => {
        this.infoData = res;
      },
      error: (error) => {
        console.error('Error fetching info data:', error);
      },
      complete: () => {
        this.infoLoading = false;
      }
    });
  }  

  async fetchChartData(ticker: string) {
    /**
     * Fetch company chart data from the API and update
     * the chartData variable with the response.
     */
    this.chartLoading = true;
    this.httpService.getCompanyChartData(ticker).subscribe({
      next: (res: CompanyChart) => {
        this.chartData = res;
      },
      error: (error) => {
        console.error('Error fetching chart data:', error);
      },
      complete: () => {
        this.chartLoading = false;
      }
    });
  }

  async fetchArticlesData(ticker: string) {
    /**
     * Fetch company articles data from the API and update
     * the articlesData variable with the response.
     */
    this.articlesLoading = true;
    this.httpService.getCompanyArticlesData(ticker).subscribe({
      next: (res: CompanyArticleList) => {
        this.articlesData = res;
      },
      error: (error) => {
        console.error('Error fetching articles data:', error);
      },
      complete: () => {
        this.articlesLoading = false;
      }
    });
  }
}


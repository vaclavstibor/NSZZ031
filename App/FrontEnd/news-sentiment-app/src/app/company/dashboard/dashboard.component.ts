import { Component, OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { ActivatedRoute } from '@angular/router';
import { HomeComponent } from 'src/app/home/home.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css', '../../app.component.css'],
})
export class DashboardComponent extends HomeComponent implements OnInit {
  ticker: string = '';

  chartData: any;
  chartLoading: boolean = false;

  infoData: any;
  infoLoading: boolean = false;

  articlesData: any;
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

  async fetchChartData(ticker: string) {
    this.chartLoading = true;
    this.httpService.getCompanyChartData(ticker).subscribe({
      next: (res: any) => {
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

  async fetchInfoData(ticker: string) {
    this.infoLoading = true;
    this.httpService.getCompanyInfoData(ticker).subscribe({
      next: (res: any) => {
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

  async fetchArticlesData(ticker: string) {
    this.articlesLoading = true;
    this.httpService.getCompanyArticlesData(ticker).subscribe({
      next: (res: any) => {
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


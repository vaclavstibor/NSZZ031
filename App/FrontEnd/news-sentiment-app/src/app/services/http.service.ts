import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

import { environment } from 'src/environments/environment';

import { CompanyInfo } from '../models/CompanyInfo.model';
import { CompanyChart } from '../models/CompanyChart.model';
import { CompanyGraph } from '../models/CompanyGraph.model';
import { CompanyArticleList } from '../models/CompanyArticleList.model';
import { CompanyNameAndTicker } from '../models/CompanyNameAndTicker.model';
import { CompaniesGraphs } from '../models/CompaniesGraphs.model';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  constructor(private http: HttpClient) {}

  getCompanyInfoData(ticker: string): Observable<CompanyInfo> {
    return this.http.get<CompanyInfo>(
      `${environment.API_BASE_URL}/company/${ticker}/info`
    );
  }

  getCompanyChartData(ticker: string): Observable<CompanyChart> {
    return this.http.get<CompanyChart>(
      `${environment.API_BASE_URL}/company/${ticker}/chart`
    );
  }

  getCompanyGraphData(ticker: string): Observable<CompanyGraph> {
    return this.http.get<CompanyGraph>(
      `${environment.API_BASE_URL}/company/${ticker}/graph`
    );
  }
  
  getCompanyArticlesData(ticker: string): Observable<CompanyArticleList> {
    return this.http.get<CompanyArticleList>(
      `${environment.API_BASE_URL}/company/${ticker}/articles`
    );
  }

  getCompaniesNamesAndTickers(): Observable<CompanyNameAndTicker[]> {
    return this.http.get<CompanyNameAndTicker[]>(`${environment.API_BASE_URL}/companies/names`);
  }

  getCompaniesGraphsData(): Observable<CompaniesGraphs> {
    return this.http.get<CompaniesGraphs>(`${environment.API_BASE_URL}/companies/graphs`);
  }
}

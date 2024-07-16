import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  constructor(private http: HttpClient) {}

  getCompanyInfoData(ticker: string): Observable<any> {
    return this.http.get<any>(
      `${environment.API_BASE_URL}/company/${ticker}/info`
    );
  }

  getCompanyChartData(ticker: string): Observable<any> {
    return this.http.get<any>(
      `${environment.API_BASE_URL}/company/${ticker}/chart`
    );
  }

  getCompanyGraphData(ticker: string): Observable<any> {
    return this.http.get<any>(
      `${environment.API_BASE_URL}/company/${ticker}/graph`
    );
  }
  
  getCompanyArticlesData(ticker: string): Observable<any> {
    return this.http.get<any>(
      `${environment.API_BASE_URL}/company/${ticker}/articles`
    );
  }

  getCompaniesNamesAndTickers(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.API_BASE_URL}/companies/names`);
  }

  getCompaniesGraphsData(): Observable<any> {
    return this.http.get<any>(`${environment.API_BASE_URL}/companies/graphs`);
  }

}

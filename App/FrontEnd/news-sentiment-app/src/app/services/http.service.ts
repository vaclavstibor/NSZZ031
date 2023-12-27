import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment  } from 'src/environments/environment';
import { APIResponse } from '../models/APIResponse';
import { Ticker } from '../models/Ticker';


@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private http: HttpClient) { }

  getTickerByName(name: string): Observable<Ticker> { 
    return this.http.get<Ticker>(`${environment.API_BASE_URL}/tickers/${name}`);
  }
}

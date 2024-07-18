import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';
import { OrderByPipe } from 'ngx-pipes';
import { Router } from '@angular/router';
import { HomeComponent } from '../home/home.component';

import { CompanyNameAndTicker } from '../models/CompanyNameAndTicker.model';

@Component({
  selector: 'app-companies',
  templateUrl: './companies.component.html',
  styleUrls: ['./companies.component.css', '../app.component.css'],
})
export class CompaniesComponent extends HomeComponent implements OnInit {
  companies: CompanyNameAndTicker[] = []; 
  inputText: string = ''; // Search input text
  page: number = 1;       // Current page for pagination

  constructor(private httpService: HttpService) {
    super();
  }

  ngOnInit(): void {
    this.getCompaniesNamesAndTickers();
  }

  getCompaniesNamesAndTickers() {
    /**
     * Fetches the list of companies with their names and tickers
     */
    this.httpService.getCompaniesNamesAndTickers().subscribe((res: CompanyNameAndTicker[]) => {
      this.companies = new OrderByPipe().transform(res, 'ticker');
    });
  }

  search() {
    /**
     * Filters the companies based on the search input text
     * which is used to filter based on shortName and ticker
     */
    if (this.inputText == '') {
      this.getCompaniesNamesAndTickers();
    } else {
      this.companies = this.companies.filter((res: any) => {
        this.page = 1;
        // Filtering based on shortName and ticker
        return res.shortName.toLocaleLowerCase().match(this.inputText.toLocaleLowerCase()) ||
               res.ticker.toLocaleLowerCase().match(this.inputText.toLocaleLowerCase());
      });
    }
  }
}
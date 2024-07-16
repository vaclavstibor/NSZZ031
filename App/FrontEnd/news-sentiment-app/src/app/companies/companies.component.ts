import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';
import { OrderByPipe } from 'ngx-pipes';
import { Router } from '@angular/router';
import { HomeComponent } from '../home/home.component';

@Component({
  selector: 'app-companies',
  templateUrl: './companies.component.html',
  styleUrls: ['./companies.component.css', '../app.component.css'],
})
export class CompaniesComponent extends HomeComponent implements OnInit {
  companies: any;
  inputText: string = '';
  page: number = 1;

  constructor(private httpService: HttpService, private router: Router) {
    super();
  }

  ngOnInit(): void {
    this.getCompaniesNamesAndTickers();
  }

  getCompaniesNamesAndTickers() {
    this.httpService.getCompaniesNamesAndTickers().subscribe((res: any[]) => {
      this.companies = new OrderByPipe().transform(res, 'ticker');
    });
  }

  search() {
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
// https://www.youtube.com/watch?v=YnAn7cePiMI

import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search.service';
import { OrderByPipe } from 'ngx-pipes';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tickers',
  templateUrl: './tickers.component.html',
  styleUrls: ['./tickers.component.css']
})
export class TickersComponent implements OnInit {
  tickers: any;
  inputText: any;
  page : number = 1;

  constructor(
    private searchService: SearchService,
    private router: Router
    ) { }

  ngOnInit(): void {
    this.getAllTickers();
  }

  getAllTickers() {
    this.searchService.getTickers().then((res: any[])=>{
      this.tickers = new OrderByPipe().transform(res, 'properties.name');
    })
  }

  search() {
    if(this.inputText == "") {
      this.getAllTickers();
    } else {
      this.tickers = this.tickers.filter((res:any) => {
        this.page = 1;
        return res.properties.name.toLocaleLowerCase().match(this.inputText.toLocaleLowerCase());
      })
    }
  }

  navigateToGraph(name: string) : void
  {
    this.router.navigate(["ticker-graph/" , name]);
  }
}

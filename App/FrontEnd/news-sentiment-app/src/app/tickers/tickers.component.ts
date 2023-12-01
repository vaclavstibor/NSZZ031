// https://www.youtube.com/watch?v=YnAn7cePiMI

import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search.service';

@Component({
  selector: 'app-tickers',
  templateUrl: './tickers.component.html',
  styleUrls: ['./tickers.component.css']
})
export class TickersComponent implements OnInit {
  tickers: any;
  inputText: any;
  page : number = 1;

  constructor(private service: SearchService) { }

  ngOnInit(): void {
    this.getAllTickers();
  }

  getAllTickers() {
    this.service.getTickers().then((res: any[])=>{
      this.tickers = res;
      console.log(res);
    })
  }

  search() {
    if(this.inputText == "") {
      this.getAllTickers();
    } else {
      this.tickers = this.tickers.filter((res:any) => {
        return res.properties.name.toLocaleLowerCase().match(this.inputText.toLocaleLowerCase());
      })
    }
  }
}

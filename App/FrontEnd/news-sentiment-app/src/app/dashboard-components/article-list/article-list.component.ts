import {Component, ViewChild} from '@angular/core';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import { ActivatedRoute } from '@angular/router';
import { HttpService } from 'src/app/services/http.service';

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.css']
})
export class ArticleListComponent {
  tickerName: string = '';
  articlesData: any;
  page: number = 1;

  constructor(private route: ActivatedRoute, private httpService: HttpService) {
    this.route.params.subscribe(params => {
      this.tickerName = params['name'];

      // Get articles for the ticker
      this.httpService.getTickerArticles(this.tickerName).subscribe((res: any) => {
        this.articlesData = res;
        console.log(res);
      });
    });
  }  

}

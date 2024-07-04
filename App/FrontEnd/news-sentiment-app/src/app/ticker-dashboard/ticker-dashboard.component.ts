import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';
import { ActivatedRoute } from '@angular/router';
import { CanvasJSAngularStockChartsModule } from '@canvasjs/angular-stockcharts';

@Component({
  selector: 'app-ticker-dashboard',
  templateUrl: './ticker-dashboard.component.html',
  styleUrls: ['./ticker-dashboard.component.css'],
})
export class TickerDashboardComponent implements OnInit {
  data: any = {};
  name: string = '';

  constructor(private httpService: HttpService, private route: ActivatedRoute) {
    this.route.params.subscribe((params) => {
      this.name = params['name'];
    });
  }

  ngOnInit(): void {
    console.log(this.name);
    //    this.httpService.getTickerDashboardData(this.name).subscribe((res: any) => {
    //      this.data = res;
    //      console.log(res);
    //    });
  }
}


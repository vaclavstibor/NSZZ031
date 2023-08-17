import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-sentiment-chart',
  templateUrl: './sentiment-chart.component.html',
  styleUrls: ['./sentiment-chart.component.css']
})
export class SentimentChartComponent implements OnInit {
  dataPoints:any = [];
  chart:any;
 
  constructor(private http : HttpClient) {  
  }
 
  chartOptions = {
    animationEnabled: true,
    animationDuration: 20000,
    theme: "light2",
    zoomEnabled: true,
    title: {
      text:"Bitcoin Closing Price"
    },
    subtitles: [{
      text: "Loading Data...",
      fontSize: 24,
      horizontalAlign: "center",
      verticalAlign: "center",
      dockInsidePlotArea: true
    }],
    axisY: {
      title: "Closing Price (in USD)",
      prefix: "$"
    },
    data: [{
      type: "line",
      name: "Closing Price",
      yValueFormatString: "$#,###.00",
      xValueType: "dateTime",
      dataPoints: this.dataPoints
    }]
  }
 
  getChartInstance(chart: object) {
    this.chart = chart;
  }
  
  ngOnInit() {
    this.http.get('https://canvasjs.com/data/gallery/angular/btcusd2021.json', { responseType: 'json' }).subscribe((response: any) => {
      let data = response;
      for(let i = 0; i < data.length; i++){
        this.dataPoints.push({x: new Date(data[i].date), y: Number(data[i].close) });
      }
      this.chart.subtitles[0].remove();
    });
  }
}


/*
import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-sentiment-chart',
  templateUrl: './sentiment-chart.component.html',
  styleUrls: ['./sentiment-chart.component.css']
})
export class SentimentChartComponent implements OnInit {
  //declare chart: Chart;

  public chart: any;

  ngOnInit() {
    this.chart = new Chart('progressive-line-chart', {
      type: 'line',
      data: {
        labels: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
        datasets: [
          {
            label: 'Value',
            data: [1,2,3,5,10,56,65,35,543,543,543],
            backgroundColor: 'red',
            borderWidth: 1,
            borderColor: 'red',
            fill: false
          },
          {
            label: 'Predict',
            data: [1,2,3,5,10,56,65,35,543,543,543].reverse(),
            backgroundColor: 'blue',
            borderWidth: 1,
            borderColor: 'blue',
            fill: false
          }
        ]
      }
    })
  }

}
*/
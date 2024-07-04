import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CanvasJSAngularStockChartsModule } from '@canvasjs/angular-stockcharts';
import { HttpService } from '../../services/http.service';

@Component({
  selector: 'app-stock-chart',
  standalone: true,
  imports: [CanvasJSAngularStockChartsModule],
  templateUrl: './stock-chart.component.html',
  styleUrls: ['./stock-chart.component.css']
})
export class StockChartComponent {
  chartData: any = {};
  name: string = '';
  stockChartOptions: any;

  constructor(private route: ActivatedRoute, private httpService: HttpService) {
    this.route.params.subscribe(params => {
      this.name = params['name'];
      this.updateStockChartOptions();

      // Fetch ticker stock chart data
      this.httpService.getTickerStockChartData(this.name).subscribe((res: any) => {
        this.chartData = res;
        const mappedData = this.mapDataToChart(res.price_data, res.sentiment_data);
        this.updateStockChartOptions(mappedData);
        console.log(res);
      });
    });
  }

  normalizeDate(dateString: string): Date {
    const date = new Date(dateString);
    date.setHours(0, 0, 0, 0); // Normalize time to midnight
    return date;
  }

  mapDataToChart(priceData: any[], sentimentData: any[]) {
    // Map price data to chart format
    const pricePoints = priceData.map(data => ({
      x: this.normalizeDate(data.date),
      y: data.adj_close,
    }));
  
    // Map sentiment data to chart format with adjusted y-values
    const sentimentPoints = sentimentData.map(data => {
      let color = 'gray'; // Default to neutral
      let symbol = 'NEUTRAL'; // Default to neutral
      let yValue; // Declare yValue for sentiment score
      let tooltip; // Declare tooltip for detailed information
  
      if (data.sentiment.classification === 'POSITIVE') {
        color = 'green';
        symbol = 'POSITIVE';
        yValue = data.sentiment.positive; // Use positive value for y
        tooltip = `POSITIVE: ${data.sentiment.positive}`;
      } else if (data.sentiment.classification === 'NEGATIVE') {
        color = 'red';
        symbol = 'NEGATIVE';
        yValue = data.sentiment.negative; // Use negative value for y
        tooltip = `NEGATIVE: ${data.sentiment.negative}`;
      } else if (data.sentiment.classification === 'NEUTRAL') {
        // Determine which value (positive or negative) defines the color
        if (data.sentiment.negative > data.sentiment.positive) {
          color = 'rgba(255, 0, 0,' + (data.sentiment.negative + 0.25) + ')';
          yValue = data.sentiment.negative; // Use negative value for y
          tooltip = `NEUTRAL (Lean Negative): ${data.sentiment.negative}`;
        } else {
          color = 'rgba(0, 128, 0,' + (data.sentiment.positive + 0.25) + ')';
          yValue = data.sentiment.positive; // Use positive value for y
          tooltip = `NEUTRAL (Lean Positive): ${data.sentiment.positive}`;
        }
      }
  
      return {
        x: this.normalizeDate(data.date),
        y: yValue,
        indexLabel: symbol,
        indexLabelFontColor: color,
        toolTipContent: tooltip
      };
    });
  
    return {
      pricePoints,
      sentimentPoints,
    };
  }
  

  updateStockChartOptions(mappedData?: { pricePoints: any[], sentimentPoints: any[] }) {
    this.stockChartOptions = {
      exportEnabled: true,
      theme: "light1",
      backgroundColor: "white",
      title: {
        text: `${this.name} Adjusted Close & Sentiment`,
      },
      charts: [{

        axisX: {
          valueFormatString: "DD MMM"
        },
        axisY: {
          prefix: "$"
        },
        legend: {
          verticalAlign: "top",
          horizontalAlign: "left",
          cursor: "pointer",
          itemclick: function (e: any) {
            if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
              e.dataSeries.visible = false;
            } else {
              e.dataSeries.visible = true;
            }
            e.chart.render();
          }
        },
        toolTip: {
          shared: true,
          enabled: true,
          animationEnabled: true,
          cornerRadius: 4
        },     
        data: [{
          type: "line",
          name: "Adj Close",
          showInLegend: true,
          yValueFormatString: "$#,###.00",
          dataPoints: mappedData ? mappedData.pricePoints : []
        }]
      }, {
        axisX: {
          valueFormatString: "DD MMM"
        },
        axisY: {
          includeZero: true,
        },
        legend: {
          verticalAlign: "top",
          horizontalAlign: "left",
          cursor: "pointer",
          itemclick: function (e: any) {
            if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
              e.dataSeries.visible = false;
            } else {
              e.dataSeries.visible = true;
            }
            e.chart.render();
          }
        },
        toolTip: {
          shared: true,
          enabled: true,
          animationEnabled: true,
          cornerRadius: 4
        },  
        data: [{
          type: "column", 
          name: "Sentiment",
          showInLegend: true,
          dataPoints: mappedData ? mappedData.sentimentPoints.map(point => ({
            x: point.x,
            y: point.y, 
            color: point.indexLabelFontColor,
            toolTipContent: point.toolTipContent
          })) : []
        }]
      }],
      rangeSelector: {
        buttonStyle: {
          spacing: 2,
        },
        buttons: [{
          label: "1 Month",
          range: 1,
          rangeType: "month"
        }, {
          label: "2 Months",
          range: 2,
          rangeType: "month"
        }, {
          label: "3 Months",
          rangeType: "all"
        }],
      }
    };
  }
}
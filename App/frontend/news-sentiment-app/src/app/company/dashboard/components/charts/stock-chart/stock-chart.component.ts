import { Component, Input, OnInit } from '@angular/core';
import { CanvasJSAngularStockChartsModule } from '@canvasjs/angular-stockcharts';

import { CompanyChart, PriceData, SentimentData } from 'src/app/models/CompanyChart.model';

@Component({
  selector: 'app-stock-chart',
  standalone: true,
  imports: [CanvasJSAngularStockChartsModule],
  templateUrl: './stock-chart.component.html',
  styleUrls: ['./stock-chart.component.css']
})
export class StockChartComponent implements OnInit {
  @Input() chartData!: CompanyChart;
  chartOptions: any = {};

  constructor() {}

  ngOnInit(): void {
    if (this.chartData) {
      const mappedData = this.mapDataToChart(this.chartData.price_data, this.chartData.sentiment_data);
      this.getStockChartOptions(mappedData);
    }
  }

  getStockChartOptions(mappedData?: StockChartData): void {
    // Set the chart options
    this.chartOptions = {
        animationEnabled: true,
        exportEnabled: true,
        theme: "light2",
        charts: [{
            animationEnabled: true,
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
                name: "POSITIVE",
                showInLegend: true,
                color: "green",
                dataPoints: mappedData ? mappedData.positivePoints : []
            }, {
                type: "column",
                name: "NEGATIVE",
                showInLegend: true,
                color: "red",
                dataPoints: mappedData ? mappedData.negativePoints : []
            }, {
                type: "column",
                name: "NEUTRAL (Lean Positive)",
                showInLegend: true,
                color: "rgba(0, 128, 0, 0.5)",
                dataPoints: mappedData ? mappedData.neutralPositivePoints : []
            }, {
                type: "column",
                name: "NEUTRAL (Lean Negative)",
                showInLegend: true,
                color: "rgba(255, 0, 0, 0.5)",
                dataPoints: mappedData ? mappedData.neutralNegativePoints : []
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

  mapDataToChart(priceData: PriceData[], sentimentData: SentimentData[]): StockChartData {
      // Map price data to chart format
      const pricePoints = priceData.map(data => ({
          x: this.normalizeDate(data.date),
          y: data.adj_close,
      }));

      // Map sentiment data to chart format with adjusted y-values
      const positivePoints: { x: Date; y: number }[] = [];
      const negativePoints: { x: Date; y: number }[] = [];
      const neutralPositivePoints: { x: Date; y: number }[] = [];
      const neutralNegativePoints: { x: Date; y: number }[] = [];

      sentimentData.forEach(data => {
          const date = this.normalizeDate(data.date);
          if (data.sentiment.classification === 'POSITIVE') {
              positivePoints.push({ x: date, y: data.sentiment.positive });
          } else if (data.sentiment.classification === 'NEGATIVE') {
              negativePoints.push({ x: date, y: data.sentiment.negative });
          } else if (data.sentiment.classification === 'NEUTRAL') {
              if (data.sentiment.negative > data.sentiment.positive) {
                  neutralNegativePoints.push({ x: date, y: data.sentiment.negative });
              } else {
                  neutralPositivePoints.push({ x: date, y: data.sentiment.positive });
              }
          }
      });

      return {
          pricePoints,
          positivePoints,
          negativePoints,
          neutralPositivePoints,
          neutralNegativePoints,
      };
  }

  normalizeDate(dateString: string): Date {
    // Normalize date to midnight
    const date = new Date(dateString);
    date.setHours(0, 0, 0, 0);
    return date;
  }
}

interface ChartPoint {
    x: Date;
    y: number;
  }
  
interface StockChartData {
    pricePoints: ChartPoint[];
    positivePoints: ChartPoint[];
    negativePoints: ChartPoint[];
    neutralPositivePoints: ChartPoint[];
    neutralNegativePoints: ChartPoint[];
  }

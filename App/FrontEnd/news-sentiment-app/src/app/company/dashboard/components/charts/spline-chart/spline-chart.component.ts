import { Component, Input, OnInit } from '@angular/core';
import { CanvasJSAngularStockChartsModule } from '@canvasjs/angular-stockcharts';

import { CompanyChart, SentimentData } from 'src/app/models/CompanyChart.model';

@Component({
  selector: 'app-spline-chart',
  standalone: true,
  imports: [CanvasJSAngularStockChartsModule],
  templateUrl: './spline-chart.component.html',
  styleUrls: ['./spline-chart.component.css']
})
export class SplineChartComponent implements OnInit {
  @Input() chartData!: CompanyChart;
  chartOptions: any = {};

  constructor() {}

  ngOnInit(): void {
    if (this.chartData) {
      const mappedData = this.mapDataToChart(this.chartData.sentiment_data);
      this.getSplineChartOptions(mappedData);
    }
  }

  getSplineChartOptions(mappedData: SplineChartData): void {
    // Set the chart options
    this.chartOptions = {
        animationEnabled: true,
        exportEnabled: true,
        theme: "light2",
        toolTip: {
            shared: true,
            enabled: true,
            animationEnabled: true,
            cornerRadius: 4
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
        data: [{
            type: "spline",
            name: "POSITIVE",
            showInLegend: true,
            markerType: "circle",
            lineColor: "green",
            markerColor: "green",
            dataPoints: mappedData.positivePoints
        }, {
            type: "spline",
            name: "NEUTRAL (Lean Positive)",
            showInLegend: true,
            markerType: "circle",
            lineColor: "rgba(0, 128, 0, 0.5)",
            markerColor: "rgba(0, 128, 0, 0.5)",
            dataPoints: mappedData.neutralPositivePoints
        }, {
            type: "spline",
            name: "NEUTRAL (Lean Negative)",
            showInLegend: true,
            markerType: "circle",
            lineColor: "rgba(255, 0, 0, 0.5)",
            markerColor: "rgba(255, 0, 0, 0.5)",
            dataPoints: mappedData.neutralNegativePoints
        }, {
            type: "spline",
            name: "NEGATIVE",
            showInLegend: true,
            markerType: "circle",
            lineColor: "red",
            markerColor: "red",
            dataPoints: mappedData.negativePoints
        }]};
    }

    mapDataToChart(sentimentData: SentimentData[]): SplineChartData {
        // Map the sentiment data to the chart data
        const positivePoints: { x: Date; y: any; color: string }[] = [];
        const neutralPositivePoints: { x: Date; y: any; color: string }[] = [];
        const neutralNegativePoints: { x: Date; y: any; color: string }[] = [];
        const negativePoints: { x: Date; y: any; color: string }[] = [];

        sentimentData.forEach(data => {
            const date = this.normalizeDate(data.date);
            if (data.sentiment.classification === 'POSITIVE') {
                positivePoints.push({ x: date, y: data.sentiment.positive, color: 'green' });
            } else if (data.sentiment.classification === 'NEGATIVE') {
                negativePoints.push({ x: date, y: data.sentiment.negative, color: 'red' });
            } else if (data.sentiment.classification === 'NEUTRAL') {
                if (data.sentiment.negative > data.sentiment.positive) {
                    neutralNegativePoints.push({ x: date, y: data.sentiment.negative, color: 'rgba(255, 0, 0, 0.5)' });
                } else {
                    neutralPositivePoints.push({ x: date, y: data.sentiment.positive, color: 'rgba(0, 128, 0, 0.5)' });
                }
            }
        });

        return {
            positivePoints,
            neutralPositivePoints,
            neutralNegativePoints,
            negativePoints
        };
    }

    getDateRange(data: SentimentData[]): { minDate: Date; maxDate: Date } {
        // Get the min and max date from the data
        const dates = data.map(item => new Date(item.date));
        const minDate = Math.min(...dates.map(date => date.getTime()));
        const maxDate = Math.max(...dates.map(date => date.getTime()));
        return { minDate: new Date(minDate), maxDate: new Date(maxDate) };
    }

    normalizeDate(dateString: string): Date {
        // Normalize date to midnight
        const date = new Date(dateString);
        date.setHours(0, 0, 0, 0);
        return date;
    }
}

interface SplineChartData {
    positivePoints: { x: Date; y: number; color: string }[];
    neutralPositivePoints: { x: Date; y: number; color: string }[];
    neutralNegativePoints: { x: Date; y: number; color: string }[];
    negativePoints: { x: Date; y: number; color: string }[];
  }
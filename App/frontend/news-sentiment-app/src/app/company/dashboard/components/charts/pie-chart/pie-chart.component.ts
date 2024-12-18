import { Component, Input, OnInit } from '@angular/core';
import { CanvasJSAngularStockChartsModule } from '@canvasjs/angular-stockcharts';

import { CompanyChart, SentimentData } from 'src/app/models/CompanyChart.model';

@Component({
  selector: 'app-pie-chart',
  standalone: true,
  imports: [CanvasJSAngularStockChartsModule],
  templateUrl: './pie-chart.component.html',
  styleUrls: ['./pie-chart.component.css']
})
export class PieChartComponent implements OnInit {
  @Input() chartData!: CompanyChart;
  chartOptions: any = {};

  constructor() {}

  ngOnInit(): void {
      if (this.chartData) {
        const mappedData = this.mapDataToChart(this.chartData.sentiment_data);
        this.getPieChartOptions(mappedData);
      }
  }

  getPieChartOptions(mappedData: PieChartData): void {
    /**
     * Sets the options for the pie chart based on the mapped data.
     * 
     * @param mappedData: The mapped data for the pie chart (type: PieChartData)
     */
    const colorMap = {
      "POSITIVE": "green",
      "NEGATIVE": "red",
      "NEUTRAL (Lean Positive)": "rgba(0, 128, 0, 0.5)",
      "NEUTRAL (Lean Negative)": "rgba(255, 0, 0, 0.5)"
    };

    const dataPoints = [
      { label: "POSITIVE", y: mappedData.positiveCount, color: colorMap["POSITIVE"] },
      { label: "NEGATIVE", y: mappedData.negativeCount, color: colorMap["NEGATIVE"] },
      { label: "NEUTRAL (Lean Positive)", y: mappedData.neutralPositiveCount, color: colorMap["NEUTRAL (Lean Positive)"] },
      { label: "NEUTRAL (Lean Negative)", y: mappedData.neutralNegativeCount, color: colorMap["NEUTRAL (Lean Negative)"] }
    ];

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
      data: [{
        type: "pie",
        startAngle: 240,
        yValueFormatString: "##0.00\"%\"",
        indexLabel: "{label} {y}",
        dataPoints
      }]
    };
  }

  mapDataToChart(sentimentData: SentimentData[]) {
    /**
     * Maps the sentiment data to the pie chart.
     * 
     * @param sentimentData: The sentiment data to map to the chart (type: SentimentData[])
     */
    
    // Map the sentiment data to the chart
    let positiveCount = 0;
    let negativeCount = 0;
    let neutralPositiveCount = 0;
    let neutralNegativeCount = 0;

    // Count the number of each sentiment classification in the data
    sentimentData.forEach(data => {
      if (data.sentiment.classification === 'POSITIVE') {
        positiveCount++;
      } else if (data.sentiment.classification === 'NEGATIVE') {
        negativeCount++;
      } else if (data.sentiment.classification === 'NEUTRAL') {
        if (data.sentiment.negative > data.sentiment.positive) {
          neutralNegativeCount++;
        } else {
          neutralPositiveCount++;
        }
      }
    });

    const total = positiveCount + negativeCount + neutralPositiveCount + neutralNegativeCount;

    // Calculate the percentage of each sentiment classification in the data (for avg from endpoint to each day)
    const positivePercentage = (positiveCount / total) * 100;
    const negativePercentage = (negativeCount / total) * 100; 
    const neutralPositivePercentage = (neutralPositiveCount / total) * 100;
    const neutralNegativePercentage = (neutralNegativeCount / total) * 100;

    return {
      positiveCount: positivePercentage,
      negativeCount: negativePercentage,
      neutralPositiveCount: neutralPositivePercentage,
      neutralNegativeCount: neutralNegativePercentage
    };
  }
}

interface PieChartData {
  positiveCount: number;
  negativeCount: number;
  neutralPositiveCount: number;
  neutralNegativeCount: number;
}
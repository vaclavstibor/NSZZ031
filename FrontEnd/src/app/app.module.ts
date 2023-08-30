import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { ProgressCircleBarComponent } from './components/analytics/widgets/progress-circle-bar/progress-circle-bar.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { SentimentChartComponent } from './components/analytics/widgets/sentiment-chart/sentiment-chart.component';
import { SentimentService } from './sentiment.service';
import { CanvasJSAngularChartsModule } from '@canvasjs/angular-charts';
import { MarqueeNewsComponent } from './components/analytics/widgets/marquee-news/marquee-news.component';

@NgModule({
  declarations: [
    AppComponent,
    AnalyticsComponent,
    ProgressCircleBarComponent,
    SentimentChartComponent,
    MarqueeNewsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatProgressSpinnerModule,
    HttpClientModule,
    CanvasJSAngularChartsModule
  ],
  providers: [SentimentService],
  bootstrap: [AppComponent]
})
export class AppModule {
}

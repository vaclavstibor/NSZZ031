import { Component, Input, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

import { CompanyArticleList, ArticleSentiment } from 'src/app/models/CompanyArticleList.model'; 

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.css']
})
export class ArticleListComponent implements AfterViewInit, OnInit {
  /**
   * Component to display a list of articles in a table format.
   * The component takes the articlesData input as an array of CompanyArticle objects.
   * The table displays the article title, published date, URL, author, section, type, sentiment, and sentiment scores.
   * The sentiment cell is colored based on the sentiment classification and scores.
   * The URL is transformed to display only the domain name.
   */
  @Input() articlesData!: CompanyArticleList;
  
  displayedColumns: string[] = ['title', 'published_date', 'url', 'author', 'section', 'type', 'sentiment', 'positive', 'neutral', 'negative'];
  dataSource!: MatTableDataSource<CompanyArticleList[number] & { [key: string]: any }>; // Adjusted to use CompanyArticleList type

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor() { }

  ngOnInit(): void {
    /**
     * Initialize the data source with the articlesData input
     * and set up the paginator and sort for the table.
     * @returns void
     */
    if (this.articlesData) {
      this.dataSource = new MatTableDataSource([...this.articlesData]);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      
      // Custom filter and sorting functions to handle nested properties
      this.dataSource.filterPredicate = this.createFilter();
      this.dataSource.sortingDataAccessor = (item, property) => {
        switch (property) {
          case 'sentiment': return item.sentiment.classification;
          case 'positive': return item.sentiment.positive;
          case 'neutral': return item.sentiment.neutral;
          case 'negative': return item.sentiment.negative;
          default: return item[property];
        }
      }
    }
  }

  ngAfterViewInit(): void {
    /**
     * Set up the paginator and sort for the table after the view initialization.
     * This is necessary to avoid the 'ExpressionChangedAfterItHasBeenCheckedError'.
     * @returns void
     */
    if (this.dataSource) {
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    }
  }

  applyFilter(event: Event) {
    /**
     * Apply filter to the data source when the user types in the filter input.
     * The filter is applied to all columns.
     * @param event The input event from the filter input field
     * @returns void
     */
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  createFilter(): (data: CompanyArticleList[number], filter: string) => boolean {
    /**
     * Create a custom filter function to search for data in the table.
     * The filter function searches for the filter string in all columns.
     * The search is case-insensitive.
     * @param data The data object to search in (CompanyArticleList type)
     * @param filter The filter string to search for in the data object (string type) 
     * @returns boolean
     */
    return (data, filter): boolean => {
      const searchStr = (
        data.title + 
        data.published_date + 
        data.url + 
        data.author + 
        data.section +
        data.type + 
        data.sentiment.classification + 
        data.sentiment.positive + 
        data.sentiment.neutral + 
        data.sentiment.negative
      ).toLowerCase();
      return searchStr.indexOf(filter) !== -1;
    };
  }

  getSentimentStyle(sentiment: ArticleSentiment): { [key: string]: string } {
    /**
     * Get the background color style for the sentiment cell based on the sentiment classification.
     * The color is green for positive sentiment, red for negative sentiment, and neutral for neutral sentiment.
     * The alpha value of the color is based on the sentiment score.
     * @param sentiment The sentiment object with classification and scores (positive, neutral, negative) (ArticleSentiment type)
     * @returns An object with the background-color style property (color string type)
     */
    const alpha = sentiment.classification === 'NEUTRAL'
      ? Math.max(sentiment.positive, sentiment.negative)
      : 1;
    const color = sentiment.classification === 'POSITIVE'
      ? `rgba(0, 128, 0, ${alpha})`
      : sentiment.classification === 'NEGATIVE'
        ? `rgba(255, 0, 0, ${alpha})`
        : sentiment.positive > sentiment.negative
          ? `rgba(0, 128, 0, ${sentiment.positive + 0.1})`
          : `rgba(255, 0, 0, ${sentiment.negative + 0.1})`;

    return { 'background-color': color };
  }

  transformUrl(url: string): string {
    /**
     * Transform the URL to display only the domain name.
     * @param url The URL string to transform (string type)
     * @returns The domain name extracted from the URL (string type)
     */
    const match = url.match(/^(?:https?:\/\/)?(?:www\.)?([^\/?#]+)(?:[\/?#]|$)/i);
    return match ? match[1] : url;
  }
}
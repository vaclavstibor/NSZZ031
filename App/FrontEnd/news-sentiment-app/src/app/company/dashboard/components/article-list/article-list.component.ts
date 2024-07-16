import { Component, Input, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.css']
})
export class ArticleListComponent implements AfterViewInit, OnInit {
  @Input() articlesData: any;
  
  displayedColumns: string[] = ['title', 'published_date', 'url', 'author', 'section', 'type', 'sentiment', 'positive', 'neutral', 'negative'];
  dataSource!: MatTableDataSource<ArticleData & { [key: string]: any }>; // To ensure that the dataSource can be filtered by the all columns

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor() { }

  ngOnInit() {
    if (this.articlesData) {
      this.dataSource = new MatTableDataSource(this.articlesData);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      
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

  ngAfterViewInit() {
    if (this.dataSource) {
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    }
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  createFilter(): (data: ArticleData, filter: string) => boolean {
    return (data: ArticleData, filter: string): boolean => {
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

  getSentimentStyle(sentiment: { classification: string, positive: number, neutral: number, negative: number }): any {
    const alpha = sentiment.classification === 'NEUTRAL'
      ? Math.max(sentiment.positive, sentiment.negative)
      : 1;
    const color = sentiment.classification === 'POSITIVE'
      ? `rgba(0, 128, 0, ${alpha})`
      : sentiment.classification === 'NEGATIVE'
        ? `rgba(255, 0, 0, ${alpha})`
        : sentiment.positive > sentiment.negative
          ? `rgba(0, 128, 0, ${sentiment.positive + 0.1})`
          : `rgba(255, 0, 0, ${sentiment.negative + 0.1})`; // Need to increase alpha to make nodes and links visible (but less than with graph with dark background)

    return { 'background-color': color };
  }

  transformUrl(url: string): string {
    const match = url.match(/^(?:https?:\/\/)?(?:www\.)?([^\/?#]+)(?:[\/?#]|$)/i);
    return match ? match[1] : url;
  }
}

export interface ArticleData {
  id: string;
  title: string;
  published_date: string;
  url: string;
  author: string;
  section: string;
  type: string;    
  sentiment: {
    classification: string;
    positive: number;
    neutral: number;
    negative: number;
  };
}
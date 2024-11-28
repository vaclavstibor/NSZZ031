import { Component, Input, OnInit } from '@angular/core';

import { CompanyInfo } from 'src/app/models/CompanyInfo.model';

@Component({
  selector: 'app-company-info',
  templateUrl: './company-info.component.html',
  styleUrls: ['./company-info.component.css'],
})
export class CompanyInfoComponent implements OnInit {
  @Input() infoData!: CompanyInfo; 
  // Data are passed from parent component (dashboard.component.ts) to this component directly to html template

  constructor() { }

  ngOnInit() { }
}


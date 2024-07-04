import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TickerDashboardComponent } from './ticker-dashboard.component';

describe('TickerDashboardComponent', () => {
  let component: TickerDashboardComponent;
  let fixture: ComponentFixture<TickerDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TickerDashboardComponent]
    });
    fixture = TestBed.createComponent(TickerDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

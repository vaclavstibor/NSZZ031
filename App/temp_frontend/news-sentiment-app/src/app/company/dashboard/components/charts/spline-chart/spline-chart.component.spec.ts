import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SplineChartComponent } from './spline-chart.component';

describe('SplineChartComponent', () => {
  let component: SplineChartComponent;
  let fixture: ComponentFixture<SplineChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SplineChartComponent]
    });
    fixture = TestBed.createComponent(SplineChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

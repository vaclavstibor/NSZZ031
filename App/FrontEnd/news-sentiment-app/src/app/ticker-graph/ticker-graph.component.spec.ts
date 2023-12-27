import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TickerGraphComponent } from './ticker-graph.component';

describe('TickerGraphComponent', () => {
  let component: TickerGraphComponent;
  let fixture: ComponentFixture<TickerGraphComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TickerGraphComponent]
    });
    fixture = TestBed.createComponent(TickerGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

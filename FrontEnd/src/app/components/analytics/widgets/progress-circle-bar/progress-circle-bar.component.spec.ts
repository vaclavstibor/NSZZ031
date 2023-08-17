import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProgressCircleBarComponent } from './progress-circle-bar.component';

describe('ProgressCircleBarComponent', () => {
  let component: ProgressCircleBarComponent;
  let fixture: ComponentFixture<ProgressCircleBarComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ProgressCircleBarComponent]
    });
    fixture = TestBed.createComponent(ProgressCircleBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

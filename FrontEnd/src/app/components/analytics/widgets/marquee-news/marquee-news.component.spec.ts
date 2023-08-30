import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MarqueeNewsComponent } from './marquee-news.component';

describe('MarqueeNewsComponent', () => {
  let component: MarqueeNewsComponent;
  let fixture: ComponentFixture<MarqueeNewsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MarqueeNewsComponent]
    });
    fixture = TestBed.createComponent(MarqueeNewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

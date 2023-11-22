import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphCosmosComponent } from './graph-cosmos.component';

describe('GraphCosmosComponent', () => {
  let component: GraphCosmosComponent;
  let fixture: ComponentFixture<GraphCosmosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GraphCosmosComponent]
    });
    fixture = TestBed.createComponent(GraphCosmosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

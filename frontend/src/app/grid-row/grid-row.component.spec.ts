import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GridRow } from './grid-row.component';

describe('GridRow', () => {
  let component: GridRow;
  let fixture: ComponentFixture<GridRow>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GridRow ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GridRow);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

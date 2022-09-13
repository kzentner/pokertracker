import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Cell } from './cell.component';

describe('Cell', () => {
  let component: Cell;
  let fixture: ComponentFixture<Cell>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Cell ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Cell);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'grid-row',
  templateUrl: './grid-row.component.html',
  styleUrls: ['./grid-row.component.scss']
})
export class GridRow implements OnInit {
  public cellText: string[][] = [];
  public static cardTypes = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];

  constructor() {
    for (let i = 0; i < 13; i++) {
      for (let j = 0; j < 13; j++) {
        if (i > j) {
          this.cellText[i][j] = GridRow.cardTypes[j] + GridRow.cardTypes[i] + 'o';
        }
        else if (i == j) {
          this.cellText[i][j] = GridRow.cardTypes[i] + GridRow.cardTypes[i];
        }
        else {
          this.cellText[i][j] = GridRow.cardTypes[i] + GridRow.cardTypes[j] + 's';
        }
      }
    }
  }

  ngOnInit(): void {
  }

}

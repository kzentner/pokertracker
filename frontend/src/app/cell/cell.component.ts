import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cell',
  templateUrl: './cell.component.html',
  styleUrls: ['./cell.component.scss']
})
export class Cell implements OnInit {
  @Input() text = "";
  @Input() numRaises = 0;
  @Input() numCalls = 0;
  @Input() numFolds = 0;
  public fill = '';

  constructor() { }

  public getBackgroundStyle() {
    let ret = ''
    const totalHands = this.numCalls + this.numRaises + this.numFolds;
    if (totalHands > 0) {
      const raise = Math.round(100 * this.numRaises / totalHands);
      const call = Math.round(100 * this.numCalls / totalHands);
      ret = `linear-gradient(to right,
        red ${raise}%,
        green ${raise}%,
        green ${raise + call}%,
        white ${raise + call}%,
        white 100%  
      );`
    }
    return ret;
  }
  

  ngOnInit(): void {
    this.fill = this.getBackgroundStyle();
  }

}

import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-main-area',
  imports: [],
  templateUrl: './main-area.component.html',
  styleUrl: './main-area.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: "bg-bg-light col-start-2 col-span-4 row-span-5 rounded-xl p-2"
  }
})
export class MainAreaComponent {

}

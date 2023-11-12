import { Component, OnInit, ElementRef, Renderer2 } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  title: string = "The title";
  hiddenElements: any;

  constructor(private el: ElementRef, private renderer: Renderer2) {}

  ngOnInit() {
    this.hiddenElements = this.el.nativeElement.querySelectorAll('.hidden');

    const observe = new IntersectionObserver(entries => {
      entries.forEach((entry) => {
        console.log(entry);
        if (entry.isIntersecting) {
          this.renderer.addClass(entry.target, 'show');
        } else {
          this.renderer.removeClass(entry.target, 'show');
        }
      })
    });

    this.hiddenElements.forEach((element: any) => {
      observe.observe(element);
    });
  }

  updateTitle(value: string) {
    console.log(`updateTitle: ${value}`);
    this.title = value;
  }
}
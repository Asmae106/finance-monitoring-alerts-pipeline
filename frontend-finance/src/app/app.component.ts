import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule],
  template: `
    <h1>Visualisation App</h1>
   <nav>
     <a routerLink="/alerts">Voir les alertes</a> |
     <a routerLink="/reports">Voir les rapports</a>
   </nav>
   <router-outlet></router-outlet>


  `
})
export class AppComponent {}


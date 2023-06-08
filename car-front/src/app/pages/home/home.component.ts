import { Component, OnInit } from '@angular/core';
import { Car } from 'src/app/models/cars.model';
import { CarsService } from 'src/app/services/cars.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  cars: Car[] = [];
  displayedColumns: string[] = ['id', 'placa', 'chassi', 'renavam', 'modelo', 'marca', 'ano'];

  constructor(private carService: CarsService) { }

  ngOnInit(): void {
    this.carService.getAllCars().subscribe(
      cars => {
        this.cars = cars
      }
    )
  }

}

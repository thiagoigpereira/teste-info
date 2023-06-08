import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'
import { environment } from 'src/environments/environment';
import { Car } from '../models/cars.model';

@Injectable({
  providedIn: 'root'
})
export class CarsService {
  private readonly api = environment.apiUrl;

  constructor(private readonly http: HttpClient) { }

  getAllCars(): Observable<Car[]> {
    return this.http.get<Car[]>(`${this.api}/cars`)
  }

}

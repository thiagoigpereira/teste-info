import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CarsService } from './cars.service';
import { environment } from 'src/environments/environment';
import { Car } from '../models/cars.model';

describe('CarsService', () => {
  let service: CarsService;
  let httpMock: HttpTestingController;

  const mockCars: Car[] = [
    { id: 1, placa: 'ABC123', chassi: '123456789', renavam: '987654321', modelo: 'Model A', marca: 'Brand X', ano: 2021 },
    { id: 2, placa: 'DEF456', chassi: '987654321', renavam: '123456789', modelo: 'Model B', marca: 'Brand Y', ano: 2022 },
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CarsService]
    });

    service = TestBed.inject(CarsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should retrieve all cars', () => {
    service.getAllCars().subscribe(cars => {
      expect(cars).toEqual(mockCars);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/cars`);
    expect(req.request.method).toBe('GET');
    req.flush(mockCars);
  });
});

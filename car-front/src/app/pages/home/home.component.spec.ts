import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HomeComponent } from './home.component';
import { CarsService } from 'src/app/services/cars.service';
import { of } from 'rxjs';
import { Car } from 'src/app/models/cars.model';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: ComponentFixture<HomeComponent>;
  let mockCarService: jasmine.SpyObj<CarsService>;

  const mockCars: Car[] = [
    { id: 1, placa: 'ABC123', chassi: '123456789', renavam: '987654321', modelo: 'Model A', marca: 'Brand X', ano: 2021 },
    { id: 2, placa: 'DEF456', chassi: '987654321', renavam: '123456789', modelo: 'Model B', marca: 'Brand Y', ano: 2022 },
  ];

  beforeEach(async () => {
    mockCarService = jasmine.createSpyObj('CarsService', ['getAllCars']);

    await TestBed.configureTestingModule({
      declarations: [HomeComponent],
      providers: [
        { provide: CarsService, useValue: mockCarService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch cars on component initialization', () => {
    mockCarService.getAllCars.and.returnValue(of(mockCars));

    component.ngOnInit();

    expect(mockCarService.getAllCars).toHaveBeenCalled();
    expect(component.cars).toEqual(mockCars);
  });
});

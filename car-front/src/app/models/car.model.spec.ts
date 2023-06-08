import { Car } from './cars.model';

describe('Car', () => {
  it('should create a car object', () => {
    const car: Car = {
      id: 1,
      placa: 'ABC123',
      chassi: '123456789',
      renavam: '987654321',
      modelo: 'Model A',
      marca: 'Brand X',
      ano: 2021
    };

    expect(car).toBeTruthy();
    expect(car.id).toBe(1);
    expect(car.placa).toBe('ABC123');
    expect(car.chassi).toBe('123456789');
    expect(car.renavam).toBe('987654321');
    expect(car.modelo).toBe('Model A');
    expect(car.marca).toBe('Brand X');
    expect(car.ano).toBe(2021);
  });
});

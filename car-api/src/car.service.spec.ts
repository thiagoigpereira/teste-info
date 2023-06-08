import { expect } from 'chai';
import { SinonStub, stub } from 'sinon';
import { CarService } from './car.service';
import { Car } from './car.entity';
import { Repository } from 'typeorm';

describe('CarService', () => {
  let carService: CarService;
  let carRepository: Repository<Car>;

  beforeEach(() => {
    carRepository = {} as Repository<Car>;
    carService = new CarService(carRepository);
  });

  describe('findAll', () => {
    it('should return an array of cars', async () => {
      const cars: Car[] = [{ id: 1, marca: 'Car 1', placa: 'CFD5555', chassi: 'xcvgfgh789789', renavam: 'SDFDSFSFSDFSFASFS', modelo: 'simples', ano: 2021 }, { id: 2, marca: 'Car 2', placa: 'CFD5555', chassi: 'xcvgfgh789789', renavam: 'SDFDSFSFSDFSFASFS', modelo: 'simples', ano: 2021 }];
      const findStub: SinonStub = stub(carRepository, 'find').resolves(cars);

      const result: Car[] = await carService.findAll();

      expect(result).to.deep.equal(cars);
      expect(findStub.calledOnce).to.be.true;

      findStub.restore();
    });
  });

  describe('findOne', () => {
    it('should return a car with the given id', async () => {
      const car: Car = { id: 1, marca: 'Car 1', placa: 'CFD5555', chassi: 'xcvgfgh789789', renavam: 'SDFDSFSFSDFSFASFS', modelo: 'simples', ano: 2021  };
      const findOneStub: SinonStub = stub(carRepository, 'findOne').resolves(car);

      const result: Car = await carService.findOne(1);

      expect(result).to.deep.equal(car);
      expect(findOneStub.calledOnceWithExactly({ where: { id: 1 } })).to.be.true;

      findOneStub.restore();
    });
  });

  describe('create', () => {
    it('should create and return a new car', async () => {
      const carData: Partial<Car> = { marca: 'New Car' };
      const createdCar: Car = {  id: 1, marca: 'Novo Carro 3', placa: 'CFD5555', chassi: 'xcvgfgh789789', renavam: 'SDFDSFSFSDFSFASFS', modelo: 'simples', ano: 2021};
      const createStub: SinonStub = stub(carRepository, 'create').returns(createdCar);
      const saveStub: SinonStub = stub(carRepository, 'save').resolves(createdCar);

      const result: Car = await carService.create(carData);

      expect(result).to.deep.equal(createdCar);
      expect(createStub.calledOnceWithExactly(carData)).to.be.true;
      expect(saveStub.calledOnceWithExactly(createdCar)).to.be.true;

      createStub.restore();
      saveStub.restore();
    });
  });

  describe('update', () => {
    it('should update and return a car with the given id', async () => {
      const id: number = 1;
      const carData: Partial<Car> = { marca: 'Updated Car' };
      const updatedCar: Car = { id: 1, marca: 'Car 1', placa: 'CFD5555', chassi: 'xcvgfgh789789', renavam: 'SDFDSFSFSDFSFASFS', modelo: 'simples', ano: 2021 };
      const updateStub: SinonStub = stub(carRepository, 'update');
      const findOneStub: SinonStub = stub(carRepository, 'findOne').resolves(updatedCar);

      const result: Car = await carService.update(id, carData);

      expect(result).to.deep.equal(updatedCar);
      expect(updateStub.calledOnceWithExactly(id, carData)).to.be.true;
      expect(findOneStub.calledOnceWithExactly({ where: { id } })).to.be.true;

      updateStub.restore();
      findOneStub.restore();
    });
  });

  describe('delete', () => {
    it('should delete a car with the given id', async () => {
      const id: number = 1;
      const deleteStub: SinonStub = stub(carRepository, 'delete');

      await carService.delete(id);

      expect(deleteStub.calledOnceWithExactly(id)).to.be.true;

      deleteStub.restore();
    });
  });
});

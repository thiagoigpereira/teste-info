import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Car } from './car.entity';

@Injectable()
export class CarService {
  constructor(
    @InjectRepository(Car)
    private carRepository: Repository<Car>,
  ) {}

  async findAll(): Promise<Car[]> {
    return this.carRepository.find();
  }

  async findOne(id: number): Promise<Car> {
    return this.carRepository.findOne({ 
      where: {
        id: id,
      }
     });
  }

  async create(carData: Partial<Car>): Promise<Car> {
    const car = this.carRepository.create(carData);
    return this.carRepository.save(car);
  }

  async update(id: number, carData: Partial<Car>): Promise<Car> {
    await this.carRepository.update(id, carData);
    return this.carRepository.findOne({ 
      where: {
        id: id,
      }
     });
  }

  async delete(id: number): Promise<void> {
    await this.carRepository.delete(id);
  }
}

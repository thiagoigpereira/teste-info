import { Controller, Get, Param, Post, Body, Put, Delete } from '@nestjs/common';
import { CarService } from './car.service';
import { Car } from './car.entity';

@Controller('cars')
export class CarController {
  constructor(private readonly carService: CarService) {}

  @Get()
  async getAllCars(): Promise<Car[]> {
    return this.carService.findAll();
  }

  @Get(':id')
  async getCarById(@Param('id') id: number): Promise<Car> {
    return this.carService.findOne(id);
  }

  @Post()
  async createCar(@Body() carData: Partial<Car>): Promise<Car> {
    return this.carService.create(carData);
  }

  @Put(':id')
  async updateCar(@Param('id') id: number, @Body() carData: Partial<Car>): Promise<Car> {
    return this.carService.update(id, carData);
  }

  @Delete(':id')
  async deleteCar(@Param('id') id: number): Promise<void> {
    return this.carService.delete(id);
  }
}
